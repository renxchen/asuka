# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
import json

# Create your views here.
def index(request):
    data = json.dumps({'test': 1})
    return HttpResponse(data)