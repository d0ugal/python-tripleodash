import urwid

from tripleodash import clients
from tripleodash.sections.base import DashboardWidget
from tripleodash import util


class NodeRow(urwid.WidgetWrap):
    def __init__(self, uuid, instance_uuid, power_state,
                 provision_state, maintenance, widget=urwid.Text,
                 selectable=True):

        self._selectable = selectable

        cols = urwid.Columns([
            (40, widget(str(uuid))),
            (40, widget(str(instance_uuid))),
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

        nodes = [
            NodeRow("UUID", "Instance UUID", "Power State", "Provision State",
                    "Maintenance", widget=util.header, selectable=False),
            urwid.Divider(),
        ]

        for i, node in enumerate(clients.ironicclient().node.list()):

            widget = util.row_a if i % 2 else util.row_b

            nodes.append(NodeRow(
                node.uuid, node.instance_uuid, node.power_state,
                node.provision_state, node.maintenance, widget=widget))

        return super(NodesWidget, self).widgets() + nodes
