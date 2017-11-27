# Create your views here.
from django.http import HttpResponse
import simplejson as json
from backend.apolo.db_utils.serializer import UserSerializer
from backend.apolo.models import User
from rest_framework.response import Response
from rest_framework import viewsets
from authentication import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view


@permission_classes((IsAuthenticated,))
class UserViewSet(viewsets.ViewSet):
    def get_user(self, **kwars):
        try:
            return User.objects.get(**kwars)
        except User.DoesNotExist:
            raise

    def get(self, request):

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

    def post(self, request):
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

    def put(self, request):
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

    def delete(self, request, pk=None):
        id = None
        if 'id' in request.GET.keys():
            id = request.GET['id']
        # queryset = User.objects.filter(pk=id)
        kwargs = {'id': id}
        queryset = self.get_user(**kwargs)
        queryset.delete()
        return HttpResponse('Delete Successful')
