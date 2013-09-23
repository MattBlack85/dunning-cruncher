from django.template import Context
from django.http import Http404, HttpResponse

from core.models import Engine, TrackingForm
from core.decorators import json_response

import simplejson

@json_response
def ajax_error(error):

    """Returns a HttpResponse with JSON as a payload

    This function is a simple way of instantiating an error when using
    json_functions. It is decorated with the json_response decorator so that
    the dict that we return is dumped into a json object.

    :param error: :class:`str` which contains the pretty
    error, this will be seen by the user so
    make sure it's understandable.
    :returns: :class:`HttpResponse` with mime/application of json.
    :rtype: :class:`HttpResponse`
    """

    return {
        'success': False,
        'error': str(error)
        }


@json_response
def ajax_multitracking(request):
    json_data = {
        'success': False,
        'error': ''
        }

    form = {}

    try:
        form_data = simplejson.loads(request.POST.get('mass_data'))
        x = 1
        for item in form_data:
            form[x] = item
            TrackingForm(form[x]).save()

    except Exception as err:
        json_data['error'] = str(err)
        return json_data

    json_data['success'] = True
    json_data['data'] = form_data
    return json_data

@json_response
def edit_item(request):
    json_data = {
        'success': False,
        'error': ''
        }

    try:
        object_id = request.POST.get('id')
        toNum = int(object_id)
        print object_id
        print toNum
        #db_item = Engine.objects.filter(pk=toNum)
    
    except Exception as err:
        json_data['error'] = str(err)
        return json_data

    json_data['success'] = True
    json_data['itemid'] = object_id

    return json_data
