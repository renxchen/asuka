from backend.apolo.apolomgr.resource import authentication
from backend.apolo.apolomgr.resource import user_views
import json
from django.http import HttpResponse
from authentication import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
import traceback


def run_request_method(resource_object):
    try:
        request_method = resource_object.request.method.lower()
        if request_method == 'post':
            return resource_object.post()
        elif request_method == 'get':
            return resource_object.get()
        elif request_method == 'put':
            return resource_object.put()
        elif request_method == 'delete':
            return resource_object.delete()
        elif request_method == 'patch':
            return resource_object.patch()
    except Exception as e:
        error_message = traceback.format_exc()
        print error_message


@api_view(["POST"])
def login(request):
    resource_object = authentication.Auth(request=request)
    return run_request_method(resource_object)


@api_view(['POST', "GET", "DELETE", "PUT"])
@permission_classes((IsAuthenticated,))
def api_users(request):
    resource_object = user_views.UserViewSet(request=request)
    return run_request_method(resource_object)
