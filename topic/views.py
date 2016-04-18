# -*- coding:utf-8 -*-
# Create your views here.
import json
from django.http import HttpResponse
from django.shortcuts import render
from topic.models.TopicTrendsManager import TopicTrendsManager
from topic.models.TopicParameterManager import TopicParameterManager


def index(request):
    return render(request, 'topic/index.html')


# TODO 检查参数合法性
def stream_trends(request):
    param = dict(request.GET.items())
    for x, t in param.items():
        if param[x] == '':
            del param[x]

    param_manager = TopicParameterManager(param)
    topic_trends = TopicTrendsManager(param_manager)
    res = topic_trends.get_result(param_manager)
    return HttpResponse(json.dumps(res), content_type="application/json")
