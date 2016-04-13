# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/2/3.
from django.http import HttpResponse
from django.shortcuts import render


def index_page(request):
    return render(request, 'index.html')
