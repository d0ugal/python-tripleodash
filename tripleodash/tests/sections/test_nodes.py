import mock
import urwid

from tripleodash.sections import nodes
from tripleodash.tests import base


class TestNodesSection(base.MockedClientTestCase):

    def setUp(self):

        super(TestNodesSection, self).setUp()

        self.section = nodes.NodesWidget(self.clients)

    def test_widgets(self):

        self.clients.ironic.node.list.return_value = [
            mock.MagicMock(
                uuid="UUID", instance_uuid="Instance UUID",
                power_state="Off", provision_state="active",
                maintenance=False, introspection_status=True)
        ]

        widgets = self.section.widgets()

        self.assertEqual(widgets[0].get_text(), ("Nodes", [('header', 5)]))
        self.assertEqual(type(widgets[1]), urwid.Divider)
        self.assertEqual(type(widgets[2]), urwid.Divider)

        self.assertEqual(type(widgets[4]), urwid.Divider)

        self.assertEqual(len(widgets), 6)
