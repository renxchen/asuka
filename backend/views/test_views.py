from django.http import HttpResponse


def hello(request):
    # print 'GET: ', request.GET['aa']
    # print 'POST: ', request.POST.get('aa')
    # print 'POST2: ', request.body
    return HttpResponse("Hello world !")
