from django.utils.translation import gettext
from django.http import HttpResponse

def my_view(request):
    output = gettext("Welcome to my site.")
    return HttpResponse(output)