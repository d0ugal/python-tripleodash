import urwid

from tripleodash.sections.base import DashboardSection
from tripleodash import util


class ServersWidget(DashboardSection):

    table_headers = ("Server ID", "Name", "Networks")

    def __init__(self, clients):
        super(ServersWidget, self).__init__(clients, "Servers")

    def update(self):
        pass

    def rows(self, servers):

        rows = [self.table_headers, ]

        for server in servers:
            rows.append((
                server.id, server.human_id, str(server.networks)
            ))

        return rows

    def widgets(self):

        servers = list(self.clients.nova.servers.list())

        if len(servers):
            widgets = util.AutoTable(self.rows(servers)).wrapped_widgets()
        else:
            widgets = [urwid.Text("No Nova servers found."), ]
        return super(ServersWidget, self).widgets() + list(widgets)
