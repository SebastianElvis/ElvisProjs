from django.http import HttpResponse
from django import template
from django.template.loader import get_template
from nlp import *
from module_data_access.base_dao import *
import logging

logger = logging.getLogger("django")


def index(request):
    # sd = StockData()
    # sd.getDJIA()
    template_dict = {
        'name': 'elvis',
        'nlp_obj_id': id(nlp_model)
    }
    t = get_template('index.html')
    html = t.render(template.Context(template_dict))
    return HttpResponse(html)


def prediction(request):
    # t = get_template('prediction.html')
    # html = t.render(template.Context({'name':'elvis'}))
    # return HttpResponse(html)
    logger.debug('The id of NLP Object is ---' + str(id(nlp_model)))
    return HttpResponse('OK! The ID of the nlp_model is %d' % id(nlp_model))


def stocks(request):
    t = get_template('stocks.html')
    companies = dao.get_all_processed_companies()

    html = t.render(template.Context({'companies': companies}))
    return HttpResponse(html)


def news(request):
    t = get_template('news.html')
    html = t.render(template.Context({'name':'elvis'}))
    return HttpResponse(html)
    
# Create your views here.
