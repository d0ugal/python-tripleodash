import urwid


class DashboardWidget(object):

    def __init__(self, title):
        self.title = title

    def update(self):
        pass

    def widgets(self):
        return [
            urwid.Text(('header', self.title), 'center'),
            urwid.Divider(),
            urwid.Divider(),
        ]
