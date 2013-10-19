from django.template import Context
from django.http import Http404, HttpResponse

from core.models import Engine
from core.decorators import json_response
from django.core.mail import EmailMessage

import simplejson

@json_response
def send_info(request):
    json_data = {
        'success': False,
        'error': ''
        }

    mbody = simplejson.loads(request.POST.get('mailbody'))
    itemid = simplejson.loads(request.POST.get('id'))
    dbitem = Engine.objects.get(pk=itemid)
    mailto = dbitem.mailvendor
    imagepath = dbitem.attachment.file_upload
    imagetostring = str(imagepath)

    try:
        #subject = 'Your subject %s: %s%s' % (dbitem.market, dbitem.market, dbitem.ccode)
        subject = 'Test'
        email = EmailMessage(
            subject,
            mbody,
            'john@doe.com',
            [mailto],
            ['john@doeBCC.com']
        )
        email.content_subtype = "html"
        email.attach_file('/Your/awesome/path'+imagetostring)
        email.send()

        json_data['success'] = True

    except Exception as err:
        json_data['error'] = str(err)
        return json_data

    return json_data

@json_response
def send_to_buy(request):
    json_data = {
        'success': False,
        'error': ''
    }
    
    mbody = simplejson.loads(request.POST.get('mailbody'))
    emailaddr = simplejson.loads(request.POST.get('mailto'))

    try:
        subject = 'Another test'
        email = EmailMessage(
            subject,
            mbody,
            'john@doe.com',
            [emailaddr],
            ['john@doeBCC.com']
        )
        email.content_subtype = "html"
        #email.attach_file('/path/to/your/awesome/file')
        email.send()

        json_data['success'] = True

    except Exception as err:
        json_data['error'] = str(err)
        return json_data

    return json_data

@json_response
def shubmail(request):
    print "here"
    json_data = {
        'success': False,
        'error': ''
    }
    
    mbody = request.POST['maildata']
    emailaddr = request.POST['mailto']
    filetoupload = request.FILES['file_upload']

    try:
        subject = 'Test another'
        email = EmailMessage(
            subject,
            mbody,
            'john@doe.com',
            [emailaddr],
            ['john@doeBCC.com']
        )
        email.content_subtype = "html"
        email.attach(filetoupload.name, filetoupload.read(), filetoupload.content_type)
        email.send()

        json_data['success'] = True

    except Exception as err:
        json_data['error'] = str(err)
        return json_data

    return json_data
