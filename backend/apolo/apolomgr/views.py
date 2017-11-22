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


# @api_view(['POST', "GET", "DELETE", "PUT", "PATCH"])
class UserViewSet(viewsets.ViewSet):
    # queryset = User.objects.all()
    # serializer_class = UserSerializer
    # create / retrieve / update / destroy
    def list(self, request):
        print 11111
        # print request.GET['value']
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        print 22222
        data = json.dumps({'test': 'create'})
        return HttpResponse(data)

    def retrieve(self, request, pk=None):
        print 3333
        data = json.dumps({'test': 'retrieve'})
        return HttpResponse(data)

    def destroy(self, request, pk=None):
        print 4444
        data = json.dumps({'test': 'destroy'})
        return HttpResponse(data)


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
