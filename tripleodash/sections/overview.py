import collections

from heatclient.common import event_utils
import urwid

from tripleodash import clients
from tripleodash.sections.base import DashboardWidget
from tripleodash import util


class OverviewWidget(DashboardWidget):

    def __init__(self):
        self.title = "Overview"
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

        for image in images:
            widgets.append(urwid.Text("- {0}".format(image.name)))

        widgets.append(urwid.Divider())

        return widgets

    def _ironic_summary(self):

        nodes = list(self.ironic.node.list())
        by_provision_state = collections.defaultdict(list)
        by_introspection_status = collections.defaultdict(list)

        for node in nodes:
            inspector_status = self.inspector.get_status(node.uuid)
            by_introspection_status[inspector_status['finished']].append(node)
            by_provision_state[node.provision_state].append(node)

        lines = [
            util.header("Ironic Nodes"),
            urwid.Text("{0} nodes registered".format(len(nodes))),
        ]

        for state, nodes in by_provision_state.iteritems():
            lines.append(
                urwid.Text("{0} nodes {1}".format(len(nodes), state))
            )

        lines.extend([
            urwid.Text("{0} of {1} nodes introspected".format(
                len(by_introspection_status[True]), len(nodes))),
            urwid.Divider(),
        ])

        return lines

    def _stack_summary(self, stack):

        events = event_utils.get_events(self.heat,
                                        stack_id=stack.stack_name,
                                        nested_depth=1,
                                        event_args={'sort_dir': 'asc'})
        return util.heat_event_log_formatter(events[-100:])

    def undeployed(self):

        lines = [
            util.header("Heat Stack"),
            urwid.Text("No stacks deployed.", ),
            urwid.Divider(),
        ]

        lines.extend(self._images_summary())
        lines.extend(self._ironic_summary())

        lines.extend([
            util.header("Nova Flavors"),
            urwid.Text("Flavors: X, Y, Z"),
            urwid.Divider(),
        ])

        return lines

    def deployed(self, stacks):
        return [
            urwid.Text("Heat stack deployed."),
        ]

    def deploying(self, stacks):
        stack_info = []
        for stack in stacks:
            header = "Stack '{0}' status: {1}".format(
                stack.stack_name, stack.stack_status)
            stack_info.append(util.header(header))
            stack_info.extend(self._stack_summary(stack))
            stack_info.append(urwid.Divider())
        return stack_info

    def widgets(self):

        stacks = list(self.heat.stacks.list())

        deployment_exists = len(stacks) > 0
        stack_statuses = set(stack.stack_status for stack in stacks)
        deployed_statuses = set(['CREATE_COMPLETE', 'UPDATE_COMPLETE'])

        if not deployment_exists:
            widgets = self.undeployed()
        elif stack_statuses.issubset(deployed_statuses):
            widgets = self.deployed(stacks)
        else:
            widgets = self.deploying(stacks)

        return super(OverviewWidget, self).widgets() + widgets
