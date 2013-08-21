from django.contrib import auth
from django.db import models
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context
from django.template import RequestContext
from core.models import Login
from django.contrib.auth import authenticate


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
	#"is_super": user.is_super(),
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
	# the password verified for the user
	if user.is_active:
	    return HttpResponseRedirect("/main/")
	else:
	    print("The password is valid, but the account has been disabled!")
    else:
	# the authentication system was unable to verify the username and password
	print("The username and/or password were/was incorrect.")

    return HttpResponseRedirect("/")

def tracker (request):
    return render_to_response('tracking.html', {}, RequestContext(request))
