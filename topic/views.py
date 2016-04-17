# -*- coding:utf-8 -*-
# Create your views here.
import json
from django.http import HttpResponse
from django.shortcuts import render
from topic.models.TopicTrendsManager import TopicTrendsManager


def index(request):
    return render(request, 'topic/index.html')


# TODO 检查参数合法性
def stream_trends(request):
    param = dict(request.GET.items())
    for x, t in param.items():
        if param[x] == '':
            del param[x]

    # ---------- stream ---------
    # track = param.get('track', None)
    # follow = param.get('follow', None)
    # location = param.get('location', None)
    # storeIntoDB = param.get('storeIntoDB', None)
    # storeIntoDBName = param.get('storeIntoDBName', None)
    #
    #
    #  ---------- LDA ------------
    # LDA_k = param.get('LDA_k', None)
    # LDA_timeWindow = param.get('LDA_timeWindow', None)
    #
    #
    # ----------- Local -----------
    # startDate = param.get('startDate', None)
    # endDate = param.get('endDate', None)
    # endDate = param.get('localCollectionsName', None)

    topic_trends = TopicTrendsManager(param)
    res = topic_trends.get_result(param)
    return HttpResponse(json.dumps(res), content_type="application/json")
