import mock
import urwid

from tripleodash.sections import overview
from tripleodash.tests import base
from tripleodash import util


class TestOverviewSection(base.MockedClientTestCase):

    def setUp(self):

        super(TestOverviewSection, self).setUp()

        self.section = overview.OverviewWidget(self.clients)

    def test_widgets_fresh_undercloud(self):

        # Test
        widgets = self.section.widgets()

        # Verify
        self.assertWidgetListEqual(widgets, [
            # Title
            util.header("Overview - Not Yet Deployed"),
            urwid.Divider(),
            urwid.Divider(),

            # Glance
            util.header("Glance Images"),
            urwid.Text("0 images uploaded."),
            urwid.Text("Use these commands to build and upload images:"),
            urwid.Text("    openstack overcloud image build --all"),
            urwid.Text("    openstack overcloud image upload"),
            urwid.Divider(),

            # Ironic
            util.header("Ironic Nodes"),
            urwid.Text("0 nodes registered."),
            urwid.Text("Use these commands to register nodes:"),
            urwid.Text("    openstack baremetal import --json instackenv.json"
                       ),
            urwid.Text("    openstack baremetal configure boot"),
            urwid.Divider(),

            # Heat
            util.header("Heat Stack"),
            urwid.Text("No stacks deployed.", ),
            urwid.Divider(),
        ])

    def test_image_summary_emtpy(self):

        # Test
        widgets = self.section._images_summary()

        # Verify
        self.assertWidgetListEqual(widgets, [
            util.header("Glance Images"),
            urwid.Text("0 images uploaded."),
            urwid.Text("Use these commands to build and upload images:"),
            urwid.Text("    openstack overcloud image build --all"),
            urwid.Text("    openstack overcloud image upload"),
            urwid.Divider(),
        ])

    def test_image_summary_all(self):

        def create_image(name):
            i = mock.MagicMock()
            i.name = name
            return i

        # Setup

        self.section.clients.glance.images.list.return_value = [
            create_image(name="image1"),
            create_image(name="image2"),
        ]

        # Test
        widgets = self.section._images_summary()

        # Verify
        self.assertWidgetListEqual(widgets, [
            util.header("Glance Images"),
            urwid.Text("2 images uploaded."),
            urwid.Text("- image1"),
            urwid.Text("- image2"),
            urwid.Divider(),
        ])

    def test_ironic_summary_emtpy(self):

        # Test
        widgets = self.section._ironic_summary()

        # Verify
        self.assertWidgetListEqual(widgets, [
            util.header("Ironic Nodes"),
            urwid.Text("0 nodes registered."),
            urwid.Text("Use these commands to register nodes:"),
            urwid.Text("    openstack baremetal import --json "
                       "instackenv.json"),
            urwid.Text("    openstack baremetal configure boot"),
            urwid.Divider(),
        ])

    def test_ironic_summary_all(self):

        # Setup
        self.section.clients.ironic.node.list.return_value = [
            mock.MagicMock(provision_state='available'),
            mock.MagicMock(provision_state='available'),
        ]

        # Test
        widgets = self.section._ironic_summary()

        # Verify
        self.assertWidgetListEqual(widgets, [
            util.header("Ironic Nodes"),
            urwid.Text("2 nodes registered."),
            urwid.Text("2 nodes with the provisioning state 'available'"),
            urwid.Divider(),
        ])

    def test_inspector_summary_emtpy(self):

        # Test
        widgets = self.section._inspector_summary()

        # Verify
        self.assertWidgetListEqual(widgets, [])

    def test_inspector_summary_progress(self):

        # Setup
        self.section.clients.ironic.node.list.return_value = [
            mock.MagicMock(uuid='UUID1'),
            mock.MagicMock(uuid='UUID2'),
        ]

        self.section.clients.inspector.get_status.return_value = {
            'finished': True
        }

        # Test
        widgets = self.section._inspector_summary()

        # Verify
        self.assertWidgetListEqual(widgets, [
            util.header("Node Introspection"),
            urwid.Text("2 nodes finished introspection"),
            urwid.Divider(),
        ])
