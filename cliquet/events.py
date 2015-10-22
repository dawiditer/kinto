from cliquet.utils import strip_uri_prefix, Enum, current_service


ACTIONS = Enum(CREATE='create',
               DELETE='delete',
               READ='read',
               UPDATE='update')


class ResourceChanged(object):
    """Triggered when a resource is changed.
    """
    def __init__(self, action, resource, request):
        self.request = request
        service = current_service(request)
        resource_name = service.viewset.get_name(resource.__class__)

        self.payload = {'timestamp': resource.timestamp,
                        'action': action,
                        'uri': strip_uri_prefix(request.path),
                        'user_id': request.prefixed_userid,
                        'resource_name': resource_name}

        matchdict = dict(request.matchdict)

        if 'id' in request.matchdict:
            matchdict[resource_name + '_id'] = matchdict.pop('id')

        self.payload.update(**matchdict)
