import urwid

from tripleodash.sections.base import DashboardSection
from tripleodash import util


class NodeRow(urwid.WidgetWrap):
    def __init__(self, uuid, instance_uuid, power_state,
                 provision_state, maintenance, introspection_status,
                 widget=urwid.Text, selectable=True, squash_instance=False):

        self._selectable = selectable

        self.cols = [
            (40, widget(str(uuid))),
            (40 if not squash_instance else 10, widget(str(instance_uuid))),
            (10, widget(str(power_state))),
            (14, widget(str(provision_state))),
            (12, widget(str(maintenance))),
            (13, widget(str(introspection_status))),
        ]

        wrapped_cols = urwid.AttrMap(urwid.Columns(self.cols), None,
                                     'reversed')
        super(NodeRow, self).__init__(wrapped_cols)

    def selectable(self):
        return self._selectable

    def keypress(self, size, key):
        return key


class NodesWidget(DashboardSection):

    def __init__(self, clients):
        super(NodesWidget, self).__init__(clients, "Nodes")

    def widgets(self):

        nodes = list(self.clients.ironic.node.list())
        assigned = False in [node.instance_uuid is None for node in nodes]

        node_table = [
            NodeRow("UUID", "Instance UUID", "Power State", "Provision State",
                    "Maintenance", "Introspection Finished",
                    widget=util.header, selectable=False,
                    squash_instance=not assigned),
            urwid.Divider(),
        ]

        for i, node in enumerate(nodes):

            widget = util.row_a if i % 2 else util.row_b

            introspect_status = self.clients.inspector.get_status(node.uuid)
            introspect_status = introspect_status['finished']

            node_table.append(NodeRow(
                node.uuid, node.instance_uuid, node.power_state,
                node.provision_state, node.maintenance, introspect_status,
                widget=widget, squash_instance=not assigned))

        return super(NodesWidget, self).widgets() + node_table
