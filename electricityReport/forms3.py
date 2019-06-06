#!/usr/bin/env python3
# -*- coding: utf-8 -*-



from django import forms

class UploadFileForm3(forms.Form):
    file1 = forms.FileField(label="解密数据：")

