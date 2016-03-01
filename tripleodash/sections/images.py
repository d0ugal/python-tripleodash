import urwid

from tripleodash.sections.base import DashboardSection
from tripleodash import util


class ImagesWidget(DashboardSection):

    table_headers = (
        "ID", "Name", "size", "status", "Created At", "Updated At"
    )

    def __init__(self, clients):
        super(ImagesWidget, self).__init__(clients, "Images")

    def update(self):
        pass

    def rows(self, images):

        rows = [self.table_headers, ]

        for image in images:
            rows.append((
                image.id, image.name, image.size, image.status,
                image.created_at, image.updated_at
            ))

        return rows

    def widgets(self):

        images = list(self.clients.glance.images.list())

        if len(images):
            widgets = util.AutoTable(self.rows(images)).wrapped_widgets()
        else:
            widgets = [urwid.Text("No Glance images found."), ]
        return super(ImagesWidget, self).widgets() + list(widgets)
