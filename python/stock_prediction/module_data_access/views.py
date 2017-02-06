from django.shortcuts import render
from django.http import HttpResponse
from django.http import FileResponse
from django.http import JsonResponse
from django import template
from django.template.loader import get_template
from base_dao import *
import json
import os


def get_all_companies(request):
    companies = dao.get_all_processed_companies()
    return HttpResponse(json.dumps(companies))
# Create your views here.


def get_file(request):
    filename = request.GET['filename']
    dataset_dir = 'dataset/stockdata/'
    file_path = os.path.abspath(dataset_dir + filename)
    return FileResponse(open(file_path, 'rb'))

def get_records_for_one_page(request):
    page = int(request.GET['page']) if request.GET.has_key('page') else 1  # The page theclient requests
    num = int(request.GET['num']) if request.GET.has_key('num') else 10  # Number displayed in one page
    type = request.GET['type'] if request.GET.has_key('type') else 'all'  # Type of the record
    sort = int(request.GET['sort']) if request.GET.has_key('sort') else -1  # 1->pymongo.ASCENDING / -1->pymongo.DESCENDING

    result = dao.get_records(page=page, num=num, type=type, sort=sort)
    return HttpResponse(json.dumps(result))
