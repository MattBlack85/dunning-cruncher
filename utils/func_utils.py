#-*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse
from django.template.context import Context
from django.template.loader import get_template
from xhtml2pdf import pisa # TODO: Change this when the lib changes.
import StringIO
import os


#===============================================================================
# HELPERS
#===============================================================================
class UnsupportedMediaPathException(Exception):
    pass

def fetch_resources(uri, rel):
    """
Callback to allow xhtml2pdf/reportlab to retrieve Images,Stylesheets, etc.
`uri` is the href attribute from the html link element.
`rel` gives a relative path, but it's not used here.

"""
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT,
                            uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT,
                            uri.replace(settings.STATIC_URL, ""))
        if not os.path.exists(path):
            for d in settings.STATICFILES_DIRS:
                path = os.path.join(d, uri.replace(settings.STATIC_URL, ""))
                if os.path.exists(path):
                    break
    else:
        raise UnsupportedMediaPathException(
                                'media urls must start with %s or %s' % (
                                settings.MEDIA_ROOT, settings.STATIC_ROOT))
    return path

def generate_pdf_template_object(template_object, file_object, context):
    """
Inner function to pass template objects directly instead of passing a filename
"""
    html = template_object.render(Context(context))
    pisa.CreatePDF(html.encode("UTF-8"), file_object , encoding='UTF-8',
                   link_callback=fetch_resources)
    return file_object
#===============================================================================
# Main
#===============================================================================

def generate_pdf(template_name, file_object=None, context=None): # pragma: no cover
    """
Uses the xhtml2pdf library to render a PDF to the passed file_object, from the
given template name.
This returns the passed-in file object, filled with the actual PDF data.
In case the passed in file object is none, it will return a StringIO instance.
"""
    if not file_object:
        file_object = open('/home/MattBlack/repos/dunning-cruncher/upload/try2.pdf', 'wb')
    if not context:
        context = {}
    tmpl = get_template(template_name)
    generate_pdf_template_object(tmpl, file_object, context)
    return file_object
def render_to_pdf_response(template_name, context=None, pdfname=None, ajax=None):
    file_object = HttpResponse(content_type='application/pdf')
    if not pdfname:
        pdfname = '%s.pdf' % os.path.splitext(os.path.basename(template_name))[0]
    file_object['Content-Disposition'] = 'attachment; filename=%s' % pdfname

    if not ajax:
        return generate_pdf(template_name, file_object, context)
    else:
        return HttpResponse

def write_pdf(template_src, context_dict, filename):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = open('/home/MattBlack/repos/dunning-cruncher/upload/'+filename, 'wb') # Changed from file to filename
    pdf = pisa.pisaDocument(html.encode("UTF-8"), result)
    result.close()
    return result.name


class rem_to_do():
    MCODE = {'DE': ['DE2', 'DE3', 'DE4', 'DEP2', 'DEP3', 'DEP4'],
             'PL': ['PLW'],
             'AT': ['AT'],
             'NL': ['NL2', 'NL3', 'NL4'],
             'IT': ['ITFP3L', 'ITW3L'],
             'FR': ['FRPD', 'FRWD', 'FRD'],
             'BE': ['BEF', 'BEW'],
             'PT': ['PTD'],
             'DK': ['DK2', 'DK3'],
             'SE': ['SE2', 'SE3'],
             'FI': ['FI2', 'FI3'],
             'NO': ['NO2', 'NO3'],
             'CH': ['CH2', 'CH3', 'CH4', 'CHW2', 'CHW3', 'CHW4']
         }
    
