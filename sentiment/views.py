from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


def index(request):
    return render(request, 'sentiment/index.html')


def query(request):
    return render(request, 'sentiment/query.html')
