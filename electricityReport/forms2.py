#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django import forms

class UploadFileForm2(forms.Form):
    file1 = forms.FileField(label="关键词投放效果：")