from __future__ import print_function

import logging
import os

from glanceclient.v2.client import Client as glance_client
from heatclient.v1.client import Client as heat_client
import ironic_inspector_client
from ironicclient.v1.client import Client as ironic_client
from keystoneclient.v2_0 import client as ksclient
from swiftclient import client as swift_client

LOG = logging.getLogger(__name__)


def keystoneclient():
    return ksclient.Client(
        username=os.environ.get('OS_USERNAME'),
        tenant_name=os.environ.get('OS_TENANT_NAME'),
        password=os.environ.get('OS_PASSWORD'),
        auth_url=os.environ.get('OS_AUTH_URL'),
        auth_version=2,
        insecure=True
    )


def glanceclient():
    try:
        keystone = keystoneclient()
        endpoint = keystone.service_catalog.url_for(
            service_type='image',
            endpoint_type='publicURL'
        )
        return glance_client(
            endpoint=endpoint,
            token=keystone.auth_token)
    except Exception:
        LOG.exception("An error occurred initializing the Heat client")
        raise


def heatclient():
    try:
        keystone = keystoneclient()
        endpoint = keystone.service_catalog.url_for(
            service_type='orchestration',
            endpoint_type='publicURL'
        )
        return heat_client(
            endpoint=endpoint,
            token=keystone.auth_token,
            username=os.environ.get('OS_USERNAME'),
            password=os.environ.get('OS_PASSWORD'))
    except Exception:
        LOG.exception("An error occurred initializing the Heat client")
        raise


def ironicclient():
    try:
        keystone = keystoneclient()
        endpoint = keystone.service_catalog.url_for(
            service_type='baremetal',
            endpoint_type='publicURL'
        )
        return ironic_client(
            endpoint,
            token=keystone.auth_token,
            username=os.environ.get('OS_USERNAME'),
            password=os.environ.get('OS_PASSWORD'))
    except Exception:
        LOG.exception("An error occurred initializing the Ironic client")
        raise


def inspectorclient():
    try:
        keystone = keystoneclient()
        endpoint = keystone.service_catalog.url_for(
            service_type='baremetal-introspection',
            endpoint_type='publicURL'
        )
        return ironic_inspector_client.ClientV1(
            auth_token=keystone.auth_token,
            inspector_url=endpoint)
    except Exception:
        LOG.exception("An error occurred initializing the Ironic client")
        raise


def swiftclient():
    try:
        params = {'retries': 2,
                  'user': os.environ.get('OS_USERNAME'),
                  'tenant_name': os.environ.get('OS_TENANT_NAME'),
                  'key': os.environ.get('OS_PASSWORD'),
                  'authurl': os.environ.get('OS_AUTH_URL'),
                  'auth_version': 2,
                  'os_options': {'service_type': 'object-store',
                                 'endpoint_type': 'internalURL'}}

        return swift_client.Connection(**params)
    except Exception:
        LOG.exception("An error occurred initializing the Swift client")


if os.environ.get("DASH_DEBUG"):
    print("Mocking all clients")
    from .mock_clients import *  # NOQA
