from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseNotFound
import datetime
from django.http import Http404
from django.shortcuts import render
from django.core.exceptions import PermissionDenied

from polls.models import Poll


def index(request):
    pass

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def view_notfound(request):
    foo = 1
    if foo:
        #return HttpResponseNotFound('<h1>Page not found</h1>')
        return HttpResponse(status=201)
    else:
        return HttpResponse('<h1>Page was found</h1>')

# detail
def detail(request):
    poll_id = 1
    try:
        p = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404("Poll does not exist")
    return render(request, 'polls/detail.html', {'poll': p})

# 403
def permission_denied_view(request):
    raise PermissionDenied

# def permission_denied_view(request, exception=None):
#     raise HttpResponse('Error handler content', status=403)