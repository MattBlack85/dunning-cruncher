from django.template import Context
from django.http import Http404, HttpResponse

def ajax_multitracking(request):
    json_data = {
        'success': False,
        'error': ''
        }

    form_data = {}

    for key in form_data:
        form_data[key] = str(request.POST[key])
