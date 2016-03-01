import mock
import urwid

from tripleodash.sections import stacks
from tripleodash.tests import base
from tripleodash import util


class TestStackSection(base.MockedClientTestCase):

    def setUp(self):

        super(TestStackSection, self).setUp()

        self.section = stacks.StacksWidget(self.clients)

    def test_widgets(self):

        self.clients.heat.stacks.list.return_value = [
            mock.MagicMock(
                stack_name="overcloud", stack_status="CREATE_COMPLETE",
                creation_time="2016-02-29T11:02:58Z",
                updated_time="2016-02-29T11:02:58Z")
        ]

        widgets = self.section.widgets()
        widths = [11, 17, 22, 22]

        self.assertWidgetListEqual(widgets, [
            util.header("Stacks"),
            urwid.Divider(),
            urwid.Divider(),
            util.TableRow(self.section.table_headers, widths,
                          util.table_header),
            urwid.Divider(),
            util.TableRow(
                ('overcloud', 'CREATE_COMPLETE', '2016-02-29T11:02:58Z',
                 '2016-02-29T11:02:58Z'),
                widths, util.table_header,
            ),
        ])

    def test_widgets_no_stacks(self):

        self.clients.heat.stacks.list.return_value = []
        widgets = self.section.widgets()

        self.assertWidgetListEqual(widgets, [
            util.header("Stacks"),
            urwid.Divider(),
            urwid.Divider(),
            urwid.Text("No Heat stacks found.")
        ])
