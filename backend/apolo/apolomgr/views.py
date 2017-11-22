# Create your views here.
from django.http import HttpResponse
import simplejson as json
from backend.apolo.db_utils.serializer import *
import django_filters
from rest_framework import viewsets, filters
from backend.apolo.db_utils.serializer import UserSerializer, EntrySerializer
from backend.apolo.models import User, Entry


# Create your views here.
def index(request):
    data = json.dumps({'test': 1})
    return HttpResponse(data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
