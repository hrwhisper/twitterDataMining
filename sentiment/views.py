from django.shortcuts import render

# Create your views here.
from sentiment.models.SentimentManager import query_sentiment_for_online_data
import json
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'sentiment/index.html')


def query(request):
    query_str = request.GET.get('query_str')
    # TODO if none raise error
    total_positive, total_tweets, positive_percentage = query_sentiment_for_online_data(query_str)
    res = {
        'total_positive': total_positive,
        'total_tweets': total_tweets,
        'positive_percentage': positive_percentage
    }
    return HttpResponse(json.dumps(res), content_type="application/json")
