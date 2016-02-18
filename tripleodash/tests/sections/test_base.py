import mock
import urwid

from tripleodash.sections import base as base_section
from tripleodash.tests import base


class Testbase(base.MockedClientTestCase):

    def test_section_widgets(self):

        # Setup
        clients = mock.MagicMock()
        section = base_section.DashboardSection(clients, "Title")

        # Test
        widgets = section.widgets()

        # Verify
        self.assertEqual(widgets[0].get_text(), ('Title', [('header', 5)]))
        self.assertEqual(type(widgets[1]), urwid.Divider)
        self.assertEqual(type(widgets[2]), urwid.Divider)
        self.assertEqual(len(widgets), 3)
