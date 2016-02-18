import urwid

from tripleodash import util


class DashboardSection(object):

    def __init__(self, clients, title):
        self.clients = clients
        self.title = title

    def update(self):
        pass

    def widgets(self):
        return [
            util.header(self.title, 'center'),
            urwid.Divider(),
            urwid.Divider(),
        ]
