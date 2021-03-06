"""ss_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.contrib import admin

from app_ss import api

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'', admin.site.urls),
    url(r'listservers', api.listservers),
    url(r'online', api.online),
    url(r'offline', api.offline),
    url(r'update_traffic', api.update_traffic),
    url(r'register_device',api.register_device),
    url(r'reward_traffic',api.reward_traffic),
    url(r'cost_traffic',api.cost_traffic),
    url(r'checkrewardHis',api.checkrewardHis),
    url(r'ava',api.getava_data),
]
