from ironic_inspector_client.common import http

from tripleodash import clients
from tripleodash.sections.base import DashboardSection
from tripleodash import util


class NodesWidget(DashboardSection):

    table_headers = (
        "UUID", "Instance UUID", "Power State", "Provision State",
        "Maintenance", "Introspection Finished"
    )

    def __init__(self, clients):
        super(NodesWidget, self).__init__(clients, "Nodes")

    def rows(self):

        nodes = self.clients.ironic.node.list()

        rows = [self.table_headers, ]

        for i, node in enumerate(nodes):
            try:
                introspect_status = self.clients.inspector.get_status(
                    node.uuid)['finished']
            except http.ClientError:
                introspect_status = 'Not started'
            except clients.ServiceNotAvailable:
                introspect_status = 'Unknown'

            rows.append((node.uuid, node.instance_uuid, node.power_state,
                         node.provision_state, node.maintenance,
                         introspect_status))

        return rows

    def widgets(self):
        widgets = util.AutoTable(self.rows()).wrapped_widgets()
        return super(NodesWidget, self).widgets() + list(widgets)
