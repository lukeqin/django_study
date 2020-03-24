#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time : 2020/03/24 18:15
# @Email : lukeqinlu@yeah.net
# @Author : Luke
# @File : urls.py
# @notice ：


from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]