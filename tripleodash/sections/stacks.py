import urwid

from tripleodash.sections.base import DashboardSection
from tripleodash import util


class StacksWidget(DashboardSection):

    table_headers = (
        "Stack Name", "Stack Status", "Created Date", "Updated Date"
    )

    def __init__(self, clients):
        super(StacksWidget, self).__init__(clients, "Stacks")

    def update(self):
        pass

    def rows(self, stacks):

        rows = [self.table_headers, ]

        for stack in stacks:
            rows.append((
                stack.stack_name, stack.stack_status, stack.creation_time,
                stack.updated_time
            ))

        return rows

    def widgets(self):

        stacks = list(self.clients.heat.stacks.list())

        if len(stacks):
            widgets = util.AutoTable(self.rows(stacks)).wrapped_widgets()
        else:
            widgets = [urwid.Text("No Heat stacks found."), ]
        return super(StacksWidget, self).widgets() + list(widgets)
