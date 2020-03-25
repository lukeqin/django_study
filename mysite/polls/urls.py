#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time : 2020/03/24 18:15
# @Email : lukeqinlu@yeah.net
# @Author : Luke
# @File : urls.py
# @notice ：


from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]