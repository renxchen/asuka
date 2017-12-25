from rest_framework.permissions import IsAuthenticated
from backend.apolo.apolomgr.resource import authentication, policytree_view, policy_tree_highlight_view
from backend.apolo.apolomgr.resource import user_views
from backend.apolo.apolomgr.resource import collection_policy_views
from backend.apolo.apolomgr.resource import collection_policy_group_views
from backend.apolo.apolomgr.resource import common_views
from django.http import HttpResponse
from rest_framework.decorators import permission_classes, api_view
import traceback
from backend.apolo.apolomgr.resource.authentication import auth_if_refresh_required


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
    return HttpResponse(run_request_method(resource_object))


@api_view(['POST', "GET", "DELETE", "PUT"])
@permission_classes((IsAuthenticated,))
@auth_if_refresh_required
def api_users(request):
    resource_object = user_views.UserViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(['POST', "GET", "DELETE", "PUT"])
@permission_classes((IsAuthenticated,))
@auth_if_refresh_required
def api_collection_policy(request):
    resource_object = collection_policy_views.CollPolicyViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(['POST', "GET", "DELETE", "PUT"])
@permission_classes((IsAuthenticated,))
@auth_if_refresh_required
def api_collection_policy_group(request):
    resource_object = collection_policy_group_views.CollPolicyGroupViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
@auth_if_refresh_required
def api_get_ostype(request):
    resource_object = common_views.OsTypeViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(['POST', "GET", "DELETE", "PUT"])
@permission_classes((IsAuthenticated,))
@auth_if_refresh_required
def api_policy_tree(request):
    resource_object = policytree_view.PolicyTreeViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(['POST', "GET", "DELETE", "PUT"])
@permission_classes((IsAuthenticated,))
@auth_if_refresh_required
def api_policy_tree_high_light(request):
    resource_object = policy_tree_highlight_view.PolicyTreeHighLightViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
@auth_if_refresh_required
def api_get_collection_policy_name(request):
    resource_object = common_views.CollPolicyViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))
