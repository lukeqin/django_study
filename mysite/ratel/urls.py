#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time : 2020/04/05 21:27
# @Email : lukeqinlu@yeah.net
# @Author : Luke
# @File : urls.py
# @notice ：


from django.urls import path, re_path

from . import views


app_name = 'ratel'
urlpatterns = [
    path('', views.index, name='index'),
    path('datetime/', views.current_datetime, name='current_datetime'),
    path('vnot/', views.view_notfound, name='view_notfound'),
    path('polls/', views.detail, name='detail'),
    path('403/', views.permission_denied_view, name='permission_denied_view'),
]