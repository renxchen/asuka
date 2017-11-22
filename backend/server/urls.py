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
from backend.apolo.apolomgr import views

from rest_framework import routers
from backend.apolo.apolomgr.views import UserViewSet, EntryViewSet

router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'entries', EntryViewSet)
# router.register(r'users', UserViewSet, base_name='user')
user_list = UserViewSet.as_view({
    # select
    'get': 'list',
    # create
    'post': 'create',
    # update or create
    'put': 'retrieve',
    # delete
    'delete': 'destroy',
})

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^api/', include(router.urls)),
    url(r'^users/$', user_list, name='user-list'),
]
