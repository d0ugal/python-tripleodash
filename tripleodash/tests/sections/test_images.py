import mock
import urwid

from tripleodash.sections import images
from tripleodash.tests import base
from tripleodash import util


class TestImagesSection(base.MockedClientTestCase):

    def setUp(self):

        super(TestImagesSection, self).setUp()

        self.section = images.ImagesWidget(self.clients)

    def test_widgets(self):

        image = mock.MagicMock(size=5153184, status="active",
                               created_at="2016-02-29T11:02:58Z",
                               updated_at="2016-02-29T11:02:58Z")
        image.id = "ID ID ID ID"
        image.name = "Image Name"

        self.clients.glance.images.list.return_value = [image, ]

        widgets = self.section.widgets()
        widths = [13, 12, 9, 8, 22, 22]

        self.assertWidgetListEqual(widgets, [
            util.header("Images"),
            urwid.Divider(),
            urwid.Divider(),
            util.TableRow(self.section.table_headers, widths,
                          util.table_header),
            urwid.Divider(),
            util.TableRow((
                image.id, image.name, image.size, image.status,
                image.created_at, image.updated_at), widths, util.table_header
            ),
        ])

    def test_widgets_no_images(self):

        self.clients.glance.images.list.return_value = []
        widgets = self.section.widgets()

        self.assertWidgetListEqual(widgets, [
            util.header("Images"),
            urwid.Divider(),
            urwid.Divider(),
            urwid.Text("No Glance images found.")
        ])
