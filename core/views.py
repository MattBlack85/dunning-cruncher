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
    if request.method == 'POST':
	question = TrackingForm(request.POST)
        if question.is_valid():
            question.save()

    question = TrackingForm()
    question.fields['clerk'].widget.attrs = {'class': 'form-control'}
    question.fields['actiontaken'].widget.attrs = {'class':'form-control'}
    question.fields['invoicestatus'].widget.attrs = {'class':'form-control status'}
    question.fields['invoicenumber'].widget.attrs = {'class':'form-control'}
    question.fields['market'].widget.attrs = {'class':'form-control'}
    question.fields['ccode'].widget.attrs = {'class':'form-control'}
    question.fields['remindernumber'].widget.attrs = {'class':'form-control'}
    question.fields['level'].widget.attrs = {'class':'form-control'}
    question.fields['vendor'].widget.attrs = {'class':'form-control'}
    question.fields['mailvendor'].widget.attrs = {'class':'form-control'}
    question.fields['rejectreason'].widget.attrs = {'class':'form-control'}
    question.fields['paidon'].widget.attrs = {'class':'form-control'}
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
def reporting (request):
    pass
