# -*- coding: utf-8 -*-

from calendar import monthrange, month_name


from django.contrib import auth
from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import Sum, Count

from core.models import Login, Engine, TrackingForm, StoredDocs, StoredForm, Vendor

from reminders.models import RemindersTable

from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.shortcuts import render_to_response

from django.template import Context
from django.template import RequestContext
from django.template.loader import get_template

from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_protect

from django.utils import timezone

from isoweek import Week

import cStringIO as StringIO

import ho.pisa as pisa

from datetime import date, timedelta

from utils.tracking_utils import ajax_multitracking, ajax_error, edit_item, update_item
from utils.tracking_utils import ajax_file_upload, done, get_vmail, del_item, reminders
from utils.sendmail import send_info, send_to_buy, shubmail
from utils.func_utils import rem_to_do


def user_context_manager(request):
    '''Context manager which always puts certain variables into the
    template context. This is because all pages require certain
    pieces of data so it's easier to push this work down to middleware
    (grabbed from django-timetracker)
    '''
    try:
	user = auth.models.User.objects.get(id=request.session.get("user_id"))
    except auth.models.User.DoesNotExist:
	return {}
    return {
	"user": user,
        "year": date.today().year,
        "month": date.today().month,
        "week": date.today().isocalendar()[1],
	"welcome_name": user.first_name+" "+user.last_name,
    }

def index(request):
    """This function serves the base login page. This view detects if the
    user is logged in. If so, redirects, else, serves them the login
    page.

    This function shouldn't be directly called, it's invocation is automatic

    :param request: Automatically passed. Contains a map of the httprequest
    :return: A HttpResponse object which is then passed to the browser

    """
    try:
	user = auth.models.User.objects.get(id=request.session.get("user_id"))
    except auth.models.User.DoesNotExist:
	return render_to_response('index.html',
				  {'login': Login()},
				  RequestContext(request))

    if request.session.get("user_id"):
	user = auth.models.User.objects.get(id=request.session.get("user_id"))
	return HttpResponseRedirect("/main/")

def login(request):
    user_id = request.POST.get('uname')
    username = request.POST["uname"]
    password = request.POST["passw"]
    if not user_id:
	return HttpResponseRedirect("/") # pragma: no cover

    user = authenticate(username=username, password=password)
    if user:
	request.session['user_id'] = user.id
	if user.is_active:
            auth_login(request, user)
	    return HttpResponseRedirect("/main/")
	else:
	    print("The password is valid, but the account has been disabled!")
    else:
	# the authentication system was unable to verify the username and password
	print("The username and/or password were/was incorrect.")

    return HttpResponseRedirect("/")

def logout_view(request):

    """Simple logout function

    This function will delete a session id from the session dictionary
    so that the user will need to log back in order to access the same
    pages.

    :param request: Automatically passed contains a map of the httprequest
    :return: A HttpResponse object which is passed to the browser.

    """

    try:
        logout(request)
    except KeyError:
        pass
    return HttpResponseRedirect("/")

@login_required(redirect_field_name='error', login_url='/')
def tracker (request):
    fileform = StoredForm()
    question = TrackingForm()
    question.fields['clerk'].widget.attrs = {'class': 'form-control'}
    question.fields['actiontaken'].widget.attrs = {'class':'form-control'}
    question.fields['invoicestatus'].widget.attrs = {'class': 'form-control status'}
    question.fields['invoicenumber'].widget.attrs = {'class': 'form-control'}
    question.fields['market'].widget.attrs = {'class': 'form-control'}
    question.fields['ccode'].widget.attrs = {'class': 'form-control'}
    question.fields['remindernumber'].widget.attrs = {'class': 'form-control'}
    question.fields['level'].widget.attrs = {'class': 'form-control'}
    question.fields['vendor'].widget.attrs = {'class': 'form-control'}
    question.fields['mailvendor'].widget.attrs = {'class': 'form-control'}
    question.fields['rejectreason'].widget.attrs = {'class': 'form-control reject'}
    question.fields['paidon'].widget.attrs = {'class': 'form-control paid'}
    question.fields['currency'].widget.attrs = {'class': 'form-control'}
    question.fields['amount'].widget.attrs = {'class': 'form-control'}
    question.fields['reasonother'].widget.attrs = {'class': 'form-control'}
    question.fields['actiontaken'].widget.attrs = {'class': 'form-control'}
    question.fields['invoicedate'].widget.attrs = {'class': 'form-control'}
    question.fields['actiondate'].widget.attrs = {
        'class': 'form-control',
        'value': date.today()
        }
    question.fields['reminderdate'].widget.attrs = {
        'placeholder': "Insert date of the stamp...",
        'class': 'form-control'
        }

    return render_to_response('tracking.html', {'question': question,
                                                'fileform': fileform}, RequestContext(request))

@login_required(redirect_field_name='error', login_url='/')
def edit (request):
    user = auth.models.User.objects.get(id=request.session.get("user_id"))
    distitems = Engine.objects.all().filter(done=False).values('remindernumber', 'market', 'ccode').distinct()

    trackform = TrackingForm()
    trackform.fields['level'].widget.attrs = {'class': 'form-control'}
    trackform.fields['market'].widget.attrs = {'class': 'form-control'}
    trackform.fields['ccode'].widget.attrs = {'class': 'form-control'}
    trackform.fields['invoicestatus'].widget.attrs = {'class': 'form-control'}
    trackform.fields['rejectreason'].widget.attrs = {'class': 'form-control reject'}
    trackform.fields['paidon'].widget.attrs = {'class': 'form-control paid'}
    trackform.fields['amount'].widget.attrs = {'class': 'form-control amount'}
    trackform.fields['currency'].widget.attrs = {'class': 'form-control currency'}

    allitems = Engine.objects.all().filter(done=False)

    return render_to_response('edit.html', {'allitems': allitems,
                                            'distitems': distitems,
                                            'trackform': trackform}, RequestContext(request))

@login_required(redirect_field_name='error', login_url='/')
def reporting (request, rmonth=timezone.now().month, ryear=timezone.now().year):
    '''
    This view returns (for now) data from DB regarding the number of documents processed
    during the ongoing month of the ongoing year for all markets. If the user is not in
    the groups required a 403 error is raised.
    A choice for the month and year could be added to the html page to surf back
    in the past to see old data.
    '''
    try:
	user = auth.models.User.objects.get(id=request.session.get("user_id"))
    except auth.models.User.DoesNotExist:
	return render_to_response('index.html',
				  {'login': Login()},
				  RequestContext(request))

    if user.groups.get().name == 'TL' or user.groups.get().name == 'SV':
        allmarketsdone = []
        allmarketstodo = []
        howmanytodo = 0

        # We loop through all the possible options for market
        for choice in Engine.MARKET_OPT:
            if not choice[0] in ['GB', 'ES']:
                # Get from tuple the abbreviation for country
                country = choice[0]

                # Get out from DB how many items for that market have done=1
                howmanydone = Engine.objects.filter(market=country, actiondate__year=ryear, actiondate__month=rmonth, \
                                                    done=1).count()

                # Also we get a list of columns where we need to count the items "to be done"
                # and looping through that list we use Sum to get the sum of all item that 
                # must be done for specific market.
                for mcode in rem_to_do.MCODE.get(country):
                    forcountry = RemindersTable.objects.filter(rday__gte=str(ryear)+'-'+str(rmonth)+'-01') \
                    .aggregate(Sum(mcode)) \
                    .values()
                    forcountryint = forcountry[0]
                    howmanytodo = howmanytodo + forcountryint

                allmarketsdone.append(howmanydone)
                allmarketstodo.append(howmanytodo)
                howmanytodo = 0

        return render_to_response('reports.html', {'allmarketsdone': allmarketsdone,
                                                   'allmarketstodo': allmarketstodo,
                                                   'markets': Engine.MARKET_OPT}, RequestContext(request))
    else:
        raise PermissionDenied()

@csrf_protect
@login_required(redirect_field_name='error', login_url='/')
def ajax (request):
    "From django-timetracker"

    """Ajax request handler, dispatches to specific ajax functions
    depending on what json gets sent.

    Any additional ajax views should be added to the ajax_funcs map,
    this will allow the dispatch function to be used. Future revisions
    could have a kind of decorator which could be applied to functions
    to mutate some global map of ajax dispatch functions. For now,
    however, just add them into the map.

    The idea for this is that on the client-side call you would
    construct your javascript call with something like the below
    (using jQuery):

    .. code-block:: javascript

    $.ajaxSetup({
        type: 'POST',
        url: '/ajax/',
        dataType: 'json'
        });\n

    $.ajax({
        data: {
        form: 'functionName',
        data: 'data'
        }
    });

    Using this method, this allows us to construct a single view url
    and have all ajax requests come through here. This is highly
    advantagious because then we don't have to create a url map and
    construct views to handle that specific call. We just have some
    server-side map and route through there.

    The lookup and dispatch works like this:

    1) Request comes through.
    2) Request gets sent to the ajax view due to the client-side call making a
    request to the url mapped to this view.
    3) The form type is detected in the json data sent along with the call.
    4) This string is then pulled out of the dict, executed and it's response
    sent back to the browser.

    :param request: Automatically passed contains a map of the httprequest
    :return: HttpResponse object back to the browser.

    """

    # see which form we're dealing with and if it's in the POST
    form_type = request.POST.get('form_type', None)

    # if not, try the GET
    if not form_type:
        form_type = request.GET.get('form_type', None)

    #if there isn't one, we'll send an error back
    if not form_type:
        return ajax_error("Missing Form")

    # this could be mutated with a @register_ajax
    # decorator or something
    ajax_funcs = {
        'multi': ajax_multitracking,
        'edit': edit_item,
        'update': update_item,
        'mailsend': send_info,
        'mailsendbuy': send_to_buy,
        'ajax_file_upload': ajax_file_upload,
        'shubmail': shubmail,
        'done': done,
        'get_vmail': get_vmail,
        'del_item': del_item,
        'reminders': reminders,
    }

    try:
        return ajax_funcs.get(
            form_type,
            ajax_error
            )(request)

    except: # pragma: no cover
        return ajax_error("Function does not exist")

@login_required(redirect_field_name='error', login_url='/')
def draft (request, drafttype, dnumber, language):
    mainit = Engine.objects.get(pk=dnumber)
    vendor = mainit.vendor
    items = Engine.objects.all().filter(remindernumber=mainit.remindernumber)
    today = date.today()
    try:
        vendord = Vendor.objects.get(vnumber=vendor)
    except Vendor.DoesNotExist:
        vendord = None

    if language == 'EN':
        status = Engine.INVSTATUS_OPT
        reasons = Engine.REJ_REASONS
    elif language == 'FI':
        status = Engine.INVSTATUS_OPT_FI
        reasons = Engine.REJ_REASONS_FI
    elif language == 'NL':
        status = Engine.INVSTATUS_OPT_NL
        reasons = Engine.REJ_REASONS_NL
    elif language == 'SE':
        status = Engine.INVSTATUS_OPT_SE
        reasons = Engine.REJ_REASONS_SE
    elif language == 'DE':
        status = Engine.INVSTATUS_OPT_DE
        reasons = Engine.REJ_REASONS_DE
    elif language == 'IT':
        status = Engine.INVSTATUS_OPT_IT
        reasons = Engine.REJ_REASONS_IT
    elif language == 'PT':
        status = Engine.INVSTATUS_OPT_PT
        reasons = Engine.REJ_REASONS_PT
    else:
        return render_to_response("404.html", {}, RequestContext(request))

    template = mainit.market+'_'+language+'.html'

    context_dict =  {
        'items': items,
        'mainit': mainit,
        'status': status,
        'reasons': reasons,
        'iid': mainit.id,
        'today': today,
        'vendor': vendor,
        'vendord': vendord
    }

    if drafttype == 'mail':
        return render_to_response(template, context_dict, RequestContext(request))

    elif drafttype == 'prnt':
        template = 'pdf'+template
        template2pdf = get_template(template)
        context = Context(context_dict)
        html  = template2pdf.render(context)
        result = StringIO.StringIO()

        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)

        if not pdf.err:
            return HttpResponse(result.getvalue(), mimetype='application/pdf')

        return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

@login_required(redirect_field_name='error', login_url='/')
def tracking_calendar(request, year=None, week=None):
    '''
    This view will get parameters from url and will try to generate
    a table of the current week where reminders we get can be tracked.
    '''

    # If there is no year we generate it
    if year == None:
        ryear = date.today().year
    else:
        ryear = int(year)

    # The same with the week
    if week == None:
        rweek = date.today().isocalendar()[1]
    else:
        rweek = int(week)

    # If someone tries to insert manually a week which doesn't exist
    # we return him/her a 403 page (have to change with something else).
    if week > '53':
        raise PermissionDenied()

    isoweek = Week(ryear, rweek)
    sqlweek = []

    for x in range(5):
        sqlweek.append(isoweek.day(x))

    try:
        RemindersTable.objects.get(rday=isoweek.day(0))
    except RemindersTable.DoesNotExist:
        for x in range(5):
            RemindersTable.objects.create(rday=isoweek.day(x))

    tableresults = []
    dayrow = []

    for day in sqlweek:
        weekresults = RemindersTable.objects.filter(rday=day)
        for value in weekresults.values_list()[0]:
            dayrow.append(value)
        tableresults.append(dayrow)
        dayrow = []

    headers = weekresults.values().field_names

    return render_to_response("calendar.html", {'sqlweek': sqlweek,
                                                'headers': headers,
                                                'tableresults': tableresults}, RequestContext(request))
