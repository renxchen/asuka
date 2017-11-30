# Create your views here.
from django.http import HttpResponse
import simplejson as json
from backend.apolo.db_utils.serializer import UserSerializer
from backend.apolo.models import User
from rest_framework.response import Response
from rest_framework import viewsets
from django.utils.translation import gettext
from django.http import HttpResponse
from rest_framework.response import Response


class UserViewSet(viewsets.ViewSet):
    def __init__(self, request, **kwargs):
        super(UserViewSet, self).__init__(**kwargs)
        self.request = request

    def get_user(self, **kwars):
        try:
            return User.objects.get(**kwars)
        except User.DoesNotExist:
            raise

    def get(self):
        try:
            print 'get'
            new_token = self.request.META.get("NEW_TOKEN")
            queryset = User.objects.all()
            if 'name' in self.request.GET.keys():
                name = self.request.GET['name']
                if name:
                    queryset = User.objects.filter(name=name)
            serializer = UserSerializer(queryset, many=True)
            # return Response(serializer.data)
            # return Response(serializer.data)
            return Response({'data': serializer.data, 'new_token': new_token})
        except User.DoesNotExist:
            return Response(status=404)

    def post(self):
        print 'post'
        name = ''
        mail = ''
        # token = self.request.META.get("HTTP_AUTHORIZATION").split()[1]
        # r = Token(token)
        # new_token = r.refresh_token()
        # print new_token
        if 'name' in self.request.GET.keys():
            name = self.request.GET['name']
        if 'mail' in self.request.GET.keys():
            mail = self.request.GET['mail']
        # data = [{'name': name, 'mail': mail}]
        data = {'name': name, 'mail': mail}
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return HttpResponse(json.dumps(serializer.errors))

    def put(self):
        print 'put'
        id = ''
        if 'id' in self.request.GET.keys():
            id = self.request.GET['id']
        kwargs = {'id': id}
        queryset = self.get_user(**kwargs)
        name = self.request.GET['name']
        mail = self.request.GET['mail']
        # data = JSONParser().parse(request.GET.values())
        # queryset = User.objects.filter(pk=id)
        # data = json.loads(request.GET.values())
        data = {'name': name, 'mail': mail}
        serializer = UserSerializer(queryset, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return HttpResponse(json.dumps(serializer.errors))

    def delete(self):
        print 'delete'
        id = None
        if 'id' in self.request.GET.keys():
            id = self.request.GET['id']
        # queryset = User.objects.filter(pk=id)
        kwargs = {'id': id}
        queryset = self.get_user(**kwargs)
        queryset.delete()
        return HttpResponse(gettext('Delete Successful'))
