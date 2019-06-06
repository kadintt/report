#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(label="关键词汇总：")


