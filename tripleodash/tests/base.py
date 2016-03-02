import unittest

import mock
import urwid

from tripleodash import dash
from tripleodash import util


class MockedClients(object):

    def __init__(self):
        self.heat = mock.MagicMock()
        self.ironic = mock.MagicMock()
        self.inspector = mock.MagicMock()
        self.glance = mock.MagicMock()
        self.nova = mock.MagicMock()


class MockedClientTestCase(unittest.TestCase):

    def setUp(self):

        self.clients = MockedClients()

        self.dash = dash.Dashboard(self.clients, 10)

    def assertWidgetListEqual(self, list_a, list_b):

        for (element_a, element_b) in zip(list_a, list_b):

            self.assertEqual(type(element_a), type(element_b))

            if isinstance(element_a, urwid.Text):
                self.assertEqual(element_a.get_text(), element_b.get_text())
            elif isinstance(element_a, urwid.Divider):
                continue
            elif isinstance(element_a, util.TableRow):
                self.assertEqual(element_a.row, element_b.row)
                self.assertEqual(element_a.widths, element_b.widths)
            else:
                self.assertEqual(element_a, element_b)

        self.assertEqual(len(list_a), len(list_b))
