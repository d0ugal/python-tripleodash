import mock

import urwid

from tripleodash.tests import base
from tripleodash import util


class TestUtil(base.MockedClientTestCase):

    def test_button(self):

        # Setup
        fn = mock.MagicMock()

        # Test
        btn = util.button("Test", fn)
        btn.mouse_event((15, ), 'mouse press', 1, 4, 0, True)

        # Verify
        self.assertEqual(type(btn), urwid.AttrWrap)
        self.assertEqual(type(btn.original_widget), urwid.Button)
        self.assertEqual(btn.original_widget.get_label(), "Test")

        fn.assert_called_with(btn.original_widget)

    def test_exit_button(self):

        # Test
        btn = util.exit_button("Exit")
        with self.assertRaises(urwid.ExitMainLoop):
            btn.mouse_event((15, ), 'mouse press', 1, 4, 0, True)

        # Verify
        self.assertEqual(type(btn), urwid.AttrWrap)
        self.assertEqual(type(btn.original_widget), urwid.Button)
        self.assertEqual(btn.original_widget.get_label(), "Exit")

    def test_main_header(self):

        # Test
        txt = util.main_header("Header")

        # Verify
        self.assertEqual(txt.get_text(), ('Header ', [('main header', 7)]))

    def test_header(self):

        # Test
        txt = util.header("Header")

        # Verify
        self.assertEqual(txt.get_text(), ('Header', [('header', 6)]))

    def test_subtle(self):

        # Test
        txt = util.subtle("Subtle")

        # Verify
        self.assertEqual(txt.get_text(), ('Subtle', [('subtle', 6)]))

    def test_table_header(self):

        # Test
        txt = util.table_header("Table Header")

        # Verify
        self.assertEqual(txt.get_text(), ('Table Header', [('header', 12)]))

    def test_row_a(self):

        # Test
        txt = util.row_a("Row A")

        # Verify
        self.assertEqual(txt.get_text(), ('Row A', [('row_a', 5)]))

    def test_row_b(self):

        # Test
        txt = util.row_b("Row B")

        # Verify
        self.assertEqual(txt.get_text(), ('Row B', [('row_b', 5)]))

    def test_heat_event_log_formatter(self):

        events = [
            mock.MagicMock(
                event_time="18:22",
                resource_name="Resource Name",
                resource_status="CREATE_IN_PROGRESS",
                resource_status_reason="create progress",
            )
        ]

        widgets = util.heat_event_log_formatter(events)

        self.assertWidgetListEqual(widgets, [
            urwid.Text(
                "18:22 [Resource Name]: CREATE_IN_PROGRESS create progress",
                wrap='clip')
        ])

    def test_auto_table_widths(self):

        rows = [
            ("Header 1", "Header 2", "Header 3"),
            ("Row 1", "Row 1", "Row 1"),
            ("Row 2", "Row 2", "Row 2"),
            ("Row 3", "Row 3", "Row 3"),
        ]

        table = util.AutoTable(rows)

        self.assertEqual(table.col_widths(), [8, 8, 8])

    def test_auto_table_widths_long_header(self):

        rows = [
            ("Node UUID", "Instance UUID", "Extra Long Header"),
            ("UUIDUUIDUUIDUUIDUUID", "InstanceUUID", "NotLong"),
        ]

        table = util.AutoTable(rows)

        self.assertEqual(table.col_widths(), [22, 14, 9])

    def test_auto_table_widgets(self):

        headers = ("Node UUID", "Instance", "Extra Long Header", "int", "bool")
        widths = [22, 14, 9, 5, 7]

        rows = [
            headers,
            ("UUIDUUIDUUIDUUIDUUID", "InstanceUUID", "NotLong", 3, False),
        ]

        widgets = list(util.AutoTable(rows).wrapped_widgets())

        self.assertWidgetListEqual(widgets, [
            util.TableRow(headers, widths),
            urwid.Divider(),
            util.TableRow((
                "UUIDUUIDUUIDUUIDUUID", "InstanceUUID", "NotLong", 3, False
            ), widths),
        ])
