from django.contrib import auth
from django.db import models
from core.models import Login, Engine, TrackingForm
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context
from django.template import RequestContext
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from datetime import date, timedelta

from utils.tracking_utils import ajax_multitracking, ajax_error, edit_item, update_item


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
    question = TrackingForm()
    question.fields['clerk'].widget.attrs = {'class': 'form-control'}
    #question.fields['actiontaken'].widget.attrs = {'class':'form-control'}
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
    question.fields['actiondate'].widget.attrs = {
        'class': 'form-control',
        'value': date.today()
        }
    question.fields['reminderdate'].widget.attrs = {
        'placeholder': "Insert date of reminder...",
        'class': 'form-control'
        }

    return render_to_response('tracking.html', {'question': question}, RequestContext(request))

@login_required(redirect_field_name='error', login_url='/')
def edit (request):
    user = auth.models.User.objects.get(id=request.session.get("user_id"))
    distitems = Engine.objects.all().filter(
        clerk=user.get_full_name(),
        actiondate=date.today()
        ).values('remindernumber', 'market', 'ccode').distinct()

    trackform = TrackingForm()
    trackform.fields['level'].widget.attrs = {'class': 'form-control'}
    trackform.fields['market'].widget.attrs = {'class': 'form-control'}
    trackform.fields['ccode'].widget.attrs = {'class': 'form-control'}
    trackform.fields['invoicestatus'].widget.attrs = {'class': 'form-control'}
    trackform.fields['rejectreason'].widget.attrs = {'class': 'form-control reject'}
    trackform.fields['paidon'].widget.attrs = {'class': 'form-control paid'}

    ownitems = Engine.objects.all().filter(clerk=user.first_name + " " + user.last_name, actiondate=date.today())

    return render_to_response('edit.html', {'ownitems': ownitems,
                                            'distitems': distitems,
                                            'trackform': trackform}, RequestContext(request))

@login_required(redirect_field_name='error', login_url='/')
def reporting (request):
    pass

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
        }

    try:
        return ajax_funcs.get(
            form_type,ajax_error
            )(request)
    except: # pragma: no cover
        return ajax_error("Function does not exist")

@login_required(redirect_field_name='error', login_url='/')
def draft (request, dnumber, language):
    mainit = Engine.objects.get(pk=dnumber)
    vendor = mainit.vendor
    items = Engine.objects.all().filter(remindernumber=mainit.remindernumber)
    market = mainit.market
    template = market+'_'+language+'.html'

    return render_to_response(template, {'items': items,
                                         'vendor': vendor}, RequestContext(request))
