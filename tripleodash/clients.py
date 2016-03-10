from __future__ import print_function

import logging
import os
import sys

import cachetools
from glanceclient.v2.client import Client as GlanceClient
from heatclient.v1.client import Client as HeatClient
import ironic_inspector_client
from ironicclient.v1.client import Client as IronicClient
from keystoneauth1.exceptions import auth
from keystoneauth1.exceptions import catalog
from keystoneclient.v2_0 import client as ksclient
from novaclient import client as nova_client
from swiftclient import client as swift_client

LOG = logging.getLogger(__name__)


class ServiceNotAvailable(Exception):
    pass


class ClientManager(object):

    def __init__(self):
        # Cache clients for 1 hour.
        self._cache = cachetools.TTLCache(100, ttl=60*60)

    def _get_endpoint(self, *args, **kwargs):

        try:
            return self.keystone.service_catalog.url_for(*args, **kwargs)
        except catalog.EndpointNotFound:
            raise ServiceNotAvailable()

    @property
    def keystone(self):

        if 'keystone' in self._cache:
            return self._cache['keystone']

        try:
            self._cache['keystone'] = ksclient.Client(
                username=os.environ.get('OS_USERNAME'),
                tenant_name=os.environ.get('OS_TENANT_NAME'),
                password=os.environ.get('OS_PASSWORD'),
                auth_url=os.environ.get('OS_AUTH_URL'),
                auth_version=2,
                insecure=True
            )
        except auth.AuthorizationFailure:
            print("Failed to authenticate with keystone. Check that the "
                  "OS_USERNAME, OS_PASSWORD, OS_TENANT_NAME and OS_AUTH_URL "
                  "environment variables are set.", file=sys.stderr)
            sys.exit()
        return self._cache['keystone']

    @property
    def nova(self):

        if 'nova' in self._cache:
            return self._cache['nova']

        self._cache['nova'] = nova_client.Client(
            2,
            os.environ.get('OS_USERNAME'),
            os.environ.get('OS_PASSWORD'),
            os.environ.get('OS_TENANT_NAME'),
            os.environ.get('OS_AUTH_URL')
        )
        return self._cache['nova']

    @property
    def glance(self):

        if 'glance' in self._cache:
            return self._cache['glance']

        keystone = self.keystone
        endpoint = self._get_endpoint(
            service_type='image',
            endpoint_type='publicURL'
        )
        self._cache['glance'] = GlanceClient(
            endpoint=endpoint,
            token=keystone.auth_token)

        return self._cache['glance']

    @property
    def heat(self):

        if 'heat' in self._cache:
            return self._cache['heat']

        keystone = self.keystone
        endpoint = self._get_endpoint(
            service_type='orchestration',
            endpoint_type='publicURL'
        )
        self._cache['heat'] = HeatClient(
            endpoint=endpoint,
            token=keystone.auth_token,
            username=os.environ.get('OS_USERNAME'),
            password=os.environ.get('OS_PASSWORD'))

        return self._cache['heat']

    @property
    def ironic(self):

        if 'ironic' in self._cache:
            return self._cache['ironic']

        keystone = self.keystone
        endpoint = self._get_endpoint(
            service_type='baremetal',
            endpoint_type='publicURL'
        )
        self._cache['ironic'] = IronicClient(
            endpoint,
            token=keystone.auth_token,
            username=os.environ.get('OS_USERNAME'),
            password=os.environ.get('OS_PASSWORD'))

        return self._cache['ironic']

    @property
    def inspector(self):

        if 'inspector' in self._cache:
            return self._cache['inspector']

        keystone = self.keystone
        try:
            endpoint = self._get_endpoint(
                service_type='baremetal-introspection',
                endpoint_type='publicURL'
            )
        except ServiceNotAvailable:
            # Ironic inspector will default to trying the localhost.
            endpoint = None
        self._cache['inspector'] = ironic_inspector_client.ClientV1(
            auth_token=keystone.auth_token,
            inspector_url=endpoint)

        return self._cache['inspector']

    @property
    def swift(self):

        if 'swift' in self._cache:
            return self._cache['swift']

        params = {
            'retries': 2,
            'user': os.environ.get('OS_USERNAME'),
            'tenant_name': os.environ.get('OS_TENANT_NAME'),
            'key': os.environ.get('OS_PASSWORD'),
            'authurl': os.environ.get('OS_AUTH_URL'),
            'auth_version': 2,
            'os_options': {
                'service_type': 'object-store',
                'endpoint_type': 'internalURL'
            }
        }

        self._cache['swift'] = swift_client.Connection(**params)

        return self._cache['swift']
