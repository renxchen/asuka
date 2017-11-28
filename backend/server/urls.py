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
from backend.apolo.apolomgr.resource.user_views import UserViewSet
from backend.apolo.apolomgr.resource.login_views import login_api
from backend.apolo.apolomgr.resource.helloworld import my_view
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'entries', EntryViewSet)
# router.register(r'users', UserViewSet, base_name='user')
user_list = UserViewSet.as_view({'get': 'get', 'post': 'post', 'put': 'put', 'delete': 'delete'})

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login_auth/', login_api),
    url(r'^my_view/', my_view),
    url(r'^users/$', user_list, name='user-list'),
    # url(r'^i18n/', include('django.conf.urls.i18n')),
]

# django jwt authentication
urlpatterns += [
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
]
