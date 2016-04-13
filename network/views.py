# Create your views here.
import json
from django.http import HttpResponse
from django.shortcuts import render
from network.models.retweet import get_retweet_network_nodes_and_links


def retweet(request):
    res = {'date': request.GET.get('date')}
    return render(request, 'network/retweet.html', res)


def retweet_data(request):
    res = get_retweet_network_nodes_and_links("")
    return HttpResponse(json.dumps(res), content_type="application/json")
