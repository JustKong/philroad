from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from modules import scraper

POST = 'POST'
ARTICLE_DATA = 'article'
MIME_JSON = 'application/json'

ERROR_NOT_POST = 'Error: Did not request via POST'
ERROR_INSUFF_DATA = 'Error: Insufficient POST data sent'


def home(request):
    return render_to_response('views/index.html', RequestContext(request))


def fetch(request):
    error_msg = ERROR_NOT_POST
    if request.method == POST:
        if ARTICLE_DATA in request.POST:
            article = request.POST[ARTICLE_DATA]
            content = scraper.get_to_phil(article)
            return HttpResponse(content = simplejson.dumps(content), mimetype = MIME_JSON)
        else:
            error_msg = ERROR_INSUFF_DATA
    return HttpResponseServerError(error_msg)
