import urwid

from tripleodash import clients
from tripleodash.sections.base import DashboardWidget
from tripleodash import util


class NodeRow(urwid.WidgetWrap):
    def __init__(self, uuid, instance_uuid, power_state,
                 provision_state, maintenance, widget=urwid.Text,
                 selectable=True, squash_instance=False):

        self._selectable = selectable

        cols = urwid.Columns([
            (40, widget(str(uuid))),
            (40 if not squash_instance else 10, widget(str(instance_uuid))),
            (20, widget(str(power_state))),
            (20, widget(str(provision_state))),
            (20, widget(str(maintenance))),
        ])

        super(NodeRow, self).__init__(urwid.AttrMap(cols, None, 'reversed'))

    def selectable(self):
        return self._selectable

    def keypress(self, size, key):
        return key


class NodesWidget(DashboardWidget):

    def __init__(self):
        self.title = "Nodes"

    def widgets(self):

        nodes = list(clients.ironicclient().node.list())
        assigned = False in [node.instance_uuid is None for node in nodes]

        node_table = [
            NodeRow("UUID", "Instance UUID", "Power State", "Provision State",
                    "Maintenance", widget=util.header, selectable=False,
                    squash_instance=not assigned),
            urwid.Divider(),
        ]

        for i, node in enumerate(nodes):

            widget = util.row_a if i % 2 else util.row_b

            node_table.append(NodeRow(
                node.uuid, node.instance_uuid, node.power_state,
                node.provision_state, node.maintenance, widget=widget,
                squash_instance=not assigned))

        return super(NodesWidget, self).widgets() + node_table
