from django.template import Context
from django.http import Http404, HttpResponse

from core.models import Engine, TrackingForm, StoredDocs, StoredForm, Vendor

from reminders.models import RemindersTable

from core.decorators import json_response
from django.core.mail import EmailMessage

from utils.sendmail import new_vendor

import json

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
        form_data = json.loads(request.POST.get('mass_data'))
        for item in form_data:
            TrackingForm(item).save()

        json_data['success'] = True

    except Exception as err:
        json_data['error'] = str(err)
        return json_data

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
    json_data['paidon'] = db_item.paidon
    json_data['amount'] = db_item.amount
    json_data['currency'] = str(db_item.currency)

    return json_data

@json_response
def update_item(request):
    json_data = {
        'success': False,
        'error': ''
        }

    try:
        data = json.loads(request.POST.get('mass_data'))
        object_id = data['itemid']
        db_item = Engine.objects.get(pk=object_id)

    except Exception as err:
        json_data['error'] = str(err)
        return json_data

    db_item.market = data['market']
    db_item.invoicenumber = data['invoicenumber']
    db_item.vendor = data['vendor']
    db_item.mailvendor = data['mailvendor']
    db_item.remindernumber = data['remindernumber']
    db_item.invoicestatus = data['invoicestatus']
    db_item.level = data['level']
    db_item.rejectreason = data['rejectreason']
    db_item.reminderdate = data['reminderdate']
    db_item.currency = data['currency']
    db_item.ccode = data['ccode']

    if data['amount']:
        db_item.amount = data['amount']

    if data['paidon']:
        db_item.paidon = data['paidon']

    try:
        db_item.save()
        json_data['success'] = True

    except Exception as err:
        json_data['error'] = str(err)
        return json_data

    return json_data

@json_response
def ajax_file_upload(request):
    json_data = {
        'success': False,
        'error': ''
        }

    try:
        NewUpload = StoredForm(request.POST, request.FILES)
        if NewUpload.is_valid():
            itemid = NewUpload.save()
            json_data['success'] = True
            json_data['id'] = itemid.id

    except Exception as err:
        json_data['error'] = str(err)
        return json_data

    return json_data

@json_response
def done(request):
    json_data = {
        'success': False,
        'error': ''
        }

    try:
        getids = json.loads(request.POST.get('idarray'))
        for item in getids:
            itemdone = Engine.objects.get(pk=item)
            itemdone.done = True
            itemdone.save()

        json_data['success'] = True

    except Exception as err:
        json_data['error'] = str(err)
        return json_data

    return json_data

@json_response
def get_vmail(request):
    json_data = {
        'success': False,
        'error': '',
        'mail_sent': False
        }

    try:
        vnum =  json.loads(request.POST.get('vendNum'))

    except Exception as err:
        json_data['error'] = str(err)
        return json_data
    try:
        mail = Vendor.objects.get(vnumber=vnum).vmail

    except Vendor.DoesNotExist:
        # we have no vendor in our db
        mail = "No mail in our DB"
        try:
            new_vendor(request)
            json_data['mail_sent'] = True

        except Exception as err:
            json_data['error'] = str(err)
            return json_data

    json_data['success'] = True
    json_data['mail'] = str(mail)

    return json_data

@json_response
def del_item(request):
    json_data = {
        'success': False,
        'error': '',
        }

    try:
        getids = json.loads(request.POST.get('idarray'))
        for item in getids:
            itemdone = Engine.objects.get(pk=item)
            itemdone.delete()

        json_data['success'] = True

    except Exception as err:
        json_data['error'] = str(err)
        return json_data

    return json_data

@json_response
def reminders(request):
    json_data = {
        'success': False,
        'error': '',
        }

    try:
        date = request.POST.get('item_date')
        market = request.POST.get('market_val')
        newvalue = request.POST.get('new_value')

        # Get out from DB the item we want to update
        item = RemindersTable.objects.get(rday=date)

        # Try to update the value if we got a different value from user
        if not int(getattr(item, market)) == int(newvalue):
            setattr(item, market, newvalue)
            item.save()

        json_data['success'] = True

    except Exception as err:
        json_data['error'] = str(err)
        return json_data

    return json_data
