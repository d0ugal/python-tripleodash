import urwid

from tripleodash.sections.base import DashboardWidget


class StackWidget(DashboardWidget):

    def __init__(self):
        self.title = "Stack"

    def update(self):
        pass

    def widgets(self):
        return super(StackWidget, self).widgets() + [
            urwid.Text("Heat Stack: %s" % "CREATE_COMPLETE"),
        ]
