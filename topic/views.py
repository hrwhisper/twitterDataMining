# -*- coding:utf-8 -*-
# Create your views here.
import json
from django.http import HttpResponse
from django.shortcuts import render
from topic.models.TopicTrendsManager import TopicTrendsManager
from topic.models.TopicParameterManager import TopicParameterManager


def index(request):
    return render(request, 'topic/index.html')


# TODO 检查参数的合法性, and change to post method
def stream_trends(request):
    param_manager = TopicParameterManager(request.GET.items())
    topic_trends = TopicTrendsManager(param_manager)
    res = topic_trends.get_result(param_manager)
    return HttpResponse(json.dumps(res), content_type="application/json")


def stop_trends(request):
    topic_trends = TopicTrendsManager(None)
    topic_trends.stop()
    res = {"stop": "stop success"}
    return HttpResponse(json.dumps(res), content_type="application/json")


def text(request):
    return render(request, 'topic/visualization/result_text.html')


def bubble(request):
    return render(request, 'topic/visualization/result_bubble.html')


def treemap(request):
    return render(request, 'topic/visualization/result_treemap.html')


def sunburst(request):
    return render(request, 'topic/visualization/result_sunburst.html')


def funnel(request):
    return render(request, 'topic/visualization/result_funnel.html')


def heatmap(request):
    return render(request, 'topic/visualization/result_heatmap.html')


def hashtags_pie(request):
    return render(request, 'topic/visualization/result_hashtags_pie.html')


def hashtags_histogram(request):
    return render(request, 'topic/visualization/result_hashtags_histogram.html')


def hashtags_timeline(request):
    return render(request, 'topic/visualization/result_hashtags_timeline.html')