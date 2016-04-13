# Create your views here.
import json
import time
from django.http import HttpResponse
from django.shortcuts import render
from topic.models.TopicTrendsManager import TopicTrendsManager


def index(request):
    return render(request, 'topic/index.html')


def stream_trends(request):
    topic_trends = TopicTrendsManager()
    res = topic_trends.get_result()
    return HttpResponse(json.dumps(res), content_type="application/json")
