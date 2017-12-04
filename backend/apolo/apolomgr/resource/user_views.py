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
from django.core.paginator import Paginator
from backend.apolo.tools.exception import exception_handler


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
            page = self.request.GET.get('page')
            max_size = self.request.GET.get('max_size')
            queryset = User.objects.all()
            if 'name' in self.request.GET.keys():
                name = self.request.GET['name']
                if name:
                    queryset = User.objects.filter(name=name)
            serializer = UserSerializer(queryset, many=True)
            paginator = Paginator(serializer.data, max_size)
            contacts = paginator.page(page)
            # contacts.has_next()
            # contacts.has_previous()
            # contacts.has_other_pages()
            # contacts.next_page_number()
            # contacts.previous_page_number()
            # contacts.start_index()  # The 1-based index of the first item on this page
            # contacts.end_index()
            return Response({'data': contacts.object_list, 'new_token': new_token, 'num_page': paginator.num_pages,
                             'page_range': list(paginator.page_range), 'page_has_next': contacts.has_next()})
        except Exception, e:
            # return Response(status=404)
            return exception_handler(e)

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
