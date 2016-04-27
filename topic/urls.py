"""twitterDataMining URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
import topic.views

urlpatterns = [
    url(r'^$', topic.views.index),
    url(r'stream_trends$', topic.views.stream_trends),
    url(r'stop_trends$', topic.views.stop_trends),
    url(r'text$', topic.views.text),
    url(r'bubble$', topic.views.bubble),
    url(r'treemap$', topic.views.treemap),
    url(r'sunburst$', topic.views.sunburst),
    url(r'funnel$', topic.views.funnel),
]
