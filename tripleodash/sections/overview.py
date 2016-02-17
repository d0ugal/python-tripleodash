import collections

from heatclient.common import event_utils
from ironic_inspector_client.common import http as inspector_http
import urwid

from tripleodash import clients
from tripleodash.sections.base import DashboardWidget
from tripleodash import util

DEPLOYED_STATUSES = set(['CREATE_COMPLETE', 'UPDATE_COMPLETE'])
FAILED_STATUSES = set(['CREATE_FAILED', 'UPDATE_FAILED'])


class StackRow(urwid.WidgetWrap):
    def __init__(self, stack_name, stack_status, creation_time, updated_time,
                 widget=urwid.Text, selectable=True):

        self._selectable = selectable

        cols = urwid.Columns([
            (20, widget(str(stack_name))),
            (20, widget(str(stack_status))),
            (20, widget(str(creation_time))),
            (20, widget(str(updated_time))),
        ])

        super(StackRow, self).__init__(urwid.AttrMap(cols, None, 'reversed'))

    def selectable(self):
        return self._selectable

    def keypress(self, size, key):
        return key


class OverviewWidget(DashboardWidget):

    def __init__(self):
        self.heat = clients.heatclient()
        self.ironic = clients.ironicclient()
        self.inspector = clients.inspectorclient()
        self.glance = clients.glanceclient()

    def _images_summary(self):
        images = list(self.glance.images.list())

        widgets = [
            util.header("Glance Images"),
            urwid.Text("{0} images found.".format(len(images))),
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

        nodes = list(self.ironic.node.list())
        by_provision_state = collections.defaultdict(list)

        for node in nodes:
            by_provision_state[node.provision_state].append(node)

        lines = [
            util.header("Ironic Nodes"),
            urwid.Text("{0} nodes registered".format(len(nodes))),
        ]

        if len(by_provision_state):
            for state, nodes in by_provision_state.iteritems():
                lines.append(
                    urwid.Text("{0} nodes with the provisioning state '{1}'"
                               .format(len(nodes), state))
                )
        else:
            lines.extend([
                urwid.Text("Use these commands to build and upload images:"),
                urwid.Text("    openstack baremetal import --json "
                           "instackenv.json"),
                urwid.Text("    openstack baremetal configure boot"),
            ])

        lines.append(urwid.Divider())

        return lines

    def _inspector_summary(self):

        nodes = list(self.ironic.node.list())
        by_introspection_status = collections.defaultdict(list)

        for node in nodes:
            try:
                inspector_status = self.inspector.get_status(node.uuid)
            except inspector_http.ClientError:
                inspector_status = {'finished': "Not started"}
            by_introspection_status[inspector_status['finished']].append(node)

        return [
            util.header("Node Introspection"),
            urwid.Text("{0} nodes currently being introspected".format(
                len(by_introspection_status[False]))),
            urwid.Text("{0} nodes finished introspection".format(
                len(by_introspection_status[True]))),
            urwid.Divider(),
        ]

    def _stack_event_summary(self, stack):

        events = event_utils.get_events(self.heat,
                                        stack_id=stack.stack_name,
                                        nested_depth=2,
                                        event_args={'sort_dir': 'asc'})

        return util.heat_event_log_formatter(events[-25:])

    def _stacks_summary(self, stacks):

        lines = [
            StackRow("Stack Name", "Stack Status", "Created Date",
                     "Updated Date", widget=util.header, selectable=False),
            urwid.Divider(),
        ]

        for stack in stacks:
            lines.append(StackRow(stack.stack_name, stack.stack_status,
                                  stack.creation_time, stack.updated_time))

        lines.append(urwid.Divider())
        lines.append(urwid.Divider())

        return lines

    def _resource_error(self, stack):

        resources = self.heat.resources.list(stack.stack_name, nested_depth=5)

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
            header = "Stack '{0}' status: {1}".format(
                stack.stack_name, stack.stack_status)
            lines.append(util.header(header))
            lines.append(self._stack_event_summary(stack))
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

        stacks = list(self.heat.stacks.list())

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
