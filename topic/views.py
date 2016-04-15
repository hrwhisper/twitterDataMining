# Create your views here.
import json
from django.http import HttpResponse
from django.shortcuts import render
from topic.models.TopicTrendsManager import TopicTrendsManager


def index(request):
    return render(request, 'topic/index.html')


def stream_trends(request):
    track = request.GET['track']
    follow = request.GET['follow']
    location = request.GET['location']
    print track, follow, location

    topic_trends = TopicTrendsManager()
    res = topic_trends.get_result()
    return HttpResponse(json.dumps(res), content_type="application/json")
