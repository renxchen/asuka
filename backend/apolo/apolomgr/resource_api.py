import traceback

from django.http import HttpResponse
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from backend.apolo.apolomgr.resource.collection_policy import collection_policy_views
from backend.apolo.apolomgr.resource.collection_policy_group import collection_policy_group_views
from backend.apolo.apolomgr.resource.collection_policy_tree import policy_tree_highlight_view, policytree_view, \
    policy_tree_rule_view, collection_policy_edit_view
from backend.apolo.apolomgr.resource.action_policy_table import data_table_step3_views, data_table_step1_views, \
    data_table_step4_table_views, data_table_step4_tree_views
from backend.apolo.apolomgr.resource.action_policy import action_policy_views, action_policy_column_views, \
    action_policy_column_verify, verify_expression
from backend.apolo.apolomgr.resource.common import common_views
from backend.apolo.apolomgr.resource.data_collection import data_collection_view, new_data_collection_view, \
    data_collection_by_device_view, data_collection_by_cp_view
from backend.apolo.apolomgr.resource.device import ostype_views, groups_views, device_views, device_pre_view, \
    device_upload, device_export
from backend.apolo.apolomgr.resource.login import authentication
from backend.apolo.apolomgr.resource.login.authentication import auth_if_refresh_required
from backend.apolo.tools import constants
from backend.apolo.tools.exception import exception_handler


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
        if constants.DEBUG_FLAG:
            print traceback.format_exc(e)
        return exception_handler(e)


@api_view(["POST"])
def login(request):
    resource_object = authentication.Auth(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(["DELETE"])
def logout(request):
    resource_object = authentication.Auth(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(['POST', "GET", "DELETE", "PUT"])
# @authentication_classes((SessionAuthentication, BasicAuthentication))
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_collection_policy(request):
    resource_object = collection_policy_views.CollPolicyViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(['POST', "GET", "DELETE", "PUT"])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_collection_policy_group(request):
    resource_object = collection_policy_group_views.CollPolicyGroupViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(["GET"])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_ostype(request):
    resource_object = common_views.OsTypeViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(['POST', "GET", "DELETE", "PUT"])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_policy_tree(request):
    resource_object = policytree_view.PolicyTreeViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(["POST"])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_policy_tree_high_light(request):
    resource_object = policy_tree_highlight_view.PolicyTreeHighLightViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(["GET"])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_get_collection_policy_name(request):
    resource_object = common_views.CollPolicyViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(['POST', "GET", "DELETE", "PUT"])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_policy_tree_rule(request):
    resource_object = policy_tree_rule_view.PolicyTreeRuleViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(['POST', "GET", "DELETE", "PUT"])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_data_collection(request):
    resource_object = data_collection_view.DataCollectionViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(['POST', "GET"])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_new_data_collection(request):
    resource_object = new_data_collection_view.NewDataCollectionViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(["GET"])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_device_group(request):
    resource_object = common_views.DeviceGroupViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(["GET"])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_data_table_step3_table(request):
    resource_object = data_table_step3_views.DataTableCoulumnViewsSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(["GET"])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_data_table_step4_tree(request):
    resource_object = data_table_step4_tree_views.DataTableTreeViewsSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(["GET"])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_data_table_step4_table(request):
    resource_object = data_table_step4_table_views.DataTableTableViewsSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(['POST', "GET", "DELETE", "PUT"])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_data_table_step1(request):
    resource_object = data_table_step1_views.TableViewsSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(['PUT', "GET"])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_data_collection_by_device(request):
    resource_object = data_collection_by_device_view.DataCollectionByDeviceViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(['PUT', "GET"])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_collection_policy_edit(request):
    resource_object = collection_policy_edit_view.CollectionPolicyEditViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(["GET"])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_data_collection_by_cp(request):
    resource_object = data_collection_by_cp_view.DataCollectionByCPViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(['POST', "GET", "DELETE", "PUT"])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_device_ostype(request):
    resource_object = ostype_views.OsTypeViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(['POST', "GET", "DELETE", "PUT"])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_action_policy(request):
    resource_object = action_policy_views.ActionPolicyViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(['GET'])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_regenerate_trigger_detail(request):
    resource_object = action_policy_views.ActionPolicyViewSet(request=request)
    resource_object.regenerate_trigger_detail()
    return HttpResponse('Successful')


@api_view(['GET'])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_column(request):
    resource_object = action_policy_column_views.ActionPolicyColumnViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(['GET'])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_column_verify(request):
    resource_object = action_policy_column_verify.ActionPolicyColumnVerifyViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(['GET'])
# @auth_if_refresh_required
# @permission_classes((IsAuthenticated,))
def api_expression_verify(request):
    resource_object = verify_expression.ExpressionVerify(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(['POST', "GET", "DELETE", "PUT"])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_device_groups(request):
    resource_object = groups_views.GroupsViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(['POST', "GET", "DELETE", "PUT"])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_device(request):
    resource_object = device_views.DevicesViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(['POST', "GET", "DELETE", "PUT"])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_device_upload(request):
    resource_object = device_upload.DevicePreViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(['POST', "GET", "DELETE", "PUT"])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_device_pre(request):
    resource_object = device_pre_view.DevicePreViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))


@api_view(['POST', "GET", "DELETE", "PUT"])
@auth_if_refresh_required
@permission_classes((IsAuthenticated,))
def api_device_export(request):
    resource_object = device_export.ExportDevicesViewSet(request=request)
    return HttpResponse(run_request_method(resource_object))
