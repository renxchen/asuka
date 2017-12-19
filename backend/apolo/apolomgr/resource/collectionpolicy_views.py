import simplejson as json
from backend.apolo.db_utils.serializer import CollectionPolicySerializer
from backend.apolo.models import CollectionPolicy
from rest_framework import viewsets
from django.utils.translation import gettext
from django.http import HttpResponse
from rest_framework.response import Response

class CollectionPolicyViewSet(viewsets.ViewSet):

    def __init__(self, request, **kwargs):
        super(CollectionPolicyViewSet, self).__init__(**kwargs)
        self.request = request


    def get_collection_policy(self, **kwargs):
        try:
            return CollectionPolicy.objects.get(**kwargs)
        except CollectionPolicy.DoesNotExist:
            raise

    def get(self):
        pass

    def post(self):
        # get new token
        new_token = self.request.META.get("NEW_TOKEN")
        # get date from request
        body = self.request.body
        cpName = eval(body)['cpName']
        osType = eval(body)['osType']
        descr = eval(body)['descr']
        execCommand = eval(body)['execCommand']
        cpType = eval(body)['cpType']
        snmpOid = "0"
        if cpType =="1":
            snmpOid = eval(body)['snmpOid']
        # set data to dict
        data={
              "cpId": 123456,
              "cpName": cpName,
              "osTypeId": 1,
              "descr": descr,
              "execCommand": execCommand,
              "cpType": cpType,
              "snmpOid": snmpOid,
              "lastExecCommandResult": "dsafsafdsafdasdf",
              "lastExeTime": 33242,
              "exterModeCommand": "afdasfasdfasf",
              "exitModeCommand": "adsfsafdsafdsa"
              }
        serializer = CollectionPolicySerializer(data=data)
        # return insert result
        if serializer.is_valid():
            print data
            serializer.save()
            return Response(serializer.data)
        else:
            return HttpResponse(json.dumps(serializer.errors))

    def put(self):
        pass

    def delete(self):
        # get new token
        new_token = self.request.META.get("NEW_TOKEN")
        cpId = None
        if 'cpId' in self.request.GET.keys():
            cpId = self.request.GET['cpId']
        kwargs = {'cpId': cpId}
        queryset = self.get_collection_policy(**kwargs)
        queryset.delete()
        return HttpResponse(gettext('Delete Successful'), {"new_token": new_token})
