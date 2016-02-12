import urwid

from tripleodash import util


class DashboardWidget(object):

    def __init__(self, title):
        self.title = title

    def update(self):
        pass

    def widgets(self):
        return [
            util.header(self.title, 'center'),
            urwid.Divider(),
            urwid.Divider(),
        ]
