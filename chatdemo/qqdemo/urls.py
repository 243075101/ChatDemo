#coding:utf8
"""qqdemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from chatQQ import views
from  django.views.static import serve  #处理媒体文件的API
from django.conf import settings
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.index,name='index'),
    url(r'^reg/$',views.reg,name='reg'),
    url(r'^login/$',views.login,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^upload/(.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^add_frends$',views.add_friends, name='add_frends'),
    url(r'^sendMsg/$', views.sendMsg,name='sendMsg'), # 发送消息路由
    url(r'^getMsg/$', views.getMsg,name='getMsg'), # 获取消息路由
]
