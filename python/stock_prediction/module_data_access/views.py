from django.shortcuts import render
from django.http import HttpResponse
from django.http import FileResponse
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
