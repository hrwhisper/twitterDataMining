# -*- coding:utf-8 -*-
# Create your views here.
import json
from django.http import HttpResponse
from django.shortcuts import render
from topic.models.TopicTrendsManager import TopicTrendsManager
from topic.models.TopicParameterManager import TopicParameterManager


def index(request):
    return render(request, 'topic/index.html')


# TODO 检查参数的合法性
def stream_trends(request):
    param_manager = TopicParameterManager(request.GET.items())
    topic_trends = TopicTrendsManager(param_manager)
    res = topic_trends.get_result(param_manager)
    return HttpResponse(json.dumps(res), content_type="application/json")


def bubble(request):
    return render(request, 'topic/visualization/result_bubble.html')


def treemap(request):
    return render(request, 'topic/visualization/result_treemap.html')

def sunburst(request):
    return render(request, 'topic/visualization/result_sunburst.html')