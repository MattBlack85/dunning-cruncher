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

    try:
        form_data = simplejson.loads(request.POST.get('mass_data'))
        for item in form_data:
            TrackingForm(item).save()

    except Exception as err:
        json_data['error'] = str(err)
        return json_data

    TrackingForm()
    json_data['success'] = True
    return json_data

@json_response
def edit_item(request):
    json_data = {
        'success': False,
        'error': ''
        }

    try:
        object_id = request.POST.get('id')
        db_item = Engine.objects.get(pk=object_id)

    except Exception as err:
        json_data['error'] = str(err)
        return json_data

    json_data['success'] = True
    json_data['itemid'] = object_id
    json_data['market'] = str(db_item.market)
    json_data['ccode'] = str(db_item.ccode)
    json_data['level'] = str(db_item.level)
    json_data['reminderdate'] = str(db_item.reminderdate)
    json_data['remindernumber'] = str(db_item.remindernumber)
    json_data['vendor'] = str(db_item.vendor)
    json_data['mailvendor'] = str(db_item.mailvendor)
    json_data['invoicenumber'] = str(db_item.invoicenumber)
    json_data['invoicestatus'] = str(db_item.invoicestatus)
    json_data['rejectreason'] = str(db_item.rejectreason)
    json_data['paidon'] = str(db_item.paidon)

    return json_data

@json_response
def update_item(request):
    pass
