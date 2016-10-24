from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django import template
from django.template.loader import get_template
from stockdata import StockData
import json

def hello(request):
    return HttpResponse('Hello World!')
    
def index(request):
    #sd = StockData()
    #sd.getDJIA()
    t = get_template('index.html')
    html = t.render(template.Context({'name':'elvis'}))
    return HttpResponse(html)
    
def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def testtpl(request):
    html = 'My name is {{ name }}'
    t = template.Template(html)
    c = template.Context({'name' : 'Elvis'})
    return HttpResponse(t.render(c))
    
# Create your views here.
