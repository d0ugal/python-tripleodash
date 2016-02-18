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

        box = util.heat_event_log_formatter(events)
        widgets = [w.get_text() for w in list(box.original_widget.body)]

        self.assertEqual(widgets, [
            ("18:22 [Resource Name]: CREATE_IN_PROGRESS create progress", [])
        ])
