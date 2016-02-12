from tripleodash.sections.base import DashboardWidget


class StacksWidget(DashboardWidget):

    def __init__(self):
        self.title = "Stacks"

    def update(self):
        pass

    def widgets(self):
        return super(StacksWidget, self).widgets() + [
        ]
