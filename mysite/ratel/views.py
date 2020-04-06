from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
import datetime
from django.http import Http404
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_http_methods

from polls.models import Poll
from .forms import UploadFileForm


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

# decorators
@require_http_methods(["GET", "POST"])
def test_decorator_view(request):
    # That only GET or POST requests
    pass

# Imaginary function to handle an upload file.
def handle_upload_file(f):
    with open('name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_upload_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})