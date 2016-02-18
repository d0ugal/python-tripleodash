import datetime
import mock

import urwid

from tripleodash.tests import base


class TestDash(base.MockedClientTestCase):

    def test_handle_q(self):
        with self.assertRaises(urwid.ExitMainLoop):
            self.dash.handle_q('q')

    def test_nodes_window(self):
        # Setup
        dash = self.dash
        self.assertNotIn('nodes', dash._sections)
        self.assertEqual(dash._active_section, dash._sections['overview'])

        # Test
        self.dash.nodes_window()

        # Verify
        self.assertEqual(dash._active_section, dash._sections['nodes'])

    def test_stacks_window(self):
        # Setup
        dash = self.dash
        self.assertNotIn('stacks', dash._sections)
        self.assertEqual(dash._active_section, dash._sections['overview'])

        # Test
        self.dash.stacks_window()

        # Verify
        self.assertEqual(dash._active_section, dash._sections['stacks'])

    def test_overview_window(self):
        # Setup
        dash = self.dash
        self.assertIn('overview', dash._sections)
        self.assertEqual(dash._active_section, dash._sections['overview'])
        # Overview is the default, so switch out first.
        self.dash.stacks_window()
        self.assertEqual(dash._active_section, dash._sections['stacks'])

        # Test
        self.dash.overview_window()

        # Verify
        self.assertEqual(dash._active_section, dash._sections['overview'])

    def test_update_time(self):
        # Setup
        dt = datetime.datetime(2016, 2, 17, 9, 8, 7)
        self.dash._now = mock.MagicMock(return_value=dt)
        widget = self.dash._time
        self.assertEqual(type(widget), urwid.Text)

        # Test
        self.dash.update_time()

        # Verify
        self.assertEqual(widget.get_text(), ('09:08:07', [('subtle', 8)]))

    def test_tick(self):

        # Setup,
        self.dash._loop = mock.MagicMock()

        # Test
        self.dash.tick()

        # Verify
        self.dash._loop.set_alarm_in.assert_called_with(10, self.dash.tick)
