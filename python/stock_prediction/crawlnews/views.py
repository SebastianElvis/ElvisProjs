from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django import template
from django.template.loader import get_template
from stockdata import StockData
from nlp import NLP
import json, logging

def index(request):
    #sd = StockData()
    #sd.getDJIA()
    t = get_template('index.html')
    html = t.render(template.Context({'name':'elvis'}))
    return HttpResponse(html)
    
def prediction(request):
    #t = get_template('prediction.html')
    #html = t.render(template.Context({'name':'elvis'}))
    #return HttpResponse(html)
    nlp = NLP()
    nlp.startTrain()
    rt = nlp.regressionTest()
    print rt
    return HttpResponse('OK!')

def stocks(request):
    t = get_template('stocks.html')
    html = t.render(template.Context({'name':'elvis'}))
    return HttpResponse(html)
    
def news(request):
    t = get_template('news.html')
    html = t.render(template.Context({'name':'elvis'}))
    return HttpResponse(html)
    
# Create your views here.
