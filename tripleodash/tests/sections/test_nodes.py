import mock
import urwid

from tripleodash.sections import nodes
from tripleodash.tests import base
from tripleodash import util


class TestNodesSection(base.MockedClientTestCase):

    def setUp(self):

        super(TestNodesSection, self).setUp()

        self.section = nodes.NodesWidget(self.clients)

    def test_widgets(self):

        self.clients.inspector.get_status.return_value = {'finished': True, }

        self.clients.ironic.node.list.return_value = [
            mock.MagicMock(
                uuid="NODE UUID", instance_uuid="INSTANCE UUID",
                power_state="Off", provision_state="active",
                maintenance=False)
        ]

        widgets = self.section.widgets()
        widths = [11, 15, 7, 11, 13, 15]

        self.assertWidgetListEqual(widgets, [
            util.header("Nodes"),
            urwid.Divider(),
            urwid.Divider(),
            util.TableRow(self.section.table_headers, widths,
                          util.table_header),
            urwid.Divider(),
            util.TableRow(
                ('NODE UUID', 'INSTANCE UUID', 'Off', 'active', False, True),
                widths, util.table_header,
            ),
        ])

    def test_widgets_no_nodes(self):

        self.clients.ironic.node.list.return_value = []
        widgets = self.section.widgets()

        self.assertWidgetListEqual(widgets, [
            util.header("Nodes"),
            urwid.Divider(),
            urwid.Divider(),
            urwid.Text("No Ironic nodes found.")
        ])
