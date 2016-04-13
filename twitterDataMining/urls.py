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
from django.conf.urls import url, include
import twitterDataMining.views
import network.views

urlpatterns = [
    url(r'^$', twitterDataMining.views.index_page),
    url(r'^network/', include('network.urls')),
    url(r'^statistic/', include('statistic.urls')),
    url(r'^topic/', include('topic.urls')),
    url(r'^sentiment/', include('sentiment.urls')),
]
