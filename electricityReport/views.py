from django.shortcuts import render, redirect, reverse

from django.http import HttpResponse, JsonResponse

# Create your views here.

import os

from .models import *

import xlwt

from xlwt import *

from io import StringIO

# from electricityReport.tasks import requestDayData



def excel_expoet(request):
    """
    导出excel表格
    """
    list_obj = Keywordssummary.objects.all()
    print('走了')
    if (1 > 0):
        ws = xlwt.Workbook(encoding='utf-8')
        w = ws.add_sheet(u"关键词汇总表")
        w.write(0, 0, '权重分')
        w.write(0, 1, '关键词')
        w.write(0, 2, '标记')
        w.write(0, 3, '备注')
        w.write(0, 4, '行业搜索人气')
        w.write(0, 5, '行业转化')
        w.write(0, 6, '搜索访客')
        w.write(0, 7, '搜索成交')
        w.write(0, 8, '搜索转化')
        w.write(0, 9, '阿明转化')
        w.write(0, 10, '竞品转化')
        w.write(0, 11, '点击')
        w.write(0, 12, '点击率')
        w.write(0, 13, '花费')
        w.write(0, 14, 'PPC')
        w.write(0, 15, '笔数(总)')
        w.write(0, 16, '转化')
        w.write(0, 17, '金额')
        w.write(0, 18, 'ROI')
        w.write(0, 19, 'UV价值')
        w.write(0, 20, '客单价')
        w.write(0, 21, '行业转化权重')
        w.write(0, 22, '搜索转化权重')
        w.write(0, 23, '阿明转化权重')
        w.write(0, 24, '竞品转化权重')
        w.write(0, 25, '转化总分')

        excel_row = 1
        for index in range(23):
            for i in range(26):
                w.write(excel_row, i, i)

            excel_row += 1


        excel_file = os.path.exists('report.xls')
        print('走了111111')
        if excel_file:
            os.remove(r'report.xls')

        ws.save('report.xls')

    return render(request, 'index.html', context={'log': '报表开始'})


# 获取天的数据 店铺或产品分类
def getDayData(request):
    pass


# 获取周的数据  店铺或产品 分类
def getWeekData(request):
    pass


def home(request):
     requestDayData()
     return render(request, 'index.html', context={'log': '报表开始'})




