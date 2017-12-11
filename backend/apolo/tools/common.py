from rest_framework.response import Response
from django.http import HttpResponse, response
import simplejson as json

def api_return(status=200, message='', data=''):
    response = \
        {
            'meta': message,
            'data': {} if not data else data
        }
    return json.dumps(response)
