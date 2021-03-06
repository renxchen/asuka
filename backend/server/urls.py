"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
# from backend.apolo.apolomgr.resource.user_views import UserViewSet
from backend.apolo.apolomgr import resource_api
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'entries', EntryViewSet)
# router.register(r'users', UserViewSet, base_name='user')
# user_list = UserViewSet.as_view({'get': 'get', 'post': 'post', 'put': 'put', 'delete': 'delete'})

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^v1/api_permission_auth/', resource_api.api_permission_auth),
    url(r'^v1/api_collection_policy/', resource_api.api_collection_policy),
    url(r'^v1/api_collection_policy_group/', resource_api.api_collection_policy_group),
    url(r'^v1/api_ostype/', resource_api.api_ostype),
    url(r'^v1/api_policy_tree/', resource_api.api_policy_tree),
    url(r'^v1/api_policy_tree_highlight/', resource_api.api_policy_tree_high_light),
    url(r'^v1/api_get_collection_policy_name/', resource_api.api_get_collection_policy_name),
    url(r'^v1/api_policy_tree_rule/', resource_api.api_policy_tree_rule),
    url(r'^v1/api_data_collection/', resource_api.api_data_collection),
    url(r'^v1/api_new_data_collection/', resource_api.api_new_data_collection),
    url(r'^v1/api_device_group/', resource_api.api_device_group),
    # action policy related start
    url(r'^v1/api_data_table_step3_table/', resource_api.api_data_table_step3_table),
    url(r'^v1/api_data_table_step4_tree/', resource_api.api_data_table_step4_tree),
    url(r'^v1/api_data_table_step4_table/', resource_api.api_data_table_step4_table),
    url(r'^v1/api_data_table_step1/', resource_api.api_data_table_step1),
    url(r'^v1/api_data_table_name_verify/', resource_api.api_data_table_name_verify),
    url(r'^v1/api_action_policy/', resource_api.api_action_policy),
    url(r'^v1/api_regenerate_trigger_detail/', resource_api.api_regenerate_trigger_detail),
    url(r'^v1/api_column/', resource_api.api_column),
    url(r'^v1/api_column_verify/', resource_api.api_column_verify),
    url(r'^v1/api_expression_verify/', resource_api.api_expression_verify),
    url(r'^v1/api_data_table_csv_export/', resource_api.api_data_table_csv_export),
    url(r'^v1/api_action_policy_mem_cache/', resource_api.api_action_policy_mem_cache),
    # action policy related end
    url(r'^v1/api_data_collection_devices/', resource_api.api_data_collection_by_device),
    url(r"^v1/api_collection_policy_edit_page/", resource_api.api_collection_policy_edit),
    url(r'^v1/api_data_collection_policy/', resource_api.api_data_collection_by_cp),
    url(r'^v1/api_emergency_stop_list/', resource_api.api_emergency_stop_list),
    # device view related start
    url(r'^v1/api_device_ostype/', resource_api.api_device_ostype),
    url(r'^v1/api_device_groups/', resource_api.api_device_groups),
    url(r'^v1/api_device/upload', resource_api.api_device_upload),
    url(r'^v1/api_device/export', resource_api.api_device_export),
    url(r'^v1/api_device/', resource_api.api_device),
    url(r'^v1/api_device_pre/', resource_api.api_device_pre),
    # device view related end
    # url(r'^users/$', user_list, name='user-list'),
    # url(r'^i18n/', include('django.conf.urls.i18n')),
]

# django jwt authentication
urlpatterns += [
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
]
# collection test start
import platform

if 'WINDOWS' not in platform.system().upper():
    urlpatterns += [
        url(r'^v1/api_cli_collection_test/', resource_api.api_cli_collection_test),
        url(r'^v1/api_snmp_collection_test/', resource_api.api_snmp_collection_test),
    ]
# collection test end
