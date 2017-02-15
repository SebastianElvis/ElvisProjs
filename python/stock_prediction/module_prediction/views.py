from django.http import HttpResponse
from django import template
from django.template.loader import get_template
from nlp import *
from module_data_access.base_dao import *
import logging
import re

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
    template_dict = {}

    # ID of the model object
    template_dict['nlp_obj_id'] = str(id(nlp_model))

    # Algorithm Used
    algo_re = re.compile("'(.+)'")
    used_algorithm = algo_re.findall(str(type(nlp_model.financial_model)))[0]
    template_dict['used_algorithm'] = used_algorithm

    # Penalty function used
    template_dict['penalty_function'] = nlp_model.financial_model.penalty

    # Regularization strength
    template_dict['regularization_strength'] = 1/nlp_model.financial_model.C  # C smaller, regularization stronger

    # Dataset date
    train_date_range = nlp_model.train_dataset.Date[0] \
                       + ' ~ ' \
                       + nlp_model.train_dataset.Date[nlp_model.train_dataset.Date.last_valid_index()]
    test_date_range = nlp_model.train_dataset.Date[nlp_model.train_dataset.Date.last_valid_index()] \
                      + ' ~ ' \
                      + '2017-01-01'
    template_dict['train_date_range'] = train_date_range
    template_dict['test_date_range'] = test_date_range

    # Result DataFrame of the test dataset
    test_result_df = nlp_model.regression_test()  # DataFrame
    ap00 = test_result_df.loc[0, 0]
    ap01 = test_result_df.loc[0, 1]
    ap10 = test_result_df.loc[1, 0]
    ap11 = test_result_df.loc[1, 1]
    template_dict['ap00'] = ap00
    template_dict['ap01'] = ap01
    template_dict['ap10'] = ap10
    template_dict['ap11'] = ap11

    # The sum of the test dataset
    template_dict['test_data_sum'] = ap00 + ap01 + ap10 + ap11

    t = get_template('prediction.html')
    html = t.render(template.Context(template_dict))
    return HttpResponse(html)


def stocks(request):
    t = get_template('stocks.html')
    companies = dao.get_all_processed_companies()

    html = t.render(template.Context({'companies': companies}))
    return HttpResponse(html)


def news(request):
    page = int(request.GET['page']) if request.GET.has_key('page') else 1  # The page theclient requests
    num = int(request.GET['num']) if request.GET.has_key('num') else 5  # Number displayed in one page
    type = request.GET['type'] if request.GET.has_key('type') else 'all'  # Type of the record
    sort = int(request.GET['sort']) if request.GET.has_key('sort') else -1  # 1->pymongo.ASCENDING / -1->pymongo.DESCENDING
    template_dict = {}
    template_dict['page'] = page
    template_dict['num'] = num
    template_dict['type'] = type
    template_dict['sort'] = sort
    t = get_template('news.html')
    html = t.render(template.Context(template_dict))
    return HttpResponse(html)
    
# Create your views here.
