import mock
import urwid

from tripleodash.sections import servers
from tripleodash.tests import base
from tripleodash import util


class TestServersSection(base.MockedClientTestCase):

    def setUp(self):

        super(TestServersSection, self).setUp()

        self.section = servers.ServersWidget(self.clients)

    def test_widgets(self):

        server = mock.MagicMock(
            human_id="overcloud-objectstorage-0",
            networks={'ctlplane': ['192.0.2.13']}
        )
        server.id = "ID ID ID"

        self.clients.nova.servers.list.return_value = [server, ]

        widgets = self.section.widgets()
        widths = [10, 27, 30]

        self.assertWidgetListEqual(widgets, [
            util.header("Servers"),
            urwid.Divider(),
            urwid.Divider(),
            util.TableRow(self.section.table_headers, widths,
                          util.table_header),
            urwid.Divider(),
            util.TableRow(
                ('ID ID ID', 'overcloud-objectstorage-0',
                 "{'ctlplane': ['192.0.2.13']}"),
                widths, util.table_header,
            ),
        ])

    def test_widgets_no_stacks(self):

        self.clients.nova.servers.list.return_value = []
        widgets = self.section.widgets()

        self.assertWidgetListEqual(widgets, [
            util.header("Servers"),
            urwid.Divider(),
            urwid.Divider(),
            urwid.Text("No Nova servers found.")
        ])
