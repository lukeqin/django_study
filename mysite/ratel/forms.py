#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time : 2020/04/06 09:46
# @Email : lukeqinlu@yeah.net
# @Author : Luke
# @File : forms.py
# @notice ：


from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()