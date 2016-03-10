import collections

from heatclient.common import event_utils
from heatclient import exc
from ironic_inspector_client.common import http as inspector_http
import urwid

from tripleodash import clients
from tripleodash.sections.base import DashboardSection
from tripleodash import util

DEPLOYED_STATUSES = set(['CREATE_COMPLETE', 'UPDATE_COMPLETE'])
FAILED_STATUSES = set(['CREATE_FAILED', 'UPDATE_FAILED'])
DEPLOYING_STATUSES = set(['CREATE_IN_PROGRESS', 'UPDATE_IN_PROGRESS'])


class OverviewWidget(DashboardSection):

    def __init__(self, clients):
        super(OverviewWidget, self).__init__(clients, "Overview")

    def _images_summary(self):
        images = list(self.clients.glance.images.list())

        widgets = [
            util.header("Glance Images"),
            urwid.Text("{0} images uploaded.".format(len(images))),
        ]

        if len(images):
            for image in images:
                widgets.append(urwid.Text("- {0}".format(image.name)))
        else:
            widgets.extend([
                urwid.Text("Use these commands to build and upload images:"),
                urwid.Text("    openstack overcloud image build --all"),
                urwid.Text("    openstack overcloud image upload"),
            ])

        widgets.append(urwid.Divider())

        return widgets

    def _ironic_summary(self):

        nodes = list(self.clients.ironic.node.list())
        by_provision_state = collections.defaultdict(list)

        for node in nodes:
            by_provision_state[node.provision_state].append(node)

        lines = [
            util.header("Ironic Nodes"),
            urwid.Text("{0} nodes registered.".format(len(nodes))),
        ]

        if len(by_provision_state):
            for state, nodes in by_provision_state.items():
                lines.append(
                    urwid.Text("{0} nodes with the provisioning state '{1}'"
                               .format(len(nodes), state))
                )
        else:
            lines.extend([
                urwid.Text("Use these commands to register nodes:"),
                urwid.Text("    openstack baremetal import --json "
                           "instackenv.json"),
                urwid.Text("    openstack baremetal configure boot"),
            ])

        lines.append(urwid.Divider())

        return lines

    def _inspector_summary(self):

        nodes = list(self.clients.ironic.node.list())
        by_introspection_status = collections.defaultdict(list)

        for node in nodes:
            try:
                inspector_status = self.clients.inspector.get_status(node.uuid)
                inspector_status = inspector_status['finished']
            except inspector_http.ClientError:
                inspector_status = "Not started"
            except clients.ServiceNotAvailable:
                inspector_status = 'Unknown'
            by_introspection_status[inspector_status].append(node)

        lines = [
            util.header("Node Introspection")
        ]

        if len(by_introspection_status[False]):
            lines.append(
                urwid.Text("{0} nodes currently being introspected".format(
                    len(by_introspection_status[False])))
            )

        if len(by_introspection_status[True]):
            lines.append(
                urwid.Text("{0} nodes finished introspection".format(
                    len(by_introspection_status[True])))
            )

        if len(by_introspection_status["Not started"]):
            lines.append(
                urwid.Text("{0} nodes not yet started introspection".format(
                    len(by_introspection_status["Not started"])))
            )

        if len(by_introspection_status["Unknown"]):
            lines.append(
                urwid.Text("Failed to get introspection status for {0} nodes"
                           .format(len(by_introspection_status["Unknown"])))
            )

        if len(lines) == 1:
            return []

        lines.append(urwid.Divider())
        return lines

    def _stack_event_summary(self, stack):

        try:
            events = event_utils.get_events(self.clients.heat,
                                            stack_id=stack.stack_name,
                                            nested_depth=1,
                                            event_args={'sort_dir': 'asc'})
        except exc.CommandError:
            return []

        return util.heat_event_log_formatter(reversed(events))

    def _stacks_summary(self, stacks):

        rows = [(
            "Stack Name", "Stack Status", "Created Date",
            "Updated Date"
        )]

        for stack in stacks:
            rows.append((
                stack.stack_name, stack.stack_status, stack.creation_time,
                stack.updated_time
            ))

        lines = list(util.AutoTable(rows).wrapped_widgets())

        lines.append(urwid.Divider())

        return lines

    def _resource_error(self, stack):

        resources = self.clients.heat.resources.list(stack.stack_name,
                                                     nested_depth=2)

        failed = (resource for resource in resources
                  if resource.resource_status in FAILED_STATUSES)

        for resource in failed:
            yield util.header("Failed resource: {0}"
                              .format(resource.resource_name))
            yield urwid.Text("Status reason: {0}"
                             .format(resource.resource_status_reason))
            yield urwid.Divider()

    def undeployed(self):

        self.title += "- Not Yet Deployed"

        lines = []
        lines.extend(self._images_summary())
        lines.extend(self._ironic_summary())
        lines.extend(self._inspector_summary())
        lines.extend([
            util.header("Heat Stack"),
            urwid.Text("No stacks deployed.", ),
            urwid.Divider(),
        ])
        return lines

    def deployed(self, stacks):

        self.title += "- Deploy Complete"

        lines = []
        lines.extend(self._images_summary())
        lines.extend(self._ironic_summary())
        lines.extend(self._inspector_summary())
        lines.extend(self._stacks_summary(stacks))
        return lines

    def deploying(self, stacks):

        self.title += "- Deploy In Progress"

        lines = []

        lines.extend(self._ironic_summary())

        for stack in stacks:

            extra = ""

            if stack.stack_status in DEPLOYING_STATUSES:
                time_string = stack.updated_time or stack.creation_time
                extra = " (Started: {})".format(time_string)

            header = "Stack '{0}' status: {1}{2}".format(
                stack.stack_name, stack.stack_status, extra)
            lines.append(util.header(header))
            lines.extend(self._stack_event_summary(stack))
            lines.append(urwid.Divider())
        return lines

    def failed(self, stacks):

        self.title += "- Deploy Failed"

        lines = []

        lines.extend(self._ironic_summary())

        for stack in stacks:

            header = "Stack '{0}' status: {1}".format(
                stack.stack_name, stack.stack_status)
            lines.append(util.header(header))

            lines.extend(self._resource_error(stack))
            lines.append(urwid.Divider())

        return lines

    def widgets(self):

        self.title = "Overview "

        stacks = list(self.clients.heat.stacks.list())

        deployment_exists = len(stacks) > 0
        stack_statuses = set(stack.stack_status for stack in stacks)

        if not deployment_exists:
            widgets = self.undeployed()
        elif stack_statuses.issubset(DEPLOYED_STATUSES):
            widgets = self.deployed(stacks)
        elif stack_statuses.issubset(FAILED_STATUSES):
            widgets = self.failed(stacks)
        else:
            widgets = self.deploying(stacks)

        return super(OverviewWidget, self).widgets() + widgets
