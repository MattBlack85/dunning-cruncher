from django.http import HttpResponse

from functools import wraps

import simplejson

def json_response(func):

    """
    Decorator function that when applied to a function which
    returns some json data will be turned into a HttpResponse
    
    This is useful because the call site can literally just
    call the function as it is without needed to make a http-
    response.
    
    :param func: Function which returns a dictionary
    :returns: :class:`HttpResponse` with mime/application as JSON
    """
    
    @wraps(func)
    def inner(request):
        
        """
        Grabs the request object on the decorated and calls
        it
        """
        
        return HttpResponse(simplejson.dumps(func(request)),
                            mimetype="application/json")
    return inner
