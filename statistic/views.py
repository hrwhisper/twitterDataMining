# Create your views here.
import json
from django.shortcuts import render
from django.http import HttpResponse
from statistic.models import timeline, pie


def hashtag_timeline(request):
    res = {
        'date': request.GET.get('date'),
        'hashtag': request.GET.get('hashtag'),
    }
    return render(request, 'statistic/hashtag_timeline.html', res)


def hashtag_timeline_data(request):
    res = timeline.get_hashtag_group_by_date(
        hashtag=request.GET.get('hashtag'), date=request.GET.get('date')
    )
    return HttpResponse(json.dumps(res), content_type="application/json")


def hashtag_compare(request):
    res = {
        'date': request.GET.get('date'),
        'hashtag1': request.GET.get('hashtag1'),
        'hashtag2': request.GET.get('hashtag2'),
    }
    return render(request, 'statistic/hashtag_compare.html', res)


def hashtag_compare_data(request):
    res = timeline.get_hashtags_group_by_date2(
        hashtags=[request.GET.get('hashtag1'), request.GET.get('hashtag2')],
        date=request.GET.get('date')
    )
    return HttpResponse(json.dumps(res), content_type="application/json")


def hashtag_pie(request):
    res = {
        'date': request.GET.get('date'),
    }
    return render(request, 'statistic/pie.html', res)


def hashtag_pie_data(request):
    res = pie.get_hashtag_pie_data_by_date()
    return HttpResponse(json.dumps(res), content_type="application/json")
