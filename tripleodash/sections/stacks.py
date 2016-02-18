from tripleodash.sections.base import DashboardSection


class StacksWidget(DashboardSection):

    def __init__(self, clients):
        super(StacksWidget, self).__init__(clients, "Stacks")

    def update(self):
        pass

    def widgets(self):
        return super(StacksWidget, self).widgets() + []
