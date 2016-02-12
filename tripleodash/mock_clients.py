from datetime import datetime


class Anon(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def heatclient():

    class HeatClient(object):

        def __init__(self):
            stacks = [
                Anon(stack_status="CREATE_COMPLETE", stack_name="overcloud",
                     creation_time=datetime.now(), updated_time=None),
                # Anon(stack_status="CREATE_FAILED", stack_name="overcloud"),
                # Anon(stack_status="CREATE_IN", stack_name="overcloud"),
            ]
            self.stacks = Anon(list=lambda: stacks)

            self.events = Anon(list=lambda **args: [])
            self.resources = Anon(list=lambda **args: [])

    return HeatClient()


def glanceclient():

    class GlanceClient(object):

        def __init__(self):
            images = [
                Anon(
                    status='active',
                    tags=[],
                    container_format='aki',
                    min_ram=0,
                    updated_at='2016-02-05T09:35:45Z',
                    visibility='public',
                    owner='623ce2146400418284ff1548b9c3febd',
                    file='/v2/images/da318862-1e65-41ce-af53-/file',
                    min_disk=0,
                    virtual_size=None,
                    id='da318862-1e65-41ce-af53-ba0f5e87c32d',
                    size=5154640,
                    name='bm-deploy-kernel',
                    checksum='f3645a7a0014b9d5594e6675af14e13f',
                    created_at='2016-02-05T09:35:45Z',
                    disk_format='aki',
                    protected=False,
                    schema='/v2/schemas/image'
                )
            ] * 3
            self.images = Anon(list=lambda: images)

    return GlanceClient()


def ironicclient():

    class IronicClient(object):

        def __init__(self):
            nodes = [
                Anon(uuid="5632b9bb-8ee1-4410-9319-8e9d39a6949c",
                     instance_uuid="7607f311-a1eb-406b-8724-742f38448770",
                     power_state="power on", provision_state="active",
                     maintenance="False"),
            ] * 3
            self.node = Anon(list=lambda: nodes)

    return IronicClient()


def inspectorclient():

    class InspectorClient(object):

        def get_status(self, uuid):
            return {'finished': True, 'error': 'ERROR MSG'}

    return InspectorClient()


def swiftclient():

    class SwiftClient(object):
        pass

    return SwiftClient()
