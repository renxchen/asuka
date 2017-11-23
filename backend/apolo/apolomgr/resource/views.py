# Create your views here.
from django.http import HttpResponse
import simplejson as json
from backend.apolo.db_utils.serializer import *
import django_filters
from rest_framework import viewsets, filters, status
from backend.apolo.db_utils.serializer import UserSerializer, EntrySerializer
from backend.apolo.models import User, Entry
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route, list_route
from django.shortcuts import get_object_or_404
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


# Create your views here.
# @api_view(['GET', 'POST'])
# def index(request):
#     print '-----:, ', request.data
#     pk = request.GET('value')
#
#     try:
#         queryset = User.objects.get(name=pk)
#         print queryset
#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = UserSerializer(queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'PUT':
#         serializer = UserSerializer(queryset, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         queryset.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ViewSet):
    def get_user(self, **kwars):
        try:
            return User.objects.get(**kwars)
        except User.DoesNotExist:
            raise

    def list(self, request):
        try:
            queryset = User.objects.all()
            if 'name' in request.GET.keys():
                name = request.GET['name']
                if name:
                    queryset = User.objects.filter(name=name)
            serializer = UserSerializer(queryset, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return HttpResponse(status=404)

    def create(self, request):
        name = ''
        mail = ''
        if 'name' in request.GET.keys():
            name = request.GET['name']
        if 'mail' in request.GET.keys():
            mail = request.GET['mail']
        # data = [{'name': name, 'mail': mail}]
        data = {'name': name, 'mail': mail}
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return HttpResponse(json.dumps(serializer.errors))

    def retrieve(self, request):
        id = ''
        if 'id' in request.GET.keys():
            id = request.GET['id']
        kwargs = {'id': id}
        queryset = self.get_user(**kwargs)
        name = request.GET['name']
        mail = request.GET['mail']
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

    def destroy(self, request, pk=None):
        id = None
        if 'id' in request.GET.keys():
            id = request.GET['id']
        # queryset = User.objects.filter(pk=id)
        kwargs = {'id': id}
        queryset = self.get_user(**kwargs)
        queryset.delete()
        return HttpResponse('Delete Successful')


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
