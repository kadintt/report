import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "report.settings")

django.setup()

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from electricityReport import models
from electricityReport.models import DownloadOperationhistory, CompetingDrainage, TrafficSources, Mainproduct, Storagefilelocal, SearchRanklist, KeywordsPutonEffect, Keywordssummary,  Recommendedkeywords, Recommendwordssummary, Mingdatalist, Competitiveproducts, Tmpkeywordssummary
from electricityReport.forms import UploadFileForm
from electricityReport.forms2 import UploadFileForm2
from electricityReport.forms3 import UploadFileForm3
from electricityReport.forms4 import UploadFileForm4
from electricityReport.forms5 import UploadFileForm5

import xlwt
import xlsxwriter
import csv
from xlrd import xldate_as_tuple
import xlrd
from datetime import datetime, timedelta
import time
import json
import requests
from electricityReport.NewDev import PrpCrypt
from django.db.models import Sum

import openpyxl


IndustryTR = 1
SearchPeopleTR = 2
SearchCountTR = 1
CompetingGoodsTR = 0.5
SelfSearchLower = 0.01


RECOMMEND_ONE_PAGE_OF_DATA = 20
SUMMARY_ONE_PAGE_OF_DATA = 30


MCategory = "collagen"
CCategory = "collagen"


from decimal import *
from binascii import b2a_hex
import chardet
import sys
from Crypto.Cipher import AES


from django.template import Template,Context



import execjs
import js2py
import string
from xlwt import *


# from electricityReport.tasks import requestDayData



@csrf_exempt
def ccategory(request):

    global CCategory

    CCategory = request.POST.get('type')

    print(CCategory)

    return HttpResponse('ok')

@csrf_exempt
def mcategory(request):


    global MCategory

    MCategory = request.POST.get('type')

    print(MCategory)

    return HttpResponse('ok')






def getresponse(msg):
    response = HttpResponse(json.dumps(msg), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

@csrf_exempt
def search_tm_data(request):

    list1 =request.body.decode('utf-8')

    tmplist = json.loads(list1)

    list = str.lower(tmplist['data'])

    pc = PrpCrypt()  # 初始化密钥

    tmpdicts = pc.decrypt(list)  # 解密

    li = json.loads(tmpdicts)
    print(li)
    print(len(li['data']))
    print(li['data'])

    msg = {}
    msg['status'] = 0
    msg['list'] = li

    return getresponse(msg)


# 来源接口
def search_tm_Source(request):

    list1 =request.body.decode('utf-8')
    totalData = json.loads(list1)
    module = totalData['module']
    startTime = totalData['startTime']
    endTime = totalData['endTime']
    dateType = totalData['dateType']
    goodId = totalData['goodID']

    # 解密数据
    data = str.lower(totalData['data'])
    pc = PrpCrypt()  # 初始化密钥
    td = pc.decrypt(data)  # 解密
    lt = json.loads(td)
    li = lt['data']['data']

    maps = []
    for item in li:
        newObj = models.TrafficSources(
            module=module, \
            startTime=startTime, \
            endTime=endTime, \
            dateType=dateType, \
            goodId=goodId, \
            uv=item.get('uv', {}).get('value', '0'), \
            cltitmpaybyrcnt=item.get('cltItmPayByrCnt', {}).get('value', '0'), \
            paybyrcnt=item.get('payByrCnt', {}).get('value', '0'), \
            payrate=item.get('payRate', {}).get('value', '0'), \
            cartbyrcnt=item.get('cartByrCnt', {}).get('value', '0'), \
            pv=item.get('pv', {}).get('value', '0'), \
            ratio=item.get('pv', {}).get('ratio', '0'), \
            jpselfuv=item.get('jpSelfUv', {}).get('value', '0'), \
            pagelevel=item.get('pageLevel', {}).get('value', '0'), \
            cltcnt=item.get('cltCnt', {}).get('value', '0'), \
            pageid=item.get('pageId', {}).get('value', '0'), \
            pagename=item.get('pageName', {}).get('value', '0'), \
            itemid=item.get('itemId', {}).get('value', '0'), \
            directpaybyrcnt=item.get('directPayByrCnt', {}).get('value', '0'), \
            payitmcnt=item.get('payItmCnt', {}).get('value', '0'), \
            jpuv=item.get('jpUv', {}).get('value', '0'), \
            fanspaybyrcnt=item.get('fansPayByrCnt', {}).get('value', '0'), \
            orditmpaybyrcnt=item.get('ordItmPayByrCnt', {}).get('value', '0'), \
            ppageid=item.get('pPageId', {}).get('value', '0'), \
            crtrate=item.get('crtRate', {}).get('value', '0'), \
            crtbyrcnt=item.get('crtByrCnt', {}).get('value', '0'), \
            )



    #存储数据
    if len(maps) > 0:
        try:
            models.TrafficSources.objects.bulk_create(maps)
        except Exception as err:
            print(err)


    #存储记录
    count = len(maps)
    now = int(time.time())
    timeArray = time.localtime(now)
    otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)

    try:
        DownloadOperationhistory.objects.create(
            operationDate=otherStyleTime, \
            operationMouleName=module, \
            downLoadCount=count, \
            searchid=goodId, \
            dateType=dateType,
        )
    except Exception as err:
        print(err)

    msg = 'OK'

    return getresponse(msg)

# 竞品接口
@csrf_exempt
def search_tm_Competition(request):

    productName = Mainproduct.objects.all().values('productname')

    productList = []
    for item in productName:
        print(item)
        productList.append(item['productname'])

    print(productList)
    msg = {}

    msg['result'] = 0
    #
    msg['data'] = productList

    return JsonResponse(msg)


import datetime
@csrf_exempt
def requeryItemDetail(request):
    list1 =request.body.decode('utf-8')
    print(type(list1))
    totalData = json.loads(list1)
    print(totalData)
    msg = {}
    mainP = totalData['searchid']
    keywords = totalData['keywords']
    startTime = ""
    endTime = ""

    if len(totalData['startTime']) > 0 and len(totalData['endTime']) > 0:
        print(startTime, endTime)
        startTime = totalData['startTime']
        endTime = totalData['endTime']
    else:
        d = datetime.now()
        e = d + timedelta(days=-1)
        startTime = e.strftime('%Y-%m-%d')
        endTime = startTime


    page = int(totalData['pageNo'])
    pageSize = 15

    if "pageSize" in totalData.keys():
        pageSize = int(totalData['pageSize']) if int(totalData['pageSize']) > 0 else 15

    if len(mainP) > 0:
        print(mainP)
    else:
        msg['status'] = 'failure'
        msg['data'] = []
        msg['msg'] = '产品不能为空'
        return JsonResponse(msg)

    startPos = (page - 1) * pageSize

    endPos = startPos + pageSize

    keyObjects = Keywordssummary.objects.filter(searchid=mainP, keywords=keywords,datetime__gte=startTime, datetime__lte=endTime).values().order_by('datetime')

    datestart = datetime.datetime.strptime(startTime, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(endTime, '%Y-%m-%d')

    list = []
    while dateend > datestart:
        dateend -= datetime.timedelta(days=1)
        list.append({"datetime": dateend.strftime('%Y-%m-%d')})
        print(dateend.strftime('%Y-%m-%d'))

    list.insert(0, {"datetime": endTime})

    detailDicr = []
    for keyTime in list:
        ishave = 0
        for keyObject in keyObjects:
            if keyTime['datetime'] == keyObject['datetime']:
                detailDicr.append(keyObject)
                ishave = 1
                break

        if ishave == 0:
            keyList = {}
            keyList['datetime'] = keyTime['datetime']
            keyList['keywords'] = keywords
            keyList['industrysearchpopularity'] = "0"
            keyList['industrytransformation'] = "0.0%"
            keyList['visitorstosearch'] = "0"
            keyList['searchclinchdeal'] = "0"
            keyList['searchconversion'] = "0.0%"
            keyList['mingconversion'] = "0.0%"
            keyList['competingconversion'] = "0.0%"
            keyList['click'] = "0"
            keyList['click_rate'] = "0.0%"
            keyList['spending'] = "0"
            keyList['ppc'] = "0"
            keyList['totalcount'] = "0"
            keyList['conversion'] = "0.0%"
            keyList['amount'] = "0"
            keyList['roi'] = "0"
            keyList['uv'] = "0"
            keyList['guestunitprice'] = "0"
            detailDicr.append(keyList)


    step = 30
    if len(detailDicr) > 0:
        blist = [detailDicr[i:i + step] for i in range(0, len(detailDicr), step)]

    totalCount = len(detailDicr)
    # print(startPos, endPos)
    # allPage = 1
    # totalCount = Keywordssummary.objects.filter(datetime__gte=startTime, datetime__lte=endTime, searchid=mainP).count()
    # allPage = totalCount / pageSize
    # remainPost = totalCount % pageSize
    # if remainPost > 0:
    #     allPage += 1

    data = []
    for keyObject in keyObjects:
        data.append(keyObject)

    print(data)
    print(type(data))
    dict = {}
    dict['total'] = totalCount
    dict['pageNoArray'] = len(blist)
    dict['data'] = blist
    dict['pageSize'] = step
    dict['pageNo'] = page
    print(dict)
    msg['status'] = 'success'
    msg['msg'] = '查询成功'
    msg['data'] = dict

    return JsonResponse(msg)





@csrf_exempt
def requeryItemsGraph(request):
    list1 =request.body.decode('utf-8')
    print(type(list1))
    totalData = json.loads(list1)
    print(totalData)
    msg = {}
    keyWords = totalData['keywords']
    item = totalData['graphItem']

    d = datetime.now()

    s = d + timedelta(days=-31)
    e = d + timedelta(days=-1)

    # start_date = datetime.datetime.strptime(current[0], "%Y-%m-%d)
    # currentdate = start_date.strftime('%Y-%m-%d')

    startTime = s.strftime('%Y-%m-%d')
    endTime = e.strftime('%Y-%m-%d')

    dateTimeList = []
    valuesList = []
    tmpList = []
    for i in range(1, 32):
        tmpDateDict = {}
        tmp = d - timedelta(days=(32 - i))
        tmpDate = tmp.strftime('%Y-%m-%d')

        tmpDateDict['datetime'] = tmpDate
        tmpDateDict[item] = "0"
        tmpList.append(tmpDateDict)


    print(startTime, endTime)

    try:
        keyObjects = Keywordssummary.objects.filter(keywords=keyWords, datetime__gte=startTime, datetime__lte=endTime).values('datetime', item).order_by('datetime')
    except Exception as err:
        print(err)
        msg['status'] = 'failure'
        msg['data'] = []
        msg['msg'] = err
        return JsonResponse(msg)

    print(list(keyObjects))

    for tmp in tmpList:
        for keyObject in keyObjects:
            if keyObject['datetime'] == tmp['datetime']:
                tmp[item] = keyObject[item]
        dateTimeList.append(tmp['datetime'])
        valuesList.append(tmp[item])

    print(tmp, \
          dateTimeList, \
          valuesList)
    dict = {}

    dict['total'] = len(dateTimeList)
    dict['pageNoArray'] = 1
    dict['data'] = {"timeList":dateTimeList, "values":valuesList}
    dict['pageSize'] = SUMMARY_ONE_PAGE_OF_DATA
    dict['pageNo'] = 1
    # print(dict)
    msg['status'] = 'success'
    msg['msg'] = '查询成功'
    msg['data'] = dict

    return JsonResponse(msg)






@csrf_exempt
def requeryKeyWordData(request):
    list1 =request.body.decode('utf-8')
    print(type(list1))
    totalData = json.loads(list1)
    print(totalData)
    msg = {}
    mainP = totalData['searchid']
    startTime = ""
    endTime = ""

    if "startTime" in totalData.keys() and "endTime" in totalData.keys():
        print(startTime, endTime)
        startTime = totalData['startTime']
        endTime = totalData['endTime']
    else:
        d = datetime.now()
        e = d + timedelta(days=-1)
        startTime = e.strftime('%Y-%m-%d')
        endTime = startTime


    page = int(totalData['pageNo'])
    pageSize = 20

    if "pageSize" in totalData.keys():
        pageSize = int(totalData['pageSize']) if int(totalData['pageSize']) > 0 else 20

    if len(mainP) > 0:
        print(mainP)
    else:
        msg['status'] = 'failure'
        msg['data'] = []
        msg['msg'] = '产品不能为空'
        return JsonResponse(msg)



    startPos = (page - 1) * pageSize

    endPos = startPos + pageSize

    keyObjects = Keywordssummary.objects.filter(searchid=mainP, datetime__gte=startTime, datetime__lte=endTime).values()[startPos:endPos]

    totalCount = 0
    print(startPos, endPos)
    allPage = 1
    totalCount = Keywordssummary.objects.filter(datetime__gte=startTime, datetime__lte=endTime, searchid=mainP).count()
    allPage = totalCount / pageSize
    remainPost = totalCount % pageSize
    if remainPost > 0:
        allPage += 1

    data = []
    for keyObject in keyObjects:
        data.append(keyObject)

    print(data)
    print(type(data))
    dict = {}
    dict['total'] = totalCount
    dict['pageNoArray'] = allPage
    dict['data'] = data
    dict['pageSize'] = pageSize
    dict['pageNo'] = page
    print(dict)
    msg['status'] = 'success'
    msg['msg'] = '查询成功'
    msg['data'] = dict

    return JsonResponse(msg)

@csrf_exempt
# def IntegrationData(request):
def IntegrationData(endTime):

    IntegrationList = []

    print(endTime)

    productName = Mainproduct.objects.all().values('productname', 'searchid','category')

    for item in productName:
        list = changeKeyWordsData(item, endTime)
        IntegrationList += list


    print(['*']*10)
    print('数据共',len(IntegrationList))
    try:
        models.Keywordssummary.objects.bulk_create(IntegrationList)
    except Exception as err:
            print(err)

    return HttpResponse('OK')


def changeKeyWordsData(dict, endTime):

    list = []

    print(dict)
    # 查询 热搜排行数据 找到产品对应的关键词 数据 然后通过关键词 查找 直通车关键词表  及  流量来源表  获取对应日期的关键词汇总所需数据



    try:
        keyWordObjects = SearchRanklist.objects.filter(searchid=dict['searchid'], datetype='1', endtime=endTime).values('seipvuvhits', 'payrate', 'endtime', 'searchword')
    except Exception as err:
        print(err)
    print(keyWordObjects)


    for kObject in keyWordObjects:
        # 权重分
        WeightPoints = 0.0
        # 关键词
        Keywords = 0.0
        # 行业搜索人气
        IndustrySearchPopularity = 0
        # 行业转化
        IndustryTransformation = 0.0
        # 搜索访客
        VisitorsToSearch = 0
        # 搜索成交
        SearchClinchDeal = 0
        # 搜索转化
        SearchConversion = 0.0
        # 阿明转化
        MingConversion = 0.0
        # 竞品转化
        CompetingConversion = 0.0
        # 展现量
        ShowCount = 0
        # 点击
        Click = 0
        # 点击率
        Click_Rate = 0.0
        # 花费
        Spending = 0
        # PPC
        PPC = 0.0
        # 笔数
        TotalCount = 0
        # 转化
        Conversion = 0.0
        # 金额
        Amount = 0
        # ROI
        ROI = 0.0
        # UV价值
        UV = 0.0
        # 客单价
        GuestUnitPrice = 0.0
        # 行业转化权重
        IndustryConversionWeigh = 0.0
        # 搜索转化权重
        SearchConversionWeight = 0.0
        # 阿明转化权重
        MingConversionWeight = 0.0
        # 竞品转化权重
        CompetingConversionWeight = 0.0
        # 转化总分
        ConversionTotalScore = 0.0
        # 主商品
        MainP = ''
        # 搜索id
        searchId = ''


        print('*******%s********' % (kObject['searchword']))

        try:
            sourceObjet = TrafficSources.objects.filter(datetype='1', pagename=kObject['searchword'], endtime=kObject['endtime']).values('uv', 'paybyrcnt')
        except Exception as err:
            print(err)

        # print('s---------%s' % sourceObjet)

        try:
            keyTrainObject = KeywordsPutonEffect.objects.filter(keywords=kObject['searchword'], date=kObject['endtime']).values('clickquantity', 'cost', 'clickrate', 'totalclinchdealcount', 'totalclinchdealmoney', 'roi', 'clickconversion', 'showamount')
        except Exception as err:
            print(err)

        try:
            ming_obj = Mingdatalist.objects.filter(date=kObject['endtime'], \
                                                   keyword=kObject['searchword']).values()
        except Exception as err:
            print(err)
        try:
            AMZH = Competitiveproducts.objects.filter(date=kObject['endtime'], \
                                                      keyword=kObject['searchword'], \
                                                      category=dict['category'], \
                                                      goodstype__contains='本店商品').values('visiorsnum', 'paycount')
        except Exception as err:
            print(err)

        try:
            JPZH = Competitiveproducts.objects.filter(date=kObject['endtime'], \
                                                      keyword=kObject['searchword'], category=dict['category'], \
                                                      goodstype__contains='竞品').values('visiorsnum', 'paycount')
        except Exception as err:
            print(err)

        # 搜索人数
        MSearchNum = 0
        # 阿明点击人数
        MclickNum = 0
        # 阿明点击率
        # 阿明支付转化率
        Mpaytate = 0.0
        # 阿明支付人数
        MpayNum = 0
        # 本店 访客人数 支付人数
        Amvisiorsnum = 0
        Ampaycount = 0
        # 竞品访客人数 支付人数
        Jpvisiorsnum = 0
        Jppaycount = 0

        AM = 0.0
        JP = 0.0

        for m in ming_obj:
            m1 = int(float(m['searchnum']))
            m2 = int(float(m['clicknum']))
            m3 = int(float(m['paynum']))
            MSearchNum += m1
            MclickNum += m2
            MpayNum += m3

        for am in AMZH:
            Amvisiorsnum += int(float(am['visiorsnum']))
            Ampaycount += int(float(am['paycount']))

        for jp in JPZH:
            Jpvisiorsnum += int(float(jp['visiorsnum']))
            Jppaycount += int(float(jp['paycount']))

        if len(AMZH) > 0:
            MingConversion = (Ampaycount / Amvisiorsnum) / len(AMZH)

        if len(JPZH) > 0:
            CompetingConversion = (Jppaycount / Jpvisiorsnum) / len(JPZH)

        MainP = dict['productname']
        searchId = dict['searchid']
        if len(sourceObjet) > 0:
            for so in sourceObjet:
                VisitorsToSearch += int(so['uv'])
                SearchClinchDeal += int(so['paybyrcnt'])

        SearchConversion = 0.0 if VisitorsToSearch <= 0 else (SearchClinchDeal * 1.0) / VisitorsToSearch
        IndustrySearchPopularity = int(kObject['seipvuvhits'])

        if len(keyTrainObject) > 0:
            for ko in keyTrainObject:
                # ko = list(kto)
                ShowCount += float('%.4f' %  float('0.0' if len(ko['showamount']) <= 0 else ko['showamount']))
                Click += float('%.4f' %  float('0.0' if len(ko['clickquantity']) <= 0 else ko['clickquantity']))
                Spending += float('%.4f' % float('0.0' if len(ko['cost']) <= 0 else ko['cost']))
                TotalCount += float('%.4f' %  float('0.0' if len(ko['totalclinchdealcount']) <= 0 else ko['totalclinchdealcount']))
                Amount += float('%.4f' %  float('0.0' if len(ko['totalclinchdealmoney']) <= 0 else ko['totalclinchdealmoney']))

        Mpaytate = (MpayNum/IndustrySearchPopularity) if MSearchNum <= 0.0 else  MpayNum/MSearchNum
        Click_Rate = Click if ShowCount <= 0.0 else Click/ShowCount
        Conversion = TotalCount if Click <= 0.0 else TotalCount/Click
        ROI = Amount if Spending <= 0.0 else Amount/Spending
        PPC = Click if Click <= 0.0 else Spending/Click
        GuestUnitPrice = TotalCount if TotalCount <= 0.0 else Amount/TotalCount
        UV = GuestUnitPrice * Conversion
        IndustryConversionWeigh = IndustryTransformation * IndustryTR
        SearchConversionWeight = SearchConversion * SearchPeopleTR
        MingConversionWeight = MingConversion * SearchCountTR
        CompetingConversionWeight = CompetingConversion * CompetingGoodsTR
        ConversionTotalScore = (IndustryConversionWeigh + SearchConversionWeight + MingConversionWeight + CompetingConversionWeight)
        WeightPoints = 0.0 if SearchConversion < 0.01 else (ConversionTotalScore * IndustrySearchPopularity)

        newObject = models.Keywordssummary(
            datetime=kObject['endtime'], \
            weightpoints=('%.2f' %  (WeightPoints)), \
            keywords=kObject['searchword'],\
            industrysearchpopularity=str(IndustrySearchPopularity), \
            industrytransformation=('%.2f' %  (Mpaytate *100))+"%", \
            visitorstosearch=str(VisitorsToSearch), \
            searchclinchdeal=str(SearchClinchDeal), \
            searchconversion=('%.2f' % (SearchConversion *100))+"%", \
            mingconversion=('%.2f' %  (MingConversion *100))+"%", \
            competingconversion=('%.2f' % (CompetingConversion *100))+"%", \
            click=str(Click), \
            click_rate=('%.2f' % (Click_Rate *100))+"%", \
            spending=str(Spending),
            ppc=('%.2f' % (PPC/100)), \
            totalcount=str(TotalCount), \
            conversion=('%.2f' % (Conversion *100))+"%", \
            amount=str(Amount), \
            roi=('%.2f' % (ROI)), \
            uv=str(round(UV, 2)), \
            guestunitprice=('%.2f' % GuestUnitPrice), \
            industryconversionweight=('%.2f' % (IndustryConversionWeigh *100))+"%", \
            searchconversionweight=('%.2f' % (SearchConversionWeight *100))+"%", \
            mingconversionweight=('%.2f' % (MingConversionWeight *100))+"%", \
            competingconversionweight=('%.2f' % (CompetingConversionWeight *100))+"%", \
            conversiontotalscore=('%.2f' % (ConversionTotalScore *100))+"%", \
            msearchnum=str(MSearchNum), \
            mclicknum=str(MclickNum), \
            mpaytate=('%.2f' %  (Mpaytate *100))+"%", \
            mpaynum=str(MpayNum), \
            amvisiorsnum=str(Amvisiorsnum), \
            ampaycount=str(Ampaycount), \
            jppaycount=str(Jppaycount), \
            jpvisiorsnum=str(Jpvisiorsnum), \
            productname=MainP, \
            searchid=searchId, \
            showcount=int(ShowCount),
        )
        list.append(newObject)
    return list



@csrf_exempt
def requeryMainProduct(request):

    print('请求主商品列表')
    result = 1
    errMsg = ''
    try:
        productName = Mainproduct.objects.all().values('productname', 'searchid')
        result = 0
        print('获取成功')
    except Exception as err:
        print('获取失败 %s' % err)
        errMsg = err

    msg = {}
    print(list(productName))
    if result == 0:
        print('返回成功数据')
        productList = list(productName)

        data = {}
        data['total'] = len(productList)
        data['pageNoArray'] = 1
        data['data'] = productList
        data['pageSize'] = 10
        data['pageNo'] = 1
        msg['status'] = 'success'
        msg['msg'] = '查询成功'
        msg['data'] = data
    else:
        print('返回失败原因')
        msg['status'] = 'failure'
        msg['data'] = []
        msg['msg'] = errMsg

    return JsonResponse(msg)





# 热搜排行
@csrf_exempt
def search_tm_hotRank(request):

    list1 =request.body.decode('utf-8')

    print(list1)
    print(request.body)

    tmplist = json.loads(list1)
    list = str.lower(tmplist['data'])
    module = tmplist['module']
    startTime = tmplist['startTime']
    endTime = tmplist['endTime']
    searchID = tmplist['searchID']
    dateType = tmplist['dateType']


    print(list)
    pc = PrpCrypt()  # 初始化密钥
    tmpdicts = pc.decrypt(list)  # 解密
    li = json.loads(tmpdicts)
    print(li)

    print(type(li))

    dicts = li["hotList"]

    keyList = ["clickHits", "clickRate", "hotSearchRank", "orderNum", "p4pRefPrice", "payRate", "seIpvUvHits", "searchWord", "soarRank", "tmClickRate"]



    dataList = []
    for items in dicts:
        noneList = keyList - items.keys()

        for key in noneList:
            items[key] = 0

        print(items)
        newObj = models.SearchRanklist(
                                       module=module,\
                                       starttime=startTime,\
                                       endtime=endTime, \
                                       searchid=searchID, \
                                       clickhits=items["clickHits"], \
                                       clickrate=items["clickRate"], \
                                       hotsearchrank=items["hotSearchRank"], \
                                       ordernum=items["orderNum"], \
                                       p4prefprice=items["p4pRefPrice"], \
                                       payrate=str(int(float('%.4f' % float(items["payRate"])) * 100000)), \
                                       seipvuvhits=items["seIpvUvHits"], \
                                       searchword=items["searchWord"], \
                                       soarrank=items["soarRank"], \
                                       tmclickrate=items["tmClickRate"], \
                                       datetype=dateType,
                                       )
        dataList.append(newObj)


    if len(dataList)>0:
        try:
            models.SearchRanklist.objects.bulk_create(dataList)
        except Exception as err:
            print(err)

    count = len(dataList)
    now = int(time.time())
    timeArray = time.localtime(now)
    otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)

    try:
        DownloadOperationhistory.objects.create(
            operationDate=otherStyleTime, \
            operationMouleName=module, \
            downLoadCount=count, \
            searchid=searchID, \
            dateType=dateType
        )
    except Exception as err:
        print(err)

    print("存储成功,%s" % len(dataList))

    return HttpResponse('OK')




@csrf_exempt
def keyWordsResult(request):

    url = 'http://47.97.51.185:9090'

    data = {"id":'collagen',"action_id" : 2,"process_id" : 1, "reward_type": 2,"num_timesteps" : 1000000 ,"assert_file" : "collagen.xlsx"}

    headers = {
        "Content-Type": "application/json; charset=UTF-8",
    }

    ret = requests.post(url, json.dumps(data), headers=headers)

    # requests.post()

    totalData = json.loads(ret.text)

    print(totalData)
    recommendList = totalData['retinfo']['key_words_list']

    tmplist = []
    for item in recommendList:
        if "current" not in item:
            tmplist.append(item)

    d = datetime.datetime.now()

    e = d + timedelta(days=-1)
    date = e.strftime('%Y-%m-%d')

    valuestr = tmplist.pop()[1:-1]
    valueList = valuestr.split(", ")
    print(valueList)
    OBJ = []
    for index in range(len(tmplist)):
        str1 = tmplist[index][1:-1]
        print(type(str1))
        wordsList = str1.split(", ")
        print(wordsList)
        for i in range(len(wordsList)):
            word = wordsList[i][1:-1]
            obj = models.Recommendedkeywords(
                date=date, \
                keyword=word, \
                rankgroup=str(index+1), \
                category=totalData['id'], \
                recommendtype=totalData['reward_type'], \
                rankvalue=valueList[index],
            )
            OBJ.append(obj)

    try:
        Recommendedkeywords.objects.bulk_create(OBJ)
    except Exception as err:
        print(err)


    return render(request, 'catId.html')

@csrf_exempt
def getKey(request):
# def getKey():
    # url = 'http://127.0.0.1:8000/requeryItemsGraph'
    # url = 'http://127.0.0.1:8000/requeryKeyWordData'
    # url = 'http://39.98.88.168:8001/requeryItemsGraph'
    # url = 'http://127.0.0.1:8000/requeryItemDetail'
    # url = 'http://127.0.0.1:8000/keyWordsTotalData'
    # url = 'http://127.0.0.1:8000/searchRecommend'
    url = 'http://39.98.88.168:8001/keyWordsTotalData'


    #
    # keyWordsTotalData
    # data = {
    #     "keywords" : "美白粉",
    #     "graphItem": "industrysearchpopularity"
    # }



    # data = {
    #     "RecommendType":"1",
    #     "datetime":"2019-05-29",
    #     "pageNo":"1",
    #     "searchid":"125060018",
    # }


    data = {
        "searchid" : "125060018",
        "endTime" : "2019-06-05",
        "startTime":"2019-06-01",
        "pageNo":"1",
        "pageSize": "0"
    }

    ret = requests.post(url, json.dumps(data))


    return render(request, 'catId.html')


def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  # 返回bytes

@csrf_exempt
def popKey(request):
    list1 = '38A9FB044007BE663C763C1D7BD71C75F5E2BB25DEF8F12D40CA3604C4C1DAE380F4E3F676EBBAC0928CADBD7AAD054587163504842F31C36A8D9F7F5457B0B6105EF1041780419AB776BF17BB0C011DF412E6CA51799B0FD8175A974FD54785FAB02DC461BE76700778357746A3E69D767CEC062C6A3C25730E6A155FE0EC725CE2D24AB03169B8990DA382833D48AF5B89141FFF12B0AE5DA30B4A9748E8C33B1FCA6CBEE95EDA8AEBE203E5E37E3ED9A0CB3B0F548077BFEF28960430DAD2F93F14A146B676EF11513C3FD8031FCF895E33F4BF5B9D1695CADA65396FCEB6A333DEBAEC5A89880E255DF0C3ABB0AC795AB5A9DA90836038E13B8F3A1ED8A3210025B98E2689920E0216FEF1262F68570C3DA83E1B733DBF11DD4C02971BC78D8C0DB40068624E76922226E45A16C6C5527081F2254C20C5383A0AA7DAC8EB3C55EFEC47AFCFA78507815FB566C37D020DA38A9A1CFA0267EC930465BBB233587265C47C4F3CB9142B1205B12C9A9C74F8696DA2B558FD3FAAB60CA3AE1270EB5735CC323CB56020E38E9FC9CBA79A9D27C6615833311ED49C9669A8F1BE993904A65B3D8A37B4277789E73B2632B8745A6B91C49A0DF7C9E9AB981E23E375CFE98E1D3C20ED2CD5026B512F380EF2737285607FE82CC4DBBA67B55D6B0580770303C6B1F40678094DABE3D7780BB2305EF2DD0F965B750A8681B0F15033BC0AEE5693E7B4048176D5E045B3FBA4B0846A5CB7BE02273B0E9170B8ABD708AA4850813D1BA6B23EE3FB4D0C2796D3BBF215E137D49B58F70D225966E8F173EC1CB1153660D9C1AA55E9B243A1C93DA3DD423BD6E40904361F73AA5D41746110EB05CC375905A8D83725CB97B5F26D469D7859902D4AC5C266E72A58DF73D1FE402199A29363A6AA9926352D3CCD69A26C2AB4F1E5A0FEFB560312A4A6CE211C65EFAEA87152FE0C6DAD633953EADE12C5DA160DCC15427D64B27E7A4FAD787490B90C85C4EF7F01D744DEDD4B71EA76D4122B80C4024B76EA089C2A01B3C8301771364F0D397319808A50313656E21AD0A6252B3C0B3DD159100F0EC2569916B773C8F9760CF7D37293384C39DBF4B8BB9C20C71BAB5E9197D9976F5B162836AC67D40C761CA947FB7655AF704B58EC9339BEA9B315EF6F58E7341711FB9EF1C366B5B0B22F2691EDE1071539D35B38D72B02C889A2D1F9C2DE9FB72602B54E2630946C82820E1B49821D0507D3BE1B3973D6FEAE55B1E52956E609F313B9A3A370EB39983764435B6D07B3C211DB2F68566D2471947EF95CA38AF4018AD726E7ED7124920E33833999A112C0D6438BA530C1BABE22245DC32BC771450CE26CD12A223456A8E3C236D5284C3570D454A23002AAF452DF490DD68B6AAEA538A7D9F6341136DDD71D7131E6644225EBED518E76EAFA8FFCCC56CC8E9890EF61FC6AD1B7F2039B8380E5D679DC68D0C3C586011195FD4538A1CFC6E5B88F56515494C2FACF4E8E141F8D89749BEE394596BF3F0A53CFF96A15BD55FBE1A3C178226E59CAC4A06A3B146BB4A9D934D77908C76DF6D0404AD6BC70E5F2A8EDE9258EF76344212B1EA9A874E7148CE360AAD8EF534584D1AFC50782F9A802833964C60CBFE10D6B18C71B409CA46EED1082D85BFC3DF68D2E37E35DFC4658BBAE9C0AEF66A176B2B4EEDF38C2F8FE3B03B9F8DF727695547B45756C6FC8A62D8D08022FFC664346C9E5A9DE59459A958A71127EF6FC9A316BC4F6392A99554BD201D0C056A02B69BF3EE506ADE86436C252F914127164D701AAA029FD3D6F33CF20ADA2E8E0D34843CF7FE78F86E3A99A0C227D29B099E353255BDA437F9FA4CC89FD4782B121A15AE9994C3DE2346F398088DFBF6D627530BA2AD7468D5FB8BC0C76E2D1C54CA5807D47D6D84CDF5C05F014E51FB571B0A56151AA763694260AE5198CB19A388FA497241D608F94C049B509C9593936839FE531FFC03DD5D74A50F6E16E0394C3B05A2CC24FF02415D7C506FEF486429B9CDE369C5185A06739A6FE2417E6CEC79965EEF8FEBD6D5DF94BCBE2329CF4C3B9A9B48D20BC519FE38B1B1ADD759E1CFDC9245420182B6C73A6222ED0F56D935B3B05447AF31D687ECFEF9BB16FF420396F43DE773B6885EB41552CE79B6D7B716E93502341FC08EC23A825DFF593F90A7F98070D14BA80EF55BFDBFEEEBC8E744043B64CE08442859B9C6349804958559B7EEB653DA9C2827B85556CAF9C20E41071BF5BAEBCEBD317CDEE92B0AD977DCA6EEA75E1A3815B6A2229746CD78A328B2269992D2645DE325B0EB1EC9325CE8907CEB0C3492F3657ACA7F8055F6F3556C15EDB2EF38C3E9CCBF4A7837F84273D65CEF9926635B292A2DF14DA77CE4815B3DC4C8E7FB6E3F2DD872EBE45AF68B83D65315D3E16F0D198ACBEA5CB839DE4B07169A034FC49FDB3DAACA6AC07DC04EC0F4B9E29B83CEC996344999B34C660A608D777E2C0474A3FC27BAE7B099B0370657F1035BBB533B3390593723B27DAD69808DDE77D751236BF2C807370FB74E9CF0F6D7F03B2767A91CACED9073315768C5539778B542063D199C3CA009BF4431F488A63A33B2E49BAC101039846B3C6B6C83434C273AEA0B8110798989BACB64C51FE1AE826480BEB7A102F8EE4989C77C3D02FB1DDE41132CC27CCC2A75D196F909CE3F473E186524AEF27D674B2D3FCB41BA4BD1B2BA97E53E5A602A4C795B11E0CFFF685B788D4E5A3879BD822CBFB1CAEA11641EF5222240F0206F4D32F3A25A632585336D664CF24076E029ACDF07026D973A624632297A53F4592CC44794B85D24CCDE02635EF93218389398D87AE33A197DBF33C11AB04992CCC256A38CEC107B2A5DD37353B8A2CA73DC12260C18C3CED74F62198324B61F78FF0BA6AD3C3CA7D749A1CB99397574637CDCF5B904703A43745D6C37A166AD48FDBD180AEE3BED2D33272CAF6DE315354DD20001203329FFE72B8814874CF65CF567C35523250D1C6CAC57E2E5ECA6E79ED13629B1A7CE45744DAEA33217BA96732DF63C8C77CE41EBCC603282FF908A13AD79E26127D9E3414CE75B40603D3121691E83306D8798043B9B584E3EEA4C1E0287BD0F8080BE143A2AE0D0ADE913B31B05DE5B06FB92686E86C9BCC1D872132084F0A96C9A4B9C990ADA4FCF994ED29CF2CAAFE601A1CD64B9B5423E816840BB546C3B5B9F5558E65E7AB33CC0D84CA9956D77173BFE4E020EA2B8EA1313B2148CCCD0D806F4AB8F9E508E92BBB2FD1D53C98F194C55B04B7FEE5CC4869590F1AFCB7060FDF8557883E1EB2D1FADB5FE2442FCEB6B9A26A07173C0915E4F75A6A775F77ED688C18A6D34152F3C514770522AB7B2672018246C66762600CFDCE6B84E92D46F6F262E06DCB0427756F6E82EB61DA9F675DF071C2E3D76F9295A0F7D7250BD14494405FA5BCC22E7548F05D0709B8E20E4A89BAC23212897F6840F7B73F8DE24F9BA4911957C615BC3FFD20DBCCECE64F8ADFA5836BFA6F7FBA1B035640055582AC2311FA6DB7F699F72D9BB3BB0FC3C9C9113F669EE676EA14350E221B24FAE1D7656566A38C1B5C8E33446E09720DC4B337BCCA06BA8D8F28A9EB9DDDC637F0C2A4538C722399781BF86D6210ED437EED4A6FE9FED490B2744CA9D01AA5BE0C69058D7B0E14C6BE214DB4AAE10ED2E1B51A2322F2FEF45332C91B92287ABA61870A6C810D81CA40467D7CCCA9BCCBAEAFDE9FDE7500DB262376BEA9FFC7E629A0B80209AC63C9FA371B791EEE5EF112F9B950B05CBFC4573528AE70F9E31BDAC54E3216442676A4D7B2E7F4B9E33AB099BBECFBDE3F20FF10CF179D383B08EEA1A60493B503E6463D70D5AFAE51BAAEDD00C76A5E1B848E9092AB3C6BD6B9F1F04E6E66DE0DEFF833FA0D35527B5AACE711EEFF757DA96155999DB8B83F8D1333E81485A1E64A2DB8DFAB7ABA0D9647DE2F3A9A67A4ACC36AB7BDF7D08BAD9292B155D67FB8A105CB0D1023BA9DAD32A695075AE2EBCD4AF425A24410AA247A52E68C4BD6A3FDABB44A891EEEFCEEC4D74CA39513C4F021DFABE8C5F60A3D8321076C2A2976E088BFE71FA1F17ADBAEF8A0E70E9CC2F4F0FF640FF4D88CB56953A7C73DB021FBE3FA844081361D173AC8B5677E9F8609A31CD4CE23682D6A7F19B568081BFC5FB62676B9CA513964B58F222AA468931FF0426DE0CFD51BE33801E04A9C2B6A4F0B43FA399B366966B13D44BD484B8E20921599E9D21FAA82CCA3E7CBB39AFFA3868B7E11CA92F742048CF0E7E61AEE377B094A607ED3635ED769E8B8D6718AC264F07F8559062A3CFD989F50592B65337A0FB0900B052A1D2D00114FAF259BB59D6BF87B02C35CB04289ECBCE60A3408F5D09ED23042E94C83E019A4EB0C817B3A809BB3E37D6208397E8DED0A7155339BBCE53C09711934D99021A7ED908C6267A4B0E93D40090A0EDF519DF8E3AC18018D4E580FB77EAB5113AC22316C2E0C9AB4DDF3E84D523CA6406BAA50CCAC8AD8D97EF491FADDA826993935C11DAD824F5FD13CC043FEBA4FC9C9EE5FD15F4804508D86887E705CE4C1A3BAE6CB6DFBC3CC2CA33FA9A5F9165CF822EB3DB4226767B6F1B9E2F2AA1FEE427B7656049855191FBD2F2E4A27A566978A1FDADEEDB63B8026EB783E0A1298C19E7023F36E82208374F583B3385E3AC5A7EE527D818863083F6B06FF2FE15FC3817F81265493EB18C5BB24E232B62DB8C8446EB6125C08BB70B5DFF5352BE29BEEB25D9CD273FB57D32D6DE0687B718BA30982143DC9E1361EFE02EC8B1F2343CC279257512051F2CCD6CC2274E7D0046041D59C2F5BF8B6DF193DEEC7A5DB61243262E30C7A31DCE28EE9E63DA18115D1D46391989BC32A09AEC5B68C76193B0B713AE7CDFF7668300D0979311CF0A914A6EFB9BA21477599E87A4019F857F96998FA91E78FA837A5D8AD78DF58AFDC0E247F7E8BBA61B9920DA82E6A804CC3D6FCA66AE7D5957F68AF16CA60C3C4959A5EF20CECB407C1E3568C91196B3C6FBD1C4A4D4D1757278473469864B973812260F9A681476B30E04299099799035CDB7409459012F3BD968C17ADFFE45AB37AA3CCEF929F2643810D512F2921B98FBB4A489E2F5B61E8D21BB4F71FEAFF4A1916396F8DF7AFB2AB4C13239ECD98242F1E1731C27BD4CBDF16779237EC655D157AE6CA7B608AD75BCDD1081350D5EC336661DC4A0626A98C40BC356C31D6DD8C320159025E37D116A33FA0F28F59D8FCD6CAC728734354433EA68C8845142713D10F1EEBACB3BCD4E4560B1051C0C7B95B548C8B87010A1ECB49679C417F487BD244D933B350756397F1BBB2F9B448779DD9C427DDBBEB04472A6EB51881D33C66461C00DF2F18CC51C5D0C4ED209A210DEEA212193E3C319CAD092F11EFBA0CE887B611D5A79F4D5AD4A74006450016E239F3F4144C4B2EF030E0A0BBFC338A6780CF850984C72C9639013135B7E27B8999A690FC2B027AD14DB501BB94CAA6ADDC27B508A91FEDEC94064B8AC12BD50263860AEB80D8CD4177F72150F934C996024C6ADF6D56397011E60F418AD540DEDE4D0793F621479B0A88AAA268D0BF32A0BA3ECE63D52CFC45240F72EBE0B99FF82B40F59AC06A7187029C2AF3CC7345FB09121D5C2026F10E26DED3BED8104B88C2B8F873CF8B3025F019BE624A83514AB6F7DBDD13317CB42F5BA5D1CE923FF53938C7FFA68A7671D47FC9208E906C4D3846326F6853B270BDB7457D7F5BDB7F7B8AA22325133C1C86422A682F72CAD3319616A76A28009B3C1AEA6DDE8048D3938CB4FEA9D8919ED1193D9B136FB201A5C534E24EE75E58F30D82526D1A6ECDB21650B4C55514C70FF7551AE11456141865219DE7471E0ECF69BE6C73171CA84961C8FE08E0B76E3AA249245FC4E973E3F501FC11A9BCA10BB85AC5F14EB9858C41E942C5A616D4EA62135D0AE6A585E3EFF09C37B0A5B966E0321F9B08ACFE37D371D438A556BE2ECE08F0518E58620ABA0370F1511CB770EB00B6289CC2AB288AF521161EC35D0894E061C3DD41E751F6D1AC7AE8A8AB5329EC37677DDC9D8B87AC90EE0FAFA67D0010F01E6595D337381502DAA44EFA517AE37CE1007CA489D40BE4D97809F349AF1CA7DE25457E07A6B8B0456049220AB18162123EC002F70B6CACCB1315C41BF1388D14110BFBEF6AFEF0B5BEF9F263C1B387C75FC8314D9117CE778B3D91E84092A1B84C0E41BE7EC198D48F80F0A717814FA9589AA20FFAF2D78E5794BBBC0B37FD5A65DBFD87C25FE7A9A2D02E9EC4CA80D6D4F585891C7B3EAEC8953714DEFC0D2F405AA1A55D38227D188E8DAFCFB36C30AF08DCE165BEDFCEA61BECA16BBF36E8DF194344D6A79E1C91DA22D2F760D592A790AB7FFF1C7925A9CE37864E75971A2BFB425D1D17E42F4D7B5CAD85A41D37F735501F3CE36DBC590A0C4B5DDE1642326FC661BE4543101778814E31176744928713FC43CE3CD3471DFBF07BE59E9FEE88B7B8DFB34CCB4ACD50C1CE883917AEE98E5C1B4BB7E23B8731B64810B728C1398BF4D4D78F64BACE052FFFE51114547F1EBA06921BED03C75A9D098900E60BCDAAA4E4723B9A7D03732562F0EE429ACF8DEC7ED0EEFC323A9A556ADBEB3916356D79959708E83981AD9BD8CCD4721F8C80541E6043A6D1FAF3A4AACD85B79CA5FF59D1EE28154C90DE1124805886BB7D077C4EC89AF89043573556417DC746DC5C28BD9F4C6CC28FDE53E3B394B71CDE0C3388219BD6EB7A29EB5377D745A1A2B705B63B3A4AD01B3EC0A062610F761C6F884CDD219F8D87F88CBCCBAB303CDAE1BA06E71DE230A88DC86C6C351266D285BB5378191E98948825B0EA8A4782AC558C48F2C8793F32D1AFD8860883BF6E44653E7166E43B9226BE9C12C2BEAF3B8E2D7CFC03264C3E87EA5A206A43F84E86E436C1AAF0F867E32D784E7580CD32A680B5EE005CA838ADDAEC79B29EE1B01BAECFC412552AA9561BFC4628D1B51C8D83B41991C4BD07CEEE4C27A9AD28727741A2378F7799052F4BF6909AFA4E8D043587E59BC8124FB51B8C3361485C78DE6B2667D9E861EBBCC6883EB85672735F2DED5F3C6F39900251C03A2493A50E26D101C19E2BD46745D727AA37EC2DFD21923F0246C5118AD3993851AAEBB0EE503532431309B2FD270BA4757EB1CEF5EF19BDD6EC67209C414435EC3022E11A075D2375BEE89440BA0FDDD3AA7EA289D64B30757D6835234F1565B1F3468CF546A9EAC4A5E834AEA122D33C0BDDFEE5758EC048161FF9CC7D32973145148F87ADF6DE7C3425976D00F0FB5EAE142CFDD99C2E5A6EE74A9410931946E3CB1F98CB4BE294224368DC52696FAA452CC532143647B02ADC6FFCE12825EC0671231D3FD5332FF79209E3924B2E6CF40264FFFD3C45024476E0D9ACAB0F8A1FDFC1B5B7635E2DF87651F8DADD6EA15D0F1DEC44A0730BBAF42A3F6B065B5948D0EC8A75B61C17750A5664A33883BAD45134CAA764FC57FD32EAAF3C8D963299C03215EFC32AC17CBF8ECED05FE45B945A2406A5A05388F96AFC408D14D328E5D8C570511434A00353A06AD4B2B9EAB3FFC8586DB79A7E076600522A4054501B3CB5B7A26AA4EA809DF9E4546B843B9A4F199477675AF0728EF427B92D18F87982F85E06E2FD6D1087CB7B91154A362BC001933F3EFD2B7834F3C604A2D3AA2969E6AAB135CA41353AC8C016150169E32BC9365976F791661A24C72FEBE5CC09474CAAE5902AE147FD155BF8707A9A4AE2A4354AF5F9C9687CEA0CCD6FF7BEE3DE67915080B2313352846C9CFDBBD216ACE3BCB2B173190034B6120276DCE08241CE69D0490117AF88AB37A385ECE8C50BDDA4557726E014BC2D852FB3F4DC1B356B0F4E331840203FE3E7A3B859EFE1F9539CA9BD19A44B0378F77E02017A20388330256679B2ADC6D3D974F1E9E268AF21675332081A26BB551D45F1953F6D4BFE2DE42867AACD537A1E7080228C9D668A41EE2ADDAA66B3CC268B3F529631FD9F58B4787B417A1B45B2AB7D0D8B4DA9DF2D707AC9031589E448BF933928CF7478369EDEECDD913A1CCF08B712075CB882029A29C63757DEFC4A364DF66A83EF7EBA8B875590F6B33CE8EC1136694CE84F746710C49AB4143D80F128431C2538F6E2E69B00D6D6630877B2753E86AEF0DA1FEF6C77BF5B354F2F8DD1931EC3CD8E2AEF3843FB35DDD82451C5BE1690896D1B983D4AD9C66D3B38EC714C5A8537B8AA2DEFBB2EC2846774F0EB985BC9F1A31C9888B8E2E6CFDE11E82E6757F9B2AF2D7078DA2F79398197BEBAFF67D5CAFB77A6D26919F8D64352D6CE8A75C811AE0DBD6A11911E38D52C8A2EF333853565CC4FB7BE2178B9C0C32E7D3CFA4FFF721C613555C041F7667A159EE223BE9D86F028498306FF10CF64AF55F550880BAD2E8BF54904C7297518E6664D05828C23BBED4BDCB9153CD5FE8470149707D0230CA00778B80A867C8EDE3DF1B215811DBD4C3C778C740A22C7E08C934DF7F11422C444A53A7DB3839BB6D48B40006CAC7F25936E00B88E2D229A1897ADE770E01B176C1781BD7D5A8C144C5963EB2304990FEE3580523B63FBC804F32054B490A0FC80723F7ACF1DCA05285877BC4ED8B31DB94EE8974C46DC772B1C98A4B1946D9B20EA30546F3A3B0F42A7A2127C0E3E750932EA1F93E4D93DEF84E432C1B5630EE440D7CE6A1D91132ED34F0B1DAE197345EE5910DBA19D6B09A837FD7BEDC9401AE4999F195DA1EEAEAFEB16A9D9B0CFE6C1032455B38F196D024F371EDA8340A31AF5D749943A8CC2BF07EF283FF88A7983D7D186A1332A110A4C35205ECA38DF9DD80AB5E7CB1B4F281E50D2B02FC40F26C6DFCDABFC3EDBD44A8C6DD7664C6262DB34F97818EE1E5AF3BB940644342ED1BA6BD1C59B57D9C7FAEE1BD5D00C481FFF53848E37068A05E00DF681A659EFB68C146F58675F05FC381F4F90C4AA797E3DAB0B95937E55B0387040C9567A4093BEF9771A26918E1D97B7A3975BFB88A81F7B05222C3A775F536549B3137D33870A15825CFA3CCE3B73A8A5EF0095F93049817979FEBC86C1BE7D76A3758AC1E12A82A78C356793015104F66EAED072B839CEDEAA68EEB64644496924D594D0EE0A7B3A0CA304FF20761BA41AC994D3CCD76567BE6D53C1DB1E3E0E35870B74F1FFBBEBC788BD8F7E4FC6E4E561CF95EB6EFAEA062556C7B74380DE810B0AEE6A40119F9D298D36EB0D731756BB4BF8B8D2BBA1FE4A8E8FFEFF10619D4BF945944CF72641147EE8D444EB6BBC9F2731D808294D3AD0EB07E282F82C6EDCC4D9D3FBF93803160CD99F26A90D605B2B1B82F5E513047BD4E4393F63E4318DFC3F713ED20C293A0B14208FD58AF751931D06C8E25378FC00002E8C30BC50EA1F56CA3A8AD4C5ED234D517BBDD8B4C14950A80728E51B11C88E1B70D0C544702E72E1C44D1A09B9E98CFDA48F93A6395BE286308490CD0CE9BF99481A9A63C9FA05B01E6E0B409C334F655C1A8BE7491507B6A6AC3AFCB256B10A5F62B94197189F4CD8670DE021AAF316EB8A30F021A374BBE301ED46B20473E4672747DF6767955F5806148CC3925E277C1BCDF82603F2A285C1122CEFF5551D14B1D684D03AEDA35A84868D1A3BF34624FBD075AAF0127471A7C04018369531BE6D77BB2C49727A99562885058064506EE8314E854B62EBCC4F0A4071C2C170F21B9BAF23AB1A57F267A794346F8D5B9CEE2AF1EA6A2C065E42CADFF6D194DA8BA58AC6C0968AE15607502215DA50A143A55C9749F0A472FC0D6F793CBEBD13164C8BDB2951772B3053337A9AB98849B9FE1C70FB63E998B45016A39A22CAD84114D01EB0AAC6FA7A6EACD2683B9601C345A5EA16B9F55DC00B7F4B7784FADEBEB19D22C6265E1F68C72017FF16BDB443BCC183E9BDD7E4DA743FB91C7310F03E63461D2EB4B37939E24FA503C0E24A4AD6898BE5D4C9403AF0E15BB0985E68A101205AFE4847771853D0E08019EF4929C23A734AB475C9EFE91D4EA3E619902EC0CC2D94AE4D7A933B2F1636C4FE3AA038644226EC6C4ED704734DBBC7DE3C34CA48BF108E461E9AC77C8C226EE403F2369616826667F9F10FB2946ED19DC9B7A0589057D407B464C028705C56EC5EB0F42C315CA61ED5762ED2F010DC4FBE64FEF5269BD496F49C21AFBC8BF286CB52A7BCABC54C50A120C0957F81FC0AED5B9CA0572BFEC81C65809B64CB2679475A957CDA1E4AF2DC528AFE01E8CA6D9103364973AF5D436C60C63FDFEC49B4520842CCC3A20FFE627D00E62D16BFCC1E84E187F039216552C3D5073B578A2DE172B69D891722A41F4DBEE5516536055D72A1E82651ED683BF15EF8AA97768CAE84BCD759C2901C4780185E53F6E0C60DAB489641EE3DE93D91A90654243E79B220679084E9E387CF47676D6556A6A7950B90278C878A0381A302BB72DE8297B1F784EEF11A93F414B3C322AFE7CD653BF17FA243ED430C284F9B04B71C7C421AA7E0F9C8881CB83ED3EF3467F1C95A61B7A5D5437A55D6A0E87845D4461DB1E5AD1C0494E380721B2A57D495FD8D88CBCBCB108A595836CCF305FD8C1A2321C0A8D3075B27FAB2F052658FF4CA53FE1022A23E201F281253387263DF31AE35DDF5C458D60F548F0E777CC010E7C4496B9EEC2120DF8D162408C3C9EF3BD9C17943863CE429181E2B7BE7F98D0A23BCAAAB31E8E8D98A1B4187F9C7AA37644A3FDA7AFA0268823A088F8FA4D45C28FF93B9FDE0696E485372D54A53316D03FE5FF328062F5DE32B88AFB7D1F2F55DF9FF0868157346652C76D692CA6EEC8FE1200C8208DE3E191EEC1D38A9439663DEE44F38796AAE469477C462F0D6569BD91AB6E6E90E73ECA3FE7222C266849175F3347834CFA4DED7153C649C7090AAB24B9C92AB3DAD1649896C2EB294937F984D034F8CB86A4FC3A245F9DA1C985D95FC43076C930DB75D6BBCF257DFF5CB8F5774D70DE7A4677CFDB7E8BF2C2A2D97B258B735C6D88BB95CCEA42F04F982A12E566023ECA3E04152E50E2FEEAA8CE0E65201D819C5B15533525342E31179614C2C774D742D07F3229120A3178992A234CFA01A1CF43A3B889C49C05ACAB2A33D08054DFA1F1F2ED0429DC5D997814DA5CFB544585067E93EA3902044A5D30872392F9F535D42CE0C2F0FE6599A4444B7F3897EFDA41989F055D11BAA0A99F34118F789CB3D6B52C89BF343A6C596C41E915A57F1C4AEACC61EF6BF9826B0B336E123552DD7009CB02CDD049A18406DF6BA180D82D10DBBB9AC33E6709D5AC459FAC0F6CB7C8CE8E4B227D1FE8958D58CC5802CE2CC0C2A8AE0E125084DCD801EBFEA206511338CABDB4ABFCE77ED0783C5041E696620F7701B14D63D8D8360A5E7698B990EA675E53B75F7A8A6386850FF6637C8CFC0443DE3417E108CC377EBA319A906535F060787F852FE6BC413D5E46C4B577DB4DA31F93B9C1CC1938A2151AB44BC8E0171314CB89EC69BC6E43CC08884102DE72ED557A78FB8F6290B55659D33B73C645E95069F180647EDB02AF8CA8C8753C7B5A7EFA1EB65BF9F753B1AF97C40F83AE4D1E216419ECCD1DC4A70533A4FF6A36DE060C4AB8BD9A27D1128E9237FD4AC211E4E3A1C99B1A74261E09A59E480C05E01C4C66B9BA65079A153E4C3873D3100EADAA5A54FF8A0B145CB1B9425FF68E50ECBDDAF50779953EE25098790C5ADE7A18F42AA97E08DC6A971A05408D9B01594BF512895AC21AEF52ADD61A201CC61FDA9B78B0BF5C79A758781D9A512779F54D217D35E4E5897F3CE485969B37EF05F4DE10CF31EEE1BF73D658AAB69B645D88E91F21031AA25C1C23164BB779B09E526D62D7253EB1BC37307822A9A4A1965A1C0ADF8224AE7C55F69B3B4BC2887F52ADE33FE356445226E64539196F1F3623AFAA36E881B435B986B905520AB2718E21DB63DFF08297EFD7EE1B9C95E1E4D0A4B28FAAC33A7451F8AFA3E5F08FE1B9B7646D4EAC5A67CBB80A2649AF8A2C5A4F402022B1C2D6BD8F644E97D124394273EFC7215E6BC1129BE4F8DF6824953C8E5E33D48D64A74A402F8AB0E6D81B5B22175DCB13C30710874550D23E5ABB908BA820D393C40AC4BFD195C6DF276EBCE2A957C26A1A2D1A91DCC0B74224F2C12A8F5A3F80D5444ABB37B05F91EC2EDB8E1A24A5F01EB31273C63564C743144EE1A8476C23C273BB6118010D7B878CB4E33CC21EEA5598D61819DCB81AB8ECA019D5B5AB47A04B48814B5B62F74ABC28C15A5CF260807456178B2EA628915FAEBC7508B82D6C470B4CD6E5E6A72018F15558F48FCEA6CBB821B057B83688252233DF0FB713732C3E3C4034AEFB9FB1FA13762FAEB1BD9BDBABDA616ECE922205EFA943E1511340A0CFB491EFC0CE3F8DD69F6AFFE2A06E4FE1CDAA53111F4D942454D46EDEE1B2F56A5A3A32537081B0C3998FC06EF61AE6286EBA3244E4F8F50441651D9899435D56BE0A22BB1DE6C56259EC8A586E831F6D285873D4EAC7652B7B64C37E9BE7BE4B9EB6E9EDE32334C0C1F00CF480A6E97CC2C01C52F96BDCAAFFE822D989C73DF42C525AAE9CE747CCB166B5592CA9D1298B210C4B45D5CF7AB95D8AA22C545F34559663373E95AE5F4FBF03111D4A62E59B5ABD1248DC26A0196AAD4CAC40F87166FFCFD981829CBB2C5E2803E86B7603E88ECA3E90C13596C31B78E8DA45CE6E6465FC9CE37EA86447C106D9B28E6193396BB79424834514A6081BBDFE3DD00143C547BBB90B0376FCD34CD65C24033FD79C4D35309074EBFE7AD4DCF4BF9E84A3C07F26B086A8EF1C62994D57268C2AE057F2A895A914C2BE32553106E875946F95E43D2C0272CBEB4B4B2169423D0206041300E2CF0F55CC057EDDE7EFA5D1668E7FCF3D8F85A3EDAC4DB8E183B8FABFAE96A8FD4D8117F84CEFAF5AB5777C866A2F48B7EEFD478C42D1D098CBED6A9C6FE0324854059A72C619754AFE16E641E758780386EA96C46D19598DBD0C6F1E87E17C2AFA3D198783C230DB586B9305264312F0D2916640D0F5EF629015715EAE5384FDB34E8E116F208BB6E1D78F49F0E17F6462510EA9548D37FA81971392B18C8C7B240E27742060406C1BF84C630576D7CCD12632D96FBA0CC8AC5F15BE38FB661115483AB885EEA5EC9EA3D5E01CC59F53423DF5FEFABEB2DB4F725EF9EFBBC6CF75F99F352DE5F324CE95EE54D29302D3CE6CF062B1A399DCE2C51BC4E5E7C60D781FAFA54BBCBB95FF813EBE8CAA18364181734756C1ECBFEF0D9DDFA9B0F9ABB019E05DD9FB1FC144DB9DF48AEA070034B82F2D28CAA63EEBE1F18B706F5B3419B5327BEEAB69CC87E8105D6ADF2BA843A627068D85372A0E66885ACF79E52D215B652DA637B71263D28E9732074D09D4A5CF0163198C66E071A895DF24FC74331620C3280A0C27CA00095BB5D143A69EC2E3B4B19063CA83C31C3F1ED637A58C8B20F5E76B095A2CF6688AEFD7508BC15B16C7B916153CD28EC3634F775AFFF2F66ABEAA44E88073F9A5DEF1E44CBD3D7A77AA07E62C673B774B71DC9E750D365B7E0F921028279F5AC46D4EB5D28A41D40A09E9C1284514C966FCD9CB18C642387CEF7636F2888E3931333ADF7F25EA069F435F5DADE9CBE96791AE9AF2ACCE8F5DDF75358D66864218CDBE84F294BEAA65E6CC103A88C24E16DE647EDB7A5F729F4E87152DDFF41B152CCA975A177386A27E71145695AE2EBBC7E92668D56B008042EF095017A30C1A628890405EB1352714388FD5758975E34ED72AD13B0E1E4C6CB89C1AE4EBF4CE132FC0B3A34C7BDC280DF281E17141677407DF500FAD673A09AAECA1332E49736339F4560346EE1E61E15F518B52E14582498E4FFCB3110AF9880332A5EB662C458CE91DA565B98C61F3636256D71B640368816B11741528559E7B3C4911B16313ED0AA86E1396B371C57660C2EF0534CE9B4CFEBF6EF48C902C8F6A6C7F10E1A7B0CBCE52EFAAFD592B39EE865ADA76671EFC22A7016BE423D4239868BF0588AF1FCFD895BB405AFC35D016D874E1D2D4CD84B1C3653DE7DD365DA0D1FA0B7D4BE796DD401229B52F66197ECF3D07A15B3862A72412AFA06EF8150C1C4948B8F11157ECD8927F99933B4DB36A847881E68D32F440120CB1099C3410910A9F02429859808CEFD91B11371AD19611BC2FA127325EDFEF06F6B8B1990E7EA3B54E1A78B1268724EFA04E9987C0DDFF42A77C85AC9A674B88F01ED37F11A3C3F19B59A44564D1C02E91515507111C3E6D21DDE926F560B5FFF285899E2502B524D5F6A25F2199AAB9768796FDD7ECC5B60B6B3CC6DBD7B97AF744ECE69B3C19527996F7D1E73B61186945510B9213AFB4A8294123A36B5F44E24F34D9D677101F6834B957820B48172D275D6D57B24CCA852C067E4117AA5AC4BCE0B4DD791BC04E9258526F168FB2A42FDB24A03DB29CA36A64BD4337BC69DA787F49BB035B4E0839A753E392F7EF62A2FC0236D9DBC9E39C52FB2F02D758E88736E43F24201C9852ADC5C0BA8110D688C6F3AA8826295D7D73FC233CF01F3D1F40BB5349A55EF0C49F8BDBAFF19C0E79846D76E1AD044E5C32DECEA093F5AB0F8527B4C0E4212C8DDE8C9B669192EB9569B1F567917C8C27DD4BCD9BBEC798D5B0EF42FD2E14C3752E97E06B6E693E5489AE642C14863E840F1B0176E6C93C6C27E0B9ECA493724496A59CDE343CABD5A299C77C126E6976A3DA2A482C444E3772C38E739A0F2F33A001B9BF75CA48A2914E72DA01CBF029E4A6917CDF53A1D050A7D3FCC2EC83945AB68BFC87E88A164193AF0233F1483013EFCF4D9D9DA908943254AF1468BC96BD913ECAE52E244D99AD5A34ADE0C94D5F91A5D4AE4B1D5BAC76D6E49E7D8F3354802C24BC383D30FD83C9E9EEF915E384AF3B46D827B8857039AD99C39AAE3605B47A2D2B5712432555554AAD19BAC014E0E051EA49A7D5F70A6979307249118E8F317A06263E2A1C282F484FDBCEB62674FC50C8EB8ECE915CE55FE2F86774A0AE16C65E4E717590BA201E825DE0A46F2EB16FFF2C7B9BC0A054958F2FCC49289F86ADA1EDFA7FB4A228DD74C3DE11E281D6A9ED2E8CF172A78418DE6C08F709422C48AD72AB25447BD2D911C24DD7FED13E38E44A93E35F54C3996CAB96D1738C41D7FD601C30384AFC226F1124FDB1B1EF3E2D3E78638A8059D45FE605762835F412CCC55C4449BD3D3D1CB40097601029CBC958661E190D77DD9D971566B499C1CF0DBB96661990CDFE5E2E958EC10C83CB84C081CD5388C4946C2C019CDC10AA844C7C229A8E50382BFF1C7178C59B871690F01CD0B9582CD6BF943267BFE9AD81AB4B21CD4AA3F6058EF45AAC979842D24FBDA88CE10FB6E601F7E8C6EF924C1ECAE74D9F08731A313CE983EB30B6D1F2A24ECB2498E3BEF15F20020D213E23B78BC0F5E7BC074E960241AA28B9220B86D2C8971CE4EB5B43ADD48B4897F0ACC4295D45134E0507BB95CB0AB6FCFFA410AC64BA1212E6B8079FD105392AE96B6EF09996D32CF6BD3718EA05A79DE161D2EB83A70DF93A22B96DC48BAFEF02BD506586AC1C86676C3867F9BF46E37EE13D359D48D4C689BBBC3E4A4E7C0E0723439D11736667C6AA5B55C7D3C49C860E145F11B7589EC348279325E7B7C331A1F9DA733517B3D1F37847BA617D5D7D38AEE0D69CA5D619039D1256B9270F1EBDB36080712D191763FBF992978426A6458E1009F948ED8B6C9014E2CD4AEEB206C7F47542E02349F398D24B74FE39E6715FB5CCC78C0CEF94E6EA3889022E698E86B0839367BEA4A459069516867DAC69511E3789633E329540124FEA87043244FD7CE39825BB5CC8B4F4B255AE6297DD79A006CB42BEC865902B3159ABF14A02053F42BF50FC8F994DFE3141A7DFCA7ACB9B307D61696ABFD118D77F34D6D304E638083F14F17E284015AC0292EBC943CFCF9074F2CAD983A2D570233A0EFD09A25F3B8801A35B934C12ED70AAF79FD62231D49137F48C77B6889637624DEFBF347C33B7357C19FB37CEA0D8D30DBE28BC26E190D61D847194327305179E2C5FADE7CFFA242D1EB2E907485B53F8D049FAE36A00BF24A4D0D65688F3C5795A12B2BF8D20C454002FC3A98C1329FFED3FE030C17677E40D0CA7FECB50D3E61E187B4B8D7BA0310CE1F256487151188BE3131167A676902952BBCEF055785EDC90A40644B4DD79CB63038023AEDD98FA22BA1F5DC0CB56FE0E32663F42B31DDCD44C43A65883B316C42F36452AA48E1AFCE8894E02E5E1442DAB2778B6A3A039A86BC050A07159988536736A2A35354FB27D6071932143CDFC5B5F680CA7874E601A409AFC0DD0A5B277B8995E851E6D23D6CE96E1B82D204174FA2C874AB94DA4C32A1E57E56278653C0165D5AD95ED2F648500D2896D1AEDEA2E20A6C9C6420609AC2CD602D2133BA462240ADEAB53973118539BDB5164DA9084EF752A1B9FE585B90C152357F4D5B11706DC2D2D7C8D3B816F0613921851CE104AA2A4B9F8B710D17610C65307078C0E855C45F7297490E813575F6BF2FB2E7BC311C64358D56C9ED8A0E86415880C83A7394BEE443217615CA9F3951546282C579F266C909A6DE0E1801EEFC095A27FA213F86F486105637A1468FE90E2EFAE0E433629D1E43B65116BCC2E12B3AEA791A4AF0548AA2A7E28768BAA56C0DE505BD94A63040DC325F1A51EF7CBB828A0A6A840CE8B7E24857E277DCE2CC6ED58D2D9D6D904D7C916C9DF5E8B9170C46B744CC48FCF60357A37C0CD4E6E3DEDFFB32579EB2665FFB07A8BAD13BEB5B5734EAFB5571F3B4EAFB14733325320328A94534FCA356EFE418F2ADA09308833CE628137112A7B99F46797D34BE14D0562CFE5D74823F0BC82BE6FCC2164504B1E9B3E28E38A4A68E1F707B4E1D7AC1A62C35BF53A080376268E46E6F190F9C6878CAB1EE68D2ADFE5835418C4E04F5CE7CC721D6718134C11321331113397D5CBF0C1D6D157E43460CD37DFD1BBDF74BFE17F595E1350F3FB79D91D778E864900C75B277EC7E33D66DB0C85E15FDA5ECD577D73BB0885BDDD0EDF51A09585D2B8510B9AA11B266DFE2D0B4A638451E33D53FECC2BD210D225A3719C90E0764382F2BCE1646C4303D696F8A7752E5309843A933E597F98325CB53E24D0F706F94A6527BBA88413EDF26E53DA6C9A66EB274CBCF410EB0B54D58B220B6EC41BF5AA357BA671080EB9F4C96EEC6066B50832F4B41EAA7CF1DABBEFC8A1CB720F5EAC1F522FDAD1B96C99D0AAA0BE05C088CAD828CE814DB3249688559248A5ADE4078AC353207A25BD3838688750197DF07389FA0AC5FEAFC8FA0FC9A6C2843D6CA94D6B8C0B915570D29E4C1EE5D30E555E0021CBA595BD07D5A772D8DA1B46295921F2C79EC1D4965F8330114DA3F7BED05ED1F06781C013371B1430662012A09347866450B960FC353FFE38B75ED902029611E145F69B284E668F91497587E61FC93546A078EDDA94761032A0785D7AB0964CFC258ACF5617005EFDB03022004DFD3595FFB00A4AEB679C2E678018C4ED28CDCB78FE9918B172F3BDE9B2F86E0515389A7BBF80A9EB416507672135660EB283D47AD0A52832AC2047EC418E6592523780FC2CF843B88C9D78EB8D7EE0D2CB4D68D56FE21EDAE10C50150B2682D46AB8491A26CECCE3D41E7E64B5DAEE0FF382287B7085269EA11BB66DB63B99B3787C66ADFE0EC677857E42EC463FF077D60BC15F0D94166DD734F0497E9B4760DC8C74DD38F9133CB4EA83244AF9655D4C3A9A09A0F4BF7FC5A4603A4011D7699C61D0687C7B53048B9A1FA2A5CF1A647C5455EB7CD1361562DDB28B5A5271E122886E7D64324E086B89397775887DC455D4FCA75FC752761C32399875AB062370707E896845CF5C77102017F458F5C24B7A77A1519C038F7E9F1AC3B5B16C3D7E937EEA891A68FCFC6BC284B7B23B436465CB3F0F078C53799A9C7EC385F831AC77790581CC7E3CCD9FC6FF2968FB3086C8D29BAE8A32CB45923D875758B1F191153DAB492D7C34E679C7EB2171DA19F3F7FF2001183D5C1EE0CEC2626506A635F8FD8F970C90B81D77A4C4240F017C40CC6650D8992C4AE6BAD94C041146ABE164AD789E8F42D47FF4CC7F36E2CF965E24F0CD0EB44D4C86CAFCA07783ADA3616B4A8F65AC93DC99F3B9E94DC9FCF554C415EE1D9FDA18645988EA1B970FCF9119BA7A97ADD360364EFE95802EDC0D3A66CD3A5ACB7C59E4855D5E39702284E5625842DBDED84370CECF085CF9D00B19E445368D670BCF4276A9A9BCD75340DDE5288931EC74846C960F102CBBFB9AA0F29CA7D23B1FCA4962A2F521751E08D05A9C5C05935F477126CCCAF8CE8399E3731A3148A110CAB7DEA943972B1513F87D72C4C773DBAF08D751A9AA2ECEB63840BBDBF8053FE57513A9024A32F7412327BC3226433EF9BF5D01B740DC9186EAA7910BBE89D6591ABF708C249AEBFD34D9D28DEAC09E822166874E77F9B4DDA95B42F12498B1143B47E226B5E8C9B1A9128B7E271D55EC322A4DBC2539A0D405CDCFFE3D93A68DC4634BCBEA8E0A19E374E3C4BB4E272B9F9F3A19B71FA4571B5EEF9D4C7351CD0E2865F027AF5083C3042BE8BCB3B9CF81452631324D6027A2F33ADD5C2149194A3FEE038ABE94895524471EA6542CBF8AF60A17CB61A700DDBD04F701FB6C3A317AEA209631AA5F1750A92A7A0360E23C6790196DB52CAB04A8648C5650A802AD14BD2C974013D07AA1215288C7B924392F0413E65E534E1B9682403CB905B0957C5952F78C12FBE6A79E5C6EA62AD237A8D0DCC38BA82B614634CF10F22BF0C167DA09270A1F77EE3EF2F8A0289CA680EAD9A1CFF95F3963EF93DF85CD158C5F4CE83C037F685E2F376B847A0EB470C990F3DE2C31FEB7B4EF05A14EF2E9D404A1530D34A9041C5739E13AD04EFF30BD39279CA3680EF4D2BE2CB8D6F82ECD024A0B40C058F8B25D46CD4CBE405317596B980754609D9542D6529267B680B498C92DFC9BAA1940C1FD3877200E1AEE79E2FC2F87833E8A34143380FA30FE76687FD357AA1234DF24B4FBF6A87F13A3EC886466A561B33F0B87F4742DBF76814BE6FD264E41AB69398E8F2803E0528C96FA79D427AAD60299C24F235CD61AB4732490E2BB1CE09108F6EBF26C5704C4EB0BFFEE99B2478E1EA7A7709363F29D5E4D07D5E274E463FA289294CE454FE533DC2126C0BF6E0BD2F9E2185D4464FD76CE47367DE07F1D977E0585B2F396D826D9DA498F628AA6D8F3CB1D198FCAE964519FDE5152D173CB5013083805D6F4E1ACE9129431E8A99CE5466BCC3BD0C9A6D2BA804B40983621E3F48658099159A0F34A23B162590E06DD9821D1AA24C2A06B234928CD6C779B6E0FD74AD3F627279D0348A03270B268F4FE578FA76BAD7287B9EE15E8BDC594E9B3B7D9DCFD521B494EECCD24BD1E0E9EED0360887EA142B375EA962AA905359EB1F0DDD0A0655922F5182BEFF18589E47DF43C6BA15AC754EAB9059D8195ACB620BB7CBCD3379ABEE391E26C4915886B4A5A1719FD53D9BEF839E69A9EAAEDD2F6D52D0870DCC87C3557C92BCCE9894BA8A6A85CB4D89EE134C0DC67B469109163E304B64FE602D5BDD7B07D2BE8D2307B9000E1817178DC53ACF8FF91BF807D80B1181EC94579122364E50CAA246BC1275FF5696DF3D40802EC6AF6C634984EA7E1780CEBE6961888CD2726FD85AE781D1A84AB30D235809A3BBC4EA973BE9D62D59695944FE963BAEAED19C1F016A2689C7071CFDB84C48A20AD788F1CB4A1210B49C83F6BDD4531BC3BEC42A945BBE3835CF4E943C3439C20A91293E834DDB01911E2876DFCD10D953AA5FF68979CC3A7CD4870288A500D36F9564EEF74AC0AD6098ECAE2211A01F0DC8AF2AFBB5F8B81E650BF074969F965C68F51C2F57F4117DF0E454DB3A966884C2B891228ED1C02A2F316D8080041AC22A3B2B2C4A8E84DFE6C75D26BDD00B4E6E1F8EA8D4C24A7A31B1CA5014D8E4A1C72E3A0470CC5BC0E2C9CD3C553C0EF24EAB4B6B689E1D2132A8EB0F15B1A7AB9C0C43A8007DB63ACD66FB1B585EA3FEDB077C6B2F2AADFC37E91593BE6BEA504F66C537FAD22A7B021C7FE6A0112A2DAE99D57BC74D041879640DCBCC1D0C22CC81BC6F579458CFD461A10E9FAB81C63E1A8ECC68A43AB12519C304DA023C3D33E8E58799A231C7A35FB889F46F7751AA59D0A771121C8CE48A0960E55C4BEEF2D905CD357545ABFBAC5A92B6A7CE74568C58B7A44C2B2993ABF841A3AA11F1592F63FE20033B4DCB0059CB5AA50750BEBC64B061F31765AB671E768140998D59B88704034C7D02D0245DF7159C84358D1C55B1EB1029369D119E5EB0E9A13D71EBF434B668C763CC83463AFD5EFCAD6C0F7EC4E7730233C451AE014FD009FFD41D370C9D06C58169C01ACADC395A13B8E601CEDA3A73F238703C58C2A74D46769D42C603248473696966AECD9EF1CD9B9EB8D8D4F8C438B354B22D2817D17CFDE17F422D7BC4DA432471A5F9236F81179372F2AE2EC3B6369E85A1F922EAA93663106ADB4316B91505D599A7CB48C5093A73E83B6DA7992B2334B81BE492B9F89616DD7C5F35878E522532C6FE9CE6D722E24E1350131D0E823EE2B5CF634575019F76AB02ED1D43F842D39C7589DF147EB59FAE0B3FE064C01145B17EDAE24A2986BB7714F9AC4D42DA89172E46596F6E050544BDC402512B1101677A1C1E51222F44D6F90E407D78D4B16A3D6804C296A417B2EB7E0447E44629AAD8D30E98B28183F5521C8FFDA7F6084A7BE7FC062E763854F1C31F3DA44AB1522F35E599E289A075189A4CBADECB66D0835E32F6A6DA9C82ACFDD2B291D7F405D4432484EC1FBA85FB38315A978D0895EB12EBB46580EB3B2A5175B4FFDB4E6160B2E4F93556FB7A70D5559A62AEA65BE51D06C1EFF54FCAEB1C94E3E66F30238BC9095AC6EB8F7702670EC011C02D7C37494999AAE3348E37B111638C12C7F288A9F2FBB9D3A6B6F164B2573BBD857F26E887F07ED5A8EEC0D3FD1FCCEB0A2F3854EC8DC7D3ECF37065A72D1F46540A72155AECC109B83A7B37F3A9444A2BDA59E8613295ABDFB447BC79A1B3FB17EA0C0C252FBD3EA214901FE4C02F2593407239774CDCF9F771A515856947C918472C310343BC8EC9CF18ED3084D8627C11B92DEF69BDD22E80AD94958FE90020238117566F94662CF8794F435DB62B4B63804132750827716E43BEE448F117410D4AC7C35F40619E6C7EB3D280E7389F0D957D705B3CBE97E6C173F6B178DD294D9EED12F313D6FE6133F0DC4E726565940614EA568E2BD4E320E8C81457C510CA419F4DC457E74743F9DAF462BD7667C35741EC1A05EDDB58195BC341AC6EF177F50D6C81CD79E1C08ABC2E302A8DAD69368056D99DEE3719B2F325840DCE810F996FA38AEB9807F0D1DD811995D487586FC353246F5D9A4B9C7AAF748B20381CBF5E08750BE686024B2EBC135F93E4200C74AE716CA372E30A115D048EC01E633AD24D1AF7D2313247FDFE45E15EFE274091A2AE04F63F850841498C77968FA184B02B3D9C305842165BE0057E9D9E3E288E929F955A246A259EC31CAC486EFC950F927979F85E9F491618F86A573DD6AE6B8E9ABFCB482B8B9EDD4CCBE0FBE2065A7F5D1F19634F2D8189EC9DD86403A0901C54CE948750265D26D5FD2137248838289D26AED1EEEBE0631B8ECE2035DC3F70E3F90A35B8C6DEA892EAF802764A1B7E6AFF35BFAADE0F170AA73BEFAD29D520D3F137B8390203163793F7A44E221576DA4EC42A442BBE7F4E65EEC440F854390DBF9A4F756D3D037B1776869CAD3C992E6C1C7180D93AA9CC4BC302BEFAFEB704A68CDC9C72F5F31B496865822EDF02BB6ECEED91A07C0D572504F62FC0C9F566985A516637A490C90766C0E0BECC387EFEC81B8682FA08A53658B6BDFFD87AA7BCF41095834E69D8EDD738BB926BDFB3EEC406DA40C2A3ABBED2F76CCCFC99EAFA420F2E1F661061B2F5C01063CC3B84EC0FEF662F866E445C95369E35379FCEA38F4593672800FA1FFC2B87438BECB4E468A73D2656C70461C62CE0B8473A85B84BFB1EFDC33DDAB885BCF0CE40C2A1A3A271226ECFB65351ED911BB462539691A54E5C86EA527BE564C7AA116EF89C179D8536791E962008D8DC792AC7C7D159215FD2CEE46E84ABAE4CEC4A73E330D44178B8E51D946592099AEA539F6E66CACC1A2A518A00BEDA9FA68531D2F94A211DC3F4E9D077F30B10E7BB7EEFF91B64B217FFA4AE3ECBC0A003B8E149E8246B5813923F6FBE9F7E36E64F6504FE201302C6CAAEC9A2C5ABF00C1CE063BFD40667890AC52C12D00D07BB7A8A5F930A67003ED4CEA32EC6D4E3B7F18E37151A9E8229A8A16D50702B61A14A7AB80E5B931001916C931A7B6A786A733EF2D4668C0CF879CA8AD942B6C492471B4AA33FA0B1129DA1EF4D5A84F6F1B39850B1EBE8D73B19D3702476FB59546052B9A8F48F1351F89ABBE9F40E5DD2D05AB69E05120FDE564DDDA570421E72A6D728EB70D9A78D3232306D9037F2F5CAF06BC2FFE8F4A84482FE2B8CBA5C870C8E26743DF2387E161A419BAA02671215BFF692F35663D05296789150847BA85293D62BB9FBFD76D2C9690241EE48962C697AB99283DF30E118B2EBB82A70B8DBBDA0F10357DD7C2E4E343A85754755E4C389362042938E7C9F9C0F8C9BCE239044092104C766765734922ECB600EE12B34D752666E1B77F91D8F8F96BF054096B670EC8AD2DE647BA7D1D164314D01E9BD0831E2F8627838B0DC51670326E766EE22CC93F9AE325A01E6D09C5327BB030F2CA195B06FC3DDA878CE5B31117F26CA1A1101A1876D188147C11A5B1BBA22D1A41EC297DF84D6CFC7755E4080E95756ECCFD4CD2EAFB2C71AC9C1F7317EAD0536D09926F677490C2C87068249D0D62F9F088AD47370A42CDF1294D22289E44B17F9DC7CF831786E05B95D5FFE08FF6E1A616CCC1E8F9D872FD7B02BAF127E09F5C787DA6B66592821A790AC47ED580A306C4CE480F46FC2380324374FF806110E6DCCE03CBCDADD35CC5DC32C875655A8CE4150AB21A23B9F8B7B8E98E05FE697624568270DABD8703CFE5DF01B9A335A4DD12C072094A83116789F821E1AA050B96E21A9CEF70FC422C8CC99D1D432AB36E7EDC5BA7D7CE5EFE9024B87CBF3F9941C249FDFE971642B16936509150D530B418CD728F6DDEE290F9B1A4623E4D44A8F70B56DDAD5807C6A455AF5AB1D6D0917B5A8F6C64B78C5A16043A863BB2876E300449BAEDA9E18CC72BE46133D35BC1F73CB5F07FFDAB4CAF18BA03B0AE149C58D4933F6830CD4ED0CE6F3931D618D72774615DE1DFF6CC51AF9708ED07980CA8CA01AF0773609E6186E094A9E89789A6BF00C22E14289D7DB1191F18B2951F1C27100301328F51F51978DDDD6167A8F0BED180ABF9304C0902010851CA12846F83615BCD08A314DE4DEC98F8817D35527D5705009099443489FFF43A4216409793DB48FF4BD43E0C75E768C926D4F28ADA4335ABE1140508435648B216112C457551AB17AA30C97A079787F6BAA9253ECEDC76BAD4A6AF554E31A08277B27D2169A33281B85B75BCCF4D8C0FAB2B125EE73C5B51B47152B79C9B7062BB10AEAA94C1DFC5B8423A0433614C5B63AB89A79610DC1558CEB1DE19E779C6E3967D2D9163E87205A291E8C154C1FA7805D2036865631A31530EACF57DB0D7E2976DE97AE12F84AACADD16A337DE5E6A1086CD2A1788600897DD7F72F3A07CD7557BCFF6FECC161A9910C6366D3506DDAA990FE5BE72192CE6D6BA066685A45788D2DC5CDDF6203279FB6508A386C51A5C49E595E8E14BF0B8C713475245A410237486D15FE651D036C079D7A186B55A5B3BA00191889A588C1698D603E9B369639CAE8167D6DCED75C2A66E4A9DDB948B2A717A394A7E775141A8C21F6616A707689D4C700484B3D56C0C3D356E0B47EB3701B5E162F88EF250BF581CB49F92BF31B83A6793DD89C51517FADE096E10431881FB5932AAEC212B301627DF0047183B125636EAC16A402B4A63BB152D01F8B43277A6F6A681390BE2321C6550F45ED9AABC59705943C64B929EAE179640199A82849BD2AF36F8347BCBD57BDB8899BF347D32AE358D6BD5D02A9663C0FFADB04C49636C36B6E66EE4A288AA51100560D3262B01AD8B516A89CAB476C192F1F5EF714E26896CEE5A95D52B7DED8B40B6E002B8B82E183DF7F6200F36BB3D624E56DEFCAA8193832E86922FB288961A5053BA9B46871B816A4F8DA45A75C40D4D2C4C81260E2401C7897542A55EC5A00270B8BBB46F6387B07D66FEF2EE0D2FEF61A1BC9295941944CE1C31409938CEA34C483C4B91EF46B94FC39AEBFD26C17C3240EC08F988907B251DE5301E0C0596D1C0F916048E2BDADAD2AB9B75B0B3E11A68A8E194DA021F140F6C745E5138AEAF4C99FA7B9C19530C4AE6628C924A2EE05F485432EAC00E6B790D59D19729E45BEE69EB86958B8605247AA5E4AE8A764D4248E8CD1C162FDD31342FE04FFE809D2B98C249C539DD9C5483781B48A24B61AEDEE769D657F08426DAAE2CE844F3FD273F89B18246F1E8F01D15DC944FE4A327DE95294E66958BD67E6DC4FA9F4D501BBA9CE5EED157A59F09DA13DD4ECE63658C65D54EB2EDD9164B3BB86205CA82A9DF6D295305F6EDB3F929AB8C7013692E3C1D6983E1D99C362D7693BD8CFCC43BA2933FDDF6826DC1870B23836A5DAB0AC69BE3A926BE477BED20B85F0B45B38F1A6A25D4DCA13719ECDADA80E8E3032205EA3A6FF2B43682C8261F63490523CF1B1613EF04F8973ABE605AAB2076FBD11B6501DC51DD63EB79E723FDDD8D8F0BC0D90DD90C500E7989C2CD4A1CFF2F89CF836AE00E4823DF5AE63225C7AB83CD75CBC73532D6E0FE5818A01477C1DE9AE8AEA4800C1AF6D90573A1C2933AC56C8A17BB9C4B7E8B0218C27318EA1458A974C1E22485E067C8F9E62AB0247AEA04C34381EC99CE9423ECC8A7B176F7A23B0131BFF377037DA6289C84CFF59C364ECA1814ECE56407487D2F960CA3889DF7FB0474CCA702929C6CD3D2996D90E8202D1E08B54937979686557843D9D4E67B58975C0731F0D82FA07C553C726CCE804E25E38B8268BD3D93BE7812D9E8F7E828B63FFED8CC506424F1DEF1D95E1869507133D68E6090A267F14988A6B65DD418D06D7D10B5EBA6A0FA26FC4220F2B367819E95CBA482074E74DE19F69D62532F933E33417E11C3539A0C02D209EFFB0F111D2DA9AD839E5DE5CC56DEA7D6F0A81E8E11F2B664EB49D2E23FE57D468BB0AF1BBCB28361F828826B2856B34A2289BF9EFCBE5416C17959FF2D669CE0C66E3A6150E6858665FD4586190D92E3B31A61D300FAB90443F7AFEFF610E7B359D6CA32E711487454DB2464383809EC338198311CCE9531B73787A8A093E3E34434337F0C992A8B67DCBADF61035D08499EA192915D36134C160735AE12D78DA506F84E3B0839B96E68A222458B7222F2D113C440EAB650878C121431867EA49F96CBBDEAEB922A296A3D7EC132691808BF5A63013F004A9BA52957C096FBD34D3866914689C3BBD504E42EBDA6437C4FAFD566D1CE891CD51AF04C5E2168C3E4CADC62C345250FE817735E3B4D72741382BD1458060F4B44D739300442DE69059BCDE7BBA2A47E492D5ACE0435B99BE20EC18306BDDEBA07586B3B689D6D5CF72EEC006B41615F21821AD1940F834550A1C2A7EB799F5E611A1F7C761CB49E20C6CF276BD18FD06792FB0048C1D58CC3724BB1230D8AEA3B1FCBBD74CE6D35C255B28304DCD9EE0C3FCE18D3D3A749762C3BA49B19E789FD0E457322387421DB60E31C39255F4B19701C8A06D2E85A976E659082EF95FCEFBE813DA8E17F579A2645B1422ECA3AD1189B5A4DBCCFADB4AADA141D8BA1A9B27091E2E69107D7A36C921B00982A6931CC34D9CBD103A11F250366C822D9D2546C99FF6993257F3C18973DE03FD0A54D93C7505A453282CE74A385F4EDDB7469929DE53E0543E0CEEA830FD467B87EE36D2BD65F6193A1A7D0EA7F3B00D7D7DA4A89355D3BA10E476E5D8DB7D1533016F1D97EE3E15A9D9D5E145C00B8B8A542866A1D70F08A976C69DBBBB257FC30CAD321FF2839C0B0387E167D145AA38CE5D66A8D8C5F0E297DD60E9010D5BB75B7A292FA768D52CAE72938D58DBB49B1690243EA786E3E21DAA2A2C2C44CB14E78C034A8C935DC18D23560243703407DC59A5D0305BA8D8DF9FEE5B37EE36836227A439B5E28305B44609042BFD951770A80768AD77CD7A0B9E65AEC7287B6011BCC771064F8BFF107F6AC108BA30303E3F33F6D0F0F2140DC526DFC263FC1DFCC81601DAA1CDD7B8DA79BED439D1937E4362C92A4E7F0BDB9314E027C7024DA0470A01AA0E5A06EBA32F448DF197B1160E9CEAA8589AEAAFFA394D05420DE926F76EDFF35F9162E324FFDCD27BF73591E0A8F0BBE6152EB3A03ABB2F3C3E2451AB584C01311BA348BD5B5EA30FDF21B3D1DB5289D9DD1BCA2FC669E93C8279FFFBE66B92BCA0444730ECC2897AC14829FCA96BC54A393DC057F70EA2A2DA89C63E4C38D8A055D1DC03B6B263C0F59029197B1A7CAB095ED099DE3FEB9D0829270DBAFA43BD3A5E8CA7D718EAB7401AB546CBE0CE60BFFB7619C5387C2864F4C077219AFE6CB3B6BD6ABF3ABDF48DF8B1A011568AA6EC755C1B9F9CE12196B323157A10E83686787C7FA9125A90AFFE6D38AB7ABFEA5A120D45956F08BF362B04E3977835EFF4987DE1CF38693B03EA1B9D115E35B45D07314A65F09DBE740C4A80D82B03A6C1815F07593013024862E9921AE9B290E4956588A5AF0134244176DFE412D586573D9190F2A3CF7ECFC11E4771B53E9890B1385D6568765A844CFB7CB76F9060FCF18F56CD3075A969E455A7D28C035664DA78D44059267F59E63864113BB5264EF9590C99861873345355EA8ACF04316DF3B6577FFDD502CF6967D15BED166A5A1E79AFC0FE65780FF5D1B7D4504478D52C9DEADABEEBA0B8E31871B400BA487CE7697C37AB97CC557EB82CBBFCECEBCBA25AF17BC032FE68CF4AD676845A930FB2A82AA6F7915E50A30096F81B46A3325068183DDC4671EB9602E14B644552C5298551AE7A144D7564CABAC544404D1420D60C06385E358E392CC79758FF61B05F1A4B1DE9B1F9117D7B6202EC94F1A1A05B4269D834FBF184EAF049484D4EA0D701737F30562DB0A6F015AA0F4FBB55939D17F5AC4F71A190EF1DE4E998F7A97967D7AFBE5352CD2F95C7DD09ADBE577B5A768AD7C6E451FEC3E7F9295BFD89B90E802F8DA424A0377D4765236F5D8D0B7BCDACD0A228069605421E712EC3D1B7BD078C6EA5E736DB7175D098D1D0F3E7E67E43ABF4C8C68D9BEEC47F849F4D79FB406745CD3BFF66A09012CE0FFD8D2345B858F205FE1673C9D4443EA34FCBD33A1A73FD60F328FB4744C45D9B311DCFDEA0A41325C9A69884423A4465363910D049F497AD1ABAE8194933A480CBC627AE1C974FBC13AD50331C9D7DE056E478714FD7971B2A8D95BAC369240582D3BDFC2D505A9EB81094BA031E6A5F2F39BB06C700EE38A405D7C6971CACD8981AC319285FFF739833798E7F5D7CAF24C7BB5EEBD155807C32264463CEFFFED4BC91896BEC68C1892B06BB7FE63B73B3B2AC615EB92D8500DD1A4458377030C1C8C68937EA9204F619FA5F0143AAA6659793DD9769C25940373E052530C39695CA6D652248A095123495D538FBE2244B61037CB49E00F588F7E3702D7CDC4302BF0175CC5046EC79FB5AF09D800679A278F51BCF901593DED9F933A7A74DC3A2FD9D2A1D8B4424712F2251C33F08976EE8B428011DB6BAA3452F1577D0268FAA1A12065A66F7A93FCD9B98816200D32F621437F6EA882FD64EFDB58B6D3F79F49F2D427B2BBB1A5855DFD02B9006A37F8FA58BC4321EC53C7226256B69828E1B8D4C58F82FD206EF61F97200EBEC64E6370C7D0BA520AC399E88BF07AE25B8B1F4D2DD0DF4334A5E00B4030E9483C912432C417FEF56799B1E5ECB1775C9F53CA51678BD18B741AA2232B2D22EDC5C479EC82367D78F2B615ECCB95960EFC9F46677C6ED61A26667A0547B646DC462058F81E707DF8449ABE76DE926EE77EAA2787754B5F383D5E23A8FF5FB974DE895DF35F4CBB474458239846B46D4C23912058B1D1F6B066D9050C5191BE933A8BD39C4EDB3DD203F979A1927489FFECCE9623483C770C202A6F1667C8428FE79DD569C0658E2293142D1EC74D14A4F8922A389EDD7B28FCBFEEB3BAEDA9D7C8E4B2F95CE886B61FFC62FC044A28DF91DD44E15E221F5E47E1E3C5E92A585130FE6CBE257590FFD4A1D6FBDD731E8CE3768C211BF049F89569902D049514D0B1355E0F51255AC8EBD5A103FA2CFCCA035CB91E23CF1845F59347CD2B3F5AAC9FBEE014B567D2C39F64158D38DEB8EEE21733899796780717625D64286286D1D8C2A03FD11F2D59B1FF2C285FE47A8E09BBE50E3EA6AA631ED02759E5B506FF618C68B644E13A5633C7618BA00F54DFEAA1BC23F01BAD246116BD615F389C5E02D99AC47327C08D4EEF4D984AD3249F629DE6BC97E76E551205A0F6BCB4FD217DAEB43D2BAD460A3D7B1D9DE5C2DD240B8198C0110AEFC61F96C2F17AB8A66F12DE043AED924AA427D3F63A7C318B41E3546371E15C5B7BFD33A07BA991235BBD43435575D3A19F7D13E201531AD7EC3C2B1AB00B769FF04842CBF357EEBCA5E1A0F00654393FCBC5717607864653B135F8B9F525A702D3BC2CDCB298B9501B4FADFD082FB969A93EB2C4F93560A5B0EBE374AE4E68C0E6AE75FEDDF3E19363EB53E1673CDCF5B07F25BC23954130E85F350ACD7B4D76B2A5DF05096F33095CE7BAFF6437FB350BBAF48DFBEEDE6B45A7B1A1A78E0DB13B662CAEF25B60991BD158714CC82251F2E4D89D3A9C6D744958B563942C0D5DE4853F750156222B99A1CE9E48A4BA7B5389DFE02C831B905D9DB089DE669318BC9D1E3DB499FC61EADC37986F4CEEAC268274B16831426BC9DD6C774D0A1896320D68DF75730F85840B8C058F86323FEC5701C9CE6625C06CCC2976616EC751070CD12AA2AD25076FD1CB3BD04A1008C1B119E15A720418BBFF5FE68C47062F69221958B9303CEBD4B2C2C4D5A6DB499FD9EF968441D60945606B21FFC19F648D013091EB11FFC05F0D2A49EE87ADCC95B48AB60E14F05DD7C03502981B8F4C8A86C67A45E7F9BBEA5DC9E6D6B0ABD3DB25A64EA9D35EB7B69770D34810C658814264C5EE524D2B83F14D928FBD052103BA29DA2C34E204753B4EA26F3988705856280C3B2E7F9B37E2A07BE3EC1A07CCCC8B0060A4CC19DA7A8392DFB9942E60C9ECC8CEE71B80FA0D624FA1FB239633A6F7ED47800D5004755049EB5FDFCC8260AE7E689A1B2CA56A774F087EE848D11FEC56FCA58DE698D1C7E9340FE0A1C2408563CCBF05CD7754FFE9A2DB94F1DA520BDA391B2FFEF788856D5AA1DF32AA25D4895B6D7D277A3F52B2147830E6D32B2722E81BFE7CDCDBDE88CA01ACEA77BED39C74FF5999997C28F3994E2F42E1A82166E08064AD136B1CC5578B0D640A43A636596E3496316D8D9F18F651964216940FD488A1AB0898804C32512D7D0FC90E5C7479DEE420B88AF4F0AC079904FC6AB1C1F359D93624140C4CD195BC178771827C1EE3AC70D222F864A88CF5C6CAFB048F0DC013F1784E2C695F03AC7AE5E15B0F4C185293634458D9DD74CCBDA4669B6286435130E3F3CF532C82EC14948DDD2EA3A359FD583B069E36BAF4772992E8FEB8979DC86067C45A2D14814E395D0EAED252BE6BE6C33BE3F6A3F332A93A168259183C29A98F8D7FF3B12A5329F2D0C9CEF9801911A36BA8ED08929EECFC2AEF743C07EBBC45A4C8A6C1B471891D2F6ED8376614C187952F66FB22B815D937B527CC46D402806CE8423255339088158755D8F4F7C5696651B7EFBD3AA2025E893FAC7D2DB1A94EB68C2CAF421900D4C9266182514D840C52AF2B45C7D6FED5DB81C127FDC2B4C40DB7A8F8F6D613516F3582830C7726EE12F1C3EBDAE66B97D53C9C8E217ADEBBED51DAF06067B65E7CA03B92538BCC813B41F33E7903529673DABCD00BE8F0AE5EBCB9C418929BCDFFB918D291B998504D1C662AF0D68CDA0EED287D20B76AD1C0444E4231683F1E7CFD988FDB5E921F1C5BE31E87AFEACFEBCB0CBB2C02CCB79C426C473B0D84B3F6DE2680F4F8D8311C37E3F96FFC28D4E1D812C04D670AA7C1C9D92BA896F25176977914A54030924D49869CF2B875EF8FCD509B63D639B9A50E73D30ECD9117CAD0A925426C0B31298D6B44194C24A63FFC73B24E417D6FDE454AEC1245DE34F3CFC9479C66A8B6324F2B22704E93359E4185E10F91B7F839A2374A2517570EC95E46F14ACACE2A72B3BE60340250CCA045F63F8187DCE52BB9CCD36797F993A9E89262CB4BE260FB1236719CE3A842B90503FFD7AE08D28806D913493524C644174C97B5820B020AF122868A50CAE8B6B10C2307080C44A4E2A3413E552697F0A0110D6D05918F78AE4A9AC416D91D069A1D3B2EFB5B626180A98DAA2DBFF3539FE1BE841F554BD7A9E2A8BF2B70722DCCA85EAFE10D3415816EA089A15BC26ED9131E98A8B4E5E83B232D52CD8E9301EFB43850B5322755F5528902D59960C436F1FA6C14622B06CF8A64BF1F0652439F4C042B84930C9818D5BF3C9060030285A588FD48F36F0031E26F36CFA0A70980579E5B591F02B51F985518CFCE2CEE5268839E455D8CE91569725A9EF79BF6B9B736C78990995D36CAFE40F45B08D4BCC6C6D1C210DA12F718FA464EE150ECC5676E5F36E38C8E447E25E4FF27C8919F25854FD0021730CC0B62947FDC34BE7FA7BA16C44C7617B2F979F89C7252D3E5D4DB96A58CC9E7FBD7E99ACF3CCCC54A20CE302B8950B7EBB6DBF3117175220B646AC99ED905D788E11D34CAC4BFCF92F6B5E8478D2A19C8D01D17FDE30D6BC6E1C5AF96E667FBEA03C3F8005B56F2382BFBA96ABB1975507FC5E2DCD807599261C568D832A4C140F58FEE0EE04DF3B0BB3569592CE378FC404EE9A4D0E0BEBBBBACCA978E9C251F6C89C849879B594E237A7C3B03247434DBB8BB34F0C85B9ACF515C50990084262E71F905A34E2085E423F78F5073751447E3B1384339714CB1BFE650A5D3F9D8B9C819E5A927FFF602B0634C2DF5CCDCF024B044424FBA9252CC0B392112ADAC5001D3EC5CAB2DD2A779D3C1C0BD0C315780883C2401543DE333063C9F493403D400A8F1A6E78BD73CC8FD3893D3E13D05BBC30F13FC9107B3EEDA1F76C946D887E4C4C4B549C5D897B3B36D4DBDD1B752DF9476F7C71BF0EA8CA36FBBD6B4EEBC5EADAB6BC75E1DBD06EC9576764089F6A6CD51B8315F5D615399EAA6B6114AB5CA663656B349A7F9109CE6557205E2BC867DFD71EC8B7F087A5F4D89F90926B29080C0FDEA01D4347E46BCD071C53C4FF48B3B30992387E69A7CEE909F8B85224FC8E355FC1A80B4BFA6B8C252565E4BF31292D78E0C49CB7A0CA7464490629F39774E4F9252344DEBF7E0717306C65397401E6B01635152CD1762B69BAA7C8486AC12AE4D290FE1EC10E2041C33BAA576CF59FB18EE668B42E1C800AF2E3014146C063ADFD3B66A8E63C3FD44C4669E935594520D7FE65613D962ED266CEFBE8CD1A42A99B32064758B38BDA3783431034B5F75BEEC4770829E3D511384C142AE67850AE2323663DC7837F9BA4EE47D2CA5B6B799CDE49C95331A33C4A9E79338024F17A08E30B3DA9A36BDB4BEF3D7DC26B1E710C07E97EB39F1580D73870A729A3954F48FEEF62A89EA8E5902DD5FAD99C075D2D760491BC5727A8F63DBFDD4B7871432E7BC1F05981C6E3B8996FD4C0961D4DBD0C254B5CF38DD8E89C4A4D3ECA59493A65A4661ADAD84ECFE79BEBA540E56C131A8C54478786F1BF2A91537F876D88CD229AA2C7A4E53237588B6D70F1C19B365B812C4465B4D21A894E321EF77EE84B4F66E606B6E165A6BEA609F6D79EA17E3FFEE5B56693F2E9A194F9F64AC2DBEF514E833386E2149B27CD3291B08372ABA92FD63A1B46EA7F3F01B8FD2F9BACF45E47814E1C9CFBF68B181446F27ADE5F7925C6EDA050A7EB3EA492C945F128FD3605E8567DA65DFFE18D9A3F7272D2767AA0E1116E299C1A30B4A65867AB7EF629717117017CAB4BC58F3AA8B42574037B9A64441A1EE37DE43A2CBD6D5C050F65F6247D21893E405237A87CF55921871BF1B34F34BC68A552E4AC0397900772234E8E0BA959877B60A6A8A4F5B0E74D531B1774CE01FD35F20AC18FBDB9FF75A41726C38029B19A62CA5737A621E79B2C8E60B44BC421DD3FE3EF741A2F6BAE8705904684EBB487C5C3734338F65E3D4486BAAE5DA1BD444B573D1F13DDCE0A7EE7200FA28822691ABC0F960895B5625DCDA216ED3CB15A3976F27EF0CF9B4A40EB89FC894F3CB85CE40D5B8ECDF0A9AA26413539E57F2443D16F67EB57CBD32F042D83B25798B38A28A386282F912D0374C06F61AAD18DDAA94AA29CB4205D737EE68FA1A1645047861661C5990950C5462533681693BC9D931083192BA91BB9D92A56F60F4B3635B5731C40C3F496384731239BE719B86CC218FCCA74103293C4B2022A0EDC85E08627D4C469679D64EDE2F878228383C86978AD325BACBFEC51571993F70839FA081B6540DE02E9391CEC6905045DD0D390F41C1F8D822D5495F1E3166904D59E94C121F8413CE7390BE6FCB48A5041DF2568D14DB4E6F45DD41FB10CD3BA8CB6C97C1963BE528505A96888350E6C8F44A123435F73B88D24DBC14403E9792E00FE924FCB227A4ACCE681929648193CD75A7CA2C3B05FE7232A1FB1357E9CB60223CB63517D1DD211D0148CD555FB844FF0E8CF97863A649EE3B1EE72C0B2C712A03B3CAF1772F70A6C3D1A5A13E89B5414C4243ABB3FC88A5466AE1BAB12E232627CE82182159AE2D137CCE0D91CB196399C96358E8F8589570F2B4E432D1E79432FE2FB48FF2B5127A568C3E0851B678F2DB53C2BBA93F72493E599D78F9F0BDE405DECA626976E2CFE82253FE6BB815D71A324829118F25C6C595549D1F6BB06514C0756A8C393F138E3FE6E4135E5610C531D80F9BE3F61A739EA379D5F55C2C84D5DB17DD55B3D6ADB41B2819252BAD5AE1FDAC5DBFA9FFC45235CD9C498CBCD0859BED5BC7354A0C224ADC770EFAE468BEF910E28AFABA6ED1BE0460F3A20CC5686FE367D2129D7040D384BC9DE09F8BC11C25ADE435ABBB1A1C93226896C10E602732B5DF140014AAF5EE873D90A4BB0CBC0EF8C08144902E85CB9FC51ADDA0759FA2F12892E5076C22CE268E9A7D3DB9DE3E6C6B71997E9972AA0B91D4FEB3522B05CC4CA87372B067E418616F8A7ABFBA16A03D4F2A58990C25A0AFEEBCA00ABA5D7377A3972C47B15B56B2F84F4D28726EE23B24ACEE166FB3E1200E7093D66E44D09573E9AEDC96F29FD9DCDC91F375513483E3C528FD7608224A593512DB7A0456DCD7C5E6E131244618B9FA398C291C7A21DD70BCF88741D76EABAFDB5576A1590480D0629E99C452621D0639020B95F9006B4E0AC3B397DF54FE6D36E4F35DA1552D8B89AB17793418FBF15DEB4EE79AE3CE1814684CBE980AC5E4306246BA9A98E632C80018CA67C48D687A5FC76257D14D1ED72BC9A26A150AD01CE6F9EB44A76BBA353E2753FED95B808D6500865F00F56CEF1F7B5CABA0784F3F99EDEE69B0881BC9E65159506A99188A7C13B37DA7119B980223087D23DF955324474ABBDD7CC07DADDC8D08A4C1B909E3AF4F4FB74001FAFBA3C57EBD3DA3078891F890AD1B939B3567128CC8E1D78B5ED86F0D6C6ADF6A924F41E3791FD0BCA3FDEE35BB663A70D59397339F3A962929C3996B7696896C9CD9FAFA871C042BF6312948CDF6A2FD0E7F5DA371E3B44D5D8976654297B5C27A29F9D710BE0E4AD37D6FCDB88EC338D9CCB819FFAA8F9526DE8B1F1DAB71EAFCDA6E6F503184BDF5BB0D8981D9D98F740C9A8B464288FC893CE253218E72F204AFAB308B30750C8EBDE8C041CC7F13FD92547E8FE6667EAC27A72E4759E38807F8D0A4754143A7D6BC1514D2CE3538BE0EA4EC3E928A62639D5C32A9C0BDD5C560489BDF5B7FA5F07129B8AF257C8BA5112D8C17BFD6D7C5E9ECED83DB640610FE3ABD1BB86E2E96DFBC708D7DFD68F4DDF0E64EF82C4E38EADD1B6D6B3BEFA2EEEC90D525C8F3E5D9556E3A0A078C7004BAF2937858493069B970BBA4DD414511FA5B94D00F2AFD5730D29E0398473EF6B4494DF4579B4ED94CEDAF8588FE8EF749758448957654DD11A07C6729B075F9BEB1F70EE95ED92904AE4BBF0BF09F0A1B903CB54CF4DAF49BDEE1BDBF07894E86D71DD22371E5CD148CAE0095A2BFA2D5712D00AA43EF725E993ACC1303016F2CA553E345C8401549D0AFAFB8736EBB4C9D2E2C9F4374236BA7D1C40398870BC27BB43AF1818AC5DB2B04D8491DB94295952AC83D3536E0A1064B066A0A9E238499BD4DBBA3743CA8701B7D4CA86E74AD0E3D870D892959589F79F2F9962981D873F4CEEE87F31BAB6F336714AA883097B2AAAB047AB82BFC55895956580F4D7DEB7EECA359F17D60CB535F05502980EE54386366BAB52348C7360442B9563AB8141687C1E312F8ABC3A6DE33BB95340BDF8B48FB6A93D8F5F5453505C2F0349051123E758EFC0F7662B3B9E0FB9E23A3F56CEF0E20FBDD49C105A3688D9D9ACFA9474FF8A20F6998A66A8D2793244C93DA631A65616C235E289BAB5C2822ABD07930971FA3377C1CAD1D5D296A6DA85403EA925675FD6AAAB56F382295596A8E557C9ADAE45466322560A27AC90147809FBC368E85076903C82075C4E3A40EE012A1E026DAB7F752B18D81C4AE8CA9B82ABD6F29B6A1683AB730533D351D92D542174BE7533284DA0FCF589D65257A6C76FE6E469779E912B717043662C0AF2BCFB77F8E637D5AAFC345152F7654C65DAD14DC7F4B934CE841BDBA1A3B8238757DAD5A0D925E27FACA8EBC6D747DCDC236DBBDDD6B2BB1E226AB1E82FE730C5399B52823FF22C028A98B1C76BF6175017DDF083D2341BB42A3DB72BA667146AC33B74DCA5FC36A5582A41988F1F64A8F6940BC60205E366AE4AEC2A0E9ADB62EBCB39781924345B7CFCD3FC31C87EA64297119AE5DCC51BFB249B48ED5882B55B669C3E2164293841DA8167637041017F03DEC13E7041D244D5B9D17A659E3D0997735E4A47DE2E74B905A9FA9BA4E9835787EC809D28B86341DE9D865DF60823F43A0A9B1C26AACF70103E80DED44ADCDC695C18B9973C9EE9BDFE588F16ACBC7149496CC826EE78F2C7F131572A10EFEE2A40D662DD7FEE346111688E1B23F61F05850CFE48ECE157835A957E01BB10B9EB9F98F830D80033B15896F17AABE9B243FFC5A6E00103D9EF00C699772B4AE4BF9660AF6842284FED3B0B697C228A48E0BEA6229EE6EACDB4070899DC5743A10CC4D4FD9289B5B644027C2FEFBB2B08E387716510E48E1B2A2FF84EE7F25C4E8C77266A149FABB0CA7E47F0C102C4A371E8AFB4197C479E69C6FCAF47F2814B1AFB79C7C818735778A9F3B6ADB19B0288F4F31954B0C80ED81789FFCD32A4A23FCC59A988AD53BDE34EEF1822BFF493A0817E33D5837AF6FCD1C41D3D261195F5DEE015A314E4A151AB79932EC376FDD8DB730BB503B30DA637932D749F0A5CDF8482FA2B9E5EF2547EF26F4990BE90AD6035A32FF5874D3C38D56F080F957D71C1412F7456F2D8695C05471A13281D7DF5F63F58359511E381BAA626EE03B261748FC2A721182CF4D6A4FA5825F7C71464A472E10221D385D601E42253D6C71A5AD45AF361AAA1C3A8823D0FDBF488CEA93BE44460A27F7BCD7363F6E7B81DDDD45A580C78B00E4DBFF76A60FBB82D06A43132E591239DAFAA8CBFEB5674731E23904659D2546DB24A97E52474DC943F7500E88E9CB068782D5064568597E268F84F575F8E28D5E009A54E91BA8BCEBA2965690C6024CC80337799171152D0A6391960479FC9DB85A3F1AEF40A6F036440AF5510DD6F5390744529E28830EDCD3FC7EDFA51F8638A0599963A2679FA9384BF581CDB3C8273F61D8AC126BA00642C9CB7E683DD53FADBA9C5EDF337CB05859D401992C0D26DCB8FC715D553A1C3869BD097CDCF8865067436980091789A52C5E8EF825755B7DEB94859576F4B4BD5C13491A9F8C5B2AA196F17CCCF04736E82F30E5A1C620B69C4466214D455BF74F7A7574A6615686126EEF03434BC7FA9AD446B190B15EA99704DCD2F470C73FE64CCA2CBC7B12F0B5170E7E7FECD5A4047318F61C78D40F351307D59192643B031B65266210213A180D8210AE19519A291C1E3EA7125A2661CDF0BB3C8B9740C0AD325D051EFDD968E97075209F67AFB6C544997BFC35BD7B1F0B5FD075E3078317492817877DCC202D3490E2FFDC935C6AD29B2E862C2AEDFF4DC745CA610AD712B01ABDF913969E11F3C570041CEB127D724B7EF1C12A18347B4A98FBDE8F81038ADB0768E57613922349DB2E4DAE0F23D77B312522D659DEF639297F88BC532CF3C2283F65B01735324DF49168EC521B670ECEFF6DA3E6E98BAB610DC2269C8FEB462B7B080318B3A40EE754F34746B2D7C53A37D4065F7C74BEED20B1FCE986FFEC29FC3FC5187045F9E1A72A5B7CE36F2739C6FBB027B3509F4EF1D1D4ED6951AD81DD940EA264D763104A5FE4BE89616FF7C722DE946555623A11D486A0F7421BF32F11590202CD0F9C84392B2B1E7EFFD09575E0F1F380EB5B1EF4779E7178D017D4395D814C62CFF5500719CB1C7CCE6166AB2BC04FD8FFCF68FF4E06261BD8833B93DAA10060B1D16EE9D15E69DBA3BE34E73EA655A8A64AD792B4AAFCBCFA7BCAA3EB98B7D4E57278D30AA498B5E8D5A317E248C5F07203DC49111DB6BA56D91AB61C46E46770F70402AB6BC343A4372A60B72415BA6A351608CEE55E2B96C66DE1C9A9A035EA9434171B305325943F8A0284AE2706AE290A5F6CBD24880241E9D3261D2FDA80AB0B63F09D068D7EEBD86F2700B3804DA855599A6352EAC4225266D7B6874F5D1F9CAD96CC3EEEF454D3FCF4E1B73FA2DED25490492511FE56A776F52B76BE6ABC84D3E9B45C4A74FF183C0486CC9535AA93212547FF0ADC44381D8A8FFEA5FD1BB8E2461EADEE870EDC3B5676BDA2F31C6151BE5FC1FDBC03E421942588A4EA6347B0848B23BAAD972A3DD5B5C25E84AD7C464636455A6326E817202E3ED378A79D1930AD65F8F9E4A828C0B30779E48F35422FE324A16437AC9B43F4F54477BDB380E986212DAA160B9AAB8266A156311DA0373C56AAB3F0599C1B052B1237BD999784145666B1BB0D79BA433545DC3FA1917FA2DAFD061CA23D01CAF5995BE09EEF2C36164117DF2BC65B99DC8D7B866FCC86B505CA41726AC6A69C5C3CFC3CE97BA0C452BF0E78532C459988E682DEEA1697C83CFF3600E2CCB662B2A66F58E9EF30D6EE35EAE1024F02244413DB5016EEAADE04AD2090BBB676B9AA06852C364769F69ECCEBF72759666E66C9F0FC2E9A1D7C19E6BC1B12ED65D501C6581DD7ACA80DDC519EA9EBD61F1B1DDA17B4CCC2DCE198BAFF690A442B5BCF7A7640CC36C2987D8932548CEAD5658EAC905940BBF9DC7E09B39275D3A26EFE90E01844DC9B3AF9B7493067A19068AD192C5A8DCB19A86D925053D7280DAD577B5B23832DB9E5DEC6D20B4A4DE632BF8E09F7267F46F7F0FDC0E4965423B603756FBF04574D27207E75992360754F063D3188C0A510D375A71B873D6451C5FCDEC73C29B2B9EA8219D1E6FA25416AECA6BB8D1DD2404C9F3C030EC9F58CE0F419705569E86BB52950A57BF56EF7378238F94A8D5BDF707CF55BD5523D230871F7449821B4001BE074140E45F69B90C0AAA844A846617C30701FC6BF7981A3EA4E0032E3DD608BB616B407BC4F9FAD03C56CEE8C8E977F137BBAD095AACEF0A6EAA27C708BD6C45C4779E5804371021DD1D0E9F620AC22F403256AF4F534248D09580EA51A1204EE89BAEB4F0472CC731655CC8519982673ED789FF642D561D253FA34196E233EDD5E6B43AB416D4C2AC529CFD9DF3E50A40EEC7CA16BD679CE18C72DF71D171BE60FAF8991935318800D5D10E763D84E401FAF4E44F54AC08993C3A117847B5AA366F2BB6AF7AA842F8A50B47FC035515813A65D7D17A35CA04EED0596404EBE592EDA202D1D80E82C6F9DE027D3BD5710935D5EE9D36849A661E534FC2970AF910CFD50381664F9B436CD73D9BBF8D9BE5BE3254664DAE6BD25F40F9252BC2E04BB995E910336A6B3B0583C967BE189876AD11CF7B9883F7315BA9D70796363F403B7EF69E2D46D4B19552B734E1364330339588ABF050701FA72BDFE219A3513CA0851E5766FDEF4C442DE62BC0842394911E5FE7DA0F407FF81DC2CBDBE042EF93659AC6285F842EF3A655BA2ED143415021F1CE6EE36EB184035E54CFE3028DB083181A8C838AD883C6ED58D4F984397B0380D77C4F41C959BE60290C35996CF6AFC4645A8C54635ACD60D5B17D41F893DBDEC9412CC79A8A9C7F25DB88C81CA29B17D22C01004CF9D33497590696FAEC2F6EF6909A34EBB8E6F52901DBCC033BE7C92239A89EE2A99F4A10D3BA09A3849761D3D145A913F73BB6DCADFD7904AF25529068C528853CA55848BF15BC5C0B959F432A5DE5C789E7FB8842B26189A69CF7C7B9AD0A3A64DEEEF8B753A1F4C6654FF6A7AD031E9AB9AB79D4CC7F34B62BEA3F44482B53F99B11FDAEF1D120EC3281FB2A2C0AE8E67088A94137C3BD678E6DB147E364ED4502340B6809DC4B74FB9BD27898A3696E2693B11916A2EDD71BDACF76B506C44A348F6C84A522D9043E6933F615F6EA87CEFA589540FEE6D1D83C03EC760AC46ACBCD657694C321798432780A2324040E9896918D9620D80064824E561D72CE10E244A8519DC921326882410433302CC70F6C387637C3CEF3B452753E7C0A3754C4A495FD41A13BF4CCE1679B246A8E6F017DC8C0857C248B0ED04C4162DFB1D22725F8257A8B2762518CE4B0AB26AC433B008378F15BC0D629C8722AEAD8EC6E9056C68451D7B8FFC0639627E5EDFA864984846E075317623D4F4048A5B026FB8069C32B80370667E17EDA1D61192952094742A0B8CB09FF936E14A0D4D62C524580EA27395AE103030807CC835D28807427B5AA34172A41EB846F02C35328F3653090E5A8E8F9AA84BA1849E10DEE2F71EC931B71695F94A53512FAD226A59CD0EE617EB8037E0D976986F6532E776D586ADF1C3016C3C05A52FF0085E49FA19CDBF8E6DFAC6B4CF9DDBECD2F408BBBE3E907D25E38E57BB0760881716A42BED1E34D762F7CFD63EB314D73C37EB33D95F9B4B34B06AB5117F06CF985013E307169674B24D5CBEB25E26F8FF2F32948E9071F73A30A44B6A0869679D8EBFC035C00FBD336E96E0FF9AB8D0A83807D35218DCDC946FEBDABFC80A4A38DDF77A7EC8AE5E2204D42A599F13246F43C6E90172068D31BACC9162378D241AC62908B5151140B347B915414A9D0E5B0ECE32C8D6983FF67DEC6954E6F27E1692EB0316789FC6D1728EE0868BDB6EB1EC19B7B867D015D2E87A95D95E0A2D0BF0824762FE4246A59979962A3163470463926CD8A7E566F65E8651BC1631560FDFAE0F3A1C4CE8C8B5C664C1390C5EC56FEEA7A6CFBA7B3B2DFE40E6B874B7144C150D8C783F10F4B640AA9D44AF66457A4296D58E17757C9D81C90030A41C314B82AFE4957DA75DC06C1B5EE1F68909370C28C001B7B69AB9FB77AC25B5D7A30A57126A84BF33BAA957F7D544B3FED7A9748371F05947865CA975A47FE7CD9673C84FAF054749D3A9E731B923BBECAFD4CE9A9EBB9CC837E3A0B798213253ED9D6F3C479A4C908AC58B399193DF64D62FFBBC743E53583945802B183C76C660C18445AFB4F097F8F560E5A0C50D29C7C75F6C0D6BC772C78ADAE3E59B243D09833D0430EF164F226711170A4ED6AB210706DB6F3CA846B26D25040E713C7D3ED10376A340484239B1DAD6931819CC8C66D0ABE0FF998069592EE48C0DEA991E9B98DBB9C2D245C198756EA6CCD539B48F3AAEACAD22B193055DF72CEF2CD43F9065A52F41FA76EE2CFBDE793059ADAC77E29B03DF01AAFBB0B68441584DFFA14DF10123604BBF2BA72AB9F7EDEA199AB122A4B37094814D63578592C84B0FBEEE7ECCE15D60481E9AFC6BC950EBE82DE05D8E58D231E1F015F113A19DBAF8483E2DF2F316F2F776AB59681C8E85F7CFEF7CD154E49F91C9956A9C1CA4C6939C4B2D3AADFC83FBCB202338F5C57A2ADEC47AC5DF4113E1060CA307926D0F2B0622ABAF239B1F101AFC1292BD4E829066F1C5E32F39E5D5D59B015E97A4E00B8520DE012F879E5ED5946CA734E7E27DFE3076B5367FA403EE51B711B1723151EBFE363E4742AAAA986CCCF2F609E8EA290BF33DA98F65D854B4AC1F1590F99B6771D16B664C0858D377F9D04A8ECB9F9C50F4A9A47A1A37EC63FF02D2ADE2A2C286549B4A5825AAD883E70E2A9EF8ED50CCA59B88833032BCDE4880B804B5A24B8FD8F0AC2A2577C7E2A0B44D0A912AFDF1D4DA4713895E1B52AADEFEFCBC091893316A8D1543D755764224C40D3BA3BF1DB699E74731FEABBAA63ADDCE1D69561480156EA286528C60D5BA5DC079CE442991B2038E7266D11B8FF6F54A9BE03CA2E92A86DD8DF8C2228215B7D53044D4A0C9E5C830F5A3B1FCBC0C93C05460EA272FD8EE093F104CC9F14FC7CF8B3653D5A58494F8314D126DBC38BE74F1483F53668B29DBC77B429F79F7106CD944A6AE3B997FC43470737DB77048EA78D77B56790FB608F8036FD39E10FCB2EC0EA960F74D83DD11596125CC5AB32E29CDDC01BCA3AB199D64D3CC7DBF1E5ACC521846F6D3FB8D298DDB651BE0F744C9DB80821E56542D2F63A5B362AD620727D621A10E4C0B7196ADBD68D3A0A825F09DDFB7E9AB498B7E17C7C3E4B27AF93BA523273112BFFAB9E390F49088525B065FCD322A7D1782700459370D8E5E421960835DAECC0345062363F818A8BC31A40C94B5B7770C3172F4A5870D143E0FCC9692C43C40488DD501A4BB8A449F78E52B8226AFF227E959199BF3ED15A44CAB4D3044E13B0D35D81DC8AED7607CC52AED21A835916A26F7984AB7C53DC1C8689E24EFD2435FBCD7D8199FA293885CE82B611E574871C8444E0E557A3AF6104466A504DFD58DBD73B2256F390950BAFFFD4E008169E8A76A66E0F3AA0A139EC1DA187D675D9447791E2142DAF3AE10B011D263B64043A393E4CF31FB49092BF5AF2027421AAA4E18946DA6F87D3A090BAA4F6AB3BBFA6A751D45A7DE40AAA80E9AFDA04DA9CAAC3E13B2F6B405371EB3215287A060321D2DC955C243BE01C579A43FF4F45E387D9DE4CDC07D5A80A46CBC06803892E8067E9372579BF96940DD3DBFB9855256231A15F261144D16E4FF5672CF0F2DFBAE027C5A8E3BB885CD5955BD844BCCFA163011692F39A563012083E621076EA84257CFDF8037575C29FA6C04B38DFB257BF8E1BFBF763C624AE2CA849EEDED39A06C0162A8398D782DD63A4590D576992B3F011E9B2BB07EECF28CEA6B34FA2546BF80E2CA1966BEF54AB07C61B75AB1F80520EC83D7F825915663E1C48E1729947AFE93E679AF67B5C5BAEDA2DFA06E1D1AAB4EC1121E2B60ADC00DD0AE6B293B8ACB074DED7D09E5E125991CA11E0FCCB9F0AB7FB385EF7A3A849E6171597D6CFDF0057DE129437D3A9AE924461257EF0F4F9F005A69A4CF171E6D539CFD54D7F929C521055C9ABE83C8ABB05633ED77043079384C00F68EC6BCD286D8C5419E56AD93658A55024306240BA4534B7EC76E1FA3105FAF8CD5EC8ACC85A024FA6CBF5FE4799B598C28CAACFA8FF8107CD09EB9A3CDF50FA21BF6690823CCF255B0C4FC362B7E7ADDFDD3741A66341A1386A51261FCDE0CCAD850D5B351F4E6C39671C350CECEF2509CE77D228AF7C42DA69078C300AA7EE3E18035F753F01CCEC22A973958646686B85DD40FCCA943C126F702BF95FB569942BF988AB25F20E048E94A93EF69BBD50C140AFA0EF59A59720B4F1967BC6FC5C0FB45A94E93917F38EC5A23D6C5329E43152271B390180F42D6996AD1138397F09604804FE9949FD1A963370A8FD08AE45B4A0CA097B8C658D067C568C5DE0A475E06DB8772F619BBCAC9F25AA8E5C51C4C6F96BC58BB186A61FE47594A4083E9067EE117222B0364B38C1BE2A48C0C715849A52325487A77BAD8D6E96C1EA2D6192980A8A11CF82B36896BABC60D5DA4575353C044A37EA1DA2C4B36D80EA6617E35229A12EE8BF44286DB6AA957D87DFAA50FCC33E648B29510458A454DAB4031144ACA06E5BF36ADD04713B98E68E5F103A3BC7EDB905490E7860DD8D0F0E124E720B392F7EFF14823579ABA52C06BE9C9254446EFC31717EBFA7D8E01ABDEA0299A4E1D7642C7BB9E3B6A40454AB3565071F57AEA8F4D7F108C6AAF89393189043FF60EFE48B246B9BB7A213BE0D0B3421F01AF6401CEB367BCD3EAFA040C599E485F6319FC58FD248C20286DD793A69FF30EF8CEF831886647F18808D96019F9685958998E91B62439DA22484F0D64C7176F51D184024CB05977F7963435BA94AD7DBFB8BA29540AD2F1AFE888B32467C392D9D34409D0F92B2D97C32E8253870B831BD8E5148086CE21CD0F6F6A31213A724ACAC30AB027D5071B884BF357C2848A7E35904B6ACC66924B21AFBE7E61778B4BE32FD3B6976515095F2A83C4B09299D6CC46E0E83CE97E226B582D81280E95F39757069B18BD43514C1C1FBB8FC0285F10754D25DE831AD62FAFC3F55759500D72FA18F78D6FD1F937F5D466D45F3B987B7323DF950861F696945532324F073E29F00823A174B7A5EDD8BE549D9C9CD103B6F78C50AFDE97DC2371AF4684267399A688BDC46AF49AA5D40FFCCD07414BB35FB2AFE06EE4B551C817704CC6EA9B3791328F454AB4AD71BD0BE0B5C1DDF979DEF4FB4ABFC55007BB3D7DD832433475E967FC6E9596D668F16EBD9D12215EA0985DCEC3ED374740ABE2C744748104DC4C8582E965FA4232A1346D973950D0FE80F0DC9018CFB49C73A1B0F7304C4850047CA19CCC911BBF8BC51227CDA4723FA2E5D0D1EC6D5846590CE00B17C2B2CFEEE53B62F6A37C002B91498585705CB0FD41BBD18FD0A2E33EDCAA1ADCB638D717CD3521E4DADA8E9E4DE341844582B6AB3ECEB167876A3E7E2E6987CB32A24C9BA3D195C6DE1475E2AD212453E494547C8C87F73AE7DED2D745B24C163CE46E60C054892406CC3A5BEB174F1343F87F389488E9500418A2E150597C83AB3DD9B78AB85580CE99B303725BA73702A4AAF148D45A58C2A5D823B716699E6E07AE90BFEAE45221AA21527F810389839868AA3DCA4CA44601B5BA1FABDC7458E5B29B87A00F670EC7E9071F9A9D7E93FD10796A9F2C624D9DCF3250E198A52DF89C5423107BAA3A8FC022C3FAD5E2BFBEB9CB1874E8B853782676687F21B1F8C722ED674B6F4BC52800338BDD9AA701022D1C38FCF2E6C7159C8F58FE6356C6C9CBEE08052E8B519455199137FE170CB1870EC9B91A207DDB0E8D563144D2CADFAE66EC07BB3162CF4DD82D3AC44C4DBD962854CDDEA773272C3157DE11595FDD2CA73BA9D383C78297DDC405DC941180DF6B10630A1D589E0351B889274DE696DDBD797315EFE92C6C851A772A715C72B795B99A4950EA6AEB91E07FBC2DB4E0EE867E0B43227FA836A48B1D5F81254C2E47532FB3AE3B4271D1070D1DB9C275A7FEEE7286F0316820CD1E02BD81579EB7711B69A36CB888FADF1A83D4A3994B55F52118DD0F56A2A9AAE9F8CBF9B4868EA5023BEB9965E3A5C0A0EC33722A3C8FAFE7DF667675A938C31D82ABC33C3421DD6DE328AE76D7533FDF68018001BF2E3645A7A1DC43C7CC2BB69C483308A8A2C48BEFE055BA7241FE864F9C9EF4090C9F7726348FFF09BE67835E1D20CBE3286596E5EB813B21D2CC3BCAAF7C575E25B806EED8D056EA8EC1D9DCD54F31FE937C7C44C7CED50A6CE824AE4FDA9A422942D7D59BD091E88DA206B4733BE0F7A70BC41E31F5EF4B0508D7745206FDFE6AA43FFD7F109686F087BA9EB60CF4A233E92D0D87C1D67785DA047EE7545A8D5F1091D583568283A364E43FD5FC1078FF6C307764BB69E48A20AE27940F13E57E63D2D6B52DE383C76FD6A914D26DB8EF8360A1386316A2CC5FAFC0D22127F51DD3E6FD38F13898B135BB5322B13186F0D5FB65559B08FFC593DAFA08500FDAB390E871A22F62C21BE65B9096A09EE1D1AEE6E4E6AA0A5891DAFB1FC6B30DFD8B093B69A69A94E8144A23B92433660338F5A84DBA5A9EE503D49CF421359FF51A04BEDBFDF1F7694F16FC6D99AF7AD33BC71E170E8C7673D333D137D561F282272EAA645536004E9589396F5F65CD314793FAF0244352AC13D982FB8AB76003E09DC22BA0BB05E036251B4D7D7EC90EE0CBB4AD452E36ADF92C7B3780ACC49FD9CF1229772A4A42B6A36D4A80435BEB3854A43023395103115DA9216CB91329F80D593DCAA64293B1F5ADE70B242B93A699AA5C304AF88337A4B43C3937824A35149713B964FC65EA90A4BAEE15EF8E82D25F21D856E524B3B3424D4FA0DDD193C1462D608F2795DDA51CC8B4E99F5E5663190988DFDE9B757B76A25B6D9CB8C295D45F6F7D4E2CD342F14B2E323D5A8A9B5C8FCD6BD9357894BF568639919525D881BDE982202B1E36F6A46F2232D79419A2EB0815C597CB7BF3832EC8DECBC8CF1E1918CD5E60E19F94EA62655313B76B4C6FB1244D35D20162D5EBC2738CEADA91501CC220866209E173AE04A3AE9176524E11B0D8FE5C0FDA8041D757A87316A595A49B654DE2A9CA6754FE7D62CEF119CA3B820E4EB1033CD44D0EE135CA8E94AFEED088CE741ACD4D5DF36DFA531EAA43EBCA24AF286F6647BABDA02A343F80DDF3DD73CAFA12D42B89CA488CA43221DEB402EBDF27376A79FBCE6BC5FD98B75609E7510DE31BB9FDC57AA70D5F66801380AD3E2E1EEBFDFFDD34B8A4A3A7C56316205D42072C6E8B387F6307609A2E67EEEE18AA8E7A7CF1A8F546126EB3E3BB1586F42522EB802B537369EAD19D33961E1870B7141458BE5C3008015ACF3FA031566DD52CF3587FAE1A5178E6C69D162D51ADA9010F83C80C4ECB8FEED1D0FDFCD415F6B72E4E7DCB09D6D4567117FC914207DE1DDD42995B17D7D150456BD288607415293712C5DEFC5D99F82B7C44346AC24A3B773CBB6362DD3440409CFFDA51D6F5109C4936D248DB03F8D4C616BD01141306462C790FA7F46EC5BD4D8EE304DAB8A00158A60DD120D456078270F60757CA786DBEE329EDD3149219A6ABDCDF16D79E921606862B00447AB33AFC710698F09E307905BE4C2B6B6BF939FAFF6E1C867742B21620BE2519A22F1F838E756369FF533C5273D515921F43F5DFF3FA8EA5D75436A73BF6617768F677DCD63F2E362F4F2C1DEC07FC70E0893998CEBBDFBF7ABB1B7048DF8C706BA1C2FF489D2C4510EF35560EA081BE64FBCDC8C1E271699D41C1EB8EA5E24850597759ACE2EC92F97A0D3A1DFF62197A63C48136566229855F0C567A9B7B5163E5D6F4F166164ED390362E09AD84BD4D03FFF8998D6593B01EA6A2DDE2473DD5D40DA5D91192F2977DF3259C6F1AF9173DF20FC8BD9973D52ADAB207E0D573153C49F3C26266CE5E4393C7BDBAC1454001FC710F7307E2BB11DBCD922E3FA5F9478E2966398EE6B32823E0B005A52C1C9401BA4A37A5507D7D970171D3ED2625D7BBC503113D4984E2E644DF576CB64C692AA1770D4642C4C5625E387F2317B2EECA2A63D60CAE4394845E781627B189E470252E99FEF6615A93442E20B0A5C779DE975944400617087D0EA7AA07860C0B6D7AC1AE906DE6303D69F8E686D1A79F01C61B74EEEF28BD3EDAE259A0F5F2814F0A776E277F0A8EBAC4FB270E352EA590ACE339567711AA9BC9615B52ABB3A8BBE64DF05BED8852883FF064E95EBFB7A947B1EB04D54FF7E9E1EE7DCC854F07DFF2A7C4DD1B10DA977B0E22FD698D08A13E80E202C828739F6D49130C2CBB6480D9F07A6E37A373EB2433BA2CE29507EA8B0C709221ED76467D0510030EFB797C80B5CC369D33430811701F84258A0ADF6BDD22BD57A60B6B4A855ABCFF98141357E582734DFB181BEDF2475E29B78EF3A40735EA81FD74BCC7A6121A50728E873CC23D7419CC7AF4208CA1E8F97EF18A1EE148CBE7EFD03E2A661C05325C27245BA90954476917ADA95C1906AB7727DBC743E8355EBE1EBE225B2C6BCD6FB3C2CE62C3414458E925D067F8B2099325B7D43504EAD734B43B3DA8DED3232486CD368727E9E02961D22F925746E5D5C9C72292E3FA9C32D27A7FEBCD6FC7AFBD1FF4A0AD433D3A47E624D38B37B3BF9D8327C847A9DA23609CE8E2ED8A81C7FBC7EC516E5FA58186EF33A879743C78A7D0156128E5D0D6728A1E02B6EACBF110C3CD9DA6CA3FD63C8625DB1D7B5C8C4937C75326227209EE77143C8790272642041081A40B90F5FC88E9CE376AD964029F1A90EEF01F99ED8E65A8A82823C7218E909E80C8CE7785E13D42653347F6EA6F50342BAA60601C08E1F69C50FD4EA6DE8DDB259623B14C7F9229C73334582FA42F2CB27E581E36D3FB5AABB7D25DC88822AEC75B7F5A164C9E97777325969E760A939B9940CEE44ADB40F1C06D4F4B134F8AEDB57B7D9B73898AAF289AFC632923548F44AB5009CC11DB925D39C0D6339E840A45F09F7D37AAF2CDF72450E9FD3257B815D04199FAC1792E272656296519C4268C8D546D001D7379DB81C847F7E076B4E7CD4051D23C7CCB14E5909B9067FDE4EB751C464B9849E3010800BD2E86CC660A366F164371C1C2091BD42F20CC7B5B6E60CFF8EC9B3EDD2FC3C0819B323897EF5173892742B8C428D16C6A32FD4E7CD6FD8FBC0EAEB2259630564946478BA938A8E7B14BC2AA7719B71F9A711F22FDD4552AB8CB121A9F7FD979DD055939754666B8C16377B5B76D759690670620ADD831B2A2C6133C792975AD5F11190897C127A2A67BAE227B1960CF135A6A4FD375FC3CFAF69D7FD835DC6BF379B73F9C00C4E29D555D8FA7599880CBF1619F720E740A043B5DF52DA3341A052425CE33CCE7309F7FDB5DAAA51A024B350E81A5702734C65246BCC2781C46C66655D1A91E9B0A382F06DE23EC7481AD17F32C67CB0AC13F0E6C5A566C7CA5FF6439A01451EC3E7D5398668230443729435211B8907C339B9F4BE9BC0F5FAF74AEDE6955DFD613CC9A8D9737CC40C2892BF1B44F90CA055B99315A42072478A788B30675779E0FBF39B40BB7D0513EDC1E64345E847B463E4E5C21617122A604F19A7F0F12AF51DA4D2ABE08892BAAA9E5A2BD087CECA624CC6EB22324EF04EE5763D5BDA58055D4F6C2E5B884F09D7B019851047501BEC75400BF09A1FAF64A8055188044FABD9FA05CADAF4E13AC40254C78CA5C38543B22CD71D12122E3F8D2B1C24D69A21C5D051246AC21DD7DFED13920E3BCA39C7B9E66E580BF0463C61D343B62E0EBE8DCC6B2BD31BF6905DFE8A2624F5EA905855E7B992CE52C0BA1C7D76CCFA05C67FE7452F225D031A2583F64AABD1D57AC3C2A9F80AA5C2825F8A9342DFA385A66B4B60A8A71DA2A95800F264AD2CF13E9AF5AC8B2CCB82A40FF0C3CB7F44470B0FCDB318D9F3DC702FCDD6D77A62222234EB86E1692C33D3F8B487B63E91CA0403BB7A936E7BF7135FE7E008C6A54A1B7FFD512A3903ED1E4ACE8F726913336EFFE449F79781C1BA36F01231FED3982E160F61C8AAF63335F5E224A2A901491408674435D3C8DD9DB4D3E6BBED29F9F1948BFB6E2CA19858422860FD06D0A6CA7DA0E99CA7263BBC4AF9CCF227E53C6E8B973C7E6BB51FCC41DCEB0CDE626FA5DBD128F79ECD4EFAD1C44FB4524390873364B81E32FE7F670D14516D90B7BB7F6408BB407D941025C25491CE586BE45E5F1352C8677D3CCB0C08CA84FE0030E6401A83948B23D9BA3C5CF5AFEB7304C536B0203B6651F574BABF2F3AEFEFF0A53E16C747C179E199129564535B8856D3E84A3794DE25EF57B7F0BC7DEA8D803D4688B7CCB99F0BF8543C8982EA1DA3DF49EF99BC6EB8CE5CE4CA6D07A3315549ED31068F6C866E2F029DE527D3FDBDF86E93F3119FA602BF6674E4FBA81C507512AA8A08605088B95F6C13546EFBDC03B2E58008B4C611FFD739D9CD467B695D300B1CA15F3CC0C3AC3B4FBB813AEF63F70341AC73F0DA812FD378D390C3A5E42FBE5343E0507F5736FCE76FF809AC2378BF7BDBD3A7D21D1ECA9FC91DB6B04219E506ABC157B23FCC12847BA2E7115AFC086A973B4A60BE117A2A47F082CABAB27F13210494E0F880B535748583900737306E671874EAA6F73876CA26FACA628E3D82D7664B2EEE460A843E41B27374C1C6F75E280F52B786AA4D8D9C187E65943803A7F37C20989DFA8D3077FD7CDE3CC7F93704FE4F173FDDB47C132398DF1D1135678E4BA11F7A5E827952A50B1B50D036638D4145D1A23F67662483F0C042CE4B20FF7B4C03BB6F73CD4B52D2E3A36D0D53B3CB0BF6E9D5D3387CE851170628E39C9F264B23F456CF78E0DBB91301F234A6B0CDB7C8227949858D51AE6FF77FABFD7EA66489F640899BCD195306B23BEA0D5C83FDECE8695C2F5BA2B1FB61720B2AB4D2164046E84195A69AF2DC9A6DC1457A492D6049E28CFB3E17D044199AA4BB46870DBA026108BC0874BC1E9EF93306581BEE9381A17D71D3242B7F149BA57ED9C96307B4324A85BC6A9D3B23981237203D7F9D68DC5AFF6D00BD4FCBEF8D2E3BF46702BCDC7521F97E7B0CE33A9432AE0A3C7D8AF6B662744B4B5E116D98D7F7A6626E4FE04A89D8DE37255FDA1676923F4D8B94575E3061AB9E449A795F4E9BEADF35614AD10E8B8789F31DFEDA0E0A5BFAD206E45F4AC0E3FF71D5646D37188B33040177BAF8ED1C30EDF405D6DE49CE173B2EA3CF94369C79D6F5C33482CB1D904A60A78FC5B17B3AAB862FFBAF121D47334602541549E21943B52812542A29D2987D30DD486B63B96FC68BB92F995FAAE586279761A6FB8F483EE6342014E507BA2BB001273BC0308D7685CA6D2471DD673B1F836A661D390BEE5115E9837D545179C68B2C3D933E5E5E42FEE52558562B71A40F6F6F11802827B7F4BDDC06BE825ED6A591D02DA4E93E6ADEE8880FC0C79125FF5952B2A85C7D8AC39E3D6EA39697FBA7BBE4FCF27F56D03AACB2C2D6C9232C6A5F035E7B4533DD9A53FE48B4249B48D8AD639B56499A1BD8378131695685729B4C679CA6695565856EEA89F3022C81CE1B026A4C3ED1A13F13F410A5DAFDAFDCD9393D460E60112AB4B24BB70994930A8C1F04592947D80F4D01D88C59771B73BEF5653B828B180A70A1178C34D46FE8B54354335943A497F7932DD642A399362DA8CE7FC146E60FE1F9D70F0281ED6775A73F30830908ABA6926BB55210407AA92630F6A1FE2360E4B101C2D29FF83B60472761CA5D1E502192ADB96D24737D984D63DC152D2034D48DCC9D5A56FA8D7792CE80C00842C0467CA2346EC46C8F07254F7385EABEF43DC472E0AD65F9DC51FD50D9D767860CA353C536C840EF9C7DCD5BFB69CBEA4469A18F3C8FC2F1FAD014EE46837DEBAEE52F6833C981A6690BA35ADB85A4DA8A3BEEB7407DB6FE7BAA932242F82F14391234A63ACD4B82C763E2C4A62E0FA3AC73F766E720278F97F25A4A82175454CFA0AB5473BEF6D574D77F2502B8BB944CAFA0E1947496A68F54EF1959665A94B97A15B22821C8479195BDD9D200D45F4642110FC10C866BE236CF78278DAE1F6575CD78727DDD0641066034DEBE47780693A5F50846CE9A71D2812D7A46475DEDC9F7E54B8BC0DFBEC8F5B2B00FB41DE8287BE24C6D0A833803E50FC516EF2FA8AAD7EE61E5558035F8D138FF70EA038D5832188E5C9EF55C1B7105734BCB63B2A34A44C88850D863706C15D24E2F625D15DA7B5C9318359FB7A070B7EAD30B8150749074E7ED8FE7DE6A92F7933F0C020C2C9B392D8802226CB88A9A7FC6D2921181653A5FEDBC82040F0B05B597EFFEC4BC1188349A6328FF9A2548F80AC723A2D7393444C4AA205D9139970AA36007FF4307B30587DC769EDFEDF5CF90AD41106804191A67FBC76BCB2C1B06BCC1565A21B19685384824B73C985CE7AE672A5D13819BB7C09E44F5134B1FC93C03A9B08AD1C67BA57DC4396BF978E91248477C462A813587142B6444C2AD17B8642A093FD9CC79FA558131F6F1BE29B57277CBAC5ED6EC7FC1C9767CB45A89F928155A65D3838EFABBB438CE3CE1E50291D76A1A8AF8ED44D19C675000C945C37014A5CDD38D5744FA2BFCD8E4930E9B8D2587949C79BCE85B8E26A2DBD6DC9D585CCDCDAD543C226AD738D5FFE5CC53A17A40355BC28366AA570E54EFC3A258067D8AE5D759B329F1AB1D92A7135C12DD8807D755B2BDEAF7251E573FA5A3762B9BB77B5ACD87DE391C2CF304B24B9694B6233B811B40CB0C3AF073F4C89C483C0425D2625170F89C7CD77AE12D243230AA2050927781E6E43CBC6006D1D9AACBB9532955B18D67B5925FB31AE82D89C94B0962418CFF0D6785A1A80BC02E150512535A99FA8EBD86D2A21D916BE1E219FB39ACA65CFBB78A5D954F9FEE9209C93FF62B0A387A7CC5BD657E5454151E793D967F96E981DBAC4F5565DC51FB82DF44F6ACC28B51EC067AE0A01902E45ECCE2AE3C8B638CC0C02F13E9AD4927C32D48C7C34BCBB1BA7BA9D85842B48F8720890ABC8E497D2D061185E40406A72BC9EA328EDD0A4889D8EC0D8BC7483661065CAC93027A93BA88D832E339D63C72CE7313A72F101597CF484931E9788904117E650E154BE3D204DAD803C0B577E8B6E89A0EAFD74AFF2685B4574092BE54F3788097D3AFAD218B1804043E114C8E194514BD2A52C91227F03D82335D696A4312C5FBD0E43C6FB8D4451A01C4F0495DCA60CF3E7361FA7D3477738FDC4C062EFFD03EB04C1A0BAD899C1CDF5B25C2227FF915C1023CAEE43644B7552EA6926EF55C5EDC37FCD07C0802E508E319E6D962FC96299ADC42ED49F647DF3AE007353A56E273F70DC49E40177151B2846B86EC632D34E4F7503C171C9E930DB02C20B144CBB70F0A89FB71D1A6F2797296F069D104FB68D049C82C8AA36D4A26780F3DA2FC6E3DF20936BE0378CBE27A1930C9E3599C81A6B7F2740E76C8A99947ACFD0EC0DC6CDC8CE3570961584EF3F005FCB9526C7513A2BB81CB290BFA819E3CE6A01646932957655B8F2E6EF6BC04C4F58B2DCB23BE578AFA45FC397928A7CBEE76384291A86B2D81D1F5884D53BD78392F95D1357DDEEF6CF992F36A98E8F9C4963EA877F69AA0E1C70B9977A3D338D38897BA1EC9FD27A4A3FA16055D71C151D7C10B18C6F36630036BEE358595B4151FA5EC045E66D440A5058FE215661F73BABA1CC756DB069A9667AC348CCE0AE8C8BE25D8557132128E0657B59F7C3B2E81B5DA0ED99BCB4653D4BB60499F12B827536D92FB528C15BCBA86A51D8FC0F91EBD6EE8B7C2F1BDAA46AF3702C1ED630F609EEFD3E24702F9D4A1BD079780C54903780F820C5F61841C6EAEA8CFDB63E831E23937D2265D4DBC2C4306D5BDD7726AC3C87F0D12117EA03793B2ED5E2ACF856B0246C38391D89B3913B6A28EF98A620C62BB2A5C89007DA7065C832E956EBF775434662604C4BD03AEB7850A97023603225FE6348F88C194CDDD963F23635E13C8C23C580EBC9410CECBEA02628129DB8DB79939AEE9A0BC40BC386349BDBB043899B81438B53FF8AAB731CE2DE5FD8D167FD29AD318CEC8FE8D76FCA8E13B1821ECD874767B900DF81F67B06CE14D2ED382FAE0B1FD11E8FBAB62027847051D463278CF582B00FB33F3A8A0D2DEB477554BABF90F274F31A0EBECAEF0CC83FAD196633DE90169D9CD7C9E871E689F4C6AAF85D22ACC5EB9F7C0C6F73CB6859907950F2B851B654202A5BDF6F6671E094ABFBF9B150AF66DADDA8FAB5DA5816B94C3EAD3B9D8AF8DF45FD22624A2D5E6391A7F41152BF82EB221D33D646B3B30EC182FD42056711E7472CED9B80DD1046F156B064D7BC134B661707B994BA0C32A976F5AF772DA9815F3D31B8CCE264F39FCAB556A4C1E7B069210AEABB178EF594CE333DEE707E3B8D03F776C282C5F5BF4C7BB544AA19BDA323BECB1542B6B1FF47EB5CA17FA5D91817B91E5891F46FFC9ACE2787ED18FEC4CB5D18BBCD078EFF0F8A4E4DA87F824D2B2D3BB1C0FB530D2F5EC0BE21A226FC9FC6C5CF1BB5B2D20DB6D1A1D9C5BAEF1143FF57F035CAC4B4AF0B5CCA7B183E1A01F0651BD2176BCB98835C8C7A58A7B64046A78349AF0F6FD96EB0983915ACE766348CA372E3A31537D1D077BB9CDB4B0D64BC1EAE344B0048274E51402352A82813A9ABC37AB287686F37E3491B66D28F5FC52003D03318888C3DB784692669FA0500FA3870C80E9F48028B812BFEB54860442D68909CFC8985F9805B8BDBD6A7392DB159030700568260830BF9E6D50F3326B02454B20A0E38E56FE2E1F71207171AE0AAA5DD908812CC2E54855BE6C0AAC417D3505A323FA3AC4DFDB3E02E7D29BD1E16BCBF74B394F85C074DB4026D28AF6779AC62D5B140AAD31300FA032858805B784B3D1D7C2EDDE07352B4200D44A201475CBC087C91DAC882B5B03BF92AA54B10510EEEC7EB79B769319BB57A9784A896C4E6A6BC75563AA9E0BB09DEA1B4815232F530F4557E29A0219DA16FA034B934AA1915D6C47A0AA9A6D76BA3464352D7F0EBD16948CDE13D4A0C9AD3CA58D09E48C0D8CAF6E1B059EBF0E3AA21622057C6EF1A82D6F279DDBF5F7FBCD1A0E4E8FD83E553C5E1E10C1B77A0EAE61E92CE6E34D744E2B9ADC13F69FA26F4048F7DC27023E04A50A02777294BBE4528FB17F89B142E06D04875D5F0E17B177B9435CA97CF9112A61AA39A2FE2C66B478503CF7F6B0F317847CA60CDE9DE12C98744CC26820A34958CBC365550119A6C1F2711CB1809EEFCCC06B57D86A075DBC3683DF9ED1FDFB57C78DAE22058D9FABA695A2BBD7C12C38851035E0F20733806B991642DB04539D2818785FD4CFF2F20B8279E86EA4A62B12CFFE2B94E957740A6B3E56CB4BBA341D48EE9B542F7B7A5BA5C2DA4D6239BF8C8C0FF0419557D8700135F0D376F34183BB2AAB31CFE2BD79CEDDC2725BAD95E1742A1C767797AD2113C805ED994C4D578532AD56B79F0E6EA27E7D1E9A94F2AA7966E1EA78D9B935FA796962F888BCF4A383C80B98DD646464EF2FEE25414C23B70B1240850C3B92531BB075AD678AA6095B56BB85E2E488A4FE6DCABD58AC289D9A23E3B1BAC069B9DDC2881218BBBB121230B2A55395D9273DD3B22A06D658DADA35EA030920C1E7A3E1597487CC400D52A658D2F702D0FB3B47B649C91B765A8AC9203CC0D2603BD618AAB4D1B1B1703E443553046216BC58FF32906871662BF32E7816DE17F48EABA040ED46E0C8544021773BFFE7CC77755F727C68E7EB715E7AA3A496E8C83EAC78A52E5152A2063D8AAAED209CAA6FF8D35008C30DDD3E2934CE1B4AB160A5D05630BD94E9A3BDCF7893C933863732E3177FEECCD9AC686A0CA1282E3A40D1DA27067CC4D4723B95FE3DC2667248E790472E96ED68D65D9B12BBDF648000EB0C578029E62026A0F68F8E14C213974694C19482EC47F1806014C260FC9555DC94B7E7BBC3CA3FD4D660747FB7204E22EC9556B7D18ED6947A044166B29418C533C007A65EFAD0B9F467A1975534F63E8E7DBB6BCDF9B794B70B5EAC2684A573997E86E83FF8A83B9167B1FEC8A04ECE24125C427D322E2B6EA02D966812680DC0C35ED47A07D2C1BFE725A26D35A4F7A1E282712FB926EA8007AB58179C9622DFF0D44146F459D90801E54E1A79279638D582F09EB979C0E9BE56CF5CC2A16F5553889D02F22F0C2127AE1A286EFB661974CAA3597A1248D90C32FBAFBB993F8E6C2B7C24B8AC63C8DF8A1A11D2388EF4B9B9CD8AF70EF667F2EB0B2C981AC8E052D3F7CA31C5A18EBB9817D6256980088CB2CFB854204666CB0FA8DFBBABB3BE4726A7386A2A48386F9D1E42C4A2706453308ED4B11656B357B09FB53F14C1DEDF352F510CCE6BF18DF15F4E5C3301F7B332EE605B6D037E1364F61C7E6C7A31C82F0E1B73ED945148551594127A7CF1C29E54BB904DDE8BC097B965D40942E80A63CA27D7767F4BBDC4B77F9916E4EE2C2D9D6423E9F1833BA2D97FD071814C211C8B8858F6985DFAB9EB431F6DA0B2C61D9FF988B28FB0B9B3C0E7A51E9C5EEA3CB2EDAC7EAE242FC0AD9EC89E50F061911CA6FCB8B7A8052C696B9A6084315A2D381074EA78B5A2DBFB9BEB7930B3EDD53470E9E4ACD07C75919DB051827E367FD5A7596BEFAFB9AB44F567A4B461EC1BA7DAEEC97E4FD4C2687B85420B3A07DBEAF08E2E6777E5C28776B449A6E0882459EECF718AF849FCEC5199466B7334DE1A63934A748528AA9B8DD753044F25F1211424F79A23FE1F7988D0FABCACCE003AE8BBA61B50C60EA0C15B9157C066451AFD880E953312B60D93AE791E417A1316FB8509E646A4696D38AE88D380132CE10CD2BDA1D3C67B4EF7F8647C9F41A94F4406FFC075F85E743EF15AB188BBF966C5E80C2E02E2BD0AF17D66BDA602D71FA79E784E7366668490B47D9947FE31A3EF3D0215B2FF132C374F9CD3896B072232CB6C54AA1DED39C44E89F635005568E0906A40F7191880E2443A98E60D670D6DF5EA9AD94417CE0EE3F4053AC37D7841514B8FE0B83D08B64E9B1CABEF313C41BFADEC1C6FAB2C82007BAC18D26D6EDF7A0DA1E57EAE82AB2444189DF65648741B0A4A32DA079068599103B14BDD869E8F0AEFDC9940214F817B090717685B59DDA66A9A3014715DE7429B93B2DC4295BC6124F29F390D8FEB05257D234FE3C91FF01F526C62EA4D5FB2DD9F55FE41A25A8D0A265DE244CB37ECE7E20BBB7D8E188CD93E2C71E02431292FF1460521CA140A24EACB34EF5F4B17E639320D6813E9DFD22737F27FFBB7836E7183220612971B5681862B0B0CC024A05A030C79ADAE3F7734D06E464970655D05082FAF12E75988B4CF6E94BEAD71A2720FE0BEF87457E7053BCC929FB0BFF13A47DC87F773D62023C4247C7A0650867F4C12876DBAF2AD368128F425DE01C897B8BD350069447CEAC4EE29A71433B4C5505B8DA891270DB3A70132C1C6CDA11F3D6B9BE54E3DDF781CE7681E4BBBFB12B2AD0772F6F1CD11902937E8EC1E3AD951D1AD8090242173E4C34E8BE5DEE702C2776C384FDF88F8D62A698FD84705D2EBC935C71DAB108D302603185E4D298D0B3B43B9F37A2F60D090D529098310FE0FA4CABC5FE5F3E38414E2D00CAB478EBCC5E8B14EF22052E0DB612F5369183E690A2603D03384A27A563275355F2DA9C06D5F2B95616DB8C67828A7254371BD9A7D12E60BC41A64C50200B1C0BA153F0BD75687AA9C1AF9F0BCB567F7515B6FDCAD0C367F5F2590E7203E7D456EAE090C243BC3E9369AA287DA7675FD52F8841461F50C9C6A7248BD9CCEBBB4717AE8A9A620AB2250E4A728BEE5A8AA6C8BC82589F1C05BCD567EDDB14C6EE77DC768069BF7B38B0D4B24576E3B027DBDD6B0F9639C251391D9E977B8B3BC13633728BFB4A888A839554C81DBC5EC60310B6BD3C4E4D64B0A51136BF013F5EE9FFD2F6D4BDEEC0053F896B9945A089D48D9B20792B63BA7C10619D3A8DB5A7B460F26FE4A2F5FE319F9100904DC865E13A954B33DD1A4B5DA9606F00B712D40DDC31A360EB04CD408684A47BD9B62A4E03196B073F59F2EFCD7F35DF1ECAD106F03E7FC631790D98CBF669C044166A325215E9A0AC0FA100F59DC18FE5F485A2A0C5D799D1915E4289773040007D6F98DF13FC5B5697319E60863B1BB05E24FCAC479839936AE91663B324ACE034335F1AF70F8FFC908B0DF99765C169E2A11195108505560DE0978065843A9E89C7B44EAE909396F16CCE126D1D4D27FC0B3E7983045008CE492B48F97F91372A3CAE97915731E2392F40727F89379341C387A9F8BF772AFFDB70B5F1FA5E5A3EBA9415BC59AB0FD1C6536757C90DEA405C7021E077D6838951375A84DA8DA48B9AE5EA56BBE9A2C176D942CC5B56F0E24A5271D3BE0D47886C2B4946BDA7824042DF7C0D7A5D5561C7299024C2012BC07F19E1FF70E057215EA7CF1F9F457715D4B79DF935F0820B55357B7F50D202BB1B0DA820EA559B99CDC392DB37FEC47FD8026C476093EA0E81F653EA4D96268845A5AD2F2428A7A7B1194908561B5CF7F14ADADA7B9C3735D9F194AB02F72FB9DAF6B700F4137470A66FE8CADFB1C2103B91243AD71E5DA54BC829ECB14A883D5AD7DF97A3D8BF568E36B88604C97227948F226660028741CB9E4A523BF5FECF4355218B49D495CF7D31121A6E9EDD00F65C7139635C559E44C792901091A35DBF523EAB54B359682728B45E6B71AFB72E476E725404AAD024DAB38837EFB86D97F2501DBF9792EC57428506F049BD365AB86CB2310BD9BB80744AF74C1FFE28C877D0C4B2BB6A212FCF31DDF2E422E93920D5D043DC18CD227587E6C3CA37363B426973221C6D999D4F2FD023A0C9468B9CDDD972653F05599F67AA611227861E6A8555958C06B7DE29E2A1C67662244B3B599B14B9CAFA8F8D917A0F7AA5FA2DBDFF0F3DD2A74A2D5C2D0B0C2BF1AAD192B501C2763610CF1D71E86D356326756D3F2A023E17BB591BBEE585B88A02E4F37CF6A4A138A1774807E70AA1436CA0F28708456D439AF480B7D7B29E926CC1AAD9793B1868FDA7831A697486CB72121DA231E3F09A4A6921EA7B5B0382558E047E2D2DF180CDD952BF84815B9A6BDC29521255A6E005CB0ADAFB82D1B91251240A1E09B7B2CEE36B1AA0D3C88C92E0F89DB895F6AC6D67E63F72E3EFF7978FF217934A3FF27CFB545BFE7970F58CC2E12122AD3C9054F530F9C812270ABDDE0BE58497C1B6781865CFEA63768373ABE87F736187BE6269279E05735E06C1330D330380752EAECE44951AB7EC99DEB788403181CEAB94A4EB40C387D07A3786A1CAD2C003F61709FAEF593B98DBB5C291E2D73FB8095A3898FC3F9CEF8D57C79B87302DDCC8ED9460720B5C003C588B32F8E45E944677D508E9AD2DF57401B62C7F8587793C03D6574ED7445A007A28E2A7D4665BBF784D1AFB3F3022D4ED6295F739DB0DEBF71A12833771BBCD26369030AB2244A585EE79429F1897764A395FF1919B6A3B675DAD6B7ABB1E7F8960CDE8F4255DDAD3B08CE13530F54F965B853E1E66257CB0380FDFB48C6BA746843C2618ACD7EB159E1554DF57BD70473D2AC841AC3D77AC862EFD75D7C1E5AFF4F7CE7DB715815EC81D7A158CC620D1B427884909065A12E24F8070B0E5AF264F55B5A8615055C5713AEE78F829473A6D829EF91D1B3C35E678ED37E3FF525AEE6B73EE6E1967ED60603F108CE1ABE7D54A754BCE50BE6C206E40A31CEE3E6006322C59BEB10815E91C66B7F263F10EB678DFF1A511C72B33A91ED0A4BA1F9551B3F2A5E0CFF7C69857985F6425EB369BDBD8C062C27DE1A0BFBDE59D50CD5853CE7A72CF85A0B9EB2DD59F4C3781382AAE5FC961FC0C8086DC96FE6E8C02277A335B06B8B2FE13DF95A35C5D462B6740F65F08CF32DE1B79178629FF1657DDCB03B040B11E14D7189838BB329AD64AA78A12551B8D5E3EF0750D24D263EC857B6F56FAFF46C058130C8FA9E4AECFDFE05EBAB2B3286C1E100C7D0AFAB9F921931F6706AB06D969AE2520FC8C8495F07B1CCA0FED44209810CC0A8437D2E002CD6EAB0B9F72874234DD849FA84D3AFE3ABE03FCCA71DA7F1097868F4DE0B764BE51672910C466DE63184C4F1FA5E95DF1666FBB346A100DBB54A2B7E3AFD1E6C588C4215B935056B77BD020972BEBA51C237661EF30D0E2962E4768DB89076DEAF86222615814C680346ABAA9400632C35A6235A1A166589ED51268D8A6959EAC27C33EA3E2EE38DE1CE3F9613837ADAD2EB94925D5B413E8D5D4EAB58898FA27735EBD85B5891B3CBD1C81FF0DFC926C5512FE55A50F90334125BA06331D8CC1BA7F36CF8D95FD4B5E56D32D27501A25FBC0C9CE343630AD7723E0D7DC77934E4C1067CC00496CFBECF4AA437C2C789219654C4BBAE02B0462FD4450F29A3F46F86934C5D9B3A0DC2AC59E4C8648A39D8632F0F6626126B0F4A28A897C0BE0C49CA03991649681E5414F7043B53FF6F29F9D0AB4D9CC834A9F5F5F502A69F2D1911218E47471AC9BA845CAB8D7D4079C19ABCFC93A93A4C7F89F3BEF8D1562128E1E71D9154E179B599F3DD5C8945DA26C9EFEA0DF57B8B54A1256BF806B6016F8D1A8790C94F62FBA7EE2CA4DB3E689C17A8504DDCE33F42398C72C662E40ED21A5BEE45C79CE381C67785EA93CF32C22E20B3F5DC1CA179CABF90607F13DDDED8AE3C84F188161AC7E0C8D80FE3F28736738AD500CA90BD568AB4C92F856D81B06B3147AA2B9E99F978C4C4B3CDCA87372A62BD4E4EEC52F2B3446DC1F055217A1E9021D9DFC3189850F963DBEA543E682FC98996831072EFFE1AC2B6F6B59EDD52DF6F17463FC111833A292E184F817D77FDCC4CB145EC2372EC01A9C10ECE2FC923920C42AD59EC9178AFF3746DCA8D86D4FCA10A679C5FA5DEDC94B908833C227CE9C70F793DC6AF5AA25317E14A6E03B7B440053383B99FEEDE87B442E04F5CE06F79B09137B4E3F01CD16B7BA2ECAF89E4F48520B98393C6DC07EFC03BEC77D94C6FE0B8B55667E90C4133A06E03062035D8DCCD9AA82ACCDF287E21077D072AECDF4BD5B015720739994335CA636254AFCF21E3A9779B2B45557ECFEA408B9D65464CFE75F7442567E54EA71CC8FC5AEC8A85324C44404086100BE7A971EFF977C06E4553045AB1B3A59FD47681CE413B38E2973B21B2EAB1562409E19DE924BADBF433F19B386EA589ED0C2A2B7A6F7327857D71238BE61863A7DFEE3E0EF6372F9E4AA8CFF03A319B7E391B0C719DA38FF61C5F0D5C88B8C40F500DC9839C4D75B0224B8EA05CE0A36DE6F8C5ABCDF27FBD2CC847FA88FA2EF5D9A322E58B6CADD26D949B9962573323158EB073BA22E41327C222D38A38C906AE1B424CF0C41BAFF504C74F0874E936642E24764DFC61353E5018A4FCA26AD1DA2DFF9F1940A439A8EBD9995827FCF9A6237F2F0FD67198116E606B7C3A3BE042DFA300D7BA4F9B3C10E1D8344B97763D25CA33DCB92FC9F661FFB9430BFFBF3545C7411420418D2801C65B800BC1E2824FBFCE0C543167D43C987AE0CF251319475912A72338794375C032D92D7CBC8BC442921E8A710440516701D7D1148DA8B01B1066B93F847C293A45AC10EBAAC463636B65FBBD542453E2008D4F429252A33CFA0FC3AED01D57721B95DF6212B04B558FDC5EF0BFC41E17D3F72B79251D15ED95F8FF26CEA8A08BB3AE70C317D5CF46EE64771684D2E6BF5510D927812C50C8FF179ABFC1EBFB29197419587F730D9C6065BD93E46A7A1293B3BB6EB7350AC3D16387D010E443E4887B61316BBC737788CA69C23A23806277E926F6D46C85AEC92CC6F7FB2AF9BF85DCC88638E381EF95EA9BA8AC72E6EB7446D585F48246274FD81AD19FB31303C7E778B2447BAE4B5194ABDA944786EBC5A699B0C532EED98A87351FB9EB7F76E6612709CECEA0C58126548704C6ABB71ECD318D26B3EC93A9060461E01E1F485713164784B267DDE7B5E2909EB9130FD18C1BA1FB10D4400BA5CADFA6AC697F006034E8929CE77FE812C5509FDE63063F570A70965BE273ADFCC0B6DD8D9E1CEA42AA81D5A8F84F1AA0928F1F0732B3EF1E072E448ED8B8FC457B886717347218C9A288A2174CD9C23880FBC0E606E77B664152C853B5BA2F959DCFBFB70A0B55B28F4120E93FE464848C7BDF9E556991BEC4815783A6615C348B1B70D99DDA86366ED260E0E67D110C6FF9C04C3C587283F79371CA2F87E2648515CE17330AC6855209B4A4469A351196BA1ED75F7A85123F40F863FF4342A32E2A6C8FF07D1BB036E2C4DC20C35236FE5BE47DF79F2CFB1BABD39DF262473D312B64FB9C386E5A5679304BAF5D6646744EEB75D382A176E852DBA3AA431A8CFB754BC64E52BC562E731D8F151461507EA1425DE2E4753E35A6E2A67A3A6468AC7023FE1106FC40981CCE94C9D34D471E0A18ECE6D4ED842E07BC8DE7D676BD9BC86B94C0507FCE2A451E3A2F154E56E9EBAAC8C374F6BB1C389D4058C8DBD389FCF5FED180E717A14B7AA2E57692C7AE1C0A3F0B832296DA8AD0B9BB34947FE644A219F2EFB27700FB25E135C1174AF767200B38778096F2A5F9246927FD241DA8D6E56DE7039F592786447C6EE5E7288071C072B6983930893353E3CEBDE5CD32E8C1D9B3403003D90BA6D9201A9F92CE2D79F07FB4860B4E4575CDF2D4CB03FB6087D78D157941FB9394D82496F414599EE4C47B0D3165D7A69897C7ED7850655308E070A12134A753ACF66A35ACDD3D2A09E6F68925A508CEA08A0897C68285FCE96FF3AF38B4748EB2F6F55D4D07435E412EC799C6CB1CA9B08DC985683AE4EE36E34D566C8FC21145EEE80486CCE90AF6DC55BDAC7C1FF5A3C71FDF595F284C878AD5BE23DE13534DF80F42EB57903ABE6CFB77A02FA5F0FDC45AC9E5529F1C6A2929DEFA11E16DAD732AC9377D254110742DCA1B27092291AB3445A71DC76610387CAEADD67E4F64A57AB4F546479843EF26FD8953E0282DF8893A14315A58588A3E4DCD6D7760188A312395A88F23274E32EB85DEE01ADB5CAE2445AEDACF27B4D1C0C5CEAD03DDBCCE96735BCB6803DB8A18AFC293EDC3E6734556084A0D9564A4D84E456620DC61563D59962295EE86C2246E2E84771D7B506C012BCE21EE7146268A0299556EC5B938CAB4BBEFFAAEADCB560D574D347CD375622FAC568418DCA5C9F8E8D50F4B225612D94B6ADE8AEA2298B9D357438661FA8F611B07416AC7E6C5AFDE1DC72F58F7A69C1ECB6ED90CF2DD1D67F1605278B86CECD4C122150BE845D061051FD738C51B7AA5AA42E8DA5174B8EA52AEF04876C228D1AC0AB14E1AC4312520F9D3B416AB818B259C9D1EB2DD9DC23348F88227C048C4442F94B35E034747BF2029E9C1CE54AB61CAD49DAE79DC57918E8246AA7D0B018DDA53A4EE91C9A6ECE8557F2134FC46599AC4C60570495B397E7234EB40E23BCD47D0893337C58D1B01D95084276722676A1969BCA2E3650FFFBFBD5475CF4CEAF486CD1BD9D90C5BC356F7B55679D07698D0ED2EEF5DE91555C68AE284BB8F3B28C0D6A859BB1C23D82DE728C99E25C5E8160B10AF35D3E9DCE260D5129535EFFDEB07FC39D84E6D73E63905EFA103A4290F585CFABD5DBC52832ED71C86C247488C404B1C6559F66AFB2C2C3CB5BCBB9D022C1BBE3F15206462FC1F4F3A476F2A8EA2DA7B1C35A80DB8D0334B999A0B43BCA04C3D130FB08C2D10E7C7F1B215B25CE78C8165898B75D5FC1C17AFC296DB91BD53051CAD86E9229684544D173C4612A175FB8E33177502087C113FC041D3E53E6BA6C6926ED39E6DD6055A4007CB22C10344B046BBA01F95A324A772E0EA049FD96874946C8561E458BFC80D58973C5EE2262750C0061C39C837DAD99FB4FF883E17361B0C966D3B384D2AC617FB57AE4B8079C157C03BABF339EE660D0EB96C3D1EFA7D4D899616C69F4A2AD157D57E06BCDFC0BA07280E6014A975CA2F0944C06143CFB38ED6DFC9EE92CA18060E9ED1E816038C3CED11476046448EFE8A6838E5E003F5DE3A68FB96736C0C1CB13078C37730FEE36699EA9B3864D90BCD3CA05F0286E7CE620D1F392F93CF2812030F678E9C966B3A539CE45D69749D0C285E63C841BA7ADAA11A14CA81FA83653F8129BB1D161C50365F0642C6036259FEE0BBDF2A3D061B6328652E827D7646758C33EAC35075B1B585D207807238C88BCA7561C54935E38B9E4CBB1F877469DACF738089C5F967BEE527A1EDFCE402A198C27BE0897852FBAAA62D15BEF94AFBB2E70CBC502BEEEB0091F210E21FEF0518C62DA83BA59FA52D2D60C5C0DC0683FA6D7785477044CC4C45A71C97819AC7F45D0CA79F2D53F2DD96A00D11408C42C5D59CAA14B4BC217D0959B01D84BE062CCC38E115E7284DFCAC9CB6CE7B4F392095FA07A6FA83303A7F24BA31AC7296DC564E7480075811322D716230CCDCDE912866DB8E523ADC3276AF891796FC09CC91113CE6EFD3F870480805FE0EA9890124527E1E19EAE1A33E1A9FCDB341268C0A61A5A72C0A42E25C32047B90BAB894F4B95EA07CFBE685123E67E391A6347C1E2743906605E8EA5E6B559C93AD987CA51194BAE20E790627D50B5440260BEA8561DADBA6EAD8114847F9425200917325E04D9A64D3D554C47CFE559EFD94CC9911F6BD93C183ED8734E834ECB4A6595A3559F8682FCDB7E3EEC3F02E48CD0FF42D24C1574F0B481899FE01FF1552D95A25FA0C9D94CAC79441CA8F2A243DEA2EB375AB80C5C2B0DB06F5660CCFD2BBD13D86F10470D9EA97554DBB6E1FFEADEF69A7812301304A134006D2B7A0094D43D513FE2BF06482133EB7755B2B2AFF502E94F4AB70446D3679C7F1464F8CBA6FC46C334977D6AAC8443EE09F5BD9178F6FB6D839AF18E15B448F64C3F9382E6AFC34C88C39989CE0BC4E07C040003F6CCB687C2E0E68E366C12490ADC51E2EB3BF8EA36DBD43CCF62E23D8E47773BBAC9EEB7A98F77071642A5FFEEE4865C147D59B763BFE9BF057AFDE0B07BBF968592F7CB7E03EA7E121D050C990809DB002A0E309DBA16883173FF27D3402568DA344050056C5C2EF36220B96359DF3520B2E7A6C5A67E5D9BD4207355465BE1C21C89C08A1838421C03BB58504E84F266EA4EB73358D9CCC72C49B3DAB13520D5F0A9231364A233A653DF8718102B7E2CF33E1FA8A5FE70717CDA659167ACE35EFF8CC94755797A59170951A6C7220727B020D37930C86ABA75CBD7DEF735C96C81C673BD9E72CF6F5B3477949CEB6EC07A19C1CE39C635FE86A56A24F6526E4FFBC7062EA0043A2CC1C8310BFB6B7DD4634988FE0974DE0B3A193F2E9BFC85093751FF622BDA558A0A66DA3E81B69DD4FD6D45DD48AB2DEE55F68A2096D1CC806716DC0F6F7F87AC4D369262F36C26D851FCE4413086A981D635DADD1C7AF0BB81E42A30B420C0A0F4F18A51839E5A8BF484A78BBD5637BEF81C9D81EF1DAA2BB24BA04ED58861636E82FFE86D721F8A580BF1EFA2DBFCF9D4A4C5DC902460CC06DCE17F170E61D7941BC323DEDBC8821B9D02ACD4F06466E31134526B21FB3014A4570DCD9D8835E303DAC56BAE61A1BC4765C3586135BD9437E9CBF331EB06C44C8DACB3083386C624BCB022FB83C300278E42DA93EEC6A28B99DC3C9D697E29BFBB3C1E47B4163A29F058CC392B5C3FFD56A23D78ADD6E2ACE7603AC44656C8686EF930349C8C32E250EE5BA7B69D2ED15A90329F9E423B5E9605566C816898C279E197310D144FE49CFD6C4330CC0AD287DD8940064FD007B660A9D7337707F64E10DE3D185C6554433409021A1F75F929BBDB2435C450254689E42B9FEE3E60A197B3CD32B9CEC77228927E6F82351A53923AED69DA2DEEA8A5E76B579D0B87DAA36311264D4CF156C4C1F7FBA067ADED18E7A0A75BA139895C303A520151C1DB9AF39C06E1A0F36F55CD4A12A333803234ECFEA6307FF602AEBBDF7DB6B8C57FC60A1FB509868AAE7AE601DBF8B177D4A9014FD214A901FEA8C1C785595283638D4E1AE3B0608F3507D7BF307745B468BC3236591F3112BAD4CBBA26116BFC49175C8A12C2CB665546F3306C6DA70C7FA112615009B68346A4C2A34C59E03B9DB85FBD4A87902DFE8B448094F339ED1BAC563408F673E6CEAEEA7CC6C0BCE60F8D0AA2BECCF561E506C21A019C666FB45E6E363724029365395FCB9AD77AE93853E65E1C5AC3D5D55CA42B69E0542757EB2B96E51A359D57D2916666751AFC7BB5DB66D5F5412DD13F99F56A19D09ED594D873EE6DA3E552F5A32445CAEE905D66B7E799624736AD7C8F79B1DEFEF0AEB81E3A1ADBBBAD42A009656F4583CE1DA9E7BEDD2192D16B7B4AB5684065F85C04F70185F6A62C132DC3E4A4FCDF874E823F87C4F6316406EA40B391B1D89A2FE0188E767D750BD52A6B5B640A91A48FCFC0A68B54D62C6E0A80C79847F84949C6503DCE8CC45CB11D5CCED158A539505E61BB37B77D06DB969D73231C0FE01A9E544630ACB235EAA1820EBB905B4154ADEA625C5B57FBA5040CB3D185D6964C591D0BB0ED268CF62E84DB71F5E4B17505F74A4D7F626FD78A765E04FB1948526C872E2C1425F29B9F5FDE0370ECD1C49ED6C0825728D46A7127D75F90688D1F99A2D8FB2646FB458BA56D03D6A53ECCFD9C362103E348FE04847455A0A2CA06002610F4A108FF5C5AF1DCAFC063BD101D0DF8477CB5217ECD3415DCBA83C6B50CE077273FB463D48F42EEEAD75311ADCFAA444AFA2371EFFDFEE152DA7C26A52F4B1B952ACC0C62CDAACCA9E46D4CCEF3A164619E6D50A4E58361440035168A1BE30A642282E461B24AFA053336A7E162B05BB7FCDBE9541A86D479C3392F1BAE030AEABE5BB36DF055D1B67B14AF71E41154CD14993E361A3A4D4F278F6F6F8237850B5B416F7141F03E49FDC881986E27A99FF6BF3FD4E02BA0FC476CF684E862087D5BFE681C7530F8F077405E5ED261B65AE3EBF3BE2E41BB766D100A66ED05DB82A5A94AD72B41C48ED48DC830BBE3D1D1AACBB82853F1FAF1F72024E1066F96016CE49A9973D52080E7E78E318618E31C9153C37D97D5B7CB1EC173227F5000C1F9717536F51BA0A7A73F44FEE4802EEE0DFF1D56A90A9BD02161D514F4D527F831660A98A4AB7EA4D2AE43EC6B31CA48D4CDFDB3E7682A891D846B43A0560A76F648110D70FB8FA0569C4C32996F6C1BFA9EB5EB7E1221F26A3EEC45B6688779988B8AAE9B2DE641E7C11552DDE544A40B254F960D9F77161B4C0F956D2813FDD54A2CDCBA59D19249EDD67C93A10D92D77D4C2CB6EE10018E197A0C3650CCDD36E74C1DD93906F12148F8B10F5B709CB6C1A055B50C5E7DE70806B08E7D75476406F7D123DD1CDCCE3BF007CB153CE8BC1B8769A0B9F413928798D29ACF7FD88E31E28B2D9F5893B9BB258BC4B22F948CA859B0A38E67E3DA9B6480666AF6DCDD6F8A34B37BB25B0DAD6714BDAEDF8070BFA391F747FE728C95ADB09256888666CA1A1B4611E608178BC118CE9AD0317ED71432C3131217C93498894C18AED4CAB3F7839D4ED829CB6DC3B7BE2CEBF75E5C2DF2C367849A9678486C7B1DFBB29363F7796A2B7F4677F0293D64EAE0D8350A35D7F47CFCD9FB8BE7874E1B01E4E2B70AEBB8E182DED49BEE5A32D58D748787465AF15BA93605D47F53B4C0B8134D139FC8A852FCC5DE7DE630982021F1D1D10A5A7F95BEAB63570274A74BCE08EDBE2F5DFAD6B321F5A577480B71CD3601321B10F34651FCB2ED8EEC5F0CE8292C2974FEC258A4C0F83DD7A11C8085BCCB3DDA097C96DCF21BEE4E83B25E695113F6CEFA93781D978F591C858BAC9C0E5E5DD02CBD22A6018C24459B81AFA3E542899C59CE8E851F0709780EC74BE31FB28900B1F04E69481576AC22D591F6DEAF918EDEF87B058963A1710F9B1282B6CC390130C0D0EF97946E53E763D88F8F530A6BC0ECEF5BD060BFC371132E6D2A801C45DE74DC349C239ED2EA74D75E30BDE56B62981E1D876D22B0E87E23B02A3E993AA37B955F618D61BCA1696CBAEAC0DF1DDAF91ACE1901C84E486600343822616CEC5D1758FDD0405097BF45CAA5B5CD26B83053D6B2F3754997F6340005870666711CA309DC1FC59ABF1D1D11656C7494EAE6D53ECC7F70A7669B7E309C0ED527997CABB0C38E2DC1021CF22C5285A16FA5A81A098E900E9C5A9189F9C9A5BB5CF5269439F983CDC0FC3BD640DB703571C5D5AF922C262CD8130F4071045F628B1F4E2360202AE451B293D10506D617C741D87AB47BA53E719FE99A1109A63284BA8D13660A4C69077429E69A52017C2CF975AB985FCCACAD3E349F4ACA10B4B43B60C360083A0A9391A1D61FC0F52A5CF3A701C4774EFC849B856870D861617033D3F217825DA45461D54FE264FEDF30C8CF1474190C566963EED4F8E87DDB2238802FAF782C473D9F2D152DD8B2105DFB7DD53CD603DC4B9BFAEAD58E5023D13C01784ABEBB3A1AF0803CE9536453A117C4E2649AC16D6B1767D3B9D0A32C8CB6BE53E64734582B4E2DFD843AF114E0C9B01CDFF2F82503328AE5F1DD9E106CF6AB6AE5F78EFDA2E8CFD42EDC9A7EBD11F7888C6894CB4F85012254156C0217CA6E05AD680B2C9F477818BB24C2261FA3D8B006CA977056F3BE0424616074F4D4BB791A2C1BB8AD51096C4DBA4DD66D351FDB887FF8CE3C9CFE83F8F0B54CCEFBED28E2D12F7E0DA45EA824876D11DDD41A5C965C160E488FCD4139DDC86DEE3F2D561CEF454D90D76B3D68FA3411AE037B6F1E64BAEA440E20C05C03818980FD3CD816342BB5B07DC1FC85A8D25C4A7550C9FCAF8EFEC93E43AC7671DBB336505253BBD19AF0416BF6039626D83844590121A07698CF0F99542CB8D601DB9C8F5479D61C08059A89C5E7DB125D6FE2B04214DF6C393F6BC4659A9BB7225A1623144C9E8B9D00E31CBB0A6B03149566E6245DE6F0D1576B1FFA613E68A53B4BB4C8DED3D9C85E10AFBB4727A1F0E01CA33D0D9867D6DC517B869CAD2C7BD90735D50A2BB350CD7AE30399BF636DD49D81DC8D1D9F4C9ED41644B6B4998F7DC05871E7A946471D26079F39F66E370E031A810C0E98849299418000E45A86CEC064025075467E113B97E11DDA3F82C6B422D435AE905AD37848C09A8C4FC0AE75F7D8EDBEDA54A02CF46B3C43DCBBAF70E5F690AFAFBE5D3205F626A4C746497794A9723A82BA9E142C5BC3354AC045E8D5C48964B87980DEBAB50B2D0BBBAC4563690272253FD34E08580B9CA902161B357284272CED988D4F2AB4C7882B260ED26BDAABD0D229C13F9FDE02788AE20547F55E7ACF7AB3714570E9191B11CB3687BF65CB97A98C726948B0C07B2F32DC53BC8EB097ED6DC701E108FDD0BE8E44AB902E169AC7624AB62953A5346960A774AE4F4C50B9EDD735F793EBE80FFB38A4882BB1EAE1CDA119E5A72C529CBE0C86B751322D48715F26255DED79F0E9DC455BF25381D6E392F053939B2AB1E1864478C5C2F5FECC47328E95575B7932056A810717BA8F2F910CB9B1AAB1656C1DB72B793F107F6F0B52527228E1D243612DCA0096075A754C579690EBE5A3ECEB78C314D524325758630E15C696091B9CE9E2662EA10DC98784A02EE22390658B75F662E0A0C44457DAF7E0A7AB07C23300DC0AE10829B6B0AD35CB968586BD61F9D7DD21F75DF44D312666D50C09624D59AB1FBA81DA0EE207E616A1523113F0568947FE0132C42E0101C6E7E90EEC6BE54BA5CAD08FAAC63290FD69A1234E984AF8A58376E7A9AC5AA26EA283C02D1024C9698B2C09EEDB635054E2E0C4E0C373B9ECE3A4CBC4E3AC9351CE34EDF64DAAF01434336EED680E9F199916979B348F721ED58B40EA7FDA423A4DF3A19DB3A6F1B3FF273FC520E0E5FEF9C61E782C520E5FEC5987859A279A67B2A3D1721468B379420FCF959F52CA600F102C1289B74D5B3D950DFEFF71B788C0159A1207B3AF3CDAB70256C69C69F354584A5DDB69902B251DFE4064C10DB1FBF54F7331DCB56A1662737D4E8C0A1901D7AB4AD06998A4E00BC930EB7D1A2D6A66FB025D8F21768B2633D3898FB3CD62C5DFC7AD1BD2A68A9D8E88446E868EABEFC3E14C6192ED5EFA75219310BF05D7684D3B2708FCD19CE34403729E4A8646C8D74627D0686E684D81155A965C18725ECE9FD93528FC6B51D3DBA4320925F3587B8396EAC0D9A8B0BB7B31D0C66F8F3EB289FE1FCF9C9DC5B66D5130176B5DE1C98852B3738857EC1590D94C7DA83F60DB0295EEC6997175C3810DF4283BDE1BCC5FE23B67E57357D7905E6D80B7C88F199EACF42DD8A8A740D73275EE27456280BBC11061FF1CAA38C6F5555D746E19C5EFAD06516BC6AB3977A1EC264A3AE4012B679DEBBD7D5FAE64A986D90BBAFB96EEB0220C7090289E4227A33922143EB20EA6952E63A4DF3C46F7F238FDD735A2E6C8132DBBAA18D69BB4A9CB71C2144343F592C98C7BF73C23DB3648F317DEAF833A3297AF2580529404A2D593424BE6224DA4BC745F8F365CB65065EA9A773D2A108E93C73CC4E51155337E48AB67475ED326F892BCDAB09B1007E46AB207E3395F3D0E03012CDB8B4EB208E8809A089C0E46AC5BBB995688CC9C10964C60376BB8DF4533FD597560A17A256A2536A7168CBD5B1BC9A4621A55BA42422F4A10C4F7AE3212D9F17FCD43E8208438C31FF2CFC66983E503339337C1D23A80D381386D8FA9AE71BAF3B7D214388934486D0DF6E1FA1B642B7C1EA1FE1C16DCA004744486981F5F07C566F2989942C7B7FE0B5E84F8F839DC43BE3ADD91EF93C10C5F332006F803367E30FEAD27AE4AE79F63B718DB3F2E4FF1252161E13D07E2DEB55955CC3E24DDF992EE790A991736368E08BCB3223C4D65A6DA03A065DAF35814C6AB60431FE5EBDA2E9A5C32290B9DB2C0E151F884561B06B5AA98D2CB0F2B44E300A2B6C053FAF1929B7E9D3AB558A4C51F10CB8A6E577B3C5BA647281892105464D142E201842E7187DE4C76BBFCA5871F1F290D20AFD30522821AB803F5A5766AAE9FC4EF2DF6AA4B1FBEA4B72BE9069D18BCF4D93AABF9D4A010883CE0F1BCB7E3C7D58E3C32DAD7E5A59F581D0AC1861644F006C61CF2DD542F6C19B6477AF3DDBD43DBE0473E99C8EF1703021F58DBD359C3CF6A831285081E03DA65C00527D377E0D9D098E6B1B9703E8CC6B3075C7F673000E807021EE9368DD07812654B2916CCDA3BD023DCF65AB236C9C6A63C780BCEE85EBEDFB48A84F3CB1F80C6EE9A12BEECD7309E7863A987320459C9E73DB535F2145B81292E6D7CECB6BE1F84C292420758E67456F0D7AA3C5D0C9C942019B8657FE7AAA60D1E7BA2C8E8C8CE3DA3EF08249043DD24A9DD54CE8D55A31259B17FD8FE0D6F1CF6E7C16A29ED8FF46A8C1A4264B4BD186832512F45487D9AC44B199B7D9ECDCEA0A2BAC22E469A88246F063A3A5FA58EA0A18544318D171735C5280005B4DEAD19E3D79755B5831E97DE84CCD68FEF2ED970921E4AC3A51EA11D8FE0B1972BD4A361A23FCBAE1165561C5C8DDE594EC10FA4754E816BB6BA3123F2FBDE0529B868E4A8F44664306134CB8E9C64BD243CA683771CDB2CA259AAA1886303AFA3F0440620B545F46A64CD13AA7E4F1EF85F88F61FDD2796B60617CBA2081AF0FF343BB952C8BBABBFF8F48B130C1E3970A61AEC61975DF31E1821C3643E572CDFB9D76F657E784FE1334573EFCD37AA37AACE147124F108E4F741F6773FE0C33D0A68D497238A6C9DC59785C9D31E7BECB94C281639F37B6E2A699449EF3D1D2CEEAC5920ED4CB723AABAD7C80E56F5773909A21AC4E107B281428D98EEA0C13CD197189F873537D61A927C90BD102982CC125138D0D011028C00C7ED66F99A8C4A03AE426F348922B84D7FFB874602121DC97F2507355876CB4D871D7EF4F2EA11BCA43C16AC388934507AF4C2E163931D825B501BB1B07850D7942D93E274F42FE3657A0DAF53AF5D66B10AF5039B5A621BD4F54F60623FF5BADD9EB1BC80350820F82841F5623293018ACB6392A47FEFC730719C7B537B2FCF287069EBABA60F77FD12BF8764609FE4B42ACC03E510317ACC9201ECDD019707F59DBE9616569E8FDE3D6EC73B689BABF671372F53DD5C6D1DDE9798C69B78A603DDB0F5BD083CDFF3AB1C3CC55C46279272FCF6B54EBBCCABAA82DFF4BB012F3A8CC180611D0A12DD32170A7A0CE356455AD2426D168360802D2C44922B61F36E8F40A7DCA87203F3AC9DF6C51592F13C0F06F9A5A776BF9B6A29F984B9A6A336CF08D3CCE499BA23F326A1F6DCEC8977813B110C52C871D4414187DF4348DAE58135AF39E271C1C04C77CA325BAF75F5C030238FCDA3BB3723980D9E21352122AE390FDF29FC8F7F0223432F03B64FEE3BB6C04E66FCF55227CEE956B567F5483E4CC90938B60D31C7ED842A4E7339F5AD32C07BCCC2DC008713BC69117FBB289036000F08126504EE05F6E09839F97220A32B8ADB7362AA781267D172F65B54D67AB46A316A8BA9FD613187B68125BDBF80DE627B4B20E9AF37FB2452299987EC8DAC48071C33000BCA93CFBBAFB1777051B3D0BB0303A8BC298340AD2CB37F1BD8CF0FD6B45CB4B12B743A10C73E4BD3622D04DB5849A192B3A1A1AAADB24982F8F19E09714F8F3596BA99EB9E80D1DF6ACCA4551D97F6623652B59A09CECADCDD50F8BB34927143BABC85421F6E9A190C72161ADC5E1BEF44E14F0F06B037E00A37A00F403EF282E4CF571B3FBC0DCA16A4B26724C17AE77C17FEB4053C518DCA4D3FFE293A22FC2D38FFF7DF64E8EE7C0BF1A25F6CCEAE7E9E010FCDD8C2449EB14FC248CB21E8F6FD9CCD89D73C268B3817EE58AFFE6454A104CCE7AE6043D6C7715474D874AA9A1B455A842E9E77CBF3BD892CF754BFD1A7FE59D3B13F3D43C3015619084B10320C634A213344913D4B9725AF66A324366BE51B10C42834C088F66814C1D275D50097B6EB937CFB9F7458F9D609E4AD6FCE9DB587F7ABDAF8FF528A6CC84C94F537FA9DF0F927ABA72202177795AEE3128F51548605775BF6E7C965D1008C2C8AB128FBD0984FF6CB06C928AFD5A75F6EED9D867CA4D5B21E35E362F60A03B325FD6E5FBDDA61329651D5EDF5E7FA2AEBE4FDD91B5760065EEE26BA9994D3BB369722479856D79F6A16952A39FECB65322C3F0D4CDCADA90CE21516AB7C195AA7DC3C7C32A120854F0AD549F94A7F61808159D431A1644E18B63434885BA05CAC23E3B9D408DCEB9C209AC1D86C060D26367F315D4E5DD2975B9E0EC8EA62B5DADE497F6A56CFD3AE36F1148B03F4169BD76989B0A0FF413DED8D06C4BDCD22F40DE009A0857D56B5805F381BA0053A9B025073668C362D1D9DCAD041FF479860854260FF7B32745967769E92CA0E5C5059ED87E80D1EEF3230A0D648B3F42B5EEA0A201BF9812E6D65D2087570E62EA17A184A319FEF425D3E202DB2914A3A621B33F441C80AC7046304A326392C80B84D6C3DED9FC8C6BF57852CD2F876FAAD0D9FEB55A0A945E87BDC7C9CF49B6F906966B386B1F77B36514E5D11321635F05A2655F9FCFDC07165687C4E5EE25D1314D4C210DE8485B3E6D88CC9FD37FB476F328326384213641EA7AF4C9FE114FCDFAB5DDF161A26CFC1FCD146C13AB99BAB6FE91528E15CD32FC606B5D12C24619DE288C1751B0E3264A9FC2B6889D10076BB52A0A875238BEFA811800D356CD8C2BFE46A5829607C97008A94972311F3F43423B502206ECD0E3B64F1EC69B9E2242C22E488E33FB649D027F2C4CBA84553183A411943FFE8604B2BD2D440E9AE6DF056B8E76963FC045BEE39EFF2BC19859A538566B9F13FA5893B622C33ACF0B70ACB11BDE47061DA0B28D4564E3F708DB3658F809FBFE9C9D073020B186A023D62ECF79ACB49E34DA5ADBF03E16310E22EC732F8DC9FECB0A01468B3D08C3D7B5D6DC4F55523C6C9796AE833BF9A9241674DDFC406C4C9810784ADA131B7B36A494553C9F524BE56794DFBCAD6C46ED7161F9CCFE5D05E8499B43AEEF3A0B78C5ABE18ACCD26F6B48F86B4FFAEA1C4F3DC1CF1277F6D5624441EC2E0970B4199BCE31AD12EE15592C2FC1294F091F746C5753D09EE3BC935B77B9B92B1AC82025D9C6695BF71295AFA2164191ED32C7E4265F3661350AFE5CE8185D8C0B330AA3DB158076282A79E6433F090D9B378A3BD7D615D06A8F3B5CCF7F9D8DE152CF57208A9B81EE06C507010BFF9448DB3B15EF23FAB6DD628946E04818BBF54D043B1B318CFF96FA375D2B4359388CA6CFE3601320994DF8AB498345F73FD6582042015B18664FFA558ED631026D6B18619451A9889077D0A5CCC43D348AE355776CFBA12B406DB801EC28F4BE90146E484BE0106FACEC4C6045425E32FC2BC06E73A74A6EE3A48441AF7B1854B924B19FB7790411B71FB5F8212F2FC641CF0F4CF212D68D23F642A901975AE20DC18FC89FFD84EAAE1CA8B57325717E2C8B29C922A86B34220093751DAD5A896A789A58C5DC606CD8E584A2181DC4E26750418C1AC14EF8D60200201CBBA4E15ED66EA4F4464EDA703E9BA4556A545367303AD7336C450515E38EF2436440F0BBC1AA5676B80C21F9AE746D8714F97DF9851615545ED0A9305F8E2B495E09EB1E716B0CDD60EAF5EC00C8C14A6B914FE16CB619E10371507DA404BD8A92888479F4724BCD7CE5C588AACC71100A31CF3FA6E0CD7735433BBA1764581F44E8F6787CCE0545670855F23AEBE45324CE1899A97A9147976016D673BF9C6C97E2FAE38318CCEB76A1515B26B1CF15C1C158B7889F32FCAA76747E6CB30A19AC986804BE14CA04696F3DB5F04413E10281FF003D2EF8DAD968916E1FE0E0966025F04723932D00483F582DA692516D1FF711567AB8B9B588E617BDC1BEA38A97AA03E994FF37E7A8E57756684159B8029D0AA37535AB5DD559D01C56717C3A632BC581BF176D65AE1CE78E94BAA9E52FA815CD6B2B301876A9CCFB9BED08E24D57EA9DE053665672540A64FD1772D5F20DDF5ACEA37A76FE7F0787B94F7D5A7E36A59ACCC8BBCB5F8CC4910184728D969F4FED672FBC75B69703BAF63506CB572A501F23383EDD5D4445259D71D756AC387EAC2C96E0F95168363EFA5C07587E9E16B1E9186802119B99EAD54F91612B01FF76B3B8EAA714E7B88ABD9DC15134E7F96B5BA6B3D39E549ED348B2AEA26347559ADDE6AFEEFE176A6CB3308A5A51747BCB0F2B1358EB8175735C2FD08A0B4C60A092C466728410022B85175503633B56CAD94A7B2DF86BCDEC8EC9DD3B1002B6D19115E9259E7398B0137578A47A292AAEEC7CAAD937F811B6D1BCF1CCCAD36F0836D8C12958575859793B04950E31E25C4D20D32E18E7AD1687375D7391EEEB2D119779012A6DB1C4AFF7B5D8B1C3AA05B13BD315218C75AB357EB96EBC7EE51279D0703CD1E9B3E9CA3E2D2208A9A2BDC32D31F5FECEB9CCA8A05CB4B95EC3B3C31126CFD06CB6223531A643A9BA0974A38FBFEED8316F33F0E72F9403FFABDAC7CF519C138459D3F0FD2E54FE3A4FA25003192800F82F5382F24E50C0E7AEA20EDF5D24DD49A55C7B6B90376C334D918227EB7570F33FC95B7C3DD3F918E72F13AAD4912F394FB45017FB5FB990E08FC5693CBC30AD942B711D3A5CF3172F0D85FBEC689499FF6373FC933A81671C3D74AC5B7E5AA0DF14566A6C05ADA8979AB85022E8321FAEF0CBC911A1083CC72FBABABB496FA4B8A9D1454F05920685F2E7F1E80D5548B1C0A9A1F0DE40CCB53EA62784D3DA18670DD4663A9A8C5E25B5499653ABEAF8B9243C52792250C01876C65E7E5BDAEDA7096776FDC8B7E67FA985499E6C1B8691EC2AC986CA1A0A74964ECA607C21B30234C2F5F202223EB2F526FE61C0A56B2D33680F3F73B8D50ECCCB5CF500CA97DB60CA1FA5F18040082FD84D4C06DDCD9D755A6AA529106141B5B1F6E9BFC744B7EA1E5A4308D24FACFF38D600FC0444C6623E5F4AF77EFA89B50FBF8B48B183F2194FEE076A5B75E2C0E2946C02AE0C48511AB71E9DF8381A9362F3C4922CD0898313D24825DFD54CA13C2645A2694BA60F62C16AF90C60237467474EF496D4C77E0F6176C8D52B624D03166F04019F37FFA5E87B41DB0C6128F0FAD914247D41C789000B456D8F355098830C22934973B4627BC8A7D34172CA4EBA434FAEFE6E886D04637134E1AD0860DDCC64D381CC58DC65E9729CCEA1736FE42E6FB99B353462FB0FCDFCBE36A393C8F31CC4FF724D8388CE8A51C5D1087176132EEBE45F6C398290D03887DB37B533C6A28D0C7E7BCF426E3BA8330517F6F7DE7CD85C19F129C10094357488AF01218CEF396BCECAF0C3E645B24ED064A47EA2A854CBB4289F0692CD292FCEF2F055381D4A669ED3434E6244B90409D735655AA1A57C4A0328A4B91E9998C34FFB00B5C84D4705AA749143C007FFF9D958E24074AAC96F744024105F15881C3E8F6CCCBC0EBC674B26B2004348DE30641E3B71AF805C39395E3336F97B1B7F49B323ADFB8E35A8258F29F0D938E15424F2B668BD4D959BE85ABDD44A25E558C37918598F5AC34DD1F5D961F400E70EE396EF21A4B357C53E516AA0D5F0D064034453E3593F2C6E490CDF3672B21044D7F41E418B75E744CD1527C7719E807AD8DE1E084ADFD4FC4346BA9BF7361E5786807CEA87189E9E29D0869720A105F34E86ACD041D37E89A84BF619EB4661F96095541945939B6EA61FDCDDFCAECFFF68029E5ABD404EE04E04C463CA5981E849C9D51DFC9CFDADE1C8ADE3A5A8722718502CC31FFB932111E5A25764FFD264611F942E966D2BE370428B55F993B31AFDD50228DA231D7C019F2DC14C5B7695AE19C0198FC394B95DCC0E06720359B5AEAF03FBBB6726C50658653A44E60D9F5AE65BC465A1F088D4CE9D6F80289E91BA9C410C4F70EF9AD9CF558A14981ABE9E1F99E4F6F96A3CD43AAC1DC439AB2FC6A74648C4650DF296543DC65FB4C4C8DE12AC04EE50985C612E786E7F2808589E8EFEF0C736B66DFBCEF933CE51CF3D9BA66EC76A7FE8AAC7150522484C8A392727BA746BD73D8998114653D5C5E2D4D2364E70BD7509A487D5A8D341F3F3FEEE4FD3F695DE5A073009BB67067057E45FD1BBD45FC2B39A4190BAC501C07ECD20DF894EF5976040CB0847AC41D87C1F932083FEF85F506A2077B0E693F3946FFC668379E309557534BC308DC8AFD854DDED638D77B585BA83A8355729B7518B797FBBADE1082C86682C9CEF0D259214A3593A48729462DE7FB399B7E5772A3AC84406FE98B6D7BC725ED97D278B87B3DDCA1F8D95F34765439127736647FD454E5697CA76BFA8244184C0F1AD1516EEB194D90D975D43EDA486C47D24F6CCF731704B311D438994E51EF5ECBAD3F2BD7F5A34A2AE6C737F0C8917E42DC353FFF502139AF0B4D593F3473C5EB968FBCBFB977550918E2E927D2A31CD15A80D3C7C50D67F4113285E5E1DA175D6BF8992EE7CC6BB4EA1CDA4EBAEF957AC54D7F154D205FFBB3DE0749F81A30E7FC602422085DAFFAAD20AF66A0A1AC3115A82F7F9280D5B8A166270BA3744C40A1BF5F6B6AEE27DC89A9D2F5012DFC59294FCBA313C52595B4C9AE95C4A151687917263EC1ADAF42D8A364F322AA73176E66E74A2D2BD4D2E65EC0B7BFF12997D4754D60D671B64A6F114C01B024FFCA388ACE3ACED2F3104C59225F4077337258523E8A81A4F7C3EC841B562C4FE1E53B3AEC7B6D43B1358E35F64CDB5CA3B98505AF650495CA2B8E27E1764D71FD86BE909DC4D4101D64D04ECEFCD37A6911D4E539969FA2F773F9B5D9024ACF868B7FDAAE6CCF17DB9EA07572C7767196DE2BBFE17E0737F3AD8C420B5BCB4B0C9DBD4ED1D2FB4F20869BA5C669A45A50EE024316E7ED4CF3285D2BB9F54FEF8B84363532876A72F9582E1C91389C49176B0FFA72954D1F8617A948A953DB72D3A05089518C6E3E1694C1DEA71D00DA7330B137422F679FD5DB2640A4E5D38C5C5945DDF83447EC578B4D98AD264F7336553CBBD902EDE36589A0FB013F19DAAFF629FC5D540B814AEFFDDB62A01BB6C7943C7E4F152598F9E43B3C5F612114D219772C6F9A47D03616C7A03165635CFB828ED3434E459B87D0885734F1B49A2BE96BDEF221202FC4455537414856D26FB7C90B1397517064139E2FA56E661CCD1DBD3E36245D7F2BBA07CC9F15A5425F3F53411956361ECFFF662EE8848CC4437E59A6E008051A79B49CE54B6E85AE7B20DEEFC979A44249E3FDFD7242AD8FAF0216F5CBAC0160CB11CEC52AD35FDFB8B8FED5F1795FCCFF90A9E61E8CE4823B9DE9F016C4BFCC676525FB866FA842FCEFF935E45E51BD071E68D48805CC5EEF9171C1BCD4F8D1644F6B8EB1D18A5948C212CAF8ABEA746674DDA51EAECB50FD9A91BA49A7D4531AB7C19E7DC8EB20394CBD10D90F3C1324B759A9D34DF4DFAE389295246AD74B92BC19E97879A6ACAED7954423C009455A7984998749BC3139F8DB52377F5CDECAAB3F2C85BD7CBA20AD00F788F3295F5CC0CC2CF2EB37162DDBDA55E20FC3F770ABD0C565F6C138BC04DD9D28DC2BB7B6EC425B1A80DB119BF0C5CEDD31FBBC7FD190C433A3890C58C89F7A769CEBF2317B1F2777DCE71348040BB29799672EF286F9D3EA7A4909F511D0AF8D30B4846CB35DEB5EE2596981D4B4D93F054D9A0D6666338F40CEE21EB0EFFC2ED24D1EA753EF791B782A4C0F041BD139A7F0E7897E7C380D25033A133EA44FF0C33088C739A13CC41FD76C6E0C0EF9745552445517FCBDF671E02B1782B1790F0BAEA95857563B6A69532979A53940FD592175D3A2A0A1BF21876B1252C42FF19A51D07DE53980AA44BE18686B3CA1E7CA3455E64BEE107FF27C036FD3DFF56A4F34415173A18349D6C1A881D224BF0E71C5148427031877D6FF515CA80A6099D23644041474235952B275FC9364660683EB601D735F3298FEDDE31BA63603D9F310023C6CB7A66C6799E39590E44C6B47340D351400B85327D8993942CB03AC10472B6045A3D806942ACBE6D896DB962506496AC80A75A3E4B4F3C9BE4AF64AEB11082F84DC942DDCDF693678A072CD4A92A30397BB0B2A3311F8189ACD796EA4CD6D4E583B952DC7F56E31649DA2441985EEEEEAC98D0D5FBCD38F1B00633EAD489551C1760F4ECB21C4C3D97374D9DF47970F22F2E75E7A0F6C1A8B7D7B92020E71F64E30AA22E8D5B973D2316EF19A4C2BFB18CFC1081A36993218205E76AD73A9F2942289691450A0ACE5AB3B05080F51402203498DE4570ED45D7E514FD2AA664B9F40A3A84CC6203FB8DB8A67556DCDEF16DCBB9E6829587B5D4BC8F5C9B03A463E9CA4BAEB02EBB355268769B9B27F9004BA2B3307AAA90F6C8655B402CD639DA08C41A64CCB731AD2DC65375E230F97E8A7D960CECA9802ABB8BE7293E8D77BFD2CEAFC9AA17B24C8EBD2D87AA9CF5C09458CA01BE9B73DD50651CA78C2715116C6A1CBB8BD6C4E3138517BCC075D979BD40E963707541D8B997AFB95DF86316D8EB70D148B8AA557DE18BF4F64305097B99C30F4AF894B08D099B7EFE64F10B89967969D7466AF6B6916E9F298BBD2400DCDC947878254A42CA3AEEB8B539BE124930C6796904226ACED2DF5C471C011170CE153C379B771A8FBAC33A6A3CC65F92F9D5D96ADED7A444513A474F7420A5A53D59D0C330F08D00CF534F48CFD1474B253FD64037252DDB949D7D3A676D793F30612B232DF050ED1202751EF613624BC7E903B284C0E20CEF6AB3A4A3C0A0EED60096825270F39442DEF88C74DE3CB543E7F970317B942697AF5138A4CC182FEA2F2A458EC2F7A0FEBFC9BF6C997F77087FF04EA8CA69F05B592C89A37C539F277A029B4802B084F24A1A50996F90C8C3D00F5D9C7D5D68795C24BA1246A97BDE6F07198B00E62AFD02848EC6C1932B0ABC697276310D9B6A7181843EC9BA1611062A4485B9BB7ABC89B5C2B698F3DF2B191653107F19939ECB8D0FF0D0061C34392FDE47A30C38686ABDA65BFB6CAB497D3157BCC1015EF2A2FF93A9FA27779E949B7470D25C62CA978AD23680E96F3DC9FC51195F2C4E325659BD83A762EFA32FB2DA9A0BF8A86C74E182781FB816751993724A870EE36B71C4192B8D145AE9C5E8E393EE6A5530A8CDE8959D00AAAB756E363C297A11F34950C20C29185872FB83400452817B480074270226E516C5B3E9D967EA527FB2B9491E7207679CEB583E72B8E690EEB43E595F6B44FB6B8F909F193C339136B616C2BEB1241885D20C764391BD7879298A65A41EA079B298E5ACFF9664CC5CE597ACE833F606599F6EF8EA8C3E3B7C3AEB05A60F771580AC7884600126B35271BE3B96FE5EEFE9AA8338B9704D1C7C412686667A9717CCDF6D3B23FFB050AC03DF59958D927F70910789C57DCCA9749BD79C2D4F85D6BE80726333DE3E5C27D91E1CB47A6AB5FF9E5D8497A8129DB021354BA033654F964798795E290E8131A309C27D184E2786EC466904F8F9444859698D19A98D8C6EF704E766107A1F753E87AD093FC90A6AC434E4E1B5C7B50393F870F0808AE175F3AEE3C0C1D256F47985FF75EB5AA8B33AE049F0868A031E2523DDE49820BC94ABC39B49DAEADB986C6C803D5EF617C4D12EFD3603A9F5C9F86F78BCF383943D1A93D949C05730EFA4A3080E20833EDEA0C6B444825DCE120C984729FC45413D709F8985A13C7760FE1006BF61068797BC6F8F8C745BC5525340CD97087CB3D3728677A2ABAE11D4FF8DE4818EC5F46B6CEB9C231EAAAC42C34A7DF4F366F3EDB4C94D4A713297B1F6D9F083E4B59F65F6F8465F588F7D85BDAAD1E3652278C3B74ED1401FFEA29D3DF8BEB9E20DE3BE095A2E9A23C117C2A85687C8CFC08127B534EAA9925E7DF3DF78259E14669D7C228FB796C681108A420BE83E3330FD26376A3E2C97D7381E46D2DAA3329465A3D10439F06AA60F34301EC528013FFD1108417CB9C9BE0A6D8995E953EB2BD98A5F669A567F9BD72F9DBC8E9E64B65A57550EFBABE55BC80AE038F1D92D1C13F933B469F91DF248F270D01A704DF8A5E4BB16DECC83EDA86A0E32A2A1F77AFD2E7BEBBF77CFDD8B0B65C7B5D4DBAB3720C6FF8B13D9518AEEB79B2E84A072F4DF64BE1466FEB89960F9E19A1B646B2FB12A3E77C66105D740C0E2E34A43A20EE6A4D2532B584D89E6F693C424D7C15AC087D03586824AF80B433B326F9309071E9F605E1E6ADD36432BF83D3768425B942C99A812CEE50CFF2B2ADCCCBDA8B60A0C3F881AA74089402266CEE445B450522D70BC6E415857845DFCFF0F7675BA3B168DC46A0471E54C89F3875AD3BDA6842236B746386F7D5CBD1D84684BBE5597564FA42D6385C498D867A02D7F79747ABBB52A45F3C6BDEACCBD4BB4DDFAF4BA2E4084E5392710FEA6BEA99DB354E8BD0DB0F4830B79A6A4B4D815D6B01486AA986C3A8B89F73756A81245C092A86C098B84C42C5E6FE98264DA6689725DD9253C592BEAC31AB24C6FEFAD194590C213908820AC0223F93950A98740FF4144DC96B910BA52343B4E2801A7DD45F12A038CC62CA16F385AC6F2FA3337EF2BAF14304680FE83F77186EFFECF2D7262E6F23E5227A35EE812E2663E5F6DA336980F2EDBA6BB28022753F51DF1585CB1295213CB84A7076FD4EB4A828E86B7DCAB482405344A8BE88BF35AC354C75D3A2289CDDE9576EA40F3D4BFA5536B6CF337C16591ADAE9C02C08293209FCD3BA432E4BED9764DA7C62D40939D0925A029FCAB0A5049CB6BA445510AB95342FC7F8CA63393F4FDE9AA3F5F8990A1269BC3647510E225A0C2B16C178AE915DAC882FC9B8F92766A79BB5905CD348FAE1BFEE7FF1E990B768F04657C07D06C26DE39087F8CF2E25F33252E4BA9223FD9CEB243098C4C3D61EDF6CE68DE9837AC71E3265A8E17A067F842AF70ACBB4745D8AE9ACE752C0FC51B6AE06856E58A09DF7B445E90F8D59A7B3E5D8A87F90328E7642F3680FECC41101624529BEFA8A669745B9027247646C9BD0A684A73347606F984A543230C1177B01F3B73D4AB7BA7FC432565B79FEAA563EBDB59A43EDEBE6DEF0852B2953D4AEA919BF425F0E8FBEC28B5B3F140E923688313AD5133DC27CE06401E16C512B5B2C23F38FFD1F5F7774711E7AB2BD8AB1871869550A1F91BB5FFE863AE1F9E3546767362DB2C547720E33C1980471910AAAD94213C615AE61105714E1E77B5D6C493E36CE7AD755845AA2E76C0450AC4811BE593E2B6D87A7E76B649DA623E43288CB5FE3F21390BA634CA07041EA9F4FFB28D029F48A357A146CC8120D43FDF59C5F12915FFACA37C23DF6E07A1C40726A7A49628195B1172BC9F1F571DC58F7E5EEC130D021B7357E2D0628E4E732870BA65F5F982D7BD0FDCC3C8ED6EDFD62B424B5247E86A79121EA4575A84B0FAA83F4F113B03762B99F52D5018AB7512912F4BBE1116792E691D65F665FF348B660907CACEA0DA92EC832878C3AD8DCBDFFEB72C5EC9DB278BE347C8CF57E51A57C6188C3DF95805B3933E2A6E9983C48AB291013AAB2E56C21BB946BADA57C1934FB7A4F182853A6C6A63D862EC56FE7E31E4E9E158DF6D8F63433656DC4DB0656BAB0BE18A6131207390309123691F10FDEFA2E392F04876AEC7B72330EB830CAC2697E542E5A3DF893062554D90BB0D023DC050F26CA62F888899A6AD0D396612FBE7B8FCD2F7BDBFE8597E836D274E49318C07E6D0A4E2EC011060CC29C221EBE2B15C91CB30D034CD948BC48AD17730438B78C38AF508C4BE481C33C69EBBC6BB4765A60CC1B365028897C9A4EE79E376F5D1772CA93782336AF48B41E205C00601C806C9BEC5DCA2E324FCFED2D7337D662B4FD1EC5E056AB2C14CC05247472D99A7CFE540714CEA03B27980131E602ADA7720D99F83029E4CBAD2FFA1542331D31BE4F2B2C2F0DC52C2D0A21B2787AD3445957EFFB83C7AC57E71D3DCA550BFB5801CF75FAA400DF29DB9430365D4802EA16B6F91A1BE58BB0CF6295643408D5B4C2FCFC7F72E7098A98DA4EC386AC13953FA3ADE7BD3748FF496A7E56AAE2987B2E4589E8556DE6A6BEC4C05FD9CF7374F7A469101E67B0BFC4E2B014C72D56A78851FA15E4B066A17CF904C637B16B15DAB72ABCC54089E7FB467286C00DE2248E7FA3282D16B589FD1693B085B3EB73716C003845899A34A84077157AD7923C8A3C0710AE74C6944C96CBACB1D9CC97316844157B282FA3C569E2D1BB9CE8E84364989B543DB98D0A9D8367B62C97B1381D2E0B57E0516B329228D931D5892E10AE3B2A77B1EF1A1BC36BE3E7DF65E35E8C5A0AC73E308CAF336D963A6EEB7D050449774CE4B8DA40DFAB979A949FEA2587895B0F0E6F469E7F7C94290F3BFF3E5C1164AD5482F04E9F3FBB033E60E2A9A05034670F668256B1FCA87D87D2941C791FF99DED969B46F77E80AB8EA9741494373B9C169E3E3B07233E584A3403A9AA81E5A3CEB6743B7FDFBBF304093A27DF3E5101F890846B5B30C2EA7BE092D51D9F706BCD8B7C3D992691AEBFCAD27F332061364AB249E1014925F6F2FC4378870BEA356A02B311F52F2FAAAC6758EBFFFBD21D72C810FA52BA1810CBE462FF7B1B6CBA827E16331223ADAE73F2C2E179BAB871E55498C0BBBEE14D388CFF91B4A0A223A8A9A057E643A969AAAC50064B40D9EBE965FBBE1DD0C0362E63510E0E6ED4B0BF356ECADB6CCD2E604369F4C1BA8B43315AAC93ADC46DD0F9784009AFBA3DE1F6F30CF27575CD0F190C4289C6F1056AD4D6F1D1C7FADE11EFF84E0B1BE01B650628F9FFFC2FF61AC3DBB2315F43ED328146EA86E28E3E49766EBC6C95343CE3BE8B15DAF84B502A80ADA9F5526AE94C1EF4BE573F9DA4FB4868D8CF63FF6F62EEA16DF77233C1B7035BB41EBB8206CD4EF25266FCF211F80FAB8D8EB6AB658D335DEDF92A094D20682B37499237DFD902EC52F646BB0A36633ADEA662F013AB84E9217E3D3FBBB0A4CC0E7D26BA6C85D70EB67B2AAABEC5967EF682937E592A31D100DD2695863DFBFAB3C2701152846D8192C2907F74653FAD4C23E74EE6A273977873A72A1BB8BD231E7BCBF268534C40B2014D35358BDB5FE6AE9EE862C3246363DC5646DDECA160DCBC864152D8F5A401A5A4FC4C5D1BBE9B3D6177F8BDB43680E668BB75CAB63C2CC3F05825FFEBF71304CB496EC14932D4755651040463DD9F747206B743139CCEAB5AF84DD4856A04A3061AFF094526FD54B5A3B3FA21B788E24526F22AC355E610D94CDAF422EB6AFED3FBB719D52C3C6679765A78AEAAA0CF272A3BA97C005F58CBDB89FAE33E7C68714C48C29B417CCFA8B9048109F3B289EDD07832BE39B486F125DFD6295818D9EB4FEDAEB2B3A2DCC987D4CFE6A202FBFBC948FA67C0686725397907A0979DC1C94B0CBE4BA7844C1E895D90B5923B63B365E85BDEF31B5725ABF4A4F4A849C3BBC1F44A09832562CD6118ED258E74225EBFFCB23579FC6DC69AD727970685A558115A30506793594641EBC48DC13BCBA63CFBDCD9EBA220DDFEC0835A9A1DF6A7B3B778183006139268D2792CFE77C1DF0876104BEC6F7774A7B1885F040F10C04D50F03EE02F97AB67A9E1C5CCA1EE9917C878C4988D85674CB122F6B7BDD6A75465DEEB23650247DA3F4B92126AF7271E33F7E275FCBC8EA4D51F134E4A0DF3F39B0F01897DE3A03FCB24350C3DF2B254A116748F317898432DBC4CBCBA24C67A083EB3D7B40C89DF2DB027FF2C63E9FB3E95ED46C306B04A667ACDDC58B0D0C6C3492C22D098C8DCB9872CC43C737E0ECA42F61FD80C97F4C15CA82C42F998F38E172D93882AC65BB348278972589780B3B39E88BDB4A96627B1BDDEB25DAAF915DD7056D9D5EBBD1709A0D54DC3988EBEFA00500AD15C62A7D95D87B500F8F70B0E31F82A630FE4742EC0812E54F50F5AB911CCB1E736C3168FB9C4E7C9533A6BA3FBA0EBBB25CB32DFE226F63727B7DA57761F7475666EDB64F6954D170AF21A99514D46FB60F8A7C3EBEE5E60D20571F1B3B0BD1A346ECAEA84CFF8726BCE508BEA6012D5BC1ADE080DF68D623AA14F209CFB0880FEB0AB23EFC0205533B5DCDBF08DD04CB798EB9A91FB01CF68331A30DAD3E9B272E3FDEB082354DC44287462394A58EADAD61B249D7A515C7D30FBEC7D6A4B06845058F3BE5C57376E38A362B856D66D6D554F3A9C88860D9374EF091764D4032DC2A1F8ECF2F65C7A57B3FCC8AFAA091B15193F8E1D89948D7BCA3C4BB6700B10D2FB0F5F7AA60FE5C1314E2AD15E62771D80F81E240730686E0714784AB975542A997D689CDED82AFB7FB58FFB940544BF46E82591FBD2D5027D07D88596255AB3A8A2A45D0A434F18468DAD4CEBCE8FED139584153EE219752EC8157DFB746EE81530C6D3AFA401B07CCBE7FA6738C05BB445C4B320F623A888A54C37DB037E7AB13E963C1DB306CC439888A8E69EAF0B5D85476E731B2367A5FBB1340BCC6436AABE6214892CD8CD4AA149298D969611909D6F085D7FAF43E8F3E8E123E6D29F2DB8256ACD81F53D70A207CF2BDD443AFD532100507EFDD453D8FFF935B1BDC568FF12E3A10DDD63DBDB4D4FACFD990F67CD1319F4E5DCB850FE605E90CA0566C3155F73AC20382DB90D6D4A03467B2E4D603068E12A9A9E531BDD71C6DC5A50CD887C5619ED21DD30261EDCFC6978405045E164FF6E78DD9523075EF47878AF3219144C9BAC410979CF68D2B6996EA6E81BF0E0A62CFF6C8A75700A0F5501D34BCE6FA75995CB9E240B8BCA7F9F8A8757B670CBDC7E9BBF79A70EBFD23097A056B03F805C5BA90ADBA6E110E1A77AA6256991A81C358F2664CB98B887BBD6C94B087907CDC0DD1B7F50F80E827B665E37BDEDAAAA1C1D7E1C8B3D8D8AED0203B85E8824AF1B5DE3476D0829BD208CDEEC628B88E45CF124383EC9DB6FF82D590FE5CF5E021A58B1DFD74B0BBBD4139F918704E70A994C2045CB2707A6A480F1ED8F27517C2933647A8CE49CD30235059C5396CF9D8EF538C630794F754F22AC5CC042B2C28B575D5283010186B1A7A6694C0EE16A1D7A7BFF4FA0FC17853BD7E163F666FE4F2BDBA1F398B3FFF482D5A2A00D5990EE77B3900CB31A1C29FC5077044017CE9B5C1F3C4EA3BE9BC763C2804D0E7BC2F5C4EBCADBB51975A5D6EBF3B2F48FE847354E9A5FA2ADCE1E96ABE3F1F7971D318778B0A53CA6918329760F61FC0F3033C193A136D1F9E812D7CFD8EEE4BCCB1090B53948E85FF56922BCB88C4C165911A011FAFAFB3E11B176A0F50D4FA8690A2DAD06E77098AEE6C31DBB8DB3BD90820530D960E5315C1A0B584CBC9F17A5756434AD03DF1AB2035958FEF4D87F76A811935C2B3E4511CE2593C8C2FED7C261CD9336FB2AD6566D109E6AC62661F5AFCE80DB7816ACBCDA1E4A0B0B0B04C6340353AD1EC756D09BB2CF146E491A6F8E320FFF5442C86A053A5A4E95ECD7F7ABC7B82C2E3A470A8ECDC48489CB5D4B1BC91CF9F02A6FD0753E8D6FC1CFB3C3D1FFEA9C4371DBA7FD58E2F3C0D98E7DD2DEA584EC97E9720A50EC2CFF384DEA01C72D56C89FC365E5BBDF54DE9DB7D9A435F5A7EA14CB4397F43E3D592B23A6B26FEF3C455C0F949C69AFE9A2EA3BECEA68FE6211F9C3E9DD36247E60141770E7BE49E1A00CECD10197F3849F6E0E19A93933571C7220FE2DDA04095B2A50585574929097A89791D14B0352DB9F934DF8B897D5DC62C63D0996FE09D4D3C25FD51663607B50D45A54D3CAA7905C3F449F6D159FB9049BDC56680F8D4B1B4D83179B47AABE699EA4C52A835398A98D9A23A2106AC442EF790DEE33A12ACA2FDB3B5D135FBC0B3D54F4F02CC1187F14E2BDC272A69F219411158CE20E6BC7629AC76BE23DF0BB06CCAFDAB174453534103773879B84A8315038A83C88B0A95BC494094CA697D3D86836CB397AA92EBC6EEFFCB2DE942BA58BFF32EA471BE971DA359282A5421E85F947FEF1ABD65199E6AD9CD9B913B1F3198D6CA3F5BA6E5C2E5D3E212C88A1DC9A389B95BCCE6C4CDEE49FD7D05C11C62812C7D9AC53D886FAE76516377725C44D9A820B48D0BEA26855518AA2AD762600EA304422CBD49EAAADB0E07628A2E5AF9DDA64C6712C13047385D5C68260C97C597FC00DE0E0A669D00907FD90CA3914FD4242BFC7E0DC76560187B40B554505333B4C529DAFA8C02D8994BFA032A2BC0E2E7C230999D36C4E9801446E7433DFC2E97F7BDF1948FD080A1B400B8391AFACACF791D01C3F7C714B0503F1DEF0690A0F707E9869841688B671CA7823CD6A17AB2B25A593B0648B053CE9B92F62B1B8B5D93914D76594DD78EFCEC84624A1E168013F08F676ACC7C3E1DC9170DBC95F10B6D84B9F282AE9225964706A6C852C0795882800CFD0C65C4BFC0C81D7FB88EFABA6D1823F2728E5117DF6982D19CAFEFC1CA156751E00006D58789AD87CF127B29615178BCFBEA8D4238675F958DC4311DA774087A1AD710F2978633BE096BB71BCD69DC03F935C85B06EACD49A4C3E7BCF3964683E3A279A8614F5BA8E65475A57679448A6909A205BC7353A894ACB43F7EC2008ECB0C3A63F223847D4156028028D4CC554106D2F04FA7E63DACE1FC1AFE86AD0D52E6018C8F29AD9AB0C4DE8469192803326CFF876A05B9682CD66E17DF0218D34551265833170DFB37147C8BE080242AC311798FF28BDA11FB004C2C1C7C1BC535F22A92670B70C9F367358D1B1CB0DC021927F78F8F1618415B2C0BFFD5AE42EFC0657E6853A0228E76A6DC91A8E166047968AF9529204C84AA267B24FF6940293B38C7592D7019742EAD27CE4A71A7829B4913011DDD9C1937D1C685A36A03B7ACCBD7B1D9A4859C484FAA6EA4B4967C1150BF057742A19F8467915AF8FCEEDA4DEF909B5D9EC407629BB5FF2E2C1FBA23C070016E34A5277FA3940D517C19243516B197806AEDF9E29AF467AACAAD5124652D39E39AA4A09A9222F3899673D7A3D004D3DFCD7D1CE569425D5CA2BB3DC54041D86B15C6203A28589C833AB4BE0DF0B0C90F7F18A825DB928D2776A7370C08FDAAF6DF5640C0A647DC85719246094454A97621D0509C3B8285482D992A5D426E9E9E30B687AA59B2AF59FE0E822F77161D67A17FF6D83D164C93F6C20315181E52606F0C3C8F93147F984D4851D212849B35D06A4A9D0770357479419A8AC0FE9434AB652A928CCEA2D9A758478596CB44DFAE8CD3E339CD95CE98978647F29F4B41637E16D94609A45E14CEE7229F659D38063520FEC0BD29FCC6D8CBCFF57C47F00133A657F65F7CD91B708BA95C345FCB11FFB8C3F1BED5851A4485D35A2C6ECBC437EE5C4BB8E9629B2D0EFBAF35A4E59C2B69935490E1BEA6251584105AA4E8CCA3FEF56057E50C30494FA5A29C76B09BC24A7A5C7AB7A0DCAB554FA69CE28E92D55F9F91A971ECB3C20544E13687EBDB8D76615C82487A8804A0F17A322DEC7F80C26D558ECDD5F23AE6FD6E49CEB88AB62F6DABD5EDF170915AF53AC38AF2BD11138570428D80BB8C12D8FC4B6089F5A427E5C263C2E0402A8D9A95BBB611B06E4A3F469D73D9E0A0C7F9C1FE9D479C04695B44F014ACCFEFD534B6FA23080CA85FCF9DB5640F049C7250933D491C4B90B4545186C8D36407EED5C98910929B46197CC04303F633852CA875479586972723A9E1E780C8BCDEA946769B26845CB9D888AE26C5C55229BF1A3EA8C886195F95A6B1EAB8C2CF3DD851949E671A55DC526A5A3800DD8E140FBC4F3D8ABFF5766C29ED9891F94E9C0AFC6B3DE84CA4908DE484C40DAF2F212166D1935D1E05C498F9C218B7D162685222D0D4AC7DEAAD4B222032E3CD2CC03C9045E59AFA6E130925D721E711953E429D1A3A034590F382354BA9A27C830178849275E65B5F11F965FB68FBD4C320C9E51EE29D308AF82980541EB3F0DD3A053A992A4F8B43470364C8566BAFDE56D5AC9BBF7DD4AE2FB61E87C12A7324AD41E9DF56C8C7F3C72C5A4F4255EE395701C5857A3613FAFF2E483CB22E604465FE98E4399D95C61D5B1D0358F6A3D697039CF81718883B2571C119CD0DA739F7DB0122284E486644F8DD48857294C00EB8F562A0CDA6432FA446F46841EF1B8AC16C3D52BB92C056A2CF482FB6AD5839DF782243790A48D33AC0E051829D0B07A517B2E832B054991B0CC178642F2144468237D72F0B0D0F9E972EBCD2C5048A0368E3B2A3F2E13A8860F5A0EF93E72F7B4E99B1D79CA43C4D35132325175132EF2A43A3F86BAF54CCB70592C281562F81E7B60364D1BD439E7F47D306C4AE35CA58541BBA6108B286EA5D7BE1661A22D563A9CC256E1225C7AD11452D60453BD4E62C126D9B1F8489F3ECDA022880940D61713D7153D5BB61896F3EE6A1D0E04014746751AF348E749D7C135B32FA75AC8DC5966533FCB377257F2811D139F557069B55DCEFF73BDE93B506FCD466A3351F3F41C5796158133A45454461B1F7BF55CEE788C9EB27C07E34A01FF36CB34CD77A30BA266EE36C3F85496E567F6019604D6CF256C5F19850B5B03F2884E3A1FE4E4165F3DF0F13760EC720837F6A12DA3AD40F6005AF2616A4391516B8163B399C0ED7E73228DD05038574850EEC8E2556DBDDC47020E4D2D2C3518E3388E3DD91FC24ABCA0C164C3D36F2564C93A52B1719BC649F35BD43E4AC81C84345AA0C31E23F3B33F6F0EAD37D8247D25EAB69E2181A320234806710373C99399918CAB2B5123243526BBB7091DC511BA20512F9F6F31DEBEB390ACE57F08034D18BAF3FB0E36D52CE59C6F286573B9AABDE2C1A046CF0DA2E1DFE813AC696786D0758BC5AB1E265575D5EB17C516ED94920C99B9DD3FD440169D1FC9D4A1CAED385D84FDA2F5C1A0C1DD9E4BDAF0B495F816E75D97A6C05A37E3A39F10C3C410C9F3F6BF5281178416D5522C2328AABA2584BBAC411C5C11D0B84CEE24CEA59125B8AD04A9AB77CC410AB39EBE628C89CCAA5ED7471EC5380E4F478D5DF439AB3955BFC05A2E6EF0C71B9DFF784C6537615B86778387869C732EBFC18DA999161C95D8405AF6EACDDEDCC3727100FC7FB7D369CC96911ED6F9EEDAE53A0F8C476DF68E65079B48C3BEB9B250D275D92A43499B67558EB4F393A69D2DCF28CA7D6276AFF64251ED3F50D6C9CF6C265C2159F6D1FEE0DC587A9E9E16A0571C384BB474375DF3721A32BDE99DCA53D4AA293CFFF6699CCDF46714F0FA9554CCF62AB4F38F4177527FE575E80EC5ED80D50EA0B6550DF7F2481BFD1B95BF0A971CBA540205B33B153A3C1F30121E8EDE9CFDDC7D3190E089E570AD61457A7FAB02E7418632D334F04603FB8ACD1E2713083304A70E50432941385C03E341E04580A08E63DBF3CD272D28DFA9EA43FA02F00413754A0415B87F587F7D6A39C8255E61B8348DFB39E0150027E1911AF9DCFA8BF572416B190A70295BDDD5C339FFA478DD0B62E430C6B1EDFD34FBABC50778D5BE9D1E1E52DD2E483AFCEFE91A46B3A39F4EEA6E1BAD6B2A962422D7227F3E5FE076D1C76063D1177C9A788294C4E8B4B5D6E751AAFB3D530129EC354565FC224C853569DB6F529E88DE9E5F504200989721F16D7928D46D199469F5004A3C87F8D3398FEC5A0038DBBEA23A59D429CF84AD5A42F5E42CF50A6F92EAA75994AD5D78B98EA547F5600C7ACA5CF3F7CDDFF3E200634D4366F18FF39E4CE23A18F6BFDF42C9953E1BB50E78FC5980470BADFBC11842A0606F95EEFBBF0101F23C477E8ED070855ACF60ED302FD3D5C12996884F9ED4CC7ACD95FEC0C2FDFC2ACD12D288FB4E0ED99255B3B20221A69AF92833F510999E89BD583C2388DCA5E83DD77FA93066D7BEB380C50838D7FEBA64EEE47EED2EEB15C6E3D503343C40B5AD687D777DEBE478FD40B50DC404113325987CB3073F9084DB63529ABDA4C08F6C22FB6A0FDF9E7999DC9DE471D8AD78CDD357873037CE2AC80D92F1F7C2C09582C353B6FA1874CFE3FFB6141591F5C0640F664DCB61729DE0064E7F719913EF81ADDB1498D8C84E7EC47D0AF2A6849605B57BC57868744E3D3CE0B6EF4FA66F91A2AD1ADC545E0744AE0385AC795200D08060130A30434359B55288C4A388F23E962D2AC28702C9FC72F6FE4B7E8F08633A2A1E7C22C28CBB3A44E22225AB6D4DB003F0ADF4D5891089A5684511B40641D088340B4C7625B1EC9695A2054A4705409EE158AB4D1A73E2C333D88D36EC54E3F805D91A4290035BBC6BEC7E82CA09835277D61A78B2ACE0EB0398B8BE25CE456449676F87AD20CFC17D2389539B04EC00C0718CF3C094D4C0598B51D35720407E4ACF79B92430B642DCC0190BD23D341B8B5C3FC1375AFFBCF40D12880ED0E8D6634C38F2E43B1E2A9E1C585B3BAAC9BF5AB7A339F603A1B061ABABF4399B2CE152B2D16A81B3AB407C14D62D1AB954625832F6EDBEF0ACF4BA4446B06D19ADD8F58252EF60B1766D7F97BF1945E8B063329775F06A7BCEA0F28A6C2DF53ED0797933C183DE7130F46AEBC856E7F44CD70630D1A1F893B9A657EFD34F900B72F78BB8CDC132F50BF107A50AC2F0F7BFE7CCB4D1B278ABDB953F20B61A86ED40DBB06DDE0D4F92D27DBE41819201A9EE11087895D5AAD406F1289AC93F8D8CCE0EFED1263BB53F168EE047233740055CBEA8757A4E37CDE9A6C42608CADECBA517398FF15A91D4ADE2917FD140C69E3012294AA3DD528D382C4AE63FC1F988ACB4E207D81480588D1712B33CB32B56BD8F1BEA3FF7433E7AADBA8C679ABA6454DE3DBAAF11A839028F2D4CE9020E8362CCD3C58C1E1E3C8AFAC9CF4C7D596AD4D8A486080C9BC51F50687709421D4D47220F4CBBED798C8BAC05EBAFC1B4DC07D0702A9B24CA42BE2C070ACD8EEE28F684F32B274CF6300F4FFB6CB8ED9936345342C9F797DC0FC1DF68369553A6D137F2F17D729DF245A50665AF62ADEEC3038C5A2B80F53112B6ED34DEA2E67CB07563B6FFCB38FCABBD42CF013EBC9122346D1829277DC3841DF3C857D25CCA2728387E52FEF79796A45299360ADFED61E8DC6D390AF0A72760BF93CEA7D63C90E0741FA070AAE4F6F65CC3C0ECBE51D5D8B1EFCD7A5DBFB8AEAF177D28C5D1A54D6B755684A62513B116A122EB8A92DD06F4E2CC243B6FDD4AECB0484984D092C00CB9C75D174AC7FC6C9C94788A12DB9C506C528094D4E441B7EBA47D80D9514D3BC414F1C6BAC92FE348B387AE44596BC79A83D4A01110C1F39C3F13A656ADAB386E6D4817203C3903C19382635CF306AE8A5327F8D2CEC2E5512E90E6EA6E04F81E1C9FCA66FC235CFBE2B052F470FC2454AB41C57F7C733641A657C228F5B7FA4913060E4E12038295AC43BFCD30EC7DC110B9C7ECAF6E8B30D011CB25DD111E5AD3D1981FAB1892A2C21AEB470B0D373AD0775917BDF54F713784E42B4E67E3A079EB739BF37261C1B920220F725247D4F88B329FDE4281A6848958E5D76F61B56A2028BA9E0266410E1CA8CF00E3CD6E7AF2FC0DAC9ECD30F72D8278CB7FD187A682D04A1F171F1F2A8566CDAA91F2C768A6B3E1EDF72CA3E20FAAB7F68D415AD050D41C368ACAA2C37FDA8A6DE31D4043FAC53C777243D4924384F098CA736D740330E37F7ACED6300190AE5E64F32E96701640CBAF223B4A444FBEFBFFC6E0DAF76FEDB424C65602E0D0D065C8056579DDBA4A4CF6BB63863E482314B884CB98D72CABC5D2596E732449ADA15F493B862E72BACA920301C985AF63E2CB21DD6E8AB5D0D100C33C271FFFD1D1F40C5659E163E0A1F4532A2D0787E3AA79A1346459C5AA1C864883570CC7C098699A4B8FDA461086BD4A56236595E27183CC96B95E509EFF899885F8481CBD205C13033AC887278A4506552625BB6F0B96EE19D2B226E6B8A68EACD1252C8809393095EAEFC79C6BE2AA5803E9970664702840EAA97DBB65F41D384DCB41393883860C0FEE63B89C3C535180CDD12EE4826EFC0ABEB9A6078BA006A1820674398165564D0CC368B1B095CF265373D4418FDE40192A295726DFAF6306175A0BFFB553815443C4731A0285BA9E91BEBC5841D489C5AEA9508665D4E0546E9B764FB92BAA09EAF882A755A97C60E40B2BBE8AA517D1366C0C6CB45FCA8E1CE333B7EACA6D91F81BC5F8FC624AB8594CC0C692183A746FF265E927C175B7BC59CF51F016E4880EC86AE3CB849504990F0916F87167EA19BA6B4363D2716DCD365A6E0E8DD8E750B84161869935A5A2B43F7B202DEE6EB988C7F176DF4F7F3C7E40303FEA71E4030A3A6A121D644AA2F49AECD26DB37D564B661C3C76CA7B778B4C6E9C4C3C70B46A043AA36540F7FC5D9262E27F4F8FE628710F1F5BEFAB96ADE5BA76CA6F5FBBBA95065A1B015B860DC23BE12FCA739F446A4AE538ACE8783E80106F9DCA475B527CC1940DA22E88DC111CCB3CB9F1D80C37723F033843F0B1FDC4C640DE3E5ACDA7D30F3607FACF3300CBB13D05455D4F6E57759218648CCDFB011ACF4B8EBD45D71EBC680017D6BC06779E22B54DF0EB03984FD7FFF847C80F542634EAEC1BF5CD33717B220D41C026CF6F2DC62E296EE72642D718FBCB51CC70C8A24BC9E170FB45C8439B21ADE8BB32904210EF03E79D3CD437432676C3C2F6B0BFA7279EAB466AD5B67EAAE325A09F05C82DBA21AE6374B4953FC1866D8C5366E86FCC1B4043EDA0C006C55C1DA68C60EB860F383968FC734846CB608519F42B8D23A6AAE366539197514FFB911C2C6614A4168678A3AC03D28DB212233A3B616E57D61B7053885B60759FB1CEA924BE2DB42BA88C12FC1644072EFA735D0756CEDBE3B420BAFB65CEF2D1801E0896CE3630CD3ADA9D9FA027261B41CF52B1C9D2F7D08ED9D45A6B8A57F438EBC75200384CBC59AC9237485D143E4EF509C2F852EDE5934C7813A7174E6A20A8263F1C318B45FB627B4507E12305BEC35AE7654BE7705B6B78BD617C02CD895A0D199C5CB0B051015C0B657197151F797BEDDF8E46FA1AB0C018CBD14FA15FFA4D133352937A21AE53558CCD905C9B752DD1C0F944583E74022186362D53535CD77BD7ABE0CAF0BBBAA45AAEE62BC56343FB41BD00BF460C5F1CA921CEE133CF3A3C79F37ABD6CA3D08A35B724E86D65FFA69365A47B2290BBBC669C058AA479DB71A5A632D858A270DF981F95A4B0DDE55A877C9E83934555C31D503C6ADB952C7C4BD3AACA5725D3FEC85BD30784517A89EEB8D088EC9B32CFA0A2BCA8FEFF48321DEC6500230D31C9D59646B202336A96C645D828535A7DCF2E1511F13272A5248AF57EE2C819B7A9CDE8A219522705767CF52E29FE8D4D6D985FBABA0B30EB0A62B9F7099CFA1DE0B5658E1DEE571A39A3CEB74A60A999C8692AB641DB2DBF1C1685CC8563A699A1D90FCF58A359885778BAFE3290A84D43B57174C9CEDFFB428576F339719033A79BEC673DC9BC9F6252FB27AE4F0B806EB1E709F716CF880B81DB3BCF9032BF485681D47A0583F2F2A8C45B9B9B2A4E9A75BE0ECE8AC838859622C32597E3869FE970325597398896768C5B057DB68B0EA7498ABFE5EBAECFF689042D387444EE996A967070D83ADC3CE290802AA069E3563A9B81B8C75491BFD9A6F81C18131F1614EB61A5F0A8A90CBBC8208D040D850CD1242429E8A2A83257E3F604B8B3CEE917FBF6281CE10AD94365DD743A93C752939D555ED9E068E3C973153E396F8342A67CD071A24EDF34DCC440E3DA23DA7915D47E2D1059C38948A1038AC11DFA5971D3996F0F7CDE972435503FDC39C58C08DB29023B27D249EDEEE2D5B98EA742C557B29E12A5BDCA22E82FC31043167DB189174C16F6A3DD1BD86C323B9832086F520C485867D181E8EB7D91F04A2EB9728E6ABA0E0DF2E6D28FFD256428CC19623953291267C58150C0E1ED5D0BEF4644673DC06558F292B1CBF1AADEB1B4F7E13958FDDFBD461E05E0EC54D7E42B82283C74FDED405C3BCA57BF3B1C8A5259AC48F8F54F12AF77F9CF77025A08BFD43FDD63F651E609FF17BA92E45F4C506142F792C6C5239D564C0E5FD6D93F88E1FCEADFF4DF607333EA0CE60BAAE79828424C5BD3E741F61DB9E3E29753ABF8C27668B37F64C758B9AA74B3EA6EF49739B1E3F62BED66411FD0B833C3AE622AB47420BA342B30C4791C184D919FD406AFDB7194F0F501C8FC56AD4A8E9BC65145853EC1F28CB61138C36624B937356FF6193A5582D9F1B51E887C7F68190DDB58A0D10A01F61B8D108A70E9289E4CA1D38516672347DCCF5EE3058AA0877277EF6E5ACC4F302C30FCFD9B5DF593153BDFE73FA3340E6983178F86DE73F9AD591AE48C21A24A0066730358D297F3D802F1CAC253C36A9B63E7698E2C6143C2DDAE10E0AFF39269AA222132F811C619732AF8917B807BB82A1D96FDCAE65D7580D6369AC30A2AA5927694D8C084BCAD28181D98E91068C008147EAD1BBFD13E035A2CC4B84D6E00C31D5A6336B88410FC58E00753C924C9BD9F46210CE48198585332BB908787706D5A4BAFD2321E38A0D0B459702B8800890936A965298CA3BD6A1384423EC99B70C3E458CE0C311B7E97F056AA6BE91EEB5671508EA5BFDB233C097D83845FC9D311106CB4FE7A44EEC2611CA2DB5D5D88908430A1A85A46CD43252D070FBD3CEE8BE40592F3245A5AF5DD12DC8AD6A8B5405B79BFFC44BEDAA27310D86E3DD59CAF7E2D4A959C4D6D8AFDCB444CC1F015FB152ECACCB12606F5F97EA81197A9B3166D6ECB28A15C263B7499F6892464D8567D5FF26827238BF3381D08F27F923EB12E2E2C9D976A372516168C2904BB147333C44D52C18A6BFEE3BBFD17C302E5871D1A2386E746B9AB9B1B5FD66713D4280D7C1E25D14E05B70707DA8C167360D1A8EB6B33A8401428BE98D31C28672D5512873C9CCBAE9BAE2C4AA3E8005D2341C21C08E29849BDB5385C810768077BEBFF3B6DDC59008F39939FA3CE17D1EB194C5419457B8008B6F2E23F05A8B1D5F48EDC17163DB4DD3614D7CAAC3BC9F843A1C3F6E9236A323E52598C1A8D97A0E9C76B154CB617B7C21D5240B7A5EAE3D51CD26FE23679AAAE69C706A7A57BA4EB5E93247C0028579375451A6A2AED089991284ED3FF8C648308C543AD3E8AE1D785666090283BD9B372A71F8250776E3AA65EF69CC5C7F3F9340B1C881806A6B7F94E91E85B728631B88FF60964BC952ED3840706978D35592DA09C46EDF08B3B9B156A5EB3E8790388274612A9689BEB60294E4A36E09236489AD7E9BBCD54B2F7BACAB2A9931E0CA9CA9593CF1131793344F2326ACAAF6B1D7170EF7C465B2B28E2A1E9D087918FCF46806E2BDE8AD71EBC409419EF25B7C3D469094726E014BBB790383C5832A647151B2A60E5B0448924540F9D22E7EE7F588925F9485068EB9EC7139AC4D2671C06CFCAC8094E9FAE0F33CF90E45491BAAB6C7A417A66C8F3606F09D8A8767679266B74C98ABB0D5A5C6639FC6E9B1ED05978A5CFB1BA1CE2F90568425AD6368717F36D182D6AB14F75168F709B34A58F61510B5FF2D41B9074F28A7C73FEAEE181F476E2B749C0A0B2B02E9B0EC2B1F8BF9CF323F162AF8F447C561FFC9843836531F0D85AD72AAE3BEFA53DE39BFEAA4FEBE97BE4FFEC7A7125A76C69495C084BA8FF7457EB48CEA33794606D3A3573BAB816136A3B1F262D0C46CD1A798D383287A31872CCF98F136AAA3EDFA4172F1D8455688754D1EE12F91B3D18576BC6E8C92055BD4D31DBAC156C366C60F23934E6BAEA41FA3240AB65DFFCAE6FD52F018B56D0EAB20492167DE3B4F22365B35669C4AF63B463AA21B8E140A5624EDF8C5C8988F7E29B4846289328BBC5E3D3C4941EDB3562F1DA71CCBF0C48A14CD68192545465E5B849445696AACAB16251E4F60681DD2CCA4B4CDA2AA2879EAF70CA1678F3E755BB5F246C693ABBE9C6C21B573D527B524B975CA9EFB116084B6943714D054A213D694616E6117A81DF61541F7BFDA18918567EAD821C40BF1A64B15150C34D8259E054B4E44E15D5218B4A4F72678E8587DF9108ED48DEDA8FDC7F648B0F9BFA62ABEB746C2834DB91FD91910A527FFA50D6BDFB1F0063FC376999149BA2D416BC8A2F4AA4C5A7F79688649DAF499D0573B0B95910C4546C3D996C821FF6C76F2BE72A42F80715DD0D142D6283193420C290E87CBC95430ED1B047834912B69428C80407F5B6CB6070B5F8D64E8C2A7041A52A03FEC6BA22B5F164BEC45A3A226C04C876897F00D2DBEFD623AB5FC5BC5ACF17A4938E9B57200AF6C788D63490598A73D014B8C63851D0D5868B7B78B288D8EA2F0A7A2692E372F8196039D9E873CC413C911BF8CA41B1641DA0D4D41133BD920FD73409C7C6032BC5569B1F1158421918BC9E9B09F8FB0CBEF16E914304DE0B2CA2C37B43E7B0FB8383DEBC29608A5F5135A58F7C677520F7833136A45DD2BAD97E14168AF3B3339ED0FC145953B6F7566252419D946EC243D43CD1E818C8675599BC1EF69364DA0DA10D6C642E0CFC6F3711BCFD658ED8636CEFF41FC86CFD6BF877B4BDB3B5AC6C306E26D5D5D87291C1D644277F7170649E1A438C78F3CBDCD4BA8022D2DCF6C27E036B9882964605773F885CEBF65DD4D9D2E22CF23A1240F53952552099CB406D2AA9C1646D58C2EF993F4A2802E2EC6F572274961F3FD9BC55FFB576440C5BE5F606995799B5BAD947EA8A5335FC7002EC5DD0B92ED320F8D5E4864E97D03790317FBBE2A67D05CFEA696784A4AC9ED1480F2E1A47C7F91282A1B5456B160E3DADE1A57C8E5EE48EC076C9C89C29E7B0B30932BA344D37FE138DADD972721D881FAA618017F399ED136DC54E29ECEC6D68B1F53B54C935A0C96DBBE421848D21591919E029FAAD4FDB3A6C8FE269B32D4A5CECF315F803D2D396DB4B93EEB21CAC4F650AF62F99439EC7D90D5BB7BE660444F20F427657A194ACCC890777089C5BC1AEC506C8FCF9E72190531DDBC0778609B33361A9713F86A9C8FDADB25B5488E081D105BCBDDA9E58D36290922D159A8084E70A98978A7A1E88F017A09E36AB1C7EE97ED1F6A4BBE542A2A167E3DD9AB73F0A62729EBD018F089DCF56314D1FA9C0530AA4698E3E02942884D5BEEA04C904BD4CA30890F6210D57D798377C3824FC42A0408C824B87908AE68A61D970AE0D839FC37704CCC006332B6D05E143D914BE6C4CF28F15703F0AF4C447C28832E2F0B3704A58F6C3781D69EB6B547D7282C60DDDFA04E22640BE7D8155636584DD4C385EF35108FF137D57998CC9A9A3082807700E41D7DEA6A74197255B2CF7F97E3324DF80674B1B48C7597133EE2E0B87B8BBC0BC514713CE19F483EC7B567884B9758DB7D6F3EAFB678DE3AFC4CCF941561996C69092DB4FD05519BFA1FC1FEAB991F4F707C3CD2461E4E35EEA8167A326E2407D5463B357EB2FA3B4C4ED03A4BBCD9EC0D1BC0A2CE92B248338F679FE01516F154393EE2A2A30CD02CB19B53F7D409AD441795C354A640F9DAE4C870F7EE202FD9600D2BF92123420B54E840C57984ED38A8006D5579576D4BBF3FAB6D504C88DFAC5416397F05A14C30CD1DDA0537520499C1B86C5B439C10113ED62CD3B4251C23B8656C4AAF1F5CDFB0F95A788C3D1F4C4BF87DA1BBF9DCEA2E8F0963F27B4BF9DDE17F9641F592C516CC0F59BA1BC715446BF529BFEBF6A7AC6E303827EB9663CC604959D578FA5C6DB6B7CCFC7F37F738287CFF525D9965B9A2466B87857A37A51124539FE9BB383F986FFE278ACF22493FD25C3CE65F3C4B60EE4F4DFA388EDD42230ED51DCBF72701C5A79EB4141C1E7F449DF4D59DC3653A757E7C67344825C08E45330B0220145628C7453262FB53A8FAF693568B2F4BB7C619D4263A5D1C28D799493BC2A7CB789E992388341471DDCD96149250C424C8DFACC471B265CE6C11AE8E082A4261AFFEB5558FFA470CB1EDBE9540E73C9FF3CD336195C32B52E3D8CC2259C2F85C17BC2BC80C22E754CF7817227BC374A61A035FC8B5ADA381994AEAAB9FCA0F2037BCF2C157F94A501320EF03092E48FBF93F56E3086F7B95F700171026A8A2A2AFA652B674E0392D9B282A08A8C7A1E2388407340C636D16DA955626224DAA4F0FBB3B46EA3E502C4B0AF1DD399EDF91BAD26F6855BDDAFA904F0CA0B88F00FAA60B71A3FDA2F6311B6F833601CC2C382D6748FB1746F39A558B418BA81C321B080A5B0ECA094CACD82070275E013580337B384414A0F44CB9619ACDF100FF2D00C0F042A7958E26BF3225E1D2E4AF81EB50EB11187A4F592938D4BFB6E698E576CCF1CE76081EF069191DA1C5CDA42624744CF8E8525CDAFD50E39D52D52BA12F821BD70D1E13F9EA60C2F4F783EB565E5D637DFBF2DE49F832F9CEAE7338F9ABC19E5B7753B83FD58988A1CC04DC105AFD82A9D0F8A54FE1AE9CEE636A3A1F2FBC2C739AEA8DE572693646F027CBAF651F34601BC27694B73DFD60D61A4DC9A2424AFAE648DCCE08355018F35EBD2E43DEBE1CA7F4E7B403B6893332003E06D28FB06367ED1BA99A0568246B762E3C661A6E7995717EC3ADD04D5E82037982CC099E16542E7895E9786B02BF64A587BBCE8A5241EC9349E82535B855EFD5DBFBBCF8AE0B306BD778ABA6484C8AF60AD89EFD705EB415477892D97BC372A4A612E20FEA51BC94BB84BC57E22C5E348A1BBD2ED52A7B0D65DB7F3117AE0D9F55BB50B7FE5558E70643C23B0C796C3FDEF79115072F46F2D582500603C288AC9B1E68D18EA5EC7B8150118B702EA13AC6764F19D8985EE3D28C906130C3DC56662E649588C2785AD70EDB5771F8D0142D36455FCDE5AD388F2EB3705CEB646A2A62E2D455F10971B8B1098E1689F741DA87B2F9308FA9A1334F3C1034882A629233FF4DBA0322450C4D3516FB10AD45A961F3DD16837A3D3CC5992AE974385C71DB071B8E3E5680D1A82FA0FF16CF10A48B83BDB3E3D0186605BDEB9452E91DBC7EE6EEA0C488E39573C9803251AB846FAB02DE9E37A141EE6E7C1FC65631309EF5F4AC7D3F6F916D756DCBDF2E2A707523521627B9F00AA8F50EFBF5D582131246D4EF0B5A8C731EC1349541DA69E96C076FA12BE168B888C82808E4A551FD089AE7F39CA4D34FC233645E79A106FE605BBAD756569A2E966747AA9EBB4F2A394815A6FB6E5643A1A8BB1A1C7F896FA526B780090526E66D50A48B524577B9D9E7A28E8939C1ADD27AC8747594AB8CEAD5670B161550BBAC743FF000C24E3AA2E6171FADCCD13C71E070135E733202AA5BD321CAA10FFEB4B17099A09CBBB8B68AF834DC9850AC22C72D451F93923019209AC3D1D2490E360AB6C833C82C8C1A9B0A53C604D04908769558B50C3D7E295CEBB11348CD27DB386AD3415F3901F743377F4DD35FAFCBC419DF3CAA89B673F1A182C99E860B267F9C026AD0556C6172A2FED5F61401B0F2757F82A1DCD6C6409C66EE4A7E6CFE9EEB59A5A8D3EFE17648543A352630D893F9F22BD9E2D49120DEDD4C2835C2C79D0A036505DFC5C60C8DC7B84F921D1420B68661437CAFB3252EA836C18EFFFB20FA81A69B75D3BA53E2307D1A4B291025E5FDFF54A2D8F39D5F57FCA98B6D6BC07CC0EEC4B2BD3B3226B3E3EF652E946E55F3FD00C8B459C46746D4E9CFACF2DC1BDF8D31D900AE27600118B6C71510CEE9812173FCAA2EB9246683BF0A16833243204501B29B31C27A0654976E95FD8B5F59C1268BFF1C463550FEE6EB86A0BCA8A62D7DEE14BC3428B34BC1DFB30C71998EEF516D078A71AC0250EDEF7F3E329B2BEA71B47FFDD7D34C9E9D4DDF8F4D79EC5CB6FA273B075309A6FA58387C8E53B0B7E84C876F7995D51144B5764FF6B9DD57BCAC313A0B9918AF1A77C476BDE770EFA4D647FF24A2B53D368E019B6BF881CD97FE7EF4CF593468DEA8924297CEDBF86DB144ADB725342A61ACB29CA891552933D6D603E208EABF249A4A8AC82CA271B44F152F1234E893F24AB812C1239195458D7A23C2AD6D1B67DA0EF4F6E724038C11854D3BE665A4D59F47EF66C6A10FE8D008A59F70FA281EF456C2D0EB45FC16DEC16A3FE7043746471932B1553757F043571AB1F7BF9B139F742A380D60238C9DD86E7BC3DA58E9FD73C28AF5A20159EA51961DE3DD8486D5D527304CD725B51CBA57C6ED9A3E1B36954FEDA6AEF54CB0DAE6C0F0C9D9CB3313498D996B86EDB3DA9067F23FC4B5F6EA43E9B4223D8B8A1147745031C1369C2572F823E78C475F60CC1DAF53C7DD42FC7ED32F2B42D16AD1C58A786F1E6AF3CFD40736A352CD26876E60144DB34A090B83E428CB0AE3B6C58C8C036690446582DE3E26AC2E6C829599F30E43024821F25B53F770307F689226CC5ABCD7BCF9AFB7F128C3C665D1E89BB10F88420754DC7A4CEBF63FA6F5C0BCD298A53206484660154D3994ED83697BC831CE73D787F6299C35ADF960EEE6E3CE85D9C11D51F55C8526BCB40676B9765D7C3A389A477DB7C2B524714DE58A20E67D3779C185AB1AE55A771E6741BA275B40D528C8590611BBBFCDA956E523F247E482E3A14B6E7BC05F31A5E08AE09F5B74F396C0DA37C6D49444F4A150C5EF5B650DE98ACF7E5CC6663430863668E4FBA304A75232C9750EDF9F711848797C6B7D6A16FD0386E80602554C0DFD2ED6DC801C410E3E35576C1318ADE9B25CAB7B1D5814ED1CB4EDD0D6D4536932A87DFDECEC302E2B098991B9C3B720A1FA915FD9D903DB6E9BBE3C9EA0038C1E2F1EBD2A2E04BD53EB7CF7458A32A422DEA8E34A1AD94FC9BAC8962E9EA9DEE45D46BD2FFC5783087B7CBF66F34B6BD49DE9BB3FA5BD60C0828F7300AA1586B76CBD761ECFE27F3C72600E416C3A61AEEB7A4FD1D2CD3D50C6116727F92F84896DD5FC39BC1FB7E7154BD47475C1741F7D2A78D84C9D2C079FE4DC3E7FBC34428F34AECA6E76F4902D42F61CD43A5FCCFBDEF636C0B84A09A62A8C9908710471A4CCBCA968D575D1F2122A975FAF7599E1E74F432A62B79B1313214650948381E2F6788908E5C27E1120173201E086B7B2C68C7453CF77875EA4E457603908504AE48D401214E2D07E990ED0BE698DC0D04BE84F5A482A4BE3D9D2E6554C8E9AC115EFCA28AF0D87252001B7824B11F8FB517237D9670BA44E2191157E21FD91D3F4C26E19842BE60CCA34C613D800A951E276F6B612ACCD011D73B479EC218BCB5978B64548B68369624684AA9E0422D9A676BDFE556BD93992C357DE0DBCE919C47FEA8985069FB33306E7437DF866CC924208978E88B1A97C589A3579B285623BCA2D4DB6AF2709210CD2F5A65497B812976284207562CC05627E46D1B3E096926A1F14608948B3B14CC356D854AAE0DCF697DE8A5836D773AC2C1242F8076831460694FE2ACFB9362BCD3FFE174F6A839D3D26EFD2610F29F792BADFABD5DB7B67CDA30158B15D8AA94F19C1D4145C67F0B33DA9ED8FE50EA3C00221E98A7256901C95382CCF833A147502A403390464FA657741D485B3AA35380EE64B30310225D377859508F365EA620A7A571A3A14A983C9BD12F882120F6BCB413BAC8400C6ED0B6A45DBA1BA3AF1591149EEB5266F8F9E199DEDE5ABD3EF4E03097A65E549C301724B4801A8C95FFB92345627EC89ECB9972CD8FA0AC77791EC7458316290D5AF9047BD11A7697DC146A33DB8D6AAE1831DFF1B5E9E6532E415DA70098D0F2229B5E787CFAF6F53913CAC26D8E3507806C9ED2547DDA1E576CF5F18CAA06ECEC4F0A60FA35AEAFF43C9AF7147950AFBC588932AEB69198F65E4058B9504F0418CABCBC040A96C24793DA2FB08DB2186AF30A5E27BDDBF792BBDAFB1276E065C47CE522D8170CC50A0BCC97AE281B51B51F719F4C4BD405ABD845142928323052F14D0FC5D432F18A900E785BCF60286EC93D178366924404B8AE112B1579756202E57A28C7DF9AB84FBAF64CCCCDA22193D0B3C694F47DDF4D9328F5628D1D22FDF26C0E39B248304063559AB43C328000C794C89CDD567CCC6A7617683D2DEB7A488EECB124DF013E7F4988DC7FB3B996A705D99F807A2DC45E1314F2AF044E849FD5C52B4305E99644FDC3BDD4EF6F7D9EBDA6A8247D232EEB6658143364F9AE5BE0597FD2AD1C268F8E20F154F40F4AFBE9A6D0A52A5D452CA661FCEBD1895648E30B5B787EE3F4B0C26BF07659221BCF1F7C876C9ABE316561C74EDAD030E095052AFB6A0067FFC1E3B1C0CE59B7809F1E1BE16E93CEB9BA27FA20E02D91714AE85794314F1D3DB393D4BB34859B746BCDB729229E4C5AE2EA6EF4E2E3A34B98D7E6EEA27699759C77FAC5EEF676AECDBC3710FADF253E111B6B769EAB9AE14FFD550207C70571F8E4C35E9B3AEE4C82B387C5201ACF5EFAA1D6E69C193EDDE629AC00A87D6A9E7CB7C89AD7BB8ECC065AB5DF9DFAD253B83E6C186D68A0DB3F83FAA8B0DBF005F37D07249FCCA25422B6DD95923AC56C8FE48351943E3F5C6703E82E760A80251DAE8B2C4B3320125F549A19E37DBCFFACA684EEF463BEA08003FE7E223E650F12CB2A5E7D3EF0B39758A31BADC9988B86464F6243901201E0F44B8F47B9B98290E74A68EA388C5F7A535F713E5ECD747FA1D6BFB15A4ADDA81201CCE0FC010F56C0FB43B9AF1B4CE21668D55349445B941970568951F1D638D905B53A99856B4452A679C1B622F4AAA4B9A379EA2B002E3BFA6AA54A211DA23198E4710E4C6CF4B3A5730E01D06E2A5D314A1A7191C547D4D7D98A2929F40D6C9E6F7F6E3E1C6004BCEDD868BE9C53EB30E395C9020C4515665A96893A0395F621674407D647567B00A007E7958387D565BD9AAF0CDE3F250108351816DD5B887C6F21AD137A5209E8D67B0DF5118546E1F47B8C554643A5D003FA9BFAEA19E32A815AB40795D467817C4746678E6F1B05F87B1682DDFCCE3D4977F8F51CF73A961E75A9B4204F47F6D07DBFDFB209428FCE5152072B1898793A9AA88F0D67014984D7871956C19B1F62D7579916805243CC0F27963A4C6FBF14ED587C69FDA305ABFE659312C8EF93F8B5A10596E48C61F2C689B72132FF1D302807A52750E432FFFF0AB39A2C64BF7AD828F57D0BF2324FBD0F35F48779C6F92724C6812E7A036AE51600802C1E0B886C9CB7D1E19315A724C778629A43253B3B52DE07D29280A8715FF09D3510A7EE88E16563AAAD2BF73223C2546AA23111CB3FEA3D347492D00C1490E7DBED70C2F89675EE3B8A6C22A0FB1D5AFF290D786C1879DA436CD4B4E7CFEDA46BD1756C0904F782062B4FC4793CF52D285E59D111FF5DF30A81DEED90F6F0EB8E5302383AB73A0B3595E435C54B5BB65473F5F481D6D5870892AB48593AD31B7CDAB7D231350806D9470933FC591319FEF7CC9F32E7828644CCC7D71B798688ED431193A95E78EC50DADB948E19755FC93243CB360D7AAF74AC3B1CAD583653539CB53416BF9C07493B9C7F63EDC6387D4F5F39C7B3DAA58209A4BF79D7C8EDFE3AEF443A60C03D34F24ADF93B1A23B57DD082C30C1AF2ED7F5B988E71566C172BF3731CC6FEC53113822A4949720215264F3075BC03589880701FB8DE6171AAFAAA9C9C83EC640F14FE14555CB6F365184157407730CCFB23385F0D33A671B9D57BE59B6D8514535C493F512318712A67CEE05B0AE9AF79EDF94EF2AAC3D0BC3DFA29B9285069A5542FFC8685C95A3D393412B3B46DB3C9EA7F57542276A1B62D75630A11B925524CBBE419D1CE8FC3B88C429C331A25DD05702B3E80C3FF82E24D7BA58D165BC5C05A1E217F8BE453D4200DBC59C4FC3ECADC12943A9EEEE0CF79703D2F8EA2646B81D3FEFD16DA284BF54CA28591704A07C2671F8EC795AE5F0F4DB39C68DB37C5A15C8A1B9185AF8DD5FB8937B06F019773DE696012349A0B5DB1F907DEBD626740F8553553DB0EBD42011AE26F38FE249BF43954BE8845F242A46F8EC7CE054E0C0D910200C0DBCB389302028A1901E042DDCF3D04F31042F2E1E52B7814414D06FA7272D03B1C44E882301B904222BFD377B4F24D79E436AE8086AEE9A3E45310D7CE8EBE6B1B3162EB5DB4A1AFB2A9926975C5649B5FB16885E08F6B4E90C02C3E6C1C04C8AF3DCE64A792D9F76E7AB026F1ABDBF66B73E08BD8403014850C167AFFD7BBC20E70345C430D7428B0F397DEA8B01F862FB4A40E29DA9D3D2816D1DBF061FBFCBAFDBD6A857AF5D805B6CAB7E64320C0B59FA2BF7F7A8424A0EB04FE6ED094E617DC872D9E7EFE2AA749E06B089D1837DFD555E775C707F6733EBC3DF71BDF725031272A3DA274DB16A255947CFDAAD0134EE4C981E26AC8E0D21F19FD61035C2E54A04B8D505B2B5D684B9977E68EF90DD987B4AE716307CA458CB4C5A15D102FADA15FFC4FEF4CF7707BEC091A008EF0618AEAF7FEFA5D8C599A80509136703B187594BB6BEFC1C8A90C041E1F7D2CA3294630B716CC6C66DE855943F5D231C15D141C5000F4F3172781E903075D312723DECA2DE59DBB18770298FF61F82B8D62CC512A797BF3943C63922942E3E00418364C6B8857E777DC4A33933D94348E7EFC76B413B7A3EE911CC9EBBC91C68306467F08D451EFACD33156CCF8D46326BADA2270BAF55020E4579A167F1599E623727B403C230BDC98360E80C5010BAD2DE8AEA59012E4456E1D2249F75A2F8E4E1ABDE06B11759DF17FC553C5DFA01E84F39BA2B9D260136F004BB7DFF61B476883050F6A8A8CA7B7E61C893ADA81F34CEFDAE34FBB31E67C5D643CFE7CD7C6C73B333412C472756F89685276E90C3D208A12A8A3E9753D1F63E13B8E1C61EF450B26E2C5F61AE426DD8A338F6863AFF572E28C66D6A0003E8F2CA287156A21ECDC39D422640E76CA088835B3FCCA3DDEE11340CCA0FF3B617AFC35FC88341B265A53AB5E48AEDCDE957006405B26F03F531B859B130DB3ED0A6AB554F5CD9FBA451C25A69C40577E8A2CAF65299CD21F116A34553C8D040BAD3D24E11F69CCEC58A966F10609999135D37F460DAABFA2BB1091917C61D0C4ADDD2F5A98AFF72681B35D633385F585A40C20004B22C182FCB65F76F0C1CCF036637E5F8D1806BD8DCE6B522017D07A75C8292AECCF753DB6D33CBF22837FCC803785867D8C574B18186DD07D11C9B4BEC1F535B9D6DA79F60746EA361747F6FDD1F0FF00FEF3EBE7F14B7C62232CE160098F5737756B6E00373F209081A25324D708DFA9D6B6ACB3DCDCC1F3E2080F70DC5284BDFAA31E386B6588141A18A94F11BC536A7B75EB71F3D6B7DEAA016AC7A3D80C5F1B38D1771C21B3BF31655620AD52DBA7B93620FC4848383FFE8E03D77BB8908F046974815A4B19B46B965EF0D8BFDF27B8FAC3489CCA1EA506B2B1DA9733DCEE0C103208C4D299E2E30C54EB279C48D7B56E4635F170D48FD6E58A08F18393C929C50BC2E09FCA622C716E4FB10353F2A8ACA821CA8D99FE1389DC4B32D0B161E8A80D85ADB33304F81401A3CBC309F312F44FF074953371E2418DD70E5C1E8066451EE973B6D215F1CC90550532AAC1A0738DA9948F4F64A04588C331996ECE399C40956F9C16E3F8AE3FDA59D3BE021D67B652049FDAACA1D1E766480DE5FABBF709850D1FB98E74679087CE57A787508498717EF841589FE81B3738BFA2D15EEEEC3097C17225663AE5655A4AA1F54649DBA9CCB3A5DA8B3C0E5020D20F448BB8D991FD94263D05E621DA1A7DCDAFDCADA222E39AD4ECECC7329040DB24855057FC891D42C892A1576E94D8C9585281F7215026254CC898DD143E4B54F4434321E0C2D94C05358BDA43389193844D3AC36D0FAAEF0560111698B8390A2D7D2BD5A531B86490596765A791C818A6F7CC889AD40847697992B681D86C2B67BAF570304265FAC904D12A45E190B2DD322A47B6B78DF727D11E76683558C2652728083ADF5BD8F047FEF1E986788045126A77BEE60C63B3DABE88F4F93B8AE94550CBE77EF95B67315F8C561621064A878303E70365EE18559FD0879DFAED0393C01C637E8A743D8AC750B9E91AD41ABC1BCA22A59D68A02D3FD36E5F809D531EAF62712228BE89567617AFFCD7F0D9EECCDEF5DDB5F06C5E4B9A4C0C2EC0C7F053D2DBE48DED43D7D13CFBBC9C96500D68C0877B9CA4407B2BE06955F3630AC797B8AF9C3D1335788E148174E8E5FD69154468822B0AB275F231D229BFF7D55951E8ED8AC28FEDE2C8544CEEF59C8ECA3E2FF62442E720935344801DE4ABB5BBA604BCE5AC719B4E1F42140D1C6BA0C6246814A0BCC36547B471B2885E3BD42E250AA2F9CF034778FE7E9DD987023411D0A95FE4011F2405A8F85BEE6078145D33BED660DB31CCD76F4848F67D3C8912266B331FD1A4F8D191958D984FD678632E4A7BC992E13A68DD2279EFF77B510C45006DB0520B794B085E57000771421A04D661687639D048541A2923A26BD8C280D38ED5CEBA98A5F487D1CF3F915A1BFC590ABA3CC2D19B0E6CA7FD364F946196D022D37D99C1B2FD2F81FA0FD354FEB19AD43E1EB7339D9873DE6FB8B6486C8E53A2F141AB0FF4CFD391E3210F255E6D7BD4EAD1B38B4D321FFF5C3B45DA5A3E3EF180EBDEE9B1176548255348A5253FCB523706160D62B73DEBBC8B487C2174CCBD0F86C1E7DBD11E41E120C68C927A2AAE42C3621BF92546440CBA44CDEEB3347D5B41C3ADE3C874009D87BA6DBFA8ECCAEA55A07307CB87ACE1CF140F9BEA3C27FE7DF953824175A83D2F55A9156FC2D0681DB0F6BB04E9167A5405C54992DB3AC1D1E9420A8BC263C00BB83550676A64DC1CBF629312A4D400AAE586E6C8FD879B4D8F5BD1324ACF11C5E29FE3A494E4705C614D3DB7D312E180A87FBA78139AA742C11B60B76CDCB0677CDFF91ED5E685B4D817BA4FB1BA16ACA17FA4E57E605CA5A8878FDAC6D08286C9418227EE5FA5CB6A924A68D37A3BC8FD7A72CBD7BA92F7CB15BB267B91009DD7FB3EEC7071E1C6A688D4FE0ADC3086605E16F52F74DD5585C2DCE54D5ABACFAB4A3F4F0FEDF50342D1F7F03598CC54D6FEF29CCD4F55DD47E7CA5CB45C4ED8E2379CD82B80A381173FD0E80AF54554BBB94CBCCC230845C0C6AEC0FB8FD1C42B7E2D3694E16FD42C6D1C35AF07B1E02FD5281114B96C3F46F2E5BC50D0BB076535EB42A4744C6EE1B73784B96E7DE6E299A1CE9D5D9EE71D7C3981F4D2C1453485F755A60AFD7DCAA75001BDE32967DF691C20D286CDB2607B7808E91532FA3CE0BC5CCAF1EA79647E38706E7346998CF1830846198B944D3078B74538AF22C87BB72CB14242612AF424BFB9135D09A6BFBA9F0FE448AB7EE1A0CF1DBBF483E2D2FEDDFB9EB01821A932990543FB21D255F1480A47738BE883022407EDB61C0AC6C01A9C4F0B945169CB2F4D45BDD97AAA0448543696410EE4BC039DB1F6D9CDC32383DE6DCCA24464C4D65350723EB602F7E85CD7372F25E6941122F50F932A9E8813A9E6406146F62DCB2B2B4DED07AF5B7169DEE85222EC46FBAD692BDEF068AD90469ED98E0E316B0683D43EDB335148CD519A9283E43B47CEC50CD70DEBFB66E2BFDEF754E45E6D020A0C10DD45EF31E1F7BD3F8BAAF8F381BD9E5BDD79BDA45BB2A98E004AD4C33F73CE6664A4BB67FEBBDFE69D9B81D39DAB1FB65F4C2DDADD335DCAA09BF92255D6D5C24B1D116EF28CE993E4E7FFBC6D6D7F4A6F4670D014BDBFCE31926E88983277EE7D273AA80477526E705F0400D68A22B5BDFD5A2A17030370EFCAB10DB05E15029E2FE95EFFA2C838104B00924C3E76639D3B1035B89287117C5534E9A71254BC0B6DC6410458FC0E9C3121B57E8EEB3779943AAA2C2BFFA14E09FF60468EE1774257FA2172740BAB7832B644BBFC51E4CA0164D8D40D372C2685EE08018E595198CAD0E4DC0AEC3769A4D4AE3E4794ECDCC682D4D63514B663B82B08AA70017813E32C8AA5C50DA4FDECE26FAFC5695E2AC1245CDA79430D2D325C5560A3357EDAB9F0DA89435E7DE49D6F30AC0F8D95894C0382C0AB4CDF0604483160F94B8C6EDDE31856F854EB72C7F82C0F82915560FE6955CAC7DFF82C5AADCA541048EA2004677A4EC9A071844E288E0EF7958481EFB3F695414403FE7582D5BABD6EAA333861CC0F4734CDB2B0B0F7672B7FD95C2EE3CE6272613702E090FCBF0411FE0A1DEF8C80EF4482F2DB8934D2833222BA527B1FEC0D15269B237037314F0746748E99F82FAAEE5FBB6DDECADC010240B9F2BA00FD6214A71B5B42907B08B6ACD849C46A6BE4AE391E7959D1802718E86072BAA5BD2D3AC1670C17FB072ED9C5C21257C0A35CF641A8837985D094FABFC7F8AC6221AC6695DDD67F59CBAD075F233498F347E373C701FD5072B4D9D7753F0A7E6357B2DB82381D410554FA73D7B27AC49CF5BB83A18FB8186865BAADE6C3576A961F9F16895F46F0557FEE004FE3916E59E682DB396084D3CEED2067FC542A72BC137943821E677FC5C62DC15EC911E7D733249442D6C6B3321A80ECDA7B61656F12F0F4A701C87FA15B4853C2BCA497219B58BB29E6F017C64BABA386964630F8F10A482043117DD3AFBD1211D6D46D693699EED456FB77FDF18D9BE7DB00B8EA74137FAD14818EF2F7E04F6B976AF2DE64D1BCC2251C40719AE3050B65551130A486A659CE6AA6753B951E2AD72E97EE05C0D295B23294F9949E99E1B8BDA8678FF80C8C56858102A30A7A9F951754E69487B0E0070561BA4A939A84558CBEBF7670FFA805D2FBF933BDBCB8E782E92BAB6EE8E6C3CFBDC9306F4A5046A188718140EF3C67773BAB6994B6315F77136BAC01B74450D89BF621F6F3A86510599C36DF786EA7BFBF145C78AB5A118CE36578D38E760F142FB1C156220A35B6EA44F6E354B0130421C3F2ECD1BB4CBF5A88ED2A792D9EF646DA9049BB4E323976B9A4B4561B5C17474AC128AD1F38548C1E2CA76762BD957607A42B5FA9B8F9BFDCE26A7D455535D67459A38C52A25D053C0EEA69FAADA3187C40276A6B6E6B6C65AAB359723388BB0F3FA488E854790D5CE3CE095E85D4CA56AD3F0578A1B826D5EF45ED0D937A45D5E8A0B67FF1E4F701AC9B8BBC027F41336999684695A5C82A390815555F13C627BD8E436D5F10C3CB5DB0596F9B4E4CEDCB85284BE1FAE28593DF46757B58415A44DB58AA86249EC6DC18F1306038618CF55D04A5BB40B818A6FEC9484DA6CEEBC623EEEED7AA251E4C768CB56F8745E5E79C6DB901DD9032B508AD09B4C4C54881AE7DD8F54B6682D29C4DBD16FBD862A9D0255A35D677944032B119A62BD95AD6D905DB5573E70B96A7422E86806535D9EC9A9C97BFA6D9F46CD967ADF42B6391F85DF15AC5A2FF801022FBEE145B5284A8BD11DBCE87AE3664CDC8A8D4ECAA54AB365EA6B9AF4B12D7F88030DE26E10E8BF67EDC41898EC8887F85D7F48C5CFDD25EFC7ABB4D8A59104F54DC0DC708B15FB602FF45449F5013997FBAE44B60A0178BEFA61EC10909B3D9DB05939A304D2852D5526D5EB122D008257B8188D3ACCBA1F076C2F4173E5EEE57AA46C31311DCEB7B10DFB77892ABF4793122BFEA5D7C18AA45BC463E341F19A50057A2271C4615806D00628410A3DEB30984BFC3681D4EAB89B0CF7C6E4CC0E9247F9936BA2BE915B51E6CCA1117008DE76AE454071D14A65CCF846D6833DC009CC17312ED75D8E3F5C610B5003BA8CD389B980DC7AF15E1855575AB853F7D35CED4C7326275AF24A26C279075A2E826A46EFB556CE3D935AAA8CECF55AA0232C806AC76CACD92EB23D21ACE78BA5A6807F77FBAA4204FDE69E089782EF97F618AFB3A9DDB185CDC3E5BFABA3BF43F2D9D563F6A01C143264B6C9C80DF6C98DCE2D29921044B8F2F29E29ADD4CC7A9222F0CF7B962B2164E8DC361C8E9A25D06B9B59212EABB1B8924EC27AA5874E95383002F7A54F72F0F76F51335E91F94A34A09620BF294AB27CB4C52E6DBD280B4E6CEAA8716CE7DEF9734D48BCACC8AE19904BD2110ACF60649F550B2E1B42FFC102D2584197D02F245F79F26A8FC9B81C9F9A9030B5774F28CD640FCE9229E5F3398B32E26D6EEE88FD26781622BC28B53558E6B4478E24F9D94ED5D6F1968C7851438132EB62854AE1FFE42CF53CDAB9D4F7E458C69ACF09095F88483DAB97C181BA91667B03A2134211F3E18B2118C322B72EEB74B86D82D2801FEBDAD2DF73417CFD156D892668BEE18428F87C6322AA736757E3916837903048B8C2755629DA3048DC42AA2F4AAF41E763F1A21959E5AD5104FAC36A2E0D221D808A66359D85A5571EB55D55B1E941662C9A0E2117719736AD7796B8010CE7B1AF0DE26EE8069DE3145FDEF3A2B4BEF2B74FCDCD699B874DFAEB952042393FDC106F0B48E6FDDD19465E956E2AEE571624CC67886D90FE47FC3A2F8620E46BDA09D40FDD251B1E465B8BDDE9340AF388C2B22D9D6E44553F0E55948FE6F47E98B6A17482B5AA4A96424FAAB230EBE5665F5E1C9844861E758891957F4F8DC645C1A239799DFE428444F19F6935DA9EF3B34F3AE235A14ED170B3F4CA53CFB083D0C0962941556C7097F1C2E7311BF526A60BB9DD10CE7E59E56F5A1E09EC9A790EA04B47710126865362E23FA5B973F30B1D20208B4F899F51B713FDB3C6E505DE8E73F3E3ACE5E984932744E554064ADBA01147341ED02E49EC3CFE898AC9CAD0636DA2EC3BBA26A9B94634323E5F9213EABCBE3660985ADD562A82BB67AEC653A50C9C5447344E744E4F0C3CAAA0195764BB97157BB2CEB91439B8136959DC34D887BE7D8F0B4642E5129E0F4FF562841163B8954B414539EF1CD8A5E5E92BAD613B5BAA8C66732C8CE25EBEF05A92DAA0EA5A556F9D4B626386F7CE4454FD5FFBC2DFD8C1EBB84EC0637FE6128B799A747F8785B07A9AF9A79C357618B0973C577E9357FD8103A9781C5044BCDC82601991B3834A8F39B35940FB190335E4663A1CBB60D9D353BCAB47194036002831B13348F0D5B0CE7AA267BF9864F989BADFF3F9DE1A238951B9267A63D2DD5C7C95CBC62B56E73DC218A846901E14F91254C8880E6040E459408646B0EE24295953E85496D52041698BBC49EF7C9686A7DEDDB03FEB6225FE3148872370C7B6B04C2FC5783CE65F7A0166D5B77838FFF81C92805C49B6641F9FEBE6C265F3E7840CA52D1A4727002B0DA2840B43254D05B384FF2D97547EB13224104D571534D650F33B1FB30317DC061BF2EE16BEDCC14232768161FC95F2701C5F18007D6070E0C97211CB758A10450B7EF5AC09EBA17F2AA30D90DD51C189D6CA5DE7CD2DF1EB7797AC9F9C7FB7EC0B0D6C9FFC3ABCCF6EB8213D46BC51486F7AA62F551407AD7B7CC23DD87F41F73FFEDE1E5022B4311472B4E23333660D7B7EDE0675D003FEB28D812DFAE38669D705B2CBEBAEFF76FEC2FA5A6CA24336FFE64B40BD707CA9EB96CAF1BE2E867719BE65ABBB5EE62F036A16DBFB76AD176940EF6BC9EB1155B120E212E886007CBC802D5D54748D274E6DD8091FB36848231CB717C2CE42F6D21BCBBDDBE44E284F48125E6153FF58856C3A0F2319A5E6D6BAE6F8E0C68E511175E8122728F1A953E149EEDB7204BFC930912358EFA22F852A0867CED433D3CD6A02A2C37D9816966E5A94BC04900887D3B14D6EBE543F10704E942E84F9DDDB20038434FBF8EB14A2735F0B88FD9B058DE467D47EB99B53DB2EEEF1948735E545E917047AE64BB822A6A2AB57485968046CD7E354AFB1A42CEE3A2B0AA734B21A2C89DCEB62D4A77A063A7F8967AF2C858C1DA31BB98A06A7403A7BAF13928E6C7E22E65B4071487AEFCC53BDEF237E733F4214FF63246E5C92687F2ECCFD13A53DEEE5C014034023B26493D6CE59FDF4C2191E18A03C098EDB5EE77509F4EF498E50BD345514B449B2FDC18247EBA1544E42D5D4642DA1CDADBEF2542FA53358E1FDEA107FF5C8C01CE7B91C01CB059FFE73D26FC375D9981CE0EA554D9E5281912F7D696BBAC96455A8D644F79387283242B45DFF2CD4DA30012295DE4D26CE8EAC843E0F9EFD86AD102DDDB39C345350558C11AF53AAADE11C6198A46C762E3147A8A1C59ED57CE2C2047D6D8FF023C587921ED61F82A6D581118A12996EAB1542B93F66187DF2D36262CCC86836AD48A6D1B8434809165F1E6CF2A07AFEC64EF731B5BCB8749F8D78DF5D228D6DB9010105F0095B51DADCDC2D7A64EFDBB8E1560D806E5145DEB1E19A97B2807E00BEC4B17C0A327C0662FA27933EE392A399CCA22DBC9DDC93A741559E8544C007396A6FC22C91C67BA9B2029E79C1A0D640CF27C638B9C52DCA94B0313A8B15D4A91C83103690484600730FA0236F3F7E5332C687FE238B86373EB1834A4F54A439E0377C682E6931D158DA811FB811418480B35FE33B63DAD4B24D8139218AF533AD0C82B2E0EC305D0B48ED054E652B10DED7CF9C370DC86BD2C8039D3D5913D1B6C48722D8C21431BA1621D7BF36B2605B780EEA85BD3E4BA9887DA721D8E4957F413F872F77F29B36C81DA29CB09E6A691D0B1FBD136620FC54A1F0D1DC655DB2AD852DB10B6781032110BB10B4FAE7F2B125873519CB8C2A4E1CA616CD6183965498D2C6C525FA6D7227B8A6E29F6C9E52D4B0F2B054BBFE55167EEE2678AD7A202CA384A6785453D0C9196D2E1455AA9DE1D79EBCF988370FA5CC9B6FFE5A20C1A9FBC4668B8954750F2FDCF1C2C792261187C5D45404AB0F128B5007B33573FA07FBE7D32C068169721F9159914C398FE7DFED964A2439636787E270497818AC961D77A7D4B67239DCF90AF5D1C2428F4AF2DA3AA178F0CE40DAC3A0EE549E1394A1B2F3AEA45CF0D78C08C6BD4588BFA478AB529D3D610C28780FDE80AC4CCDC47578B5AF52C5E348867181F1E2C0B7A4B38C1B7D19D34BF3B251EC5FBEF16F68CD8AD785933C0D7B20511E25D29FD4D0FE199225A11E59F6329679D3FCA87B4486385E9356A2AE11055BACDF6D9F8D87DBCC07B7181176722705A352825AB48B2BC7EB6C2F8B8C380113E118D7E7525969CDD430637813AB71933AA9A04C12FEFFB90DE216E24DE5D93DF494B978C09DBB860A9A9282EADE72C1E4B48B15E6D0D9A73E6ABD6DE20A3210E5F07EE5B3D79CBD7587BA221818178319C8641089A56BB820B3EA848C3FCA29AA911F4AFE69DDD1A89307C45F4E62E79A11FFBA75CBC0F354DFFDC5F01CBACB97AD5722B288EEF127D3881F0BBA7D889C69815AAA2C1F173D3330330D5144DD2EFEE9EC183EB9B3AEB88EC3FFAD9FA391B602AB585A038AFAA1AC20324176681CD9F5B73F8BB39285182CEB7C718C13AB4592704D7A56A9E1709353503F7F3354F864F7A284EA1BF3083F1893775168718C18AE75B1BB4AEEF46E2F39165A253A2B7C07BB312344446E20234BB7A375AAC819CDF24A686F00003BB99BB947A93C1B907213759230B3F28C3A6AE6673E217AF33CD16E980B8300DED473FD6C669B99252A02A94B07C3BFF6F2C6D465A134AFAC6E3A63A8DF78886EF767F7F5F41C87937002D7DCD72FFBCBFA52289E94A4FBBE18DBBD7F403471E4319045424775069AE604B1D4C54959D410D009229A66FB0FCDEABD6CE07DDEC04D7668D1E821846BA5FF605B6A04974EFFF66C53E85FE49E199053E476CD47F1B312FAE88329BEDB314A1C74D47D9052BE7CE21B7AFACE2C5BC02320A43692F52343A18A1A53DD35FD8385EDA43C4B616C46EDD3CAF34AE97F24788A21851EEC657016A0057D10CF8836C02FDC36879462E623158C47B0EF1561BC88CBF361546818C706623222DE7601317270245BBCD572AD2C074B7B69186973DB8757A1F9577F042C00A0794F2FCA741245609106C08874FA9E542D962FAD1EE27A1860942A6E54636AC2889D73B151D0D2A686D9F4CEC926B2D751C862637494FFD5DE4659141235DE9BAF39986E21A806AE7BED4B89F7285A21448EAF6D76FD91906C348E79A74D82EA6398D5F314C010E937A1AE3592469003E09C202B2EF0BA6531DA9040E243B59F5CF6B022D4DF9803035FA8EE67F2C5504E52125FBC3712DCC14448832C0BF1D50C18D410585FDB244DAA9284C39CFB28029447E81D3FC2063FD0AEBD5558273F3766C5D9342FD74E16331526DADF71D817C8D0A25601DCB66752007F3F52FE579607C3C5E6DA85FF2119EF97C2078F2DF88B7997E5C42133FFF89A928C215CCA3C2554C02BF490B9CA1FA256FEA497364D8FF3D579B069324B6F794093483A6441ADB191F110B377B7CCFD1AC86853392039385EF9215216B8BDCECFE4DB181B8A50FA3E3C1CE0E86D4DBF168891806712DD341538368B3CCDE5591E2F55716127904B9ABB0987DAB90C469574D3665BA5BE5C64C218DFCEE6D109359B5F505D3D6004681639199E581AE652D44C1E4F1605ABAEE01EB41BF9B91984416AC14018129AF83B520261C55DBE6EC3A49E903F97BB770CB77A53D5EF4F1D89F4D47D1ED2B75FD35AF9C9952FF83F9E82A8A96081B39E429787A8F3BE9C45F91E892C76E7062A5ACA0F07921F053BE1972EB5B3D5D7F458E9FE6C7273A545AABA40A1045AADDF06185EE1FD24E8C4FE0D0E4A48F1F645C0FD0F4C7A967F515AE4122AE97DF8D32C803CE029A56DB58680E76004E0AEDC377ED0495615E0985D6A5E9450A228052033D523CE1BCA6C90D86A8A939A0762763A3FD352D5DA9E3D983EAD183C9D5AA0BDB26D6D3141D85B8CBE96C4C1E418E0A9B8A52FA939F372B271CB45E990290009627C26D549BDAFD1B1C9BC6404EC31C7650DFE820033D8C820B487955DF8B6710B580C0B3659020FA06FEA203CC826366E227B4D5A9AF70AF51C616EAE8DD06514FF02FDD63115C4BC7568AF71A3287B172944DDA4A371D355DDD4F3BF549069E13C53726F210F1059F8C1EF2625DCED79F313C4E1422AED746E9C6F94E8DD0C0EF8FA7205BF86119C50FD0022D9F65340E2BA98B02B9CBF06AD77AC589F7BFDD212D34F4831B77B580AF0F3EA8498787ED2560785DD228E6DFE4B764DB416185246B28FF79705C71DC124F0ED6E6F5D1CFEAC6500BEA00289D819D91CA4D8DD37E1567124DD524F8EDF8B7B7E40BFF5079CED14FC8C536FFD23B61046DC7BA796EA71B616182D9A49EC2567E25A677659BEDA53A69F54AED8534BB955E3F996B1CB459F65D4E70A8640F4594BF9B7BF564312B21374D38CFD0EF52697C817EEBB5541CD0C774397291F4B889FC37E0EAB1802FC84196BB369DF2ED2DD5AA9706087D276FA968F543C5792694BA2D3D6DB9D29F73CA9B308F60F7A9B290611959073F1FAFBEB12A3BBC8E5040B0C5ABAA933E885D4749329768286A0451653B583D4E3DD7A057CBCDE41339F73B2DFE512C582B35C44BFB8A1A07D1B1E9DCE6168A5B82CBC6C811E4F9AB129D5AE27C37C6F42799825AECA9261C0CEA25EC0520F7B4617A68D7D13779344CCDDB4EFD6883A1C78F12CF1E1D4230CEC37F3822C3CD91AB59FEC1300853D50813E2D7039FF17F7CE56280BAE0F15D98E32867F3398AD6D054212DF4FD365B49D6B8E78E8ED0359D94719FABE2C96CCCE5D4E5F0490D1452CE426AE55B813C0BD5852E53A028826DA8E1AF8305CBBEE7CCF1D1907C58D719D4DEE9E6AB755744691B72D5DB170C98F3020D99A4A14FA70BF8D4AC14AD8EC1F37901C50B1EECAA9D4B5BE78E406DBEDC26ADACB6FA94E642E90381C60D6957A0861797C0870C45232B9983CE7EC4819B47DDFB50C8D282F4E053772C2031011364D0EF12A5EF82CD94130F8F227814072D4464D5867ABDEFDD20982841486093DE475CE8AD932AF530143875FD7D73F77CC774BF12D49B8EDAC8379112B3B5B7439621C3EF2FA909CC6175B3331F9D2939EEB8D0A225CC3E86E5CF3D133F7D9212A69D3C04E044656F25765822F7D55BA8020D04B6C01D18A14AC8A63ECB000227E59D2FB624EDA4E3A9DFD2799863AB0CB1B1FDDD4A3E51E3C0B647237E69789271C07EB48BBB8133A8FF52A24E7CFD0EDAEED1F5A1FF79F3380C11EBD5E28600A424CDA9D5E560CB67AD1C13396515D2A95500B329703EA54B3153CB7636F4C4BB7D777DC2C79B0E5DBE8670DA8D91B5E028EC83953D9849F72396AD8CA5A66518D25AD85056BD9DEF16576C65179F2029E750B8BCA522F9FAAAAD7AE5119BCE338D3E93FD66929301F51EDF274361DDBCAF74D5D609D41789DF6A8D911F646FC6704C55D57C827A63103915E542E14C01666A3101B73657AAAF07243BB4ECF6030CCBB3CD484D8B1B5035818466532905194C816B90EA91A58098397DE7D41F51C508C4771D46A67ED6CFA3AD0000312277908B2FE9AC83E540589C640B7092376DC0274984716222241D1CE987DACEA37ACA26ED13F4AB5B3B7743B45F47373FBAA80559A7B213B17AFB97946C0D8F893717A97F12CC51CB51D97DD1D6E2DD7E488EA7CAEE53CE50CA25422C93B7BE27FB4E5ADC965D19E809A55C6130C8F9AE6FE6713A11F594C393F63FE40BAF5B5B43B8437FE113AE24271703827675787CFB70B76DE23ADBF34331316F66E391D2254EBECDCD63B6C8C41A70AE540081D9256CEB1EC8193A4CB6AED8DD3B5F9E59174DAB229EAB3DF9C96A17AEA90B0A14B2B540C57F7B11F4667759F7B51674F31694A90584CC8116264556B844E60816209EBC16F2895E46C035D2430D53E88031F5206D4506F4842F2F38F9767D4C433322A4EFD49D0A4FFF0FD31DBD15510D245AA493B13D77FE8A60FC0015AA90839508B15456DD79E83FC1CF3BC6734786577F14231E498DA936CF33EBD790C7978C32290FF76AFF0C27A59B85CB3407EEC9C525ACC1234EA7A1197ECEBA69FE2381AE77F2F3F50EC6B1BB7AF1ACD24CE5082E0C52FB53FBBAD9CC13E2AB06D07822C12D59DF7C2DEB2F3708B50162D7FA03248CDE8680C86219B7F928B2D50F5EA3EDCA1026A16875E77176E21AD8EBEE4BBB7CE6E8F9B6EA8591EB5147E430F27D7DFEA6923CCFA77725C3886F4B30FBD59E6A4DDE125EE688AAAEE86102547DDE737252D0D7772F377FF63C15992D3297E8DAF7B69ED2A75EDFDB54808C1D7ADACD3D055402D8B683270167CFC19F955271197D00C36D44A31D21990CA711659D9D46B5DE84C40824EA4E1C303FAC55E24BE4F58A064CFDC4C93D4F7243EF0E40AB72F556DC16ACC14FA4B0C62976683EC964E9EE3FE7BD70895E0EDEC6693E4C1005A2F686EDC3803FF4D000E5AE89CD16EC8E5E255B1F41BF11328B8A9F2C1727113EE942DB6D4F534E628C413683B0720AD724BBCE54C7920F2AF26509ABBD391547707392DA3B9EC6326A45B41910EAE05DA14BD493942DB8F843304A27E337F3C16D7B9B63E026B73BBB8E2F23626F34DB0E081712CEFF027F069C1808729A7C6ABD85BD05391216843C47E543A130EC01CF164E91C5FDC2213BF6B6EBE81FDAD509550A7E9F3D611F80119522CB206A4090F9D7F49520C15AF62967478FF18D2E81C47DB39AEF4C28E087E7D90004B1B186A09B7B40F4E8A21214F3D2312A61B3B30ACE480A323D24E6E93E4907446F5F147903D094159185D85959E4A65A78EB63B84BCC957BF7FB0324C7D51268E892C14B52A3200926DE175F5B48F76B4B27C9954C3F5E48EC8A364CAD992BBF6899A34B861F959BB7028F51BD9429DC9938737E16E6CE06AA1F80EB5384DD0D7809528522B125DF52DBFA198E664EE334E0DE1372CD2A46A697DB9209FE2232D8E404420818A6DEF4B49BBEBB69C515BDEA9F30E556094B5628142E3C8C4C3CA72DA97CD92AA6EBC63DA894427075C713D65B6B68CD994A208811AD2A7DF51C3BEFC1AF4BAFCFE064C9B09250260C74EFA3E9251AB740415CF7DCE9D76F95021C68DB7E5B48911F290692C4FE99A49DC4DD509101D9FE7982E22BDB25C22A871931B9C7C0D5208144F78471D828996F94CC14296C1C42C975C8E5797988DC4629B5171DE06778A36E2242D1DF609C2779EC2F72A6CA076B3A3BA24E134EB5165AC35EFEE29C61988148FCE057FC1838040FDDAEFAAA653006755CEE0821045A3ED430D33DDB2C49E9162EB7F8D13B221C3A54E06B894B23AE46AC7F956E5238AF4BCE5E87C7D409BA71497C9FBCED1CACA38D99A06469F68CCB243BF753103C0ACECFDEB0ECC1104760DF66B69FA1102020F0A578E116A4991CA8E49C00DF60C3F8191BC9A2056E20A56CD9D15F00BBAA75B4DCB8814BADA7AD7696322F23FAF62D8DED71AEBAB3F1FD690D0822E8F1F369DED47C844E2A7C746AD9217AB22319D724664CA35AFEF2CDBC48379DF22C2AE2C2BC322967B7F44743BCCABF0C671274AF80252E57A996A9626EA3978A219BB79D0BBEF0C12A3895162C2531438DE255FA65DBCDFDAC356C674288CC2AFE65C02BE83242D3A303C8B71AF8F26BD183F270260A43DF8DE65C73623E239867F7743EB90E6059C4EC90CE216C4374B68A24C3BCC40AE27A69C8ED23EECA96176096064DCB45C72AC6E388E293626E5BFE4D895414FE771540F811522D46B3A75E906DD9864F5D01E7AC9D05BEAD36662F8BEEB81ED04285E9263EB41E6C911906EF27DADB85DAB14269C05B00339DD911FFF0027DC1368D861E9652EB4C4F17EE83252FEDEE69E9FA00E4CE96D5D9DE5D8D8CB65FC8D73D04C34A88FE9330DE82E516BD628FC7B410E22758CC3F2C7A7093A5F1B882A831EF108672C51865CB656DB69A018CB843C658F17AF50A6C6ABD5C55C03566A23214D2E1086DE0F600985F97BD8D8A7A7E836D34945A9FAD94F9E7C866630EDDD3A2B86D4E3C10C832FFE67FA9B78AD1BAF6C1260DCE335EC745BC14D15FA4C622327A35EF81225796ED62258FC2862345F60ABDE6984AE50136EC4BAA571DF41F7294BCA3082CE0AAF43BA570293E577A38211568DB14F7D4E40DAC68693A576BB2297E44FD7C00A978E3FC32C9D8773EAF81ABA25EBBD20501AE0743ECB6102E9A5FDF78D1A3B9502A4751CE04F4BDFB412E3C0079CE59898690AADCC3CFEF8DFF8FDAE192A5FB0A61E87F0EE853D0F9C8AD33B9A36649DD82215A7207ADCBDCA3B50057F83A497EFFA498852CEBC3A546BBB049604FC1C08EFD26CF51998336A09744C6CF531391D912B1EF07DF53989CB4BC4766F91DE4BF01932C41CD5D2663D765198235CFB2C4AB4DA6949F398CFF064E566F54CF0EA577D07DBA0A2CFC69B585AD0FA0BFB115E9083346905B2138AC44EC76127B9C561F6C03660B028B5536413E24A9C3A2D279D6C1B20FFC42DAC3D862A695B47F2EDBC86045A6BFADDF03F252B9DE0BDF91B249008CD6DDB751317F8FAE5DDA3815FD3B2479D703B09651A72634A1D87246F476BD0A4EA7CF0A101F365FDAB2A6DB88CA770DC833B3AC1844CC0F96A9BC8534B116B050E5658F1465BD996392F6424F58350B9004C420CD2A2720B493E81B4678335A959768B009758E321DD866ED3365A3DBBDCD20A0568EF7FA4F3D7B5B312A9F652FF0FC5F3F35CDBE63702ABA3D2F398ECBEDFAD33E76BC2CF73215CDE354262CD0621167772D203894653C1939FE525C6420C709C2F7E5A2E9013FA8CD1E203664E3CC8860CFB71D6997E537B19C996BFC83888F4ACEDB6577761CED88496015F456D5F51B808440951A1C9C9A855A927E95AA6F26E7A0905BEF66B784AB6A991BE5DA7E244EF6EB74EF87AA12E03A100EB0F68BEC4D44B5B849F6CCD2749AF5ADA0FFED4D450874A3341C18BFD8CBF786F53E134F2100FC5C1CAA35700DDB16EBB15053C6848C1DE73D67A6E74595E73AB7027BDC41A97AA1E5C077EF58294EF442FC20F2F735CB440A6BF0ECD68B596877BC32C14FD9C702842AFDC7E4BF1E5AEE4DA3235F4E543B3AA2F30DFF0B8B588BE32B8B494C1BF9049CD1D40F61CCF34692EE83540F4918736F3E6A5A6381F2B38C6FAF5F8189B0A78DFC78B5CAC19657969EE83E08DB7D009F58EEB9EAFCF19089E6F76BE6D29227BB15668AC3AF2847495B8B48D33A21B905C840C5C0D27F0215B50E078F8917F068B5B2E6C7BBB175D0CEAF24C10BBA31C3A7C43B37C314BAFB6EB15B697F78E52DB6A556CE3FA612CA2CA6D10A817DB18DFC745EBBA36BFC2DCB935EFB98912CFA2427EA162BAF44173B15F0A287D46DBCF07FB4504E1F29D73F08345039F4262B12EB71C1468EE49D54B1615545BB0D34A3036C48E0B0A0E82CFA5786A8C887C4DF9F383533511469019E6CC3FD23275D26B959B032D4A5237E6041CDE180E647AD8D0BF5579BF08DB426EFA65FD4A0716F989BB5A23E4A766286E0D73AFF31877DA81B7813E4E6AAA995A27C51D051AA788AF36CE98F0709F3D2740F2C1E9DF4079F8B4B3857E9C4A4AFCA3CDBEEB6C1DB3F7250487F94F9BBC64492A42A2268B80F9324534607C1BB3E4C23AED8BF15DAEEED48B321E8A9D4A50B337CE67B39C0D83CF2799875E99168433B6B2B3D3BA85A642C607F190AA64D722BF43CF46C21AD168A25FDB19395FAC2DC1905002D996D7B446F8E506102EF319F50B57CD215C976EFE38B3B511F1278D936D0AF7E98E1E677F0092561B6F2CEFBFEA9DCFBF1DD4A3EF0104D5F3C2B1BFF23B050DEC7C49B949BD1A46C8926D899A8A0AF17BD51B9155A54FCF932E468568288231E1524A791ED42F237FC7CC85B3FEA72E02D855D4D455BAFFF5CBCD35584326CAC13D22114B38E802AE14459BA0582975D794A3DCDF9ABA3F9B6F5428B7FE993D872691E8B26BC09F1070E2E947D3B3040F2C4351C53BEDBB6DF08F117D8D8AA90A8D74CF1D30F00BC4AD084E24D01046FF602C6F1A608F2ED920619CE246E4C337432F94A29C6B15CD35F8D3C21BD35DA2CC559EECD4504EC5121D8F4C308E65FF271BE30A4B01FE7515D254B0F457AA53B219A67D8712726AA6410165BA934375C4A5A50F2B9B108DE2F45C0B1994B1A6E59164F1B40BFF78DD7999AA7FD50DA6A723EBD700F7FEEE857BAFBFF902676A93B2F572DCA23E6F121F8CE75C7D2E4DD02B2FC51BF8AECF9E3CA488731CAF91EDC39D0B02A30C206BACC8382078B3FF4A0C4805221BA126050F119EE0EF80BD4909E37F1BF048D5FF280415682794C2EFD26B2B099C7BB3CA874EB9D45D981E0FBFA48B2A1202DB4F7B79CD5E769361BACEA7920372685E3F1B598068A625DB522FC8A048F5105B3F078D3429A42012205B2C9D9234B625822F9F9FDA8A7814AAD1111F9FD828217426432277A4C0148C9E2187BA861AA89C56AE376A889670A19FB21DAA54ECFC7F514AB55861F087DBC58E065BAD3EA1227AC336850A8F6C0DD7804D3725909C202C3231165B15C8E97DB5634E0592369467E665A9008CB80B1FECFF3E87FE5B01E8ECFB7B6C0079F3A3F3DAD3EA8BDD7F073E926DD157D14A7ED046B36FC0502D5A48A63437310CE334382A616B1752E028981C6908C09B15E7B9791C60F392FDC7F8AE327C77088E89AB7E414D7370BCB711406F4C6F12185E7D4CE91F2251EAB5C170FD4F7BC9655014B722F6CC9C2C6DCB30A9C0ACE7560F802D34C846177ABA2A8D533850F07DAE2B71D9261E7797DC3CB36926DFCC320D04D9537617FA9F2AFD0A1831B45F9146F3DE3C3886C68473F6E11C17B70DF446280AF8753F59C9B9DE8F13262BF9AB03A1FD680810D525FD4E9A59570E40EA40769FAB314D78DCDA2143470C9E64BAAFCAC00F32EF557544EA55A4DF9645FAE2C11D02860474F6DDFAE4FB205E9B9B3D28D1CBC4E1B3BD1FE692618587AF4453135AB758413E76EC961896EA622915EB53190F7751562B73E4CAA92E976B8516AE61778A877BC5B978ED406A16735FADB39E612EDB1883140FCBD08C537AFD424200C9D8B9D2672A2D5E119D49FD12A7B632F617481971808ED05F097657012C4989104A877BC66052181138891BE344D43AA8DFE8257990B33F0D33C04CAFA854AC0B85AE2F9A51A8A6CDA0EC0EA8053D5A4CB2EACE87A78A307E20162DD2B1505DA02F8208F2EA4517ECD1C48734CEC5EE8830426624D02369CFC8D6AF078B356596CC7E96054D7E3F3371F058C0AC4144CF835FEBCDE62ED6CBB9798ABF08982E93F6303B01A699FB306D46B75A416E0B2F3FD551023BCF934C5C0549FBC2D806A513DA940E41A3DD3AE47D0AD0954810E5505CF6C2B2A658BE79F9F7E2BFE380F54B53CD8C7F6B33CF79F10119956E4F6E735292C009FD5737C2E943F7001B726AE875C80EAA247382C44C6C3FF262C529318892B14D28DD359544FA10ED0DA1D45D355D02862E521B548A31DABBF80334F5675F1EDCCE4BDF7B3AD83790A6E0B6C29154B0AFD92DBA6E52CCD9E41B1BC4BEAF10536764EC56328CBAC0F0EDB389BE0E50414E84B998F433DE569EB10F066A091EFDA2A7F26719C6355B2E6AF20CB45A3411C8692BB3B7CEFE271DFE653CA0372EF144C57AC03D8B211460F9F24F68BE2C227FEA8B34CB77D7941D9D443342A67021A8A0AA889DDC0930724FC76E328714A91CD0D3437532C1A3793D3F9E05B6570FB1FFB03C4E985E18DC93424574E70630AD819C0A7B7223995ADEF0F12639A104F37835B3B5A7F377C8ECDE33CDB8572B9CEE22CBE51A14640CB539C2B3070F0CC09A49E4CFA548D399D7E0EF1AEEA999C57F2654B88CB73E4484BF72D2EADD5DDE28590E074BE09328DB0E3714D18DECAB85523BAF16B726A818BFFFB171E8279E63F393F4A2BFBF6DE2485FCC0D709B28E327CE118EC522B8E49A4BB7C66769F9E55A17A6F0B406210CEE62EE37774926659CFC0D4050454D9BAEF9A0042B3EF841D57E968C0333A4705E5AF41C3FA9046A7F897FF0F680451E01E268F277EFEC63A8C14803A16A51DBEA6524EF3EFD7A085122AB08933C18646A78C9EC1C6ABFC5452D2C6FBE450A30E2E3209D2375F18FCDA63AB5836A686192829138603EBD50152F64EE6B1D632F2ADD1FA1C4BF5519E07E9D4994970EC203F17ACBC563F8FABF567C4B3792E9CEA6D3023B2A15820CB3C37FD38CCCD2970951BC84259F1EE6265688E66FEEF1696AA2D0035DFEBD995A440C522B854D1484B16B3D98B524E4E408AE5F5D24B21DE3AD05484787FDAB88EA9111FD5C4CB338BF83883EA0002C00A6E564FED83DDFD731625FEA476CA86148C05FFC514CF9EF15383CC1CD0D5B113410D7705646E40152DC453E0322BF53B210B0071F43272110D1DEF4E999D35CA8E458C877C1D845C371B3AC3C65D9B3230DAC32E876A8DF9D7AB77F4C6541DF3334513B89179BFA0D6F331164F7760D54FCC66A756B0E3DFB74FCEAC937CB3765BFAABD04BE038EA9C0F64C69C61CC7A92A7F9B9A545CDE51BF148849EEA76A61D02B3819B894C1EFB1C03173AC087C93A4B1472C06182445FC3139B8A6C58B21261721D35356154AE8E8BF24A22E1864FA9A70DE778079504FE8EB081681D69A4E1B773BAE23F500BEC78754E48C506FC28421582FFB37B6A7BD57042D01A3E94CDB0CEC6DB6C579116C9724966D1E3014DB62F9094F228969C1EFB7615C4B39E351BC8842140C0516AA3FF97591EC0449E0B1F6FE57EDAB8FA7AE947E71995434940B34DDE609E1A41A85F85B4ED5A56B0EBF824AA65D1B38BCCA70D434FE782786C92E1F73820B26CE01A57327383C6D2948D2EFAA6B85FB8FE90A1D331D49D9C70C4844E2C9B56E3066BE46397C6DF860AC547E0F5E3715E8627F168C57F1683CFD5F7FFCFBEE03CC5E3A8771D6D9D57F31A3D5AC385405372FEE9D69570B03DCEE45D374E60AFA262756105F747EFB5833D213D84EFAD742417E5BAAF236B0D9B66C490D580A56A3E8AA2F0690D9D9AD6E9B46C714B9876CB7E723CCEB78EC35E78530FEAFC722BF66E8500C78E97B77DAB95034804EBC9702FCE2C238538AAEF427C6EC4CFC7B6B7AE1639078588FF43DB0D214B57E4BD756FDEB8CC0B16F67FC7131CC4A6623BB887421AF374F0A3A69CCC19152F6DF33EE12BC535E326D927A0F537C7EDE932A1E4DD9A6C22F0BAFBD42376782E52F89A17CF89026E2EF88E732EB01B16ABF0BC09EEF17A9377F3DC4FA325A3EF9FCC49CD324625340B3FFA855708372F1E658FA39FBFE5B00BD4B457829276724D3E07464B977859A979D04C9CEE5E97FD10403F3E8912BB7F682A74EC6BD2E09364AA5EDF9F4DA884BD35CC0C77E6CCD4880C33E68589623F49D5C9EAB85E02F1B72938C75135938154FB099F0BAB69D0529296C6741070FCCBA383E48D44315F5F8E6867CAB94933F74AD50A8D838EA304346993A4E764ED0D88C44F516E362DEC839B975F773A07333917C524BA6A2E647DF25640F1A520EFDD562082B0F711F15641BF11969E11A522E6C1344C715E5823816AEA6E8357E52B2D29620F62FEEB195515FD2F5E48BBF994D0EE275B517D82989B846D95EB193C056BD64B66FBA73758A59AF7A852D6BE7EF2DE33C6216409CA5A8B9AA4BE1816A335717FCC4D74E96D9022CD09A50AAA1A42BA5E8218C5A0171EF00C33B5983452232981E968D1429EFF33BA672FBC46C05B045B90CB0C7F0DAFB92FE30AC3F86D2EF48E54689F7B31D7B9B84D66DF00AF7EB288F9F909226109AD8225E6A6053238549C9E508FB4B0AA6ADE46F7AE3AB94779E928C288DE682FBF9C60407B92BD743819B8A0F6145B19308DA1191AD9BC2ABBB8B9FDF42673E2372D8AB3E739C3AF7A328E53D285FF02AD3A9E30483C80583F213CD656999D860B9972FB6C2A6CA8D31DEF5B5E18B0597CAE29423B99C5BB3D76E0D2FD8B28AD027D0A764192854A48EB9EC85F49EB7763656478DC23E34FC6E2C8972B81814F2CCB3567249FB748ABE41625159CF7CD6E8CB3929D441696B6B2102C8A22C3E741BA467A5F353F19430F13CD1F8D5B2F3CAD0E62EE0B34FF1D423CF40B3023E14C6831F3C6280B4F6D04227562C0DCDB1C5E8212DFE710923461876FBB862EEB334621B74BA1BD484172B812C9181EF8E7846C2F9B336A13205E4BC4F4C0E90F2A6F53CD1A58499FAD04AF550A5D9E5A07F56E6454F5041A556F64A3C1497AB3325612E6510FC911D9475CB0E594E051160EDA18CD7E0D05ADADB5A5D9C678B7D1539BEB204630962FB47002D9CE6B20DF92F9CC14ADB116F0B989A50DD863F66AE3FECDE106C9D839DBC35759F0EBCF49E65A1E3007556BBC88204A2268F191E87F3E971D406E7E147F43350A55E5BBC75CE927BC75DE46E885B9B87073F96AA083A87649D80655E8627578E70BD48F0460FFCF5126D6883EB29BEDD14CAD122186876B3320B32FB87000679083D0060E50B19A2DECC999CE0EC2A53725F99EEB4C600C85E323DB1EEB3C4B056848E5B1EB6812AB23BC499BBC9F95D33BE590CD3FA72E657F18A45A6FB4BFF9A5ABA5CA4D2A4B47B23983B3758D45C37B46E866C5D0F1F72966E800D0FCF766F316A1031A506F0EB26BA61477049A2B8EABABF33BE5135AE8A00C974DBB860E27FB710B53AEC21F97AEC7E5CFD717BDB0A39707A8C8DD5C40F4E9275FD1FC823F702FC4CFF7FE3715D4D7F315EB7BA4AB32370CD2F17B7D02673BAB1AE4510F4DF797D8CDA54CA7BA2A572115494477DCE9028A92B431BE85FFB0AF9C9ED3BF876AAB59CC9F63A6D8FD1DD7437F878C2E81989FAAE6A17B07517A1F3017E81CD47338E9CBC82F4FA9DE75CDFEC725010ED1C042EDF4E420DFBE205C0CACE088FF81F235E9FF8F146CB93383647E2EBAFEAAEDB987F33D645793615B7AC9BC032246C02F2B16F2490DBD30F39AAB450B3CB1E2AAD8D2AE951133F23C29FE2CE94C3E9BF101CC97EDF6B781C3D5D33885D4B77BF2A25E8D63375542A6CC8BC37CC4205BE324492AB38E739171152D5090ED528F322CEF54FE269180CD33CA31FD232CF93760E4BCCCCBA3F812FFBBB99FB9D41D86C1CC5D78BE548F2E8F57408239B7C8EC650A05965EE27F42FB11A4A52A6AC3938BE14EEA9FFFA754190B9668B173D8E28482BADC9AF00A4946004DC7C933E7866A33E89DBC67AF3605B9C8503D61DED2F8A8ACC693247A6B25EE677C961EC1E73684EEE23B6CE7EC25E8E5CE2AB9CAA80E4062051BB1453F97FA9A625214F94963D24E24720E942C6143C747642855C86075D18C26CCD83B7C1FB015F2BE5604089FF83FEEF373B75BAE8D116229B68E6034045F499634060E8148C6A8F6501540D5B67B6EF8A2E1D154C858AC54EADC427DECD22BF13FE69ABB40028A068404EA6A51A23CCB65DC500ADCB429FED433B33F540C934ECC5649E3439846FBF2A869DBBA97BA9FF2276D769D22FDE991838BFDDCB4B1899906D6B3AE70C6215D338FCEDD0D684A13FC263E408AACD65CE55F1B89CBE690E4065F98B51F614AA85EADB5F99279DAD9EFDF58015FBBA03B440211AF6F9A1E60E7CABF888FE1399F9ACF9285685330C55B339E49B11C837BBA998E682C5A21CD0421FD488ADB8FDD30546A5271D0AB6D80419E15B41E70F3650FBB6EDC2ED5AF3C2ADAD1039355E4BA3027D735787B12DC2B01C2337297FD6A68CC9CD14B43CD29F321042D0B810048E54940F01BD0179C47156287A4DB1DCD7BF83CC83AA00E5BC01CD2BBDDB4B31E1E9B3D9467730A39FA7C742C5109478AE4BEA11BEEA4D7B33A85AA83137D44BFA36EB8657DA1557CBE9F5F4199F38F926C284F0CDE175ACE29CAAAAA5CDCDCA08210C87B90458DB49C47C5281701A824384BB71D7503183BDB61F56E9C7B001C91724368A82F82DAD3EE49B50CE4F8BF28F9E92308CF0F4F853BF5E15E437CDA39E4D76C606FBAC855C8584CD77A778BAC6717A50A3CAA6E0A35EE4862A1483ABED13816C5CC76422B4ADED260F93E908F818D1BD08BFDA1AA83132F4F901A395CE99B9A6C1D594838C0971EFE2579A35AEC5F5278CDE3B9B2D6F1F494051BA069F652C3B1758FB4E196C49322E705707A6F7A1E8AB55AE3D255F156F01403253497E37CC006D71B3B1E4BF1D94C2E36AC3BCB4D2EBFC2EE2DB25BA272E121DB2070EA8D411A2A92D2FB9E28EBDF34774F520E0218B1E91F3018A0B1E729DE59ACE6A78CB38CE6F1075F2D6C4FEDF6DD1656E130D37D23B768F34048B8AC8131DC7CE2C93783CA57ED22A941101D98B6D97A2866ED74F9C4EE0A084ECC3070F12336E109C286D9FF74EA02033205156889EAF6792BF0003E90735986B7E789B58774F52003F2AA0AB7420147E9B48BE5D4711DA5AC8E1B794F06EC540C6905195D758258B05C8C2FF57A7426EC97D67D99989FB1120BD8AE6D6F2761D583E17548A77F5F8C8C922B8C3CC7244E7CFF7920187A0F46A4ABBA61EDAE4CA804014D457404376EEA125C8A7184AA92FDA05AE53A70D0525E6947C0FB691A723982C12F65215F15ECD460358B7FED1F65BC144312C406D2A1427139A65DE1FE79F2C6142DB75DA4A767D08B87E34DA7C06237C3484650016F1A73A94B17C1ACDC8E4D10D62ECA9478E425ABA382CCE758C8B5D9445456184B1E8E9FC6E3CE64FF04EC005B0D286C5302A7FD30971624796B766144AF88F982D72E919F1E7DB3425954B72D8B005300972A04CFA623A3FFF8F7A9E5FFC708A96EF692E6FE5B00406B86F3AFAFA75ECB3215E5BD34DC4002465A72A89BA0A2DD590D5D893304CB48E05B358E7421120EFE35BBCA8A542011E39C5C12B96D4A724DE1209F2F91127D9A648A493CC1A0089EC3478DB17D508DF025254AD4A5776F274FEE94D03AD08029A216527DAFFC120E8B7092216BF7B58EE5D60DA2C45E3DEF728E2869EF72C1959FFEDB6792483DE8998A8161D73BF3275743AAE7D25D85E8F39635EA84861850BDB75FD46955DFEC6EF791903C87CA918CF0CC88CEBFED9744C84F52050B02D5833FCD5030DAC006DD73F5F45591B05E67488D57B5698C6ABD70F56443F6D3EC85F5BD6CAB91C17E6F5A2708C95655F3DC41B7627C717AEF8A98C4934DE3F157BA3983E8541B84D72696C7301B2A7EEADD80D687AADF0C830A2953D24497F62E3CEE49BF5C7B37E1C9BC97A212D73C01E82546A71B7B97165D6D960DADFA98EA0A12AEC74385B14C91B650E3F9205F7812D2EE4FE85F3E52AD81F609CE576F85383B285DBDAFC60E87A95459D1186FFDFBDF84082D05A676FDAAE5B77854433CEDDA3AC14D28A60A47B0CD9799CF958D839697CD4CC2644203EB98D27EEFA5378B9741C177241F98F4105F8010A1BB58953F409D4AB08537D231DF248178F9F63E9CA44F2C6FAB9C1F193F4B3D67CC9899A08504A84973FDF62ED28F1405F299059F9E96023F2E7972FB32733FA3BC2A5CDE09F897747B1464E1EDE42F2809A8E906BDC76BA2A5E44521E647D150B2C06CB1D8DDEFD97F11B0A7350DC47104DF1DFCC074A385E67521975F550CA51FA85339F928BDEA45D292C4E92231925F9F9788A259FBEADCAC057E90B64966B458F91B7C18872427BF5CE6B5C14717FD09407AD382B41A130672A6430BA5760AB4C4368CBD8A5CDD98C1B778E9DAA6C4B7A36580366D22943B908971EEA8527A50B170625394B437FCC19539E1C82E7B5015089AEE5A4287E53E2180CB8401D9D9DC598AB810ACE255E37C2699767A72E71085FAFDDCA057FCAD37C6ADE547D111D9F67D2C29DB6D0D1271666713E9CE75D192CAC4C1EF88DB65AF8B987D4A679CC0380B4E1A15A3A6EA8A50BC5F10D23C8847AB5933FEF36600BB3E7183830F6DCDEDCCE37B1E2073F5192B68F903F62E9B1B032FE3160983D36B18F5ABB380F279B20D00F49EE11AEA0FFD17F8666F8A4650F55C1920DDC427AA5B0C8F8D2686F3BFC7358702BC56C6EC0EEB322AC310916E81CD137991A428D134F9555A7302ECCB5DE3E14D0E4A04C28B7011D5315DE42B858AD613AE173C67AC7E48AC1D693D8C2BB5F31D693B04A7DFF27C5024506A97C6A735E32809B243FE0870BCC984FD6512C8F76E8BF53E817F8CDE97CA2A51E30E805110309207500066450C00FF238D96DA42B2F0B016076A034E1FEBE9E47F145C1A5D76810A2CE94371DC6505234AB38D5886780FDCA16F79ED01FC33F66729F50AE3B5179CC77EEC5C4FA997F331E0288C6269AB640BB5B3239A658D1F05DA2DBA7D14A72268BE76A439D188CD314B7450D41BEA969ADE960DBE65D04ECDC8D8FAEFD70D5FF65CD9D860251849C6E6682CA410A284720A4D187103D9DAC44C5DB88704842BC0E6D9848E4EFF0A09113C7333F2116E513B4D1F52FA2349DA6E672299BB27DE6EA4CBA57D17B4A115552B2B9FF3A08CCDE80C65C535F47B5777E94C96360E1971B9994EA2902707E08E218EC1267DB699FE28DF03555462DECABE3DF6600358431DECC2CF516C6EF1FB3C6AEB5BB587A149CE11BE3982400F744821539696CBB22287B2AE2FA198326D1EB39FB64F46596E86FD9C9A874362DCFD8E9D3AE75849F27CCF487E7301002EC490A9A03205D1619F233214F3F0E0A523B899D8BD4A26F59A8BA2828766CEB90D0B183CE95BD826D291F5FF12E23AB3589CB49B0E25D547E6F61867C7752FD8F80CF61E58650478B85E99362886F6296B88A1B777795B802F17C5F288BCEBF2F55848A35ADCE096E888457A414C02A1425327561D07FACFAC1DC869181A184DD271508E0C298FFB69996B9CB33C7C376D021DEB3F75F1E99180AEC0B2D0EF58F43157B896DA5DE29D42D39D180533C44F75A2ACAC0B1314635174BF4CF5ADB3C2ED19CF20143ED4142D123355B9EF2226AD97D9A97703000864E2136DA1E5CE882ED226CBF636C6EF19F8D62FB476F54D069A71E8690B0B7D4CBE192C381FED9E24B77135D1792937502876E5E236D631820DB231D3B01118E4A6CDE28297AD1FC5F33A0B9E02BC91D8E43B81726C45CEF8C0A8C945DEA0248C33E7C8C5F91B5611B8449E2DA36BE8220B3C7EA74D2A367E92E8720D2E4C4C5F291B29C8CF694E82A9164630D1B3E323D776FAEF5B96B5747A352DCAEB7B56CBED37448394CE152E1300B4D5AA271AF944B86B47422BC80A0D77D6D617AA13AE727F105CAA8303C5AA1F4E3A88EE6B16E2C162C45EA0103C8C4CB2E201397A7B34EBC087534DFE09F8177E1AC8BB41371B0FB27D40FC7882A8008A55A4A29E8182B2F2A4C84F06337942D66E56A4C61BD9EED76C937F1DD5B1910265714E6F9746A333C0BE03D27F15C4B2CA0A54E5174043BCB87E9CAAEBFB6CB9683A4883C7F5DBB3423C54BD8D78E7738761F463445850C236A29EE1486201E4213B595A4B4D5B76BBE39BF860130AD33CB85841BF4829B61BE0881CBD51BCBEA5BEFFC1BC90476BB9A9B5EE3F07302088A809F8B29811B16A1514B54EDC293CD784F95AD33E60EA38AF39C42F4EE5E5A28DC39096B91105540AD0883E718224883FCE386F3C19570347D021DF9B342FFEDC3F76B6A1986494FA3E282B0121D0B9E5FAE9AAEF4BD408A20C1D00D493DE6E2C5205E6CBBD9DAFE1EDE407FEDE5EF357C7CC86D1C83D37036119BAF95E209BD92A46E32C51963B879A3C95923F4B02EA1CA16BF95FF70326A3DCD6580B081F6067F3E98318C8606C3AF343AE350831A919BDADD502321D0E905E23E73673BE5528703BD8ACE9C05C3BCE81536ED613FFFB00E6BCE3B6B5548B4D72000F1CA79F320AB83B902EA2FAB9EDEB74BEFB1FC13F8E83DE2B9F38F758704D95C9EAA4BC1CD52EF3A6F83D282063CCD2CA38C14AD29E796AE2C53130F37DACFEC8AEEB3068F5E6D58FFB107562A9725FB802069DDB9655A767032C7F046D8B81BF089471BE72B67F64EFD430F94F0DBFA6359C2A7668E69CCCF2D3233A9D5B386974684E8DF3E3F3169C8B37F29BC1CCA40353100F70F673206D04DAFFD8805217E1536899B5D9A7E420E631083E20BC2AD7D0524499D87B8239FC8274DFB8FEF450732B99FCAE56B983813E4DD7A07E5099D80EA87F1BC38167CDFA2BC0BAB3BFE2EBF2D2E5506BCF1AA85E824971242174828F97629B4B897FF979ABB507FD56AE4F249CCF398AA4DAC51B3CA0ADBF9AA286A2C88C34D8FD17F416D0E5F72DE3AF7D7E4401574D9F157696CC2240F8406CB03F7ABEC1149642E485CC430EADE29E29442FA950A393EDEC04C6196D28CEC8152792F22A2C0C1241F168722CE30C2161DFE947D94E795CA7AF2F1D0DCFBB415AC1EBFD83A197FA51D93F3825A944D31F11D21A1108040EB7AF69284CB5E7B8E0E03C18E6D202E0F11AE29FCBAA314FF3044FE4F5595690DACD6C376A0639E6404B900566AF6F454828222C39AB873CBD1B4DA63476D8DCAEBFCAF07B16BE9798E85B7F19CFA146E0729358445E50163BB003E3049D466735E1881762C894A237A3A685A0DE19C488D8BF38C862A5D0A15C8F55E6D8104F3BE4D670735CF002D58B282AB737CF744887F7345049566DA37DB1596E20CFD4F32DBE0B1D3ADB2F999BDE8620D8BE53223D406AAB4687114D13ED44136B3E7104CB832E3CA7B2310A41084406F335C4F7F2AA24351195E37D8E9870D9DD9155424081DA24D6CA6779182823BC94527AB87D5D6CDB937EE5089FBAE0E4896D64F0156C3A542E58F33D9BE037872E8055DFDB330A85F5BE3BDB573EF42B83D3AB060365695BBEDE4471D4FCF4356AA457A6C08B8D1B5B31C062F641636A7AF288F0390A2FDEE5F6A3C1E3432D4BC53C6076BE723086FD25A4F727F1A89107B9F61A68FE5E39CF98B484E0DD97BDF969B7FF584241C54530ED8F8B95D5C52FCC1A22E306E59255C19FC2DA779AE734EC13376266C42F7F46D9D21024B08EB629018FEFB729CAD8FB99EF6D0E54FA7594FD0CB85914AA2E0F3F5FEA93CD8B776F3543F2D40A95A95D439A06D8893655E3A01AE8707687881D07B421A04238537F664BCEF2A1910F0C2EEC41853E7E29D6FD544774527C949E1F1D33FC8E1F34463D45CF9BC98E7CA179E32E3433055C11B304A570934A08B9518487DDE152E919F4A0C79CB291F63E8A041C61E15CB5405FC4C5A872759F2B4E175B41CD652AFDE118D2FFA2D9E974C796D0C518C8DB13923B79A2175ED2E85439963B024FC91E7062C4B66841802975A66FDAB79A62A5D34462C6225B636B9D4517F532702FBB49E4E6C85D821637DC314CA3471F82714C48641B27C634CC6A18093CCA9C41672D9D6986748F3C6297C3F9E5B64250AAB153326919CD0BC2557D4B85D82A5CB235B26B2035F256DC863DBBC477EE406C7AB0EC534696A4EF1E525594A542B255C4E364CD26A3A9220EEA99B303F6F624F2D51123BB3E1EA460D8FB7096FB836C7F87FF092D62171B4E1E49463288CB14778EF73FAB14D8D300A09D6EEC355AD5A2A706E4408D249B200B8D6F946DBD11DC44689F9C8BF18CD2C859C2264BD9E2CDAFC75E344BB30F5B06105FFC0553CCBDC93F7FF08B3E4AD19D927F9F1B1C2B4A0C176030AB7F15D5A2AB5172877BFDA4BF37CDB6B6BAC12249C2CA0CED8539ED28E56B069AEDBEEC8CEB8DBEECFA1F4696337A68A8B7B821C8242D1A9A7AA9B1709ACEF73058F734F945AF01811D61EB0C726C2DB7B5C4CCDF0B92D97943A7C804F4EFD9B0715B30CABCC2370CF0849AA444EDC8F282378373C644F63C81CBDD91E767BAD34CD1AD4E2139F9119FA04FFCDB8B3AE112B5EB95EB8ECBDE53B4D39360FAC0825352B150D408F1CCEBA4454A38DD08620FA1B16A734473F5F9CAA76BD4103FAEC35FFFB7B220544DA3A7BB311E8F28EFCE98F51998E3B32DC0C6DFB13C0602B4E4F4539C5075FB498370AB197FA5358C914D1012DB9618FA7154632365457BA410E5CCC8B66E54D8525B71CFBAD17DB5DB216C565839763A57C4D3516A9BC52DA1B2D79F50E27AEE42BD47FB49C1C71FCFBF519FB0A9DC883B87F8FF411F62737C21D4156F8DD8FE248C58402F19BA7705880032A92A952411A6C2870F38F0C9B5419A6CD440FC1396E466AF727D837D1C630C3E6FA5E014E6AE8E1B78E23CD3407102B17350EF5D6605B71CEF6C9845024EC6EA685F0C697CF1FB8C86055F85DC37070046ACC64D001DC34A110C531EAF26E31738E86BEA86891ECDAE955447D59BC64ECB9DB53F8141751D162EEAD0D33C666CA96D85AFAE3CA219D18302D645FC9C222B37A9123E797E301E77E65D3045B3E28AC18EE3A013055C3461F90C38F51B35EE889869FF89856E13A65810BC0A61412E54490829E1348F3180F0D08838FF0A5FAB6B4A4C384C2C9B66623BF82E47575374E4E987CA1311C56226BA924F1EC9A7B14115BD86A238C7150D958368E63CD4A1D9B536DD5A2803DB6732D9CFD834D96ED4C4BF18391CB09F5C61172EA9076A7DE05B8707EC7DC15B38815A767414C876F603F5B33501817A189BF80682C1D2F366435FD1B35D1C4DA5AB79FF3E5ED824363CA7562F926D1E2D991DDE6C160CF85B4FBADA1C1BF7148765FA71958C4ECF4FDC3496644E03B95A1ADC43FD058D926A28B74B6A27339F89D3B0763F28F8EE992B17E5584A1E61D51D30DC114A7133EA8A7CAE0DB8C8F0563745C53336CABFA1EA2E89AD3C8616F177B272A086A77025A05A6FCCECB6A26F081BB6CC7AF630C3CDC98FCCE605AB630F33C29B6BF8DC7725E2DAF7DC20BA379A5AE4719696A484B1DCF009E26D82B06BA976901BAD901E65B664323A2D7B52F94A357664768CFFC15D629AB223996CF9196F0742FE920387A74461086651D2F70B07EADD7FF58FA69F01BC58DA75D6DDF0324456DC14E0C4A7844F8D517A2A7379C0967CA9E3F266FCADF0069C860762CB72075716C7ECB7087DCBB9C922F9C94E2C2D0C53A948D1AB04CDC86B895607C2468674BF016B758DBAAAC92DD530B8A37C01C095E9CC9841F65876E547F100BA5AC9FCCE1508434A49686813831C0F2204676C1D0C642482DE824F994F5A26E90396A28EB627374D8DA1B25B39510B757761D1A1A638F2E36932E0D5FFA0BBE46AE3A6760659DCDBA20A6BAC9DEDA1FD8B728B3EFF5EA32774D2BF89828727C5BBE2CB9A378A983FAA68C6BF9C99F3E3002CBA8BB3EB8C632003AEB6C1A8CB935E7AA3E9FE5FE2B0622522AF3F4097E61B7C3991B2FC03BAF9154A6F16750E2D41185E0C858FD4433D0046EB3ABABE63491D8FE69211307D8A126412D7C16C292F4F09EFB8AF77D2A30FBBDEC80ADAA3AF1499B835747D69B9CF182F1348714B7C06634D4322FC837243EA52DBC817F032A5A9E960EA320FBF68F32C038CB79F4CE11CD183F250031192ADA4B8F9F73D8144F222921F5CB6B3ED11419E79EC9C4E923754A4138DC7ADC9C4A26FF23338EE7BCF11CFAD40300875A8BECB1407AE659C62D8E53FB9C2C036B56A1750381D3D5CD41878DC8D561C672E74C41C9D6110E3720DBE4CE6E98D84FA6949A35C12719E4CC966AC790D058DAE86549D4D41FA406F7F3101476A4443B1648C304D8961817C5FD14E29E0691A6D4B57A5B7BE76256A1A138F506EFBD3EFF33D58FD27AE95F105A5F2375847CFC5CDA48624A691773350EFE9F2771B369F7F28B1B209F9685AFD0D4B68F15F9A1A27C5C8D7BC409FDD86B8C596DE363C9BF34E95BEE74B2E6F75EEB7705BF399DFBD6FE5B1F850DDE11BFBCA8B5304B09F86679E3E4D60BD5529F9BEEA162B5EA4757D3AD1E7B4AB0863A582A1C450AA5EF4CE29156070A7B572BA64F1BA3BE597117E67566BBA3E444EBBA7A4AD9A32BB9545CB8966C8821B45678F42FB39474B6F507182D99AB1B33188BBDA829D4A2D02930A8C436D805DC171596D7C9255DFF4D2C8026A94EB1EEE553EB250CA7B4A3205345EDD14AD74BDC69AC81F6189EF34B2F36BA537A4BDF5F5E901D14F7445E9BAAF473CBEC9919CB9CBD9A2C5F29FD0FC737D8AEC564DF774E331FED221191282CE28F1A41A30233E17742D83E825EDC24181731C21865FF2891B595E851ABE48ADB7126ADD62A827A514283D56F6A4667C517C92A12797C6AB02E85248B87BD52A9730B92DEB3B052527784C9716A99C7B606555FE3B8AB083009AF6BED6853D0B81418E29B51EB60A0BD3826DD76F9BF64CC2F16EE9855ED6D6A44A24076D5BEE1F2B3B4E432C795E81E2A2046660FBEF1F44AF9DAC1FAB495E5FEF9365190F769DC1B495D62311791301FE2D5FCF3E58F1F56087BC8EF29807FF1218B012994A4DFDBA8D7C3CAD4C3D63DC67E2BE4451E009B0A65B36D86853866D279A73E903ADA4E62087D3DA7E526A981500F0328C32F3A7CF783AC7625FA45F4C7984683EFA9B76FAE716D97EE167736626987279BB204F17B87D9F1FBD4B5055AEFA76BB98BD506E27A0911FFAE1AACD8D2C62E780F74BEF759A627D52005A393BF8738BD9627DDEA49DA832E9130796F880D99255BF81AC00F0CA8866D3E2A7F925984349753D7F6A4F4AAFF4F27CE3612AE310C519584D7C1BDDFB5AD5E065589FFF8858E6F2D1F1814B41B5126EA814356D9A925F89A6B097D92AE7E529B280582CFA31AC6E9271AEE6F09E25350A968E0636632C97797F307CC4ED644BC8F9BF7C074E804DD016CB258D42C4379828AD4FE03EB3C9CC10690F670EC150362AF9C510DB237A2276C9AC4EE5A2361806F3452201A7A5659834AF5731CDC029BD067E4892B6FD7975FD6B610A35438B2FBD0DE00D98B0762582EAC079A6176FEF7B7B019488EE76E9B12E5E3F7AB242432699F0A577C8D69E704511D108D590EA1AB6E337179E6CF3EC1C1D1650540501319E7F5C968B47EA3D9F7BA2553DBF4F44DA6822A6D4252B21F6AB568E6323661753C0C5D78DBE610B261F889E6B69A9F8467E76E34264224AECEF259557D6F2341FC8E4786ED7376A130AFE58309F6A8373BAC6ED808DB0FA3DDEE9D4000EB2A4FB7457826EE1CA0B3C3E0C285025DE53D0F8A4D205B14BE463BE268F5E0F0ABF4DD9919F4AC34CD2EC337657A7A4D205C626651C73140F0889DCB328EA41E4548C9D6BF7F064BD4EA58DB3968A7EDF1F52BBC34AC85134B6062511D1E37709DBBA358D9BD6625277DD787FDB376B5EBCCC609AAFD8F37451814B2C1ADEB1D91A79CCF8AC905562957AAEA2C4161C05E7D61D53A28BBD489193A071693252C2FB5C1031ACEF3A6A3BBFF06ECDBC5799B52565B7030414263B6C2DD57C34172EF0BE0AF7B8A26F33B2435F51476E7BA309039D5E7D986299E00AA24158896D4FF3639D61C6A56B2EA79313D59894844F3988E6DFB12029C3FC81952572ED94E58A97D0C61DE2803385E331E7CF64F59DD7A33B048E9CE8ACADC1C0E7210D73A397D4B2FA154A480AAE6C01A16FA8626D2F5CF079C04F924C6EEC1966DFE7D1A4993F7537B2BC31E66C6B8B871B699E5A5BFFF125150964B1B0FFA1C78F0696B990C65DBE72DE216C53714E3EFBCB520E5BECEE2FC1D7B78E05020E4DA0DFEDEC18A2524AED0C63EBE1EC6BB84283BB83553BB152CFEC0F503EF8D1D0C33464FB52E2D2354A93DA434171098914E761FFEB1C494C860E143EEF49EEF85C4AEAEC8C371723FD5ADD33F3C0E8EEC3CB433DA7CFC29D068173C185A448788F3927048D94895A91677992A200BF603A04453D27B1A32951264FA20E8770955C05B6F8F36825F087521A8C39AA4CF8362C2AC6E7AC8CE44AFD935CBDECF994FE3724D289DF93B8AC1D6B60162E444CABF1E1BC7784DD89B1893AA5E5F3EDB3E1A6CE5311F8208E2FF03EB6045BB620532D59B71AA2C699B0920811720B4A9DD08A49C7D29FA110ED4F88D1D52A7FB7620FEF93DEFAD01ADA5E13028A7FA6FD14FB42C267D7F5BE357237BB7C8B3294C7B66AA217E18E61477450FADEDF65DA979E5EC28CE6388DDADD75519B85DA610E5FC6198B1619E2F5A71087363E6746D0135323B6C441A92A22CED12F72E38B6C75E99878BD9FFD1A08C04C2FCA595F4E17197D3B892775F70D1D9C6E1FFB3F05182812E66136091649044874187CC5CF29CE60C458A6D2C077771A2D0467BF7752D05BA8A9B98C1596C15500BC317D13C73C086D7621D6E848BB5456E976585AFCC33C13037507B1706429A1826FE213620D752FF9DC889818A1535FC1CC870BE9CF4B162C856C50162F3A3B3B3B004072BFE60EFFFD36E347ACAED65888C85A64B16B8EAF09748157184F7247FD0D2DCFB550E7715992A8928DAF3F8721E5D14B62D5A5FF8B42931F615348A1DAC335E6CD778EB639F61B9C0159F57EC21ADF4718772CBCB92CACBF8B34F51906F1AFF8AB13A8E0EC198338BDC41358FDD280E181BA457FC18E18918FDAE77E0AAAB32C3624195A84B3F36BB8F04EF6A55A5AD8DFA413583297E4D6E2FD159C5F62C7012540B64DB9637B443C16508F9C845CD4F065881D8D7C65676BB2C70D7775B6F9DA39F361F50574A7CB818A68F05E08FAEAF5ED9213FCA55FA2DD17E4C8E105B0771CF769423A717C1AC06CE878A7428FBDEEC6C337E6475F6A30909A31CB22481E26D864619872FA68596BC73E4C2EA11EB281B2CA4337274CB510D3E8BA03A3D2DCB2C8DEEF69962BCC50D2037682EF55A63FAEB9B70B01B8276D5BAF9E1543A739DFEF3B8760296AD3FE6846DFDCB4C9DDEC389F39FC77D7155579121FAF1365A73CBA8B4E5E90D6FCF49993BA03D0E13DB6C5207987F1E36206BCE2B83F7F19B0A502B7BDEF70B94682E7D97D8697E16B23DAB238D34BB36904EEC1F93924D0434B76A1CEA0520E6E6817950903C5BD001A5F04947645BA9003982D6B3760E2DF6EC41D97F476664011B44EABB2F9B91222148983EC5E6BC106967876ADD9CB5B9831CCAEC36C6B12DA5FC84EBA6F2D0C42132E43F83D01EB94D68A575E6C352F93EEB1B6F321BF22E19E9108EB4998A1D37952DBD375E80C10E9D4C0F95AFEBDCE3C7DC2679C3AC210381EBDF83D1ADD41B6DF9A44DF0AF3C670E6EC53F98EBE04A245D121B7345E5384420FC99323515E5AAFF60968AC20622157FAC9224CDCF4A16B4C836543D4D43DAB5F96D02A885D21C5065DF1DF5E74BEE9BD8A4F6EDCB5055A68DED03495F9835261A4FC0BA268C17DA5F899623FDAAF4EEF6DD5B8CBE511A8B65423CBA3504D189AE516ED7A806A36B25033F52706660E0A48A1E00ADC6AD0E1064DE0F0443E7B81643AB9B92D51D200827B51D6F01DE2FF8694D0B233E7C9A4C825E3D5224BF54795CC5E6047B26A935C73D7C323910DF73BC07C6D3EBF22315B52334B806BA441BE33E7FA81D02131E5D5F7A11209C76C4DDD3C98DFF9FEDE9B21CA47CE4F06EFD0F766C6C97BEBDEFD777B7E6CEDAD5D7D4B904549787BE8163FC055190A630FF916B7910002FC96DD1629228B2CEC74A0591DDBC60DD477F1DD01FED829F46BE12052E8C5DD445E31606565155CA77C7F3F326CEAB23D929F674B53FB04A95C0A82246058622F4EA759DBFBB04883619109728D84A4802D84D7F3EE0A05321114642FB3897260C5B12AD7F7E6B41F6FA3765279920F511EDFC48529CE9857171F7F342355799A604BE9F2F12F7650B38F91D486F1FBC1A2EBFF5879EF7C2AAD4316CCF6F9FB29578BB8F8CA6E2FF34A621A2E145329E35895A75F2E7382F8A8EF00BA8D503CE4E6504FC2D8A0AE34982ED48A7628646C9C5CEC5FC4A7B8AF8902DA2569D05F6A46D3296292659471BB1FDD0C59106A86CC5205221C026F8E464E4BEAA5F35C823640CC40CAE2C95B38B9541D0432BF2CB068F41DF93F2720ABF6E77139334CC1F2B2E1E4682F7413201A2F36FC1DEE693319994DB32F088F97FFD1F2C40B42FAEB348B6F4F0139954CA086180C911088C1003224351BF4F36273FF3F60994E0FA01A32A91828C332926A6D456C7EC476F0AADFE9167050B4451A79A9E307A744BFDE575AD954EDB4F8A41A6E91CFE4CDB3957BE69978B308F8C85B3E5BB4E43F895DEB2184CB9AFBD45F0B392D00BCDBA5489B4280A15E50D3E0AA836CFE7DB44045A93BF784AC5B93EAC98FAC9406AAA264AE45103961697D8E8AF9ACE7F0FEA3AE8DEDCC73013F5FC47A33DD527B563E0A5C6C06A24B41F04B99F71F23D02287839E4599517A4BB08A57A65BE8C902965F31F14A649AAC5CB0F971F46BC699F34C0D691D1AFDEFC8743F06564821DA8462C4D4F388B9F6F045A29CBE86B5AEC17AE9129D5C1FE37E290635CEB149BB7C18E1B8BB8084963915475BC235BA9A8E15A36C6244E3F2D4524297DA9931F4FF1D00CEF316C2C950C388B2D3D22AF7D96FB5DF97B079C67AD8C563B2D50A79E23537F89DE94DAEEFCE8CB4D6B7754C8647E080E3A825BA18628C563B62E9BF8F360A35E5D2D472E7BFC4BDC99C219FEB31FECBA1A55A5D926B0B6ADB94BA828D57C1B7E830B1A33C6FD106D175BE6674CD92D21556D46EE90CDC5B05351EA2AAF5494BAE3952130F6226C3ED0DB102E1AF33B383B0132638FF9B1DD8CB7CF16B37E3119520CE697FEB34BC2FCCA79C379F4C6BDECEA6D316E2604CAB9D8FBF6AFFB8D955FC5760EA5EC5253DD4448907EF49B47BD96BD33BB9F755FA9776A660ED646AD782E7D4F6308F10A529E21BEDD850930E2A253AE327FDD2C76BBE513318A8D2C3ED60E6B3A682A8FE8449B195958F353820F5C5401AA24CA057B420F49F1334F60BADEB917A373D672EF67102FF00D9CF868A67C14B192810AC4BB851531D6913655F757154EA9E469519E2EF8FC2849368B4D8FD989F1F48A06ED3EA6B812CCD40882016A0552DEF6D5CAD0D81909F28CFBBD06F37F8E6B7872C465D97204C216991BB5F8F53879CA9ABD4968B25C1FF7DD1456A52BFA0BD865E13661EACBBA9C3D174A6BC9C56CB72EBD02ACC1B69AF9D3295A0AA0EE01F40F782DC48528AC11575ECF401F68127A91893ABF460528F7C97874A6CB104162FE58166D0FEFF0E9497106B7121B41B386F99F35BE5E8239E520D27675E02DA638184D8D3DFB049AD6EA7F7205E4D79014C85262231624E784D1895ABA19E5ABFA2805C908656902EA287D147331F0F8798513523361A4AF7656EBAD894D45023D7F3DF0AA86C3DFFF9F3F88DA435CBA284C98404F727AA651358BDE9944FF1DFA1B691C423B01E773B4920CD0CC121E6DDC67C68886177D27CB496ACCCC2351B7639876C37A35525F920C2D4BBB7A3CA1FE391A9EBD5CA019CD67FA8BD30C088158199419627FF716F885D47BE98899EE9390DBB66A79991419557B5BD7455A54528DB0300FEC58A3E83467B217409B160AA3A332607D058B8A66D7BE2CB628FD765D03932815CCC339427CAACD3E0B23BAFF92927ED738E93018B1BD375FA096EC51935E33E334EEAAEF97A2DC25CC5ADCD1E5B13C80AE9F28F08A866A183B08C1C2EC9D002290727B465D4542645643A9074BC2CC16A26104D38817DCD179BA1C55C154DAF8B5AE847873665032B9AD376D37943B651E07FB258B9C27985E0FD8320612DF33C31FF06F64FFD4540A3C1EB3126FD63EA0D633927275DDA8D06E66AE5FC5CE389F426A0CC4A7768D73D76D25BE00B9F287672463FB55C26372192103474D9C228932B85321A22793EE04AB306EF08548950076DF8F571232E7198550E768DA73FF002A0BB49C10B3AB8CBA2E50EBBC9A5BF35D50DF1777217BD345CEB105497D5B0E6659A7AF3BB46BF8C0E44015472691FEADA5A81ABFB69CA3C1A3DDADB266C817B0407B7743E38C7CD39B00D14F3BA91FFFE45F7C1CFC27690EDBF5D9F52FAC778D71B1446DF6859E0F39D00F8ECDCD8D24E3647125C6F9957102FB738F5C650D42CA60468E7AD122EF17B0DC8CC54980AC8750AA5D1ABF5D4E62FC81556B4DC5B8AABC59FB8103461000FD3F18D0AFD2FE5DCEBC2856CF67E728B0A4CAC6B4E59C2CCD6DD813B928536E68FDD96DDF9D36E69DED764ADDF2EC4A51BA7129B8F0F334DBEFD216A602B53EB65CE5A690AA3D0EA35981D55FB01987ED88B7754C43DC42EEE7C01ADE519CCF698FD8FFEE7F6C982EFC004867B1D46AB7D4AE0409EBAC3ED7793079A41C657F19371040B659506D5E0D7458A8314CA278B4DA66642A554F94A92479C7B6DDDEACD5032325CD4383300DDE5CBCB799D20E0BE0CD07FD26C79571285EE8AB0AD4204346EBC595910FDDDB6FF5044421940311ACC210455271139863EF6333DF80ED5D4236EC92E357BA12F2E37EDFA701FE6383717042DFA9D67BBDAD1F85C1BB65BBED58121F53869EC1C021C582D82CAAC27E3EC5353164606705F4FEDA3E0B24CEA567470B8DE431E8D72C6EF6579AFC6518353B85BF0F1C5F757B9D7E41B9EBD7F85BAB85647F1BEBE233C8B7CFCE120C27D1394597749A42A96489BCB41CAF1277C5D14A4F8EA95E85F33D5C42A5F3D6E98F8A5F50588BF12F3360D161AE9800644BBDE3BB90AF6292ED5756E81A6ED629DACD8A25CDD891E03F328B8BA005967CCBF1D37ABAEE82A8F67218037AC9465D2B73B40C5692F306F295930B204A6B8686F3D54A34C1E609C73EBE7F8FFC381AC95C214FF15ABE3E098AE5256EF251E7E4CC075AD829956363697A0786D93C224AFD165D79E024D2A328A92F9A5301703A37814BD82CE6999571C44B8143BD1807DC4F18BD9C93C1B17B69C5C2FF753A9B6561993CA2DC36BE5E0CE189F262D6CF774DE486993414AAB4A0186FFF4F85EB27F2CAE1F208867F8B34633A0CFD4FC5D8B1285D85F7B062AABAC681472F186691A5A380DE2F9D568F8D6A59E32E2C498BA5E44D0F2D4C9E373D0F34FF42DF7D96EB3BEDDA874A7C7EEFE31FD1DCC18888B4EE114EC60EDDDE524F5BC5A2AD81462677936A45FD0DFEF1ABA5B0BA1BD9F4D12306C53B67277B948006A508A3C02BE4935B6F74299006FA64765908B33480C118DF5B109337540CBFC1ED2367CCA597DAC8E61F2C84F364580BF43880C436F0FABDD5DD5781BAAF7E12906ABF2037EBAC360885921FF9521C0B23868CFAFC13AC02186B82D0AC96DE47F218A35560FB81D12C301CE5F73FCBF580A5A13FC83D61FEA8FA6DC9E6F7D7EDE6B63501321E62C8F639F17C76BDA0857A81BD666F2106421C587D57B5A468BC7663BF447F1D5E0EE217DF13D686F0F8CF0BBE64E070E764C0630DEB7816B08BA18544E056D9B1EFE542FE73D97B8CAEAC021FED5BE705E394FCCF78E44A0F15C4A7A30CAF1803AD413B56E0A1B463F3E061FBE59A6E894E64EB1BF8F8EA8A80C17604EB8A9F873CB14742A9FC322CDE972FE2ADA28C8C0D004FD7510D73C3234FECB6211CF37D3242F1124ACD3973A9FE38FFA91FF163C79A17623379A7C27CBF763E46B7274E4BD191739B2E65AE677CEE0225C3928D8233C8529D344DFB2114FD29BA03551E637289B043C257712D7193B5110674877DE982AC8A86A30D49B4287FDF970EDB78420BB07CA9322256869E009A772B0CFACDE0B929B78B41B58CD2F070E7432F62C75A25013339C6B96ADD438612724617CE9A3427CD6C5D9933C846B5DFC268DCBA6F6CBB2AACE893A5EF5690ED9B204C6A0B3B0B7E795A2E9A11D0F9D30FA34D28E55A63AC9FC68759B67005317B8140929993B0141C8B75DBB73B51A436D3C744F3AC243DCBCC0985ABB37452F0BA32D7C2567738BC4E64AAB9AA9455FEC0420B23FFC477239E7FB23D0ECEC0914B4E52860FEE57A8740DE5E4FFAB38E268AF180A86F99C66DF8AFE011F014DBD50B810C43BB634C37AA69A837D70E90DE0238F7DD56BB5EA80EF1C690FA5FF6569CAAEB0420954DCDAD351E2994AA547F20D24DC5F0966262348CDF81BF91D1189F01CF8BBCC5C1FDD9FB060B9435FF745DF7DDF8B50D0D0BD97DAA564115FAC8472D526E5584C89BD8A05C1DEA12129DB9470236D15FFB83090DF485D142074059DC310A4930F13FB2FDE5AFEA3D9E73D86783BA4628B13887A6E233DECB2A57FA193DEF11DA1D892CAA7374CC65BFE2DAC7BC9E70477F7ED6834D138F62787640508CE82B704BDB60A1F85C4BEB8E76114C2F5266E0BA76F30672574BD9907CB6B6F026318B9266080E0526BCC250B37213EC0761A51E3A77FFFF6BDCD4614C92E9F517805DAB07BF4BF9D6D8C1A55E6C7CBF785CDC7B3B3B86D3ECE1934DBBCAB42866B8B1A1E268FF46D329E32001852E6E6DD4ABBCC95BD603BF3E52FB09FE3CC44E7C8EECA6EF42D0D7EA520F1C29B796F64432CBBC70F456984E8446D3EAB6FF9AED3625B6678AF8637E3EBC61BCD0E028DEEC4C9F8862DE3B64B10D83718DEA58CBCF0D313FCA9A55DA07947D08428273FF1E68C82DFCDDA81CDF483C9DBED1AE721A96EDEA2773A3E69CEA9460245AA3BF115F70103BDB89A460F80871352A9B96F4E2D1B32C83E85AAC30D0F650ED385B1B14382D6DB6225DCA0BE5532214DD6079012354F90F89788D67284B847395B06CCF1DEBF80E6350BDCEB8858F8DD4ACD7850D2E5252C25F3BC17039D33B2D595450754B28E45F3B44FEEFE613834A60F5683AA7049F2972BA56EDAEEA3ED1D97C3C4E500EA08C6CE858E4AFCCE7070D5A991F1843E23D3C88202906553064CD8668DAAC333C40F3EA16CA7C660A39484BC1A154ABD41FC2BA6A03AED79F21E03452897281B9FD86A93DE5D01174D1561EB71AE3028344CC3CE87F06A70CADA55408616DF006990DA1AAE54B7CE61A8428493E6330AEA602358F0F58C80E15A4AA2D8A8C7AC57B5E9465AE36AC9F444C4EE7B9BB809A48E57C159031C61832072C5B70AA7EE86AB981B40555DDF2CC2EF0FD2DC0F5FB78DA9EFDA2396B0043B98DBF630D4C64D90A28F2C6C75A84190778D593BA890C8141C8B0AF3A85723B53A31E6060369ADA451331D26F24125455E6EE50BF52E4EA155AF082DCAF8D3CD9AEB2AE27A8EAB3A29458C5810251CB991076CAB58D862033F3F34DC0EAEE37FA5878D0203B235D8DFEABBAEE1553A069EE06FC660C5B13F5520F41E75A1C6939869E3E2EFF654E6F87AFF3C516B37147E88F76BC8AA2420E92958A3FC42F1D740A78D7BAE89F3066D228EB9E63BC5348B1EFF1D213A3C4ACB7B49315CC57FAA6096290F05650093221C241BFCAF3C7485346144006123175045D9181334EBEE2095C7F001404AFFBC4B26696F6676BF252125B0A60D7D5A342725005BBD4001686F7291E1CC4A9C716C9B7C44223F705F559F5EFA6AE58FCBC6BB582F09D885744C291A302761F21C937A2832E302F3F0CF7CEE46D6D4C2D027DA442F695D04EA28CADCA16984DE97E88015D64F4A6EFD30577F3C962C5911F3B9080FB032511EC04AFA6482C64BCB299AB55777D37784EC131F775DCC207FB6B3E014F4FEDC2765C41908713BC2D54B6CEC0F1FEE71F7C3761212C3011EF0F34F0F8ABA7C5432B251F0717E3F42D098247E5443A39794B066EA3FD6358A84F9C74625BE2EC3FCBA469CA96317F685B1C9386B536365079018C2A4B0028C4B2B6B8ACE82191F3112B72908DB4E4AA6F7CBC6EDC727B0790B10C0D93DA90F7E4D0A1DDF57987BEAF136908B8465CBB23AA0AB43312094F7445F0E574DD2E01C2A8B25C726186B25D057524061E1A87F3AB825F8D34D9F7A0E5C6EC292F208DB9D45ADC49C6D5C6FEF74B64B2F5EC13725091DC08D573CA6907BE67CC62A81B9144845B99069379347ABC18F184A5330384FDD19057094CCFF5EBA62C08900974BA06CF9C441F3D34388C0EB42F32294D91898D7DB9790E03C2E3D21D1C6A2B8D366742C4DDC5A6934DD1DB2D3892A39BE5CD4A5BDC2E015B41C7C527A4B02530420AF25599CE2CD016968A2F278E2D84373F65E59E7D241A6E01260CB714D88D3F9F8BEB5301F1CC27F5388B94FDA924C645177F0846D9239E087027CD35DB707957901606D7761A5D0120892B81A265DF390286AB32C65DEDD82C24817BEB30ECBBE09668D2DBB880CC026F805C08DDC9DCEF8E98056022167A04E0A4CA0C46455BF7BBAF6B2C1F33AD2B244C8A117DADE33AA782DC9621DB7B5E942489FA1ABC7B6CCC0DD77233FBF33BCC749C9508F58CA669A89D382567A340CF2121E865A43AD64C137B704E95B7ACA0A0C648D477573CCBCC533CD53BD17ACB1F13E98B02D2DC55D96C3043134E89CB9838E16D4292B0981BC51A684C3FA61B0FCF419F343405CE1B587D1DD789EB093D98C542B69FE2387C5665BD7D039E563B52AF673E06D112EA0FC5E2F5D8C967667CEBEB182A17A46D2CD3DC78F49A2E897DFF9BC7BFDA665DD93138F5664FA83B190068E80AD3419DFEF99C23BC1302C48838F7F429FC4DB62D91F340D17F4E8F7E4CF9667D3FFAF97D5745270C7109DFB4308037E65ADD49AE53BF444A215D67A9F6E0AD18CC5BBDB665B441A49046F83ADCCE81E909C18054CB204B5C15CFF6D354615BB437E444E35FE493EC69118B5D0E57DD8A50F8E4C17547B21199689EBA7B4A96CEC767816777C03D5CFD0D4F835CF747CFCE278AAA9B0488427DF95C76E865C95A9595E0B67C4FD99B75FD3E80C4E6302902051CB8250CB660C3817B38078038F87A4926B62E7841A27DF0B99A4D8D529B6661BE52DEBFF7E3CFDB7014EE71421D3FAD8C5B60FDC7731B12AC547B5B1E37D50C41962E786B4B60096106029582E317C4D2F098CC94F4D96948E4FDD6E101E69EF9A86FFCE1B1116FC9AB32745C8A310DDB096250A1B7B98E8B5E4893BD37D83859F3DEE757FD8789340390D2487EBC73BE170DAD833F3A6239361ACCC0FBD8740C74EC58C3441E17CBB6F028818DABED3DE39F56D1857F1E25D57BB7264A6E4268AC4311E4958B9EB69E9844EC915E74FF03F25073A6B900A1FDD04E75CAB3810CFC630A9802287C3807FD6E9B625025F66B0D3015E1135A47D5F2F36ABEA1D9B046052DBCC1BE55FAC3CF007B125483D5514F7893358410903B5D4E7EBBD2169011D9ACE3B57F29493B5C9BD0FDEE2CE24FFA8C0A454CCE34DF3256E587D6D662FEC533BBAAE8BA2633CB83F1B7FE7B358AA3B7571FAFF17E97A61EB4580A801E5B3255867A7DAFA47F778F313C0CA896FA0D581C02CDC252FD6E2BE80CAF99BDA54D50645B50674764B39D90CC4964BFBC6A6058435694FB862354A624656650AA3029E6DAD9916DBBB1F9C5EBED2F5CE0148B23529F3263D58EA03BA8705A9CB9E83580A8EF18915AD78E7FB9860FE7DA42522FD3F4C75B0D51F99BEA2B0794799D0C64CB877A2B7A13183E8752F2CB2F8E8B38F0B735C6053CFC5E67BDFE1581FDF2CA728FE0C7084A832E3132C48D3A6FCD36D932B77BDFB7A1CA4830B8B4BD15CBCF8E903BFB8419AE607AA4F130E1F111763554E228A427E53833F928E55F2449DC6DE5D2FE9480E77EE1067FECA7F89443377E531C7E56FC55E1428031A92E1D9294023F57BA0F2DA20F76C693C75D3BC0C0FA75D95F45C097DCE9AD38179B0DBFFC004B64C73A11DB86FECB8DAAA1AEBF241EA40FE698175C82793992EA7D6DB6CDA9A8C7E7E4F711495B26B492F7E78A4C901E9C647051CFB3C07946A50ABDC1937ADF872BF30F2756DBD10A027AFF6034DC2DEE2DB97364DBF2578D030A247452D60608A578777666A86BD4997EBF4CB05D2AF3205E1F0D18FA31BB342235EDBE55C73F423F1350E6091D01F6AD53DB8A0DFAC2EA46A3612E05F885E12A86C65BE4369DB261315C46E9856E81B0443F15FF9942EEE31B0FA3390A259C785CD8448A27C1DD2BED810FF1D2A9630196F6BAB7E50228D3A1D94A3D0A124CB3D832EA946CBB432161E34E87E5B595BD5307C16D54BFAB5D441D2F43FD81FD9C1CBC67282BD9A58321AB40460CA7CA21D3AA851910F434425BCDA36B37F0271E43BE962F2D783643162B16E9252ECA90D86F33BEF70132C7221895FDD777079DFDBD2151C17BD4F4AB47D1DC006F21E9753374C541205C097E5716F36E6C2DED63AE753999E355A0C07DE4DAF5699244CA84658CE80B63E746CDA7AAC8E6E669A1197AD7F56D22D187CF6926EB422438223AF12F7AF3C7AEE5878B63DD2E7207F3E35B8C56E60DC3900F005C9C75F518D0DB46CEC4B83E4A8AF5A3E9F95CC5FE0C00DA78A4610A50211F186164B0C0C26ABD480F7387231DC8C79084FD3BB74A7B522C009B1331AEE4609F8549D1AD847471ED78D32A8F5B7EC39FFC96CCB2F296A2C3673A3CCEF52B3269E786BB11AF738CFD5FD4E31DA0D4874CEE081DA71B038DD02C5F466857142FF80EF80CC4A97E1690684F5AB74D1CE5221E046AA793B80BB71A995B024DB4D2F8C6A8055F8ADB710B111CD57EE2B4C7FA44A2CD2CDB98D8580DFDE330D3982F9EC077EC69D4E5036DE0DD98520D2323D081BD9001B30B029A16B8496618B947D6A84FDE31C2F980513B12BCBC87AB7CE62C9F3A6C8D6FD4AD13B9929951D2C8C1EB4465B1584F22B0EED08F7A70F003B1618BD50A05A68C69FFAEC19540BE0BCE8D63AE69B271083944924BAD663C6C1729F88928685B836534643142058D0213CA205C41895F5D065EBB07919A7EE395788EC1425A9B1E3A55D498673F81F4B57FBF81ACADBE6EE33011F027C952EACDDE89BE9F9F7E560C622CB5494CEED9748BC064F0B2AE48B1801634695FE01F827145E72D2C2E0C4C16732F4289B4AB131242CC5A8ED0327751DA2C44EF1E0B39B913B33FB993BE66E5B7B2C8A9ED0109F74184EAC4BDFDA215E125A682453C41ADA5AA01DA0EEA27C4B62D87D1C7F19208D75B5B0372DFC09A0DAA582C89A5FDEB9632570FEDD23ACFEC6556FD8A798B75453CF6BD81AD9A140CD23AF37D735FAB45730790DD0DFFFE6AB05E6DD52A9485D66CF862045C9CE8C12EDCB64D1DE4B1B581021517A8BC454C98F0E7E63E591ED1D9BDCE05100D2B84A0BF1B69217847AFFD1FDCFB1DEB7D7017BB1D97C28A149A365B184571D3F8BBA9E604DD5A46A72CC1A5E7595206885E4E2C12556D77FB2C1EB06F09E2222EB4A39CB8F0C0255CF608FF4CFC0168E6ECC02E85DF1C0F5AFBE3C85265842F4D3D5F689E2CB88802B0205122EDDF55CBAB428B5FDACC5B3D5134FD63477DE8DB65498482D73A525878C73B2BBA98F5E4CA30F172596C12149E8DA44B774B6B9C38BE7DC3349CC9914C3ED3562F28E35C5A17D86372641E71E47FA7CC03816A0187FBE108BFD06D41A7885827FD1D6571A36C48C630F1132A97FC4F48682932F755B22ABFA7C751551206A67A7398D9AA3A99E520830AE6D2898DCF5CB8F34740143C06D83181AEF30747A7733C6146579F38DE4DAFCA864705EC95BAE7B35451096BDD1F32C49877BB279EF8C7E57E7326BA9B5AD8921D8B9EA63175909ED6A9026ED1D3ED3FFED72FCEF02C94A70EB90DBC15E5EF3C76CFF85F49D8DAFF57AB249BA1EF890AA0A02D8A2727A1F3963CACC210CC8243F2A57FC2568177DA0B1DA10F668E006D68B7B695AD36A8361B28B424071933464B2FF00E89F6B89719BE7C70242C6977BE2AF453888E3F51B83234921B3A66A5BC856856FF65FEAE2C2372FD29DC40FFF67463598D0D55B0FC20DC58E3CBD8C4A4F3E1E90BCBF6BBD95A7ECEBB521E81A26DDAEDABB1FA9CFA775230C727C0CF351032BB298F1ED4E59AFF93793BF39D5A166E2CA574F84ADAD14504E3C8923BA075C63700EBDE2C335BC62D780D27F19F632E1083CBFE0630D2215DFBA6F16DE120465C96E277DE85C2EE02925DAC0C8866C58A78338A7EA5235B3FEC5ED3BB6D64C563978149177569F46CB48F066506E8D7ACBC41E05454CE535979AE68F8BEAC2130D6B51A1423AED38F46E13496FA6EBCB9C08FB2F68D41C99755303A407584E64F1B1CDE05955296C31A83C104CC935255F7396D87380A72C43DA5953E517348983D4E29DA2ADD580F0480416ABEAB977D24F40417FAE943CE9A65E6EF9AC74A9C379AF459E9B3F155822ABBFAC397C6D62CC9BE3908DD4DA4CD0D84F3782BB7F157195360B6B9528B05EEBAE153D81C32AF2D3E00E71A116BFDCEC640DB9CE8E799DE7FB31AB37205C31175B7758C2D88A508B7CED536895AF30DEABD217EE7B966111D3C3988025518A3A21B1AF2C6DA9403AA33008D3E9C6612F0F327CD5BCE3D32F10A21A7DCAB8CEA44B3C97772A78396DBBEFEEAC0DFB6CE685158322C55891B07EF994710E0B7D6EB48A91176EDD63205F9194B78080BAF5867C06291D0161171831715D46DCDB934221A82E5449BBC0B9773D2997A41C97802DBF05A9BDD87FE17128758E0F2AFB092A82C7B6B46547769FF72EEC76463228268D6C9C567418B5CC896D3BF49052F6F148C03823E7ED37C2075084C22EF149B84E1685C3D60E4E5367EE67B0FC5386A589856544097D0759B7DA7EEDA0735D5B59AD77AB74223C7F3CF023BC9D9CB9003AF29A049C7EF715FEAC8889144B5DCB39B812356BB771C52E5F6EE6A71A3E645CE24869689849910C460BA906859261B6FFA331BC68FECE0A0982A820C51363F920B7D6EA2C5643167C81E09DCCF6A5C2B99D84A226DC22F8D20D6867DA2DAC7BBABC7157436D1F1D2F1C202A7A5CF78BE6EDCDDEF9E774A48E84D1BD3F15540433E66EE9DF083A7210A36C5C743383B18D8FC511A6BE5F03C1F37D85E01E1EACDBB906A63C703FC1F9B6415F8EE63114CBE2505F9D9C81F3C86ECA43B9B5FF138DDDF9964D2FA5FFEBBA78CB5AD549AB07827C117C5C7C9FAE1DEF7F324A1207407B261F145F1863575CC49FD2AA4EA5B90F58F1FE7079FCABE650D109F415E074308DFD769A3F5E969BB2D5030104660C2E6F6BDCA68655A2B287969414C1CE81280856371DD61D16D255BAFD26619A587EE58CACDE9E1AF65D52DFC18141C635C420075942587931B6C63432C71289FEBD8E8B8FE084FDF4EFE51A559C312908E13F9A0112C4081026E5D18D5DC771F48ACFADFF5DF7D84DD38FE31882CDBFBEE949C0A86E75D41F152CC4E1E1CA6804332AAC30F2A9B718A8D82AE40B430D14B8E672A61B815C8C9904DB1AECF358EA9FB0F1E7CBB0BE592D96CFEEA2AFFECDD6B5C1CA3D8E0C11F065DF9BE87FAAD5A8F2779B3E7395A1ADA0B6E0376C3130B6681AC19543212FE6BB325F60F14ADE5E219D5458EBFCF2E0057F178CA9431C24C4422308088296D11C6C01C056AF282C28B01F25BE38834222A420A1D8F751F124001F368CC400B82CA141FF9594B7A256CB85E71344ADF88085EADCF66C8C2730E892E95CDDBC4E2F3A5EDD8709F70CE5FA1ACC771350CEBEBE7B065CAADC3CB10F332C16B6F8B99120B8951552EDA9E7BE102F76F1B8C352A5C0E3BB02265C29374EDC4FA06113D91ED610D0A971B1D402D3DAB313E582AB29A5905CEBA270A9FBE0A96306C67623213BC5527812383910379F6307745B900141646C65EF61D4EC8DFEA4D469DAA496B60CE170269F235E3EB4C668FD77761F51E71C8310FA6B75C416788440B8D3D511BDA875718A0C6092C5A0B70C2E3D6E2A62BC253476164E3056D120DDD52BCE2048F12201842100CBAF115FF70CD3F0E4C38FA64B2E8FF4295719D35344B34A27F9B6716AF90EFC03E4DF9DAD939F1627ED10BC54C8BBCAC7ADCB9CC303EE00384EEEF5C44B95F51461EAAC59D7DD2655E51C16EE28DD69FE41872421649F177CCFC7E2D03600A9A4DBB56506EF05FCFC6DF2411F61851BA7CDEACC6656B0E131BE87D7787003DAAEBEB2A9D3ED3C8ED07F88EDBA9330F8425A85C88A5AE4AE201770A658670807DD32410518F6C628CBB0FB4AF47F533317C104613850A7E7BE6C7811C586DCF5D4284CC47E9BA0C7F9EE136189865369CF200DE7E58DE2F71DB6210381E3D5B774D94E73AEAD331A27FB5A659BF589E738CEDD39EC0990BA4084AFDB13E780F8A5F06CB055B987FBD7622BCC53F43C4947CF42DC20EB93B955161CAE2C95C3C0AD2209ABC8F20748B57E88460E74C78B3322FAAB02CE7B71E461F2926B3A3D1A41464A9969922A0D3A58D3B2480D4214BE1CE49ADF1C9A3D1506F9B786559147C3D1C86754A2004F283C2BA3E4B0CCEF22A7084E960D77CFCD9C855A34AE176675AA7FDFAFEF649412AD915F2AF152CB01029E0CE94FEE496B13C81DCB39E37C262FD1E8121307F71E0544F01431AFD3BA2CCF3CF3A97F10A036BFF5DDCEB167D9AFD02C8C072410829BFFD8426C9393A63F828A4DDA01FA0EB85ECC13A14A080834ECC38637592AA4236BA542BE5BE475303B2199C22BF0312301D98637136E820FF7770AEA1C6CB5D1308C36B519FBA00C07E8E669BE33AF76B1964CEEA3EC85206070B5602FAA97936107394D3BF7E05560F1ABF689A14B78103D3B6A88A3E433390472B1391FF34593B1F42E36E893D533BC5A383202519CC2F7A4063085136B8F7BE22D858DF32BD20956526D0D86AEE6A669F4DF1BA3E684DB64B52DECEDE5D2AAD041183DB9AF1BFA2EA19C5E13DD0917D0A985DFB1C761A6B746CACF5B8E21EA68A6FD0AF0E26A2C1E94D56400A77C1C7FC38D0517F7B37BCEAAB03B2512A4AEF3A84E829F6F42F90E6DF7AA14B81A7562F441F72F77F78AD8C5FB51D6C736E20E94895181D6413B9AC28CBA8D0F0BF7C7316F60F8BCA87E3B09797A9AEAD3624AFF96EAAE029791C21700FCD5CAF2D3690E94F6ECFDD7FB6BC5ED4163380D44503C8FA1026BFAA437D9E33918D52DAE7220C090C7C9527CB8871C596A22AE8D8A2139B2263F240E2DCECDA2723DC8B6C265699A5BD11660C009FC8932D084D8C040D6D98F4F457E5F19199596551A9F2F2E1BDC4DA4C6DEDB9A180E153D4EE0CC5D864AE2D2749F35E9BB962015080A035462C722B4A38721340B2FE916A8197A939CD6C0290ED5A703BD02953205DEE5C82ACE301E1A4C4BFAAEBD018EC45EF7D8F90640E6721AEB9993336DE787B3D273E1E7180BB7AB60DCC22F268A8F73741CE3EDAA026B2725D052B885EAFE8E1A5FF8A56936FFE3EC311CE78F9738372D0999916C75C0A03F00161356A447FBA2E07EC3570A2415F4743C3DE61B6F020E2230A401FE432BF82144632F6C4046EA8211E0C4FF91FA0B8ED7EC93CF0452C67EBEC4651F6F8E541EB7EE82E1D420CF577D1AB4C5381ED28BA03A60D4C1CB826B59F9FBDC94E868FA640B4039F67F01BA7BC6218F54A5AF5076548BA8290AFA25FB260A9AE4F5FB6906AF5D7E153A894308CD41A5855E0FCC268C28F64020137B84F3AB54A471320E88A8844DE352AE928D1CFDB413C8ECA12E69D901D851EFC929BA509137389223FB31DA496DA86593C7EB7CCAB17BF0CF52E463BADDDB32FD594278A6D353821A58D82E869F863A8B70DCD6D04A2BB3B6A885A33CACA7B5418833E07C232C74CEC72C230A8A3850453B82D2DABD0190EC8044051F20A532CADDA33394881534DA860567302159091068D85487BBA7816CD43118D567447BE3D51C72BE97F5EAF9D1EF9B6B5B61D03B2EC0167C74EE672B73A3CBB173F118133A849761946FF24792C425F11015094C980453FD1071D33059B536A46A8191FEFA8F66A54E0A77C94E939B531BE22BCB10B28F64C261E3402E2F596ED5F5AC17FE53C9AF4DA3F29A8F1F85C20E45C5BAC26A53202CF0A04EB6327B45E12F83FA420E884338AC3EB4361A42B4DECCF34A5292E2060EC7B5AA61007F2BB53B5684B41C4CB98185C37B53CBCB2CAE5BFF5FC7791B3F5C285883AD6125EDF79D810DC7C5299B4462CEA1AE9E827FB37A22A1304A1B0FFDD9A73CBAC941D8EB282C3E0E476C916D8DB4B808B5D983123597DA1D9688531B3DD0A3F665CDFAEFB2C4FEDD9EBACD592B87574594E21BCCB8FF3E93914A3B402FB05519D02F4CF5A85AC51FB08C9CC314C5E8942285279288B986B3BE91D363218C0DAA08180549B6C84133C8F9CA2E7EE7E77BE911E1B3EAF3521DA6EFC6B3FB4E2C9D0D5E4476D49876BF7EB2A55580DA8A249527719747F214600B5E7EC14DF69032834F81C092C8C7550C1B0CB8141A8E525A1514B469E206EFEE0DE38F8CE1D67A660F42F892A910AF813390C12023F24898D876F00D44D073F5A9FB1F6398F3201C508BAEB7CE2201F6FBAA9E5D37249E2842C074CB60EC2DED06762937A40C4DB437E9590D8B11801C218B614D2BAB48659FFE38023E15A236E09502BA144BAFA36D6ED387491CF3BB934F9B422317C12A009A89001C99DDEFF50BDFF17C5D5B9A985C013F0F6A4EA0CAEBDC5C0CB94395A8FA323D96265EB948D5D331A00F3AF87A588494405E609C95D70095F41AD631566479073771CCD6F151F842212F2CEB1BE9A67FE35BBFD1CC59A0D8073A62B7F8B2C08FE1AF23F22225BEFA07BC6B01E9178BF4D7BDF0EF9C7E1968D4DC34ED14840DF80BAFE98067132748DD76C95E12D6D48E61C8F7F0E9D281091CFC5105DFA4BC7B616C2BF2C17E5FC7F322CE1F3EFDA4C81692120FAB5177483999443542EA09A81BA73FD4A4877CD396A477F2D9F67D05482F20E6134EEC6BD9CAABBEB8A42275CD6FB975F3C3CBA94CA178A3306FB6D0009439DA4E9BDA41C0E5F41AD6887BF5AE337759D42488B876BD72A7D71F8AFABBE4B5C7A1A90B9F7ED9EB9253997FC9857CE4A683C06E09E66CBA6B46E3722F2A4EFC67BF09327552888B128FC35CDF55C61988F6ED4AEFF7364CDB491B0A69404E26E82010EC890EDAF3E625840A8FCE794E379F50D4BC0F6CF76F85260245310E88851843C5DDE8B6320CA824DA1C9BE6FEE3970E136AC06A6954546C8141032B8EF6F097D21AEBBB4AD86C879B5F60D66CDA062449A2BC99ACF4063753AA4FFAB30487706BCFC77BFF89F674A481C42EFEF79A1AF52B3AEF5067CEE25A092261108A4474B5ADD11056345714178CD5730692C8D772C4C6761D61EFCFC8DE26EE761EEBF44D8C6F934B6F4E807139C215E351DFEBAB118E2630D997C0D8B82ED1FFFBB4B8B01B59EDE322F6981BBB69C1019F88E4CF45F442C2EB6210460CAD38430146A011F29DA8FB444CC2D44386042B5750E2012764DA5FD6772FA1D44D1AE773F72B6C4FEB465105AE9B2E9E6552AAACE27105B66A9B01B19E11EC084C0821836764B08AC574A5999131FA4947726E3FEC6DE16313EAC1992905B9ECB1A4A1A1E93D46BCF949ED7BE6C328886018F4A3FDF89C294EB3C160D188BE48899577FA97E138E0F02A187F673D509950D21079C299E552A27A54C9F830FFA8B7E8DF2DBF173EC28DCC60883A6BA9CF6B32E82F6B5D042B72C1937287E09DCFDF363A6017791ED8439F5D4871907F6198284EBFFDC720A433B2CB7B4EEE85522DB77088E53ECB3F200BFDAB5DD5AF1044FE4E87A381D3FD9FFEFFDD522904499F65549EE9FD30FFFC06A68C71221C2F7C9326BD9D2DC7ACF2A16A6EA3F3C10FBB49267575034CD538033FA561FB466885F62F8F2AAE55FA0CD95D62669BD79DCA303517FD9799D20A2EDF31B3EA42B45E6436E1EB76DB5E9BC0B059BBBB006C4CC518681BFE4B8A243FFAED2123626AF09F8DA21C95EC6503F3ED940A38FC268FB121A46C672C857FA044D668C1EF94DB399022D7F26AB85EBD0FF17C5A648AA08BAEF9A35421F580E79E1550AAA5A6B73B0A5CC495CB44EAC640A698ED38D4FD334AC40831C74D502DCD99ABE0BDF60C8205E8B8E53AE2C439D83B96FFCB71D07EFA922AC4BEDEE075DC20E207F76F9C90DD71402F54AA70BF3BC9B1EE65257E0BED0E35D2C5F22EC40EA8AB5F98033AB4CD523642F30E664C0DC736A3FC1EE90E687625F22898FAE15CC76F8EC6FE440872D13E1E3E1EDAE61637E19F42287D6BAE0AB2BCF27192D2DB8988980B3CD104B7677CE57E865C019DCC1C06EB7AA84434A7A6AD2B17F6C631FC604E479D82A6799F9EAED803F83851A09E5615CDCB16B75D47487A7DF68AB01B4F0C7720FF711F2CCB4C5C4DD892CF2E68980D32C50FF41586D349DFFEB535D294A9571C88B874FBD954103212DD65CA8F046279227404A9097EBF5A0145AAE937D4B763D22037D1D67BE1A9D34F3C07521D41A3D116435887A6A9CF33F2816028063D6CBABE6CE1C65B3C492E5DC4EBC4EB73662F5CA1C6F060B23AFAF69231722EC93ECDEDC777155C55C1EF3C76E8970E5C564B1C65EB890E57388673DC84980C05F000280D87DFB1DE98A3560DF8B4D22BA6835BD4AE8ED6EE62D6CFCA6A1AD599299E3141AB47807A8B0E7B50C0C40907B5EA81862C893CBA8CD3637833897561ED09467D2A4893AAD3F08CB5EF2E125170E797B932D4ED613231ADAE52124FD71224ACBC7F26DA512B4C14E5A3CDE71C811B7EE65D2926ABF5A4F1CE05D75A88DE76141155D08B69C7C03598F7E3ACABE1B9CF8DADF0D2B42665CE2A0A7E3D1819B8339846AFA87097A937C5D584FD47C7B2AC29FBF7CC20447D5AFB264819446725763F988C4359E2B2BD78AF2DE7D2EE638C0D5F7FFFE1C86A4C8C15E2F484259A884A00D9C7BF44235CE60F7BBAF1D98DFAEF5FC0F7F378C7A33AF1108677CB182A62892DDAC024B29344B5DF600193C9AF9A3CADAF30B26A7D22F52D32AAFDC45033FF61B933DBCF6A8BAE7A793D9753FC6A90CB4F1B126083DC111E31FA937362E4B9411D333977E5E1125CF89EFDB115033A77B2A6E4F46D5645572F8835A2D49EB4CADEDFC0479BA1ACC5F55BF71C6D4125FE7A286CC291CC2CB981782BE097AAC4E32CB9557B340D35B8D1D284750D47AF7E53C2B4D2D21A03CE948F8010B1AB04041017EFBD7DCA9973C29D324B98499EE6BC80D0C0C1AFB8A8D5C2E3CB6DA3C9002705F35645C59B9F610173E10014EC423E8059301234A1E65EA9561BA0D03F2EE40B7396987FC4AD28BA3EBEA9D7FBDCF2EF8B3F77BCC435495D223C6EA573773EE84B7C4007A84290E54B399CF163F63064B42F0CFE10CA50E2C20A9F6CC94214346B45D500EE3300CDC447A8CDEA6B99D54A5DA0FEA0C1EC7F76EDD4F46E974B8C65AB7F6F58FF8307212C202B0E6B6FD64C751F9D2193CF247C6CBFD408443BF6B5A2126A4EA8AF3908C9BE587D586DBBCBDD099ACA3E4607C72C467A252ACE32A24C2BB9712F45198498A548A99064E7BE8723B81A319DE88901DBBFDD557C516A0A8FD61EDBD92C71BFFEDE775844DE691F4B49AFB10D6658A3C2D0524E7CB46448AF012F647DEB531538934BFBB11BC474A18DF8CEE588488077DA86A0FB37DA05F2BA491506B38651B6D6614EF6A4FB9132922CBF1D9985AE2EC34970BEFDC8884C659427811323BBE3DAB3A46BEEC502D30B6BAFFB21D6DD9C5B0D199E23E2DA19A5AA2FCBB052AB9324E9C4EE1EBC38FDE6B036A51350AB6174754943154001D2A4C98AEB16380A6083BD5F528F881C3670FFAED7561AD8920CC41DED436950205E2D9F977E9C03F7D5F1857E0C2F4275B9429B417CAD7C3DACE8AE4FFB25991D6C0EBF9C560B62AFA7B685E87D6481CDADD1269D4B4992E71B0AC108EAA7A1E3F44E593EDE2F5277F0610510F05CE3EF072BD091E5DC3EA4B05B2DB03B204DA2A4A03E0BCEC2CEC662E799CD8F2F340E7E6F47C94E79936AA3C037960C76781F9A019279E43B7F6A8035CBB339C57E131E32DF9D0A4DCF4FCBAB0461CC007CAAF0D3A3C2A7C85D2FCD206DAEE8E700A38E7C5CD53D33C492788A9A41A2C65DA87FC8144F67804FDABA025E0731CF9224CC82B176822580EBF5A48709C7E6F67D868459F379FF0793CA845FD13E489F67A1DE4D191C6269742E416A417388E34ABE2E4DB3F800A7E97EDDE951A90794F67C28F0D395B31D5021809EF3C8AE28D699BF2BAB8B2B763477CA1E26F093F135C065B2A5DD0C05A73E252FFB2F1554BBE4C0AAFBD76FE0174CE61B3DFBD149570560FF227E21A10689F2B299A4FA62DD44BD25DDDB7831A0F2B4AD9893C5385926E8968CAA497DF8A19D424E58C093721D3CA112C16D68C660D93F6F90273605406F3D44C54E330F1ABFF2D0C27D9876A8D72712545DF817E2902D219A8BD1B1481E9097F35D36A418B117A915D8D8C5A6E47E2E1704DDDD1954B5037DC07EC179BFAB6F42DA34EE8EDFF4CC31D6C5B789CF79BD0C2FF9743937978E93EC96B478CA7433E92EAAA096231243A75ABB24BDBF84B908F5BAF76A8EA72761FFADD53B72A8B91F8D5AE4FD2A825B54F3F5AB4D3C64AF3CF72388E52B7F4A561D65274F243C1B63564EDFBED5A2B2B30FCA21E0B6077F27BA66B43384BE1984C1FCDAD313D42D162E64004D7F5A1DB6E206C48266DBFF89F33EDFC80A9E1B9704EB12A8EE50408EB2AD03F332F1D4E382BD0E69E47E4DCA851A6A48D03CB2BA686E74F14618DB6F43CD31A2B69D9BC4CAD8F882F1953DF1B9E96429DC3B658B5A0014DA02E76B42E0E8EE9794F115811A367B64A3F6B4E4E1CEDDC507561FC08A1B972D7DAD66054B7C22A0EA475666A081AA5C4C9DDE5747E09BC8EE05C851FBFD9E6B4F13197E230E8A05E487BBEE1D6848153309C2ED676B517EE2A6CB20935465DBFAC2676235AE45B943D8548B735038DE7364AC6B267DB57ABF263FBA7DE1916C97C35476C627BB5BB5BE3B1DF3BCE8EAF0FA0DA0C09B288E87D1CAAB17DF836310A1E05C65095AE59129700953B6592C1574C3F2D9C08ABA06EC403EEAF19DB37D5CA964D58B0BC494A602CFB233444C0A1DD035C9415E7230A6D4B84462CE71F96AE23BEB68DE642AC4C4D0F207AD4769D329B45B1ECFEED315E7C214EB4EEEA19AE67CF0F5D3C3F759F620376C4EDC0808BB2F990DAF6622788AEE159A0239424D30DD40DDAC915030EC17AE6A7E1AF2ECDF65855F2821100DB7F2D0EFCCA3C4E04CC8A9EB307A9A6BFE2CFA6E694ECE591540EBD09854BBF5DEBEA55D61B490E9CA59FDF93265598488501299EF7013737E022A882C4FE956D3D79F46E44A5B95353F9EF35DA942965501F28ECA0492ED6346B954C96B3AD44E88ADE7B5DF2AF63CB940B70431B4BD86D010DDEE3FF3C49EEAE500572F5A5187ED6A4DDF1D238B633974453132640A4DDF8B490B6EA351050C2B6D8FE817885A484926A66083AFF6AA817517C48705E2F9163150E7483CFED09C7A91CE7C6C95B5C4BC24AB55B0F9F076095681D9E15A8A1A3E01BC5199C2445F32DF7D58C17FC47997CB4BE6FE15716B85FCD813A067374578E90290A1B189D3390A87FF3A9B7085D02FB0B7E6E54ABEE99D5B738F1C57737C8B1BCCB3CE8F54DA050807EEFE97EE3B83279794B736F65B24706049E439972746068479EA70D97BB6E0027C562F1357123DD371F12C86469171616455B0F0964511E9A87AA2CF0ACF3165521E796B8BBA35AF7DE89204E875B1AC099297B82B0844F5ACD0EF55805E0022D6578C12480B458ED90FCB07841AB2AD42F6DE9A6A97D992ED4BC8D3390A47C6E3F42A77ED2B50096EE8E79157714071A33B381A1A7FF669E397DBFA77A159300436100782E18F9A310F03B608AFA442942D5B9E7E4144030466D2E11B34AC0FFC78D2B04339CEF2E1086D1C3915A087F5B4EF75E7456F20FF9D42DEF1D76F2E39ABD0534E22CAAF98C86E0F639DBCA1465C85534C57CAF3D2E0F4E7AD26B93C2E2F1979848D6786869458E6E75BF72AF6BFC6D9EBFB35B9FBA345CDE2023024446574A6F618FA32894A823CDF0B3327FC828BCD40E4A33878141E87567BB78C690FAA889789F3818A9FDDB0C506091B4B72A83E2E00D723F86BC4AA77D447B6F411DC5E279A0D05DD569DC315C1532F1748850DABD543CDE668B168EA44642FD2103F8A63E447AAD782A97C09924A8146B319B13CEEFB10631F616CF454B6621DEE59FFFF233E886AC2652EB11FC50C44F2FEEA50DD8E5BE8347559B01BCEB6DB397E565DDDFC80093A63A5C235A5D17F3CA1DDAC609A0919FA36555CDA4AD8559B3ED1897DA22DC78928B17362F0AF31E9A8CA1836A5018336FA0A7DF7DF2835031B438DFE645615C05A4029AB2EE202E982B66D4FAB95214FA635E1219CE038F7E6954C47DA1C31E928483B66241123B9901CB05A02EDA3C7B2C21C7103C348E03A8C45F67500755D8FB7B8697FF9FB05F92EE27843FC75BC413AEC0372E804787E3ACF150DC620242C45186B8313E067F02211002720079CF7EE182DA0E1AA5C8D60F6BE31AB8FE1810572919843A777FE622BA981FC734AC2D400B6FCC4496172D276046359DCC801E5DCA5647EFDDB15BB40A6DD23F9FC79DA283F59EAF0EDC63BD8EDAA1A98108EF87C3F99C08F0F6103A55EDB4CEE4255989CEF3A9FD1F1B05F0A42C8C0B58EBBF37AE460E05CDB0FCFA9BC9487DB516B4E208C2481DD8EE1DBF67A7186CCFED5DF6D00C6B68D23C518D662F97B7CA14D3291C942BD54F03CCBDCB8A6109B4050DB2BDB67A8557995E5E7464E49E876208CE7CE40A7EB94080CB6B44C1C0EA0744A2AC0D9E32208976523833269CFB6BE7ED5004120EB2036FA38039E48E51EC155A141BD5C6017261B97F6BDF0CB741A6AB33EE9EE7CC03CC08AC01516078FBA186686AD2EB61049121998F7062687D1D43BCDE2C205B5EBDE684755819EC11AC1AD1BF87E2AB0F2A294B6A8FCC5398C049AB0525331D560B2DFC04CA7D360C8031FB5B6821093172E2C2FCA04921EBC9375B9D474747AAA21367AD12D6189770F07F49A18373003AE8EC470BBB232E61CEEBA91E4CAB6171A8558349FC48AB39D2FDA8B5654735AA637678C6647D43BBDBFAEF742E1D8DA71EBA43AA7512D6A6F00878EF0E1C4BAE91B7A6F50958F0EA26A974D1950A6B327019601EDA38C41808D305F7A57887435DF478B94C23D0EF6B595DDBA3C96DE7EDCA8657CAF89AF8D5D98029AEAE15DC5F1D76DD95679FC6104784907B05C9720D176BDB85DEDD0EDA623E3FAB77728E6D66D82920D099DE3A5E9B2F3608BD940274B7D361A3F0D03576C279E3F65F5F4FBCCF4DBE020780A6B6FBF0122672EDDA7AF2553663AFB9B39CF6573D3547FA80910C0AA9988C7B51DE0CCA2A874F1039DA63B6088DAC83EAB3902474C7A96996F93DD5C685B8745E9C1D7CFA33E0420E8F5E73D328052D9D9EFC6B12059052BCA72B2A40386C43EFAF5403F843B601B4E47521F2FD5FB3C6CAA58294A87032CF80EBC80A1F03BE35D5C2F790183AE46FEA82C94AA9BB49C4A7B12603C552E00D38368E02E93D65883B991AEBBDE91897A0537BE85C106C620980276EF43FEF5D3B5F0C6DCB9784EFE938577C5BA59051ACC854AA9A62B75F0063AE5965A816ACED17727B06E5C810E04A3CEF988E4DD3A4E881A6C472B0E1C2EB21733D08D2FCFEFD2C76451F7659A4C4E32C38E0C4737B0BDCB4351963802DEBBC65A64C4F28C5AD43D32EA3939978FD85066328661BF6A46F2DC058C70B49300E8CB0CA962875B08EB891B86933046154CC5E01917304291EE914D1FE2B3F5B8ED9FE671ADF59974178858E11FF335119616E6C3611ADF260DC355865326209C5507C7F6845C9A433A29935047CD716792B945AB8D3188A22A2AA4F36A66AEEAE030F4234F3238C846DC213D752801C0BF7951B656995D2810E65A0675C33ADD1086BA8F7D080997E15FCA2B602C949A43CD4796B99E4C80369CA4A379454992C4FFC1D0A1B34AEDF04F6F1443B63F946BDE1C241F852D3CA1B5665F32868896842E431633E0166B55DD8D2F02B8CC2328C3E163EA1FAFBD527FB5F824938203BEEAF7A5AE234EA107937580C3564E93BBB0D78B09A877F2ED3A4C6EBC01327086A265ACC468698F9BD0BBFCB924BED0BD7C31BECFEB3372F298BE2BD32BE25F2A8F283AB03B2A8C605F3D091481613802E950F9676508A5DC516CB2F8FE7ED7B0FED312BFCBE31D6BEF32B655B0AF5D8525665B888418471724017193BD62524F85F20D4A8A3AE429C8B55A68FDD4CA9EADFE948FEAD0BA58FDA96C2544594520B2546B672BCF36052A092AC481D8498C20703360A0878EB7D829ECF242638CFA9F925E59B48368E7F5228CC2031BF39C441B0FBE5E67D4212E7E8D76C195072C9B25EBA609658DB0C321A05606A7DD4934F14BD858755B8B603ECFE86F9A103D73586272544E962E3A2E27DF4F0F9AAC92B233C588AF2AFDFD6C5B7639125C6C8DC593A226DC06A2DDF8763E9F1C19CB9E3C3E2087116ADD69C252410DF8F34812A43EA83616E12D8D8C91BAE98D3042B3F00844F19EBA22F05E3D3C0BFCA6AAA5FA3A7877EBD5D3853B5C1C2835D7FCB6981C9B7CD41832CB10F847159F93380F419F7259D172FBEA81AE2CB41EEADAAEDFB0D9C3FAC40724F0E9651184060AA47FDFCE290E7CC9AAC9F2ECBCEC74A4EAC04EA915D4635A01E01D7A1E0D2B31200152B4DEFA7C0873C3C0F631F8327D83DA6C3658BFEC22A38E94A68912FFCA834838D231856BC4B94ACB84A1F4219840BCB89F14DFDEAC0B87E98B06DC8555126B9C58F72221B3D28BF451F571946D2DCB4317871B1FB052A321707A972425A113677CEFD8A34B3C9F248561955D7EB162048FC70616CE64B543D1FF48A34B71E8C717B041CBA3D1AD7A4740845023BA2F9FA78E663C338A28B83B0F4D2F1A66E02F6D2BA413EA448E8BCBAF33FC566F59E31FCC20FBF680F438615D17F6A93EB5F3D9E6367FF395B2DC0251ED347B5453853DBB490D4AD979AC215C53AC3F67D075B52142CDCB2AF25AD0041B699D51A561C76C78E6163C28826545DD4A93E6185588B2C2308FB30534FEBEAF108359C8C258C67BE15F6D961F01ACACAFD57884CF65510F516792E389520F34392AD51E1A0AE2F4A6D113D11817454B77B9C293911D39A0CC5574A5C5B2D7A980540287CE57F1EF90734990422D956C7583CE18AF8228519520606FDDA787AD7D2E475AB8C68B1446B098877D805F46EF978AC4F34115203FBAD39601727AFC326A5A60C5FED27FDB2CE0F7B6E657FE1DD08FD068D091ED8C3FC52E58ADD3C20A3032FFAD71CC467430CE6D1FAAD063716FB349F58DFC0029E2B00A1F93EC113F5EA0DB8F026BC383036B2761FC62003C448662CEE34253955C620F3EE27B18EAC215D857BE92E5DBDFAAAF103439F17351E43DE7A6E31946E2E292DE182F74C1ABC51D87913FC9643D11AFA8FC8493D2E9C438D338DC4197B6673DBE4EB96AD3BC979253EDF7EA92A28CAAD37F04730376403385CBDF6DC6BE4102DBDBCC2FA1D783F06D9EED97A78D21A626C2427B44B95B9FB4E62C1DE265CF6738FD68B5C6CF25347E321BEB42122F6085BA9B127C6735016F8B992A38389D570B8DA0ED4DBB317708B561CE3AA5B2126771AC6E90337E0BE1E06FCC7C5209DB6AE665C8CF54205F6DB725AA86545C2B8D9978FA774EAFA04850F222FF6EA8303EF335AF21FEA6D173121129A74DC7C404EFB12F6D29909E04FF00C2F3452511B1D0B3252991507221346A73B94A5CEDA8F2D95C7A17E5E5095A1632BB6B9429630CDEBFA4383FDA8EFC8145BC560A911275C235B483573ED9BB55A17BD6DEEBEA0F380D23718D47AC9CB628CFC66D5DE17921F8C1E076FDBEC10A424946B4AAAEF3654DABDBF147DF042E1E312DF359CCF481832FEF68E9CCAF0F91E04D7D72CD81885ED8F3A4363166F2F0615C58A621300B776307CF1B4DE49DCF5633BD5840DCD38383A7E11D94F5D05F6CA679744035FADF2DB514567270820B8DFBCC79A59D48AED2D5E6E252D3D81B8FDF737E43E91F7B4CA0BD9F258EFDBD6E76E70E429E4B2D672A2A3480CB380586B074C881FD7422597CFD4741F5DCAE55417D0768E7DD42ADEB649CF7ED2D94476B4D3E5E3D96F28F18178C18462B047575EBDFC9A5E8B48B8401A8DCA063F60B2C2B9CF83C1963337A4FDC3DED1E37AD67DF6060998532D1D22F29B99740B0660F6B3CEB843C7A96ABCDF6B18BB5C30C17E326F22B1A50F3D571221838E46A724A3B4E6F7FA5023C5A63EFC4AB310202FE597A97B3D22E7B77E99CE1E9E5706328A84ED4650363328E2773878D28823144928E948BBE7710EE936745F7C64BCA14F22DDBA510817D6EDFE8A1BFBE3193FE157689F06323F362CE128B6D6A1A189B1FE990CF1DBDDB22DCF97427A9F536FA2F6414B95C90D793C9A2DEF27C79FB2A66FABE82A7FE84D96228CEDBF4142A9A586EDD0DF4D0E024E6B6E2ECDC8D78B9E7C7E88BF748A1F3AF2CE645CFCF8442FB8F91AE4183E59220122E3BC18A557C47FB9F6E7108F6503D64ADE1AF5F861986F04C883CB4038208BE207CA1659B14156DAA2D7BD92B645A24296B2B26A14E799396D265C82EADA36289272527A88ECCF3A591B68FD861DF2500A70CF48497218D495422A5C2F243EFEA3DA2358CBAFB408BCD7DB0F87017AAA4A998092E9C8B04A44E055AB2D85AAC6F609551A50BC5B8E8574BB3D2B5CEFBE8F287A26FF683AE47B5B172743CC37D80BC39A99518F254481D32096E5792F7E6507AA645B214641636129498F1ECFE6B009525A182BAC8FECD899E94472E0944EDCAA6AB8BEFC5D5AC0FB3E0D8FB8643348F1F13184F05369710C6DE26271F1E2845B97FF938362130879CDCD2B14A7ED6CACF695325A93A346A0B6BD9829C35CD21E0BA164604D891A06DBAFFE4EF5BA9D33D28E4B3C16187FA7475A00FC45CD1C0970C1B6FB9408BC5D21DFE9FC41C9AD6AEB228136ED8CC5CEB34A55A2CD3069F415EF1A69D2F498D112EC571A2992DDB3CB14B94530C5229867051153102D5301DF18F68E76760DD15F2CD816AF22C512F18C6B91DD262ED05B5EEF4FD13A015027DD4C4E96662647CEE07C57C9ED726DA4B325511B97B57E64F402EB93948F96E32376B0660130A7FA3F3D3CC4CF15082C5B98574FDC00EC9A45F26BF5F267BFC18D414305BC08A71CFEA589B0FAFC986462388487F6FDF54E8394B77B31A37870902C963C9D666B925E0346CE7A91241CEFC8834163FF75B191D7CDB94A24047C5F1308433D6D0625B381F970EEC0FA2D497C17D6A968D6D779AD21A9A1DAEBF95EE5868BCB7B318056864EF41CBCE3F2E2D907D66DAB689EFFEA73910094CC8CC34E99BB5ED589535A2DECE16DCEDB34D7E80CF37BC968B23AFCAF57B4258F14625AC2B6CC6A946359ED0247B2ECCC26F0A185F90021342D211336E77575DB509D06EB5B3EFA4CE5C6D76168B63C45343DD863E6FA5019400127453D4CA57717B65A6666AA245C67578E40D19059D4069AE6D872528B6447BBE972C19320926592DB003CADCCED104182CD42E21DDC9FD19BF89EEBA7D9A1E5F184BC09705453F2B35A5728B66B3F9D87E379DE6E1F4B75EDED69BDB7BAB87ED25E38140F8303A98BB90BFF46980AE9549A3DCED7955FE93FD7537C259EEFF0D1C9C8C6914D9981EB15536C10FF0E6CCB006A91FD9422B6F600991ADED3CEA79F298A5C0257E5D5A5C4461E62CCDCAE1A5A421B659CDC0DC7914CA0679F266F29C2AD1DED583240749D6CA9361667BF40D5601FBA0CC7CF23509B46159E0A21C434E433403E3730DA6F3298E9656895E72FCA06F817D8EB1F087A3BD5F2EC580760F9AA10E4B550806B3FBB16E57B5FE7C48FE72FFFCAFCC448FACE5055D7871FECC7CA5BD88CEBEB0D727A51090F7BBB76CA8C3F3FA7C823C7302F102353956D919E6CC317C95AE0AE0D767B1433649DFB32F8526A15C8A0542826FA38C7B04F7FD4627B9C1DCC20A4B16C4AB11EED5A4F2B1B94CE12E70BBDF61DDAAAE113276382BB8CB298AEBCA843D8FBC02542EBB418A9E6372DBB22E38B1E46F41956498107AB01ACEC4C61534E0E506311ABCAD82DF91AE5E2AD9D22B33D0798A9B5F4B92B869E427D1DB377BEA7F7A5F838DECAB1BC5106922C074DF27F78AB91D4690F2DBA03A7CB6EDA0407251F8786ACFA7337CEDAF534E26EC3A916F1EA42E5F1ACC7597792ABDBB8F917290415A088623DF5B5D297E067264A7E3BEC417DC7E46D63D4EFD6FB0B18FEDDA612E9EA2A4793ECF8015CB241FC0678E37AE24B26A6C26A4C6EB007362160A9049B69025FAEB99A1FA38B98D271F6F374DF2653FA739A2FEDF71DDC57DC8450843AF74CE327FF5092F3E471FE338A24C0D4D012EED961BE8E7A81E2568CB500F266D7A48A12A9705BB1314D00A20232F15353FAA6CF325619A9161E1B71525F2D91CFB00DE7FB083A5A22583E5CB4FA2546520221B7523099DA195F453DB3A22C1DECB4EAB4BB3E6CA7DABCC3316912C38A6A176E8C8273A36A97E2B371375B826C879E3D23EA57DBACD74B29F7A9D6F69A98B729B996168869F740D2BCBB8FC3277935F15E3727371C29B1135D36DB1FD75FC018D8BEFDBCA674699B22469109A7EB985EE62FB915A95207B059B470D23C906C6C628D467327708550A84279320EA9B211093539BCB077C036950B4836FF471C1A8F1C617D7A23D245C6BE2ADA07B80BEAEC252EA9AB054BE18657DDE6B983934FAFC5B3DD095FF61ABC7EE83A71AF87B98782BB6FA08FDD853F1965B454636DC3B7CE24D2DBE680C823061501A1EF68BB11384A2F0910AE4476FC236BAB64D7817CA9E4FF44767770EE8BCAA03921ADD76C146D18B9335E247D927B393E2BB3129E0821649908529A2345908023DA47B924D52A88C0982408BFF54A24174460181F2E3BBE2FB73AE0713E3E82A87B98040E07E8665392AFE29CB8D2543BDC9EEA1542364DB2DB12AE53DC4C09BC7F55584857B644B3840C7AA34600B5F0A3CA16AF1B2B070A36CB859D0D1DB14171143D270D806BCF7AD285E2DFCA609DEDE13D81EE8D40E3795AE05084B5C2164E4516CFEA491AB976E2DF87F30E6D46FF495FE9B88716E772967AB6E3556A8961E1BC2E927147E9F34D798C645C0544F21E1E3023EC86F09B87B1AAD3C5607C114E5A403E24BA8798B341CC35B94C116407F9FC87D61B623842D9376211546A9FFC07C23E807C4ACCF1EB7675D7B811EF86642435F217A8BD2826CE4D239A9D65DA9E7BF9B0DE7D39AF23E5A251ED2395470F44E4C31A2A3D75E3AB97F62BC513240680612FE57020B22BF25F1E83A4BEC8B8BC84F5277139C1671D0A2E8CDF586D032AE7004DB2FA3B92A9E652304E1236B02C965A6DEDCE1A1E7BD7357D54579004CE9025657059747D3CF831C8858978CFBE1FABE230D339A74B257908DD4FC01266C62DC9A9977FA1B4C1930BB35B2DC6EA360B425D8ECD8FE527CEE68D70B608B2FC280F7F0709332E829273AE6C5322ADCAEEA59F07F8E363E11BE14AC45AE0F821643DBE7567CDB549744A9EFEE235DD74CB0D99A938E0C22E204A11B71472DFE001A258A843C004DA82EA6BA74D75A9AF8F62194F4B3B70820D93AD602251B7BE2C51912BBA48F7933C70D511076A181AAEC7C849C0D93EB8EA642800777A513EC9049264678F0AB2D19681483BB54F178050E42B0A8B22EC1A5B4DFAB768CD8086F9D914250C585090F423D960F6E7450655E73C0FC8EC7414FA17324CD1091B6673CB8C72A7B6580CCAEF8ECE36923C008B2D85C0D993E4C6C2EFB15B4CB709AD16F682516709F9A41F8C7D0B4BCD06538FD4922AF52012ADA96FBE12CC1E8F8BB07E6A3AA32B4FEDC6192F641B76FFBD9B22BDCB58B52302351D56114C31D1CE4BFCBA0B3D3B31AD60B6887C9B9658B436836E9F90B1486ACCCE7D0C668F1663D3CEACAC519FC7BDA7DEBE4428A985908FFA10645493DE0673691D91E5EAA0164B200C2F9E56B55F850A90FEFC24C59F577A5182D3269C44F2A9FA30EEC22D625680C7E9C99376D52F9B58F624B2CD3FCE8C6702BAA5853107DE0A8D8A9E8B4B6BB53C36C39126C3E148C7509A6AE339D39AB6218A1D7F49FB3F6DA02D66BE8F5811BDBC83004742F5293DC6A2F58D63423BB2E9F6E17AAD4CEF61744B8A9B5954736FC4F7F1A25057F0A6CD135E55FC8AC9548BB584B685BAF0F5FAA003268C051DD3521F737A7E22A245B880BEE70DAB8D6CF21665DA2B21A27EE0590C3785A8D1AAFD94AB38359682BCC14DA4E70C8FBE953E32EBE03A15B93EBA5612F5A5ACB793E55FA6FAC615201C29AC64CC859EB2B0D62C4436BAE9CF20CA5F01C2DA5B715F636EE8980B1F326FC4F4AB317ADF3527528C6638A4996300E1D474073AC585F738F9CFE46D93094EA36F5FA9EDD5CF014C0C00CDC398CDA3B0B0C8CBD66171E0EC5A164CC06DC2551E92A5AD230F8CF4B367AD113C156A176FE9274D1D97BBD357FB8238207C676BB29B4FFA4DCED5664C9E0D1B1632C7163910D728964A1296936C453D79807545C15B530044BDE54EE854C5C3C5A84536F15E7A15FB25F0F03B1D6FA6DA5BA6C1D7A74FC41A0CD545402014DABD638B80C6F20E99C9B7F71ACA64B89827FC53822D6701481B258DBF8E29BA844001FDB8563DDDD0C76175F3A3AA6C368B5B18D8EEBA2BFA2F6495C487EFBC23B0814C36013A341CA786421E42B5F5A0203B604FAD620D35A9CD9373BF25899DACFD3D9D02D44F81B3C9DEA374822697BB729BEBB84E96AD6FBA5E1B70D47F31A3F40080E8A03D7F8118020EF39BF453D563BD49A41D6849974A35746FC5C9BE6A41FC21D70FAACB7F5A29B68D8FB91E8EC14D5F5D61D0C25F61B88E9841EAEADEB3637179F2D15B0AAE29F5CF329D6BD70562C72308B7BB03FC39A09425BA0D3F7206C9B9287A87B95EFB22F67D18277220BE666DB0399DB67CB749059ACA627B0BDA49E13E1A3BAC4617F2D4D482FCC89B4550C9F0821BB1ACFA01E61512C25951D3E0BBE2715569829EF5F2351453298EEA85B3FF068A6438FE1E08B64CFFD1E07F3F2039E47F65CAD4DA00001941E746BEC08C92701959EBC333FA5ABE35226ADAC7CC9590DC406CF7A8F35C24DD59B551F64C49427F0B2EC856B8C2E5BB3F573C56262D64D4C9A1BC7481824F5B10603F3E780F5D513A75B1AAE45865F0BA516781756E65DDB3C0432EF2695C7A85D304A6D2E5599446F87B6EC58659E4272F24D6539396C5F9C1256FE6D123E02FDB05AC9CA14C24653E83946CF275C74C4118933737A0E81F2B230D8CCD7C09BF5CC2EB0CF176194682917268708628B40E3B908F4EB4C2A15B1814DD965132D63ACB41342A9B9C77988B01E5B9E36040DE08EA2D658F6633C08E18AFC5124AB0392E2D67126E9A94B04EE97D08293E01A4F541ED6E07B1D60C4F241601B975CBA03F7B522B1EF78BFF1B4B1C4FA4A71AFB5F7DA91F952C0C40C5DF551D2D27FB8066833E60F4511C50C5C3F71063393370E5483C90CC71C04C4721CFFDD95C6475DB3F86992A5FECA5547A078664045C1A49671E322DE75F51552DD886710C49548646E07D63E161843524EB16CCD6200EC7F8AC0C0E1DC486F28AE58F4955A80F8B98DDB64EB98D98659377D90A41B93AC9AC0D6723FE7B857F692F417BB9CEFB55696AF456A9A6432AA6347DAC624508DEDEB4ACDBA506B12099E08705C021F37410E92210C5D09D101AAB55A2EC3D7950AB43520221AB91E04D652BF3378D9F5F7B669379E90A0251FE2B4713391A8E65109F9DAE1A44FB3EEBA3B12023DE0B332E06271A5F6D41FF3D51715F310B9FF5ADF4A0D3C6E2A75AC53D81815CA3AB1EAEE65BBC402C47A4B8F0ECF6799E902386786F992B2889FDFECF3F7A8E5F9264CF3B31649215E253A2F4A8DC9E8ECC417A7E52F927A8C1E984D81CA3D8118733A7A77E0EA459B89E6E471B96848FB219AF4D74A61406479B7B869E57FE347C6AEF149B1ACE53D75291C6DD61A45A9A6528374180D56CD7597975258E23D9E8C16D313378B31BF917BAF448B38E678AEF9F56412D7BDAD5272A41FD55E9DF88724EAA5A3B0EFD2B22BAF8E40952EF4B05CABE46ABD9CE9FE99B3D5067F0A4C5D8175FDEADF4C83EA9EC3EA790A507A9AAC6751E8DEB089E378D79D66E226A94554D0ABB34A35CBFDA75440988AEE4C3D031D83EE2FCC0290BF62C608F4D0CE31E1EC5F12F5688430F1D3EF3BA8CD68BE1D71D75B71582B41486EA20E5BC2E91CDAD983776A24AE54224C92DBE9C142E2CE620D10FB674229306DD6C4D286E3216D4D076329C4AF048C03EF683B86D02D36767BD3F8B1A3EE475A014C78D261878BDFE2BD7BB8F6E4800FDAA771F968FA7DA98EFB207A78A75690DCFF0CBAE0F3446B7B4DAC7B2A304D2F0A99B03438A26B064EDE4F73E0C0911749D67883184CC677DA32FB2F59766B3125761875D365A377044810AA3DC6AA215DE5BE4AAA3F38B637F0969632CF4F93203ECF18F8E47D8D839874809E8677FEFBA11162619C34A9A93E8E3B1C720B8051017649CBFB9171242BD0B276E7CAF8A083170ADE47450E437F32DBA51A91ED760705D79D6597EC957AE9526B9D2AE7FC49947C3B422840C19B4049E05F2ABB7549D5E6AAC31296503B3A86885D5B0B09AF81A7B552275AE5583FB975EDDB7A2B79F1F18893628147C1E5F761D49B71B9494FEEC90F2D2864A73F72D7E1F3319C1F72398ACEE8D6ED302C5D0332787B444E7382028C19FAB6F12591B62C3AAAE6D16CB7D9F1AE834477697F93ED36B814233D70FB23047446E502EFD0F8F5A08F27A2802943A16A72CE0E98806740905CD5770CAAE2BE44091C569EA626CB0CD2EB44960EA698F82BE64368CAE9E0DBB680A39B4E6B688CBE4FA86F2405C8E107B29FE496F48264C216C389FD684886915E959120040E6B93F3000A1B07A6864BCD7D940EAA82D09651EE1362BBD77FA9B1714CDB6F0B3309551660FCA4C6B3654807F64C443B0D21876F0C4D7CD08C6BB037855CB0E3F047D61F1FBA2FE3E928DEC1B7493EBFA6161D7C9F406083B5F2DC5D87C69C401EE1C3ADA4A090344012238A53B530313307B455EABED2DEB84A746430AB11CB32ABD56238AC471BD48E3CE55DEA4C09503D66CBD12BD33838D9E167EAAC1709DCA2F55982945B1CDB95E724AD8E21EE329B939FDC847A50E4C8E0EF35DAB86577412F60366293D70F06E2E6CC26543F9B85B6CE5EB5A357DBB9F66E95E1AB45169B102690DF97A28984562C2CD82A1AD51F7CAB58D9FE61707675679D943B5515B03F93C72843750081E64496F313EDA9702DFEB7B04DB05437C63CF109985BE8B4908E154D4449CA1C3E77E5AF63CF18426F145DD841091EBADED2A757F6BF3B387F0D414D920389AC3247CB12A23933309F985990603968AC198A681421603E32178FB0B1B8011B7C8A854A5AAD2E5A95AEEE5EBC893F31A824D8E07453D0638544ACF4E1A1ED9F9972B9C4CA521C493890892C4E7415B1E305AA049B2DE9F28D5CC33C18FBC2E17DDF54F56F0CC163EC3DD3933079E4252469216520198B6D573D782EC8727F44950E8C57176746F78F620840E4ECED239CFFC6509CCC8147B1C15BA3AB16440B2236889171C7F548799B3AA1333C296AE7CDB83FFD25B30CD16F182A8A81E3DDC2B1408BBCE60A91C46800D3F3C964DC992F46E99837BD2186634F766510B74D6264D491E6D3244B0D51394A46D854133F5C14EEFA8E6139F6C490E38D03F0FAA5140298174AB7923BC34CD264303CF3A6EA526C5FA6F966FCA9D9E97DB09234B09FA275684AEED7E43EA7B39D26403FCE4E906FEAECB7C5134CBCD3594F9E591190B0B6184E8F30C3F7FEC27F9D01BE553CB1E1FA1A89D192B1E97950A252057E53823A5DC2F97F546428A447CF7704E47EFDD3D43E6A20C95EC6707CF192B26CEDF711DED315612708D771A0785D45D6D0D9B9B4B7970754AE370C2A881F439E5B760FB0A161AC51D33CB7F842924351FBDD2BC633BED5E757CB5073031A7BE5502D17F93FC4D6CA9C951566EB7433CF60F1A4F07CDE86B0B89C5EBE34FA4099C60AEC20B086A76D92502670C048D48EA6CBCFD7AB91C24D12FC8DB16F85C14E9E0CC96710630428EAFF7A020EA6831DA3D036CC3BBA89B55CFED3E8ABCEE3E4BDA9874810D6AF533BB907AE7931237F840EEAE038A57664749492E31D36FD56EE734ABE01739138D1D8008BBCC1E6853D1E8AAA9D9C0FD66405D82DA168FDAC04E24FAB51D5FFB178F81639B4396B3EEA299B9E9E38AF3B636508C817DED795FA1F1692E4310C4E2FCA66AC84F80B42EF555C1BD7818CC8B7A57C981EAB435C334E566FE1524502F60011A7959A641CE4400F58703BDEDA6458E7A87222B1E3CF5CA7087A94BFBD1B6BE7F625A461ECA4D13B0448D1B1889225E9C1FC2EFA3DDB8CDD3E9D0FCEE905F4C8A5E3A59934777EF525EDA3D4086D0D7FDE40FA63274BD2CE9EC4B5DB7E9EFF440911728B4921FD5C8C17377C0255F7845E1168D08BCC22346A721E362FC02B2C296C830CF0CC725A124E909297FE97E38780A212259CD773C56A0494F9B3238DB580885DEC60B7969D456A36F632D053530E16704D5521B05E46D88E1B3AB50CEC9D25C85783CD792959918C255DC18FA852E647E4EEB710CC1DA05F11222C837D5A0CE0E50CF15AAE88CBEDAF29868D13EBBBF18ECC1A45042D8B0D9225603E9DB5D48FFB7D5439A81219A8BE43A316A5F61890D9532ACFC31403B904FFA2AD57A4E6ACD43E9E37E3DD340E49C0458F916FDBB2B1F2BC1D82719F4F523F4C68819986F5A19D26CE125CF3288988C11505A6A67AC2F248A74357D0B2D91C75DC669A2A5F0F330B1960CF788B9AD1363EBFB2DEDAFC48D7E5E4779BC487973EBEDAA1C1C0653CEDDAFA75DE94B36EA99FD5E18F9714250AF2F9F4B8845979AA82CCE792FBE1CF9A8B218D791BB7D9AB96FA35825BAF2280E0EAAD190EE4F20C0B034AA562934C1DFA037654786B2D66EAF5D06B7FB4E94FDE1A000D07832DFD92D587744DEA7DEE104119972BC09C5E5F81B030F2D46C9642484D5BF4F6A8125FC8A70BB4435FF404F52370A406C2B28B6BEAB771A5B8F0CF5D7A2F78182428535F2AB225032AB90996979FAAE7980E3FE98205448B7A35C7D7F4F5C7036029890E53ADF080956BAFB98725FC12FD047DB591E132CA88BD400BA5F1856D139A6D12AA06A40E0BAD3B0CEE567C181344B9B125ED96549EBCEA447346DC04E3F92EE9D991373B8EA7ABB726ACB63A7836E67C67347AEF80C9579CA8F828B54ECF41A54FDF91223483F4FA97B696FD7CE43E28FC8D433DDBD288D404F60210CE8ECD330A6B6D5D9EA9DDCA6E1CC2D7D4F6A52A36B8243AD22354CD1D58D6F06A44A0001B9B6BCA90E5931E5B4A8D593FBD36A9BDB357BE9E5C9EF781B6E4ADF45CE3BBA3055864A48A7B0E859ED3161B3479DB910B6C85796EABF371BEAF79EC95FC22372462A7EFCBFF57E8E30BF78D83E81745CFAF898F40C140353346B0B7F6867013B5C8004DE9DDB2FC3ADCE9E4EA91823F9131BFB2CAC51D4A611429DAAC24B746402F9A6C2D118D7227A872B736E58234E5A48E5F68A70A6FFCAB620C04186DEA9EC743162A9609B34C3AEE021C917F8573C556E0E04D853B72CC088ABCF1532A24E65D47D4E6F97FEE8E7954861511B4A87F0FE75BEB58A7EC5F233DE10F2BD87E1BC225197BD57ECFB58665662C1080601143208759B85D007934B1D2316E59776AAF0FAC577037CE27D84B2CB7B63A5FA6F3845C621DC6CE58303A843CFFBC3514E13C000FD91FDEC4FA481BE4E6EFD445320BD5F1D631D0940344A5930BE9A2F7DCC29F80B1F27C12894C6510BCD40DD77D0174B70297FA5667BF27B596CE0D34B883481F646A83D2486573987E82299EDC32F7485D2822635E2BE4CD0552976830450BB768CD28566A3C143CF93E1E7BE2DD566A75D93D3852F72AEC54AE6BABC37F23C1FC39EB0E1F9C7880FDD37564D31176B50BB7750ABA2A5DCC6380F0390E5C58B239A3509B104FA48FE8479B59079532A24FF7BC0C0F6591E05E45A557256CDA0977944BBDA51A39C620C2BE323F8DA106E5C4488BD7C9DA6853AB49720CBCF5A31A8CB3197F0F14B0F9D903A47D5952BC443C95938DE52511F2FDAB2518C4414FD6438977034DA9A05234BD6735A8DD62BB66D6A8FAC99C33E5A144F12F640461044D3FC8B5936BA718DD4A0B1808FDCA029CEA18298006F16327FD74C3423740456EDCC8ADC70B4F823D2A1FC4F17E5D1241B2D537805CC6F7400669977EAAB88B427CAAEE753F734E3A9E5428F13CF5345B4E86E2271B61ABF2A8731E86D015873D24CD18D7AC950D34AE79C27522803739DA7BAF9D6D38765E31098ED25DC566FC53BA0DE5A295BB51C292FAC91B350EFE111612C27E700CC0FCC4E3DBF354FC004A60815C4A8EDFAB0670C26AEDC5F3F1A9E55FD9DA6CF7C94E2588A4C2A117302CB106DF1458C6F40D834D312A7C302D06672BD02AE1AC7A1EF8268EA4E03C106F046329E240F83C89961E877B04CCBB03BDC8789076FECF83A81040B8F13DFD0669374EC1BC2434246BAE4BC15EF6AD321B92582D8860A2CBBF4DB401351D3C75E3875A7B7AB535BFD2CBE05E0E4A4E53429F501207A3D15ADB2351E6CACCF9D948A50FF1223E56B6D4890746978E2ECE5F9D81DE5594332B3BEF3F5DD0883A09C301A9B7C69F9F2CEE77C19F4BFF8B2E0C5629C349115701C1E189901A27C6FA893C214C8CDB7C23EC80AB51EFD3A0C7DDCAB44E1A33C2CF646AEECBEDF93A81687BC06F476BA8E0D41A1E4AC8F7D28A4542DD695734102E0CE70D33F813026FB7DD72ABCFF883F6CAEFBEDDF07B86D057AD47713ABB135DA98F26267336C3270FA9C70B2787A66EA281C9E7F8253976C325FE030ED191894A5CAEBB5E220F9A7D8D4EFA6D6BF08FE60F6173814406BA26C5583410C492B79C92C211185A375CBD348DED23A2A1A79D2990DDCCE57FAD23C9E7D54B4ABAAF977A1539B80AE313622F1A25A4B6E5533DD9548A901F14E6AA966ED8D2C983B8A453FDE0B9DE27CDEB8D5AD3DE379673ECFCF3298769668E28E7DC3EFCCF727F3E8DD60ACB8D2E23F1D016F747B9E44945B898536667EA64873510F441EE29106009FEA0BCD058E13BE0552DF370A166756B7B4E0E50CC9A82BC280C302361D76CB32AC02D30F5647681BF9700E7A1635B22568B21B0AD17A6D3A2FF6364E6A50D398F71362ADE6BC3B4E1337CD07FEA42792ACDF12DCDC009B5B0A1712A04EC9671A6FC75EF733412655B27C5F0230B5846897589CF3294D09457D0FCEAF15C17A31042D86ECE9473FBBEC7ECCE20493298EFDBED72AFC490DD323F6A7F664096661F67A49A65FC5D9670E272DAE7D059800575FB0681FC5F164119F539197EEDF9030E5CB7744D5818759BCBAD168195C08A4B3D252D30C76D19ED431988B86EEC2E99757BF12E0ED9E245A954FFA4C240FC5A5D6ADB8F63994039DECFCC807A50AEA7886B9B513B740CA6DB84C2C7D1FD90EC5A91F281D67903A1A749BFB81527F5298C69476DCAC64C52EB1AE11A37DBDB238F1C0141B277F277090D45C957BDDF7C256263C2661DE565678148643A2C8042B05626F34F6D9617DE4ED848E08CD07D1E3FBA12ED528007FEFCEEDFFFEBC1ADDE26ABFA13616F878217362816D53C1D3A5A8ECDD808CC59A9B8661CB0309B73A67F2E468FD5E6C0CF6F8BFD08E358BC1922BFEF93295374261D8DC03FD564C834D1B9D8309CE3A7D1C4F7A48C19913FFE69CEEB409C20E2A64D520E361739710F1E4E56C9A63F475074B2CF7F53754D80C3C82ED3C1A043CAC4B98E32A009728CA15750DA4F0FB962F1FF6B356DBD89D8831AB1B30F0DED57F27546E5B68C35B2BF2487B0B21A7B2DAC26F126648C5DAED3F5FC26D960CC6DF44EF551D3DCD90B25AF331B6F5FE6825059A7F85AC08A721AB2FD16BA3F48572936B8E414D8D94D926FEAF56BEEB7012756C46B99E150BD0D22EF2EF7914ABDE361FC87AA1E4A1402D7C4F588E3457ABC7B0F88C3595B708EB8D14FDC5B7C0745DF5824FB746D51887A1DA72D399C444EBF2A5F47936AC8114DA56F7FEF56ABFB9CB9981B7E922A195133549E758D6870F6A60B22A72FEE14B400EB5AD3FF9A6182B06142A7F7A62D9ECD6B38BD77AAC24A58928DDBAB089D252518335996D8770B283E38940384F09E96E94E088D1BFF230E1BFB79A2F9357833B0EFE1655ADA149F7AB9532D09648A9FAC8657CEBBD9CA24283813064DA76B3766A3ADDCA670FA9C97BEC874B61A1EDA0AF2E762F3871250DA7EC2D8D1DE9AE7927987570591D685F404B0C59504D45F4B6728A76C83F21BED13A35F214F45AC7C7754BA0938E15A092CA99EF1F4402A90058ED24A31394F9D0B9F8DA0915CD7A7F29F1234C1B9AF65CA6C3F5E3D4CC808B265D07DC90F9CCA4BC38ED1ACEF0D55A72261143B2180E0D70FA814C3ECF536FC05101CC0B6D28ACB5C6755BF7B50A621CB8FDD3AAC9CAB14122650B89204108C9635F2ED6A79304577B6B4C581AD0190EE28697BD6CAF3137A5F82B33B31C6504554426485427F4FAFCE133CB931A9C1699ABDD4A854B20198E62E71A5259151A27F45A955D4C177EDE532E55A0748EC13260FA985517FCBD9480D431495E89A8E9F3431A1C4205F80C6E9827D416843B50036A7C0623E48998163BA3F9D1C979BFF2ED563632BE2384CEDCF93A89DCE021E72D9C8C3CFCE0B3C13A668652366F4DB258FCD4AE30D273141D5D0F4CFAC1218F86DEEC14DB12C18709975ECBB8D81772222E4DECB967EBB9E9131366C438AD7420C411E5894380685AD963677A6B6D4280CEFA81CD797346F46ADB2DCA5F6DF1AA8066023F52CCAA4A5E78108AC5893B8BB047A0379D5EAFAAAB203449A89A75673028579E84414CD986717E8127622EEAA892FD73FDF5C9988117C7DF6F167D222C4929934B94A8335D2D2076AA79818F9BD0E7C4ACDFBEE5AAA57ABF0CC3EC9BFFD491D8C944DB5E05049C4A07F5B5D955E1D32CE2ADC3905101CEC3F904DE8DFFA6571117B2491F72857DB460E0D46A26E2AC4766768863AD79B3BC55EADD34C7FB9CC18C0AF613B98473DB4DD2CDD8F1B43E569B834ABE2B29654888234713C9F8CD02319C662927E12D5B9E9C0F43B564F995FDDFCBD053BA6948946905451E9C7882F847D55C4C40AB5C24AEC8A11603DF447B551BB0ACE186D5DD7BE28F73CCECF2A61BA97D6012B363582851497C769D03BAA8445D3DDAA50CFF1D5A7F3AE55D5ED5C14CB7C38FCBECCDF29BCBB5704FCA467141933112356E91AB1A9D5C5E42D440E7967A67D82AC8E87063A089EF0964C61236217166B5F17DBFD6C29C6F8E4B68E9DDB8CA3E6260DB84990E9CF60226A79D654DB0040539A8D2778E563A9198E800A6A4BB74E13C9E96B8ECB752BA6DE2B47DB4D681A51E81812546EAFC0EF04CD61022BFF208FB50D6756F5CE8A24492747E2D7362EE3A1E898AC40CD5A316FE4BB5F123EC354DE062053E866E1911FE433B843567EF5770A0DD2B8CE46249AACDBB57E34E616504B859D0ACEBBA3588AC01F6AE4C9655FD3747FE2D75EB83038E52C58F958B3FFDA1777DA0F6432E5A88D44BB04F16FD0714877CDE255CC05BC8FF95FC5A1EF1EA3DBC5923DF99009EC7381129D6F23A9E3680F45E8056C0F7C902B376893E2F563A88C67A37E1B3BD051DE6BD11A2179C871A52C0108DBF199BF9ED9AD08C081B6AAB018F65DEE196F1ED7988398930E9531DEF47B6F6711BFBCDEFB0F7EC95F29D85B0D7DE64E71D0D525D5A0C6822AA450F6EB190D9F008E54F98E786F1DD7AB2AF434A023B7FD280A1B6E211907CA3B8C3EFE00DFB174323CA0DF5B4225FDA58C434F83FCCDD3786D1A7810BD54CAB48C9889BFAD78AECA5F5A9087083AA044D565A9DFA1A830DB660F5FDC26157FE2453EC3999B36AC693942A37AF42A9DBA67708A4BE2D2232443DB715230D578065555EB62683C264509787396FD20009E8112B9630E7742DE045D5E4AE5B2069BA3E1985465002BFC240FF1C41BEB01A8B2853B852BF35C667850A0AE30FFC3CFA0AC12C2B453E7272799B284C1EEE6C82F7692BC4F14B9745032D08869B444CBA6F481FEE8B0FDA11409C6946EA8354669B89842F2344B95996A5BFF29A232F5EA452F2A4031EA99A9A77015D57BCF0AE01B4E1F56C874A6F4053015E9B7045F28F907E3AE61E0B562DB4871AA4FA57C6BD6B70F353A6D829B189E71419E2BD0B27CDB0E4428F0D0ABD5E7BD47044A6489B6303CAE6A41A7604DFEA8AFFA07DE3E459B73D556F5802E705A9B75D2F6A4B685B95063879F52E8FBED4FA89B9B7A8590D44789CB0FB4D7131772BEC2B63D5EF57E103E0C2AF400EED391374A1AA186C6705CB74864C34250C336125C03018188D574196F2E44EF7F81C833B956016205B2C71C242E03491DD80A87FFA8FFD1E409708F24F6A94551F0E390D8D78463A3296031213818B4F4915003F2E3F80A06B3D4862CB65266499CAA76F6062D2A3C54938A90AAD8A0415A3D19409255EF467BCD1EFFFBC30D5B06395A8BE3D4395E45DD0BC05EBB7FECDA7B77EB86530907635442400948BE0F067E5D600B56CE214702B959B598B98800FA28B85536582000D7B3ECEA519E30DFFC83E451AD56734FA0CD4201692ABF78B612D3815B11AAB63AF9F722B2F614D5C3DD021D2DAB10F6B169036A4B76F1869C4D2B052E9CEE18D9DAF87C83AFB7056F02B305B13F03B3F186D9FB66AC9A26DFC64783389D82B4AC18193DE47F53CC84A8E67DF72282FAB8D8BF8E3E82142BC3378028D5F895D0C6D498DC816C88BCFBE6FD7E5A6F9350BE6B4E3E01E91A02C4D6045FBA8D74A0B44019A200E791E4E67049AE78EC41D35FAEF6D890D9175501E3B40213243BCFC6CBB38A8F87CF51FA4F58D7183DF558A6988C8541DF6AD85FF8408DE184F14FF575BB0B09C5667433F6F65E7B7EC2D16FDD87FC85BB4E91F913EEB21D2BCEAEF1F751F0A376DD7AF81CFC18EF935D88329415A86CF420C1C993139D2267E25D4B044AD605A7527F721A6E607A21CA4938E4624CAD4C962D6CA60555D7BE1D1473932F9FDD19D2B837D0B82931E371A135C3EE20E98A0950AEA6F5690DF4A7315288750470D4C4BBCCB04050EC8CF6A9FBC2CAC2E6D1228E50C2BA739CCE0F736D9B96EC8C78262B819497DEDC9E5881C51D74318F9FBFBF7520CC411D4409BC4726AD7E01ADC4D8FA1D75FD775AC345603C530C3D8ABC582D0BDB254C4A9EB513FD1226371B34A1E342D0CC087D82E10CF14CEDB16B2D42132AC60C09236559BB5FEFADF7C0E65AEC7F862F330D2C4B636C752F809A3AEF5E6BAEF59A6AC1D5B5635B0CFBE98E5E6E67E5991E11C6DE416BCD25E7E20CCEDB98B30713B1AFBCFDB705A7B639552973BF19D66D94D97AFA1174B2030E365E64A1DA1EDFC0E8BDF5D65559E7E18FEDC0B6A19FD5AE5C1530C5A065E817AD55261263BB3C3BFBA2AD2A2411CCD11E390DAECB32A259A7BD6897FF0E3B695B2494C82B2A180003A7B8C24587EACBEBECA1AA18110CE190290DBAC8494DD47270E5B363CC0AA1B43B3CA6BAA66B3BC57C0C12D8CF4BB68516A3DF12491254717A4FBAA2DFC1085B8D20A1DE7FFE7F52A09E921314BCFAE279C0ED4642F79857AF44F3B44DCE6C02B1EFF299BE2603421B9CEFDDB33F1BAF2608FB2CF063C025297FD9167707B057DE09E62F8610FA5874676EAE9D7D05CE583AA38EF96F97372810DD74C79683B450F57B5F329FAC82E67A8F153BC21CAF7F5F7AC90D891A44EA8D7841D900701487C90D847903EBF4306D6B9CD1D8D4D99AF01318BD25AE53057A20F096F7B8F0FF7EC74E8D94D26600781C7D844E221421F9DCC2BE0C5FD69BC449851A450963975C2C4C1934E187663FF5ACF4E154BB3A17E4F9CECADF1855CD38B962A46E8BFD02328BA7715D05BA05ED4B0002807326B7F92B574C1BB1328F18DC505F29B77A1E034725A80F7DC72551FE2091EDA407C48B92555BEF7626320EC05488E8A1D821A52B2A0ED9C5D931A3CC6EED3F9CAAF1AA6C1E1C3990A914E2BF4B764A9DD78E55827A856B1537420AB172198F864350F55773A8F8D2255E6CE1277DD2AEBB39DAD6FBE5B8A23D3F7B2A0BFB3BC47C173947104C453BED7D5C5C53B75E7AD0A19107CA4FBFEDE864E0613434061E96E4647B67AC364F0781EC0C35F29002D5DD71F1F4617CE8BCD78B301DB1F9BADF3D3397E3E07FEF04B53714D6439789C320C72A4BB135C229380E4C6AB682CDD20E02B73192D49340576C4F17DD086E5A4EC28D280A83B4557BFECC93C697BC530462CA89A91710CACF13888CB454127804BF3B6C1CAA797B59F5D0729FFBB1C881BEC17C73B16265D9B5D64C0245FAF9DE1FF7027E18E24BB7F7F3E0AB43B666207D3BBE3BC25DD225634C9B235DFD394DF4A896AC0DAC740F4D49ABB12CF7D173E00960BC23D51D51C0D15B586A923D3DB25525B5521D5CA520A6FAF4B8348A502705FC0CE236B9137209DF171032070442C00AD56456A4A31F4C5291AF8480C46DFE2DD3D8CD9A3BBBD38A795FDC891557BD839E83AA64ADF4FF81057BBD5B6FA33F5727F9670ECE10585508AB9F4B85C821181808AD43C479336B08F0E99002CCF876FB2FBD23F9891EC8CD58A358AFD03D9AFDCD63E7BD853F66E4763EF39373B18EC605D5D4A06498E0BB3DA68D53931C582A49A8A724437E9F5BA5A086D1100C149B83BF6D7301D842CAF1774DD31D144169C1BA24115CF5EDC7FF1AFB627BFB5F60AF9E41FFE4CED484ACB776CCDC0877B2959B331A81C8A7CCAA0C6004E8268BD26465784ADF59B29ABE3EBF90AFCB67B56C207AEFCA5FC24BB6A1D36ACD92D5C8A447FF37A88267E41A64C7FD4BE28B0A4263B2873C3DD700684DE2F497D143CF025DDA097120D052EE8D6F2DCA690EE17FD2D649AEC5DF192B1A3D4E8FF032A4D54F1C69517E666A37E5C6DE3749EB1F292D7B4E8D26AE37FCEAA684A17018518FB2B42BC299868CD6EEB281BCC46834820BBDA5419D38C833982F8DAEA17F694D8202F60ADFB8C159541EEAC374B23993E4D18AC048BCC66E2D193FCA95965B91076CF0F14C028CA826D058EE75D6BD328ED26ACFDBD2EFE5F5DEC751143B4DBB839DDE9E673385E469F739C2DAC91E6A3E8D57F45F8EDDEC367560B7566F5C1C66C5CBF59D4B3346A6764A5AEF64BC216FEF9019E2C32D8C33199419480C9348F954A40C21AE8C6740495FD0B1E52A2499A888F6D7B3ECDE3EC0B441DEBC44EA464A6E5BC4D99953C44B8E5E1DF81C61B85E2FCA6B57DD5DD04C804F90FC020CF2A913983332D4E544891400D24638D42C9C394D6D136DC96BF6357F4FE77B015E9968BC34B8E56FECC31F2672DA3E01BA3A0096F892A1AC0C2D377C91B04BFFECE935C60545BC0E319C862E5AC37937EE11C9C68386663EB68EE243BA6D783A00395A27F71D4130FF7FAB571893825C8FE76297C38C078FF65A835AEE5ADD5610C02F9ED0E9DBCAD6FEC3F919DE9313C58949B47AB8BFA59E869167977D1BC6C4A8B04DD3934F4865BB244BB68F4A6FB7F238FD46D4D6EEBF8DFFD36B936200E2A1C8DAF42B912BF76E695B81342BFDFAEF362DA51D5CCCB6425CCB5D43F1BA1D747C91C22AE67B4DE5A998261C42B4736F96231702D6CB6C83C86CE6EEB071D331175CBF4B8E1185FC6C852755083C5D5D101EC185A3DE7CBC92215DE9384E89C907FEC59F2EEA849FAD4BA3B06F43468E7C693C5D9B97FCE581FD3C84F87917E82849E40482B24FFF1253B887ECF3886126436A8F32F98BA3CEB3F8AA798F3D7E8FEBA38D3112AD658999A8D0911DC9C0BCF6E58646D3B0B2BA6941C1AAA6F36D9D2CEE7FC14FC0784DBFA75526AF171D52CA17B937428AA310EB1BAF74B2CB5C6BF65715CB74D79E89F76EBB08D54153EC4C1A2EDA5B3A272365CB5F7655EADE742C682E58C8A2A68D22C5356F0455669102102F3B94A9AC0D2C615272D0CAF8C941D52D5D621BBD4033F63FDBBA16FBF3298F5CC7205F2517CA0E38CE4C1FE127CFBD2FBD239A0F14FD977476014BA033A70910B342BE1192936281D6C6243C35328BE94076FDC82359D87DEE9D8E2FC0C868B61EB0C1762E9FF2D58ED2FA8F8985BAF4439DD089D1A35659E38E06105A2303553BC60FED0B8816D4802F06B818F2EAA868F81FC00A69A636DBF1748B569A40DC7D4D245AF47558B714CBA2BF07266DDE7D403A056900242D01948F1519424A4220CCA33A4788413D87A9017FAF925A3CE43F33F2F6794FB8BB81D0A6975C2AF8F31A687EE99DE809C222FE4CE1CF485B91C4227CE8A4D4F42A57F637A079906F371F3BFE91813EC7D8555C5B0A741376A6D1EC78F81744D1B882397F2CBFC0060C309C1BE3D8C075A38D91F1F8BB0745106CB37DAD1D569CA474D9D04B63440BD7EF81B16CC913E12F1A015A189B91B426C2BAA6CAEAC9250BEEB540C0B5E803F6DBB262CF209A7F240DFE035BA829A2B4E5400C4CE242EA91846145FFB0617BABB0342679C62474C097C9FC5ED4D3E70E2E3FE8BF24D51862AB2008E23B4C0F053C3DC3D7E097EC263D1AA5007AF21390A20F64F3179CC2DA3F7B4C0E460CAA8B94C639AB41ED000FE1FB97269F26A8E0FF8D8294AC2C237A0142BFD7483D492B367CA425F788AA6E10F1D08A99813D26F090C4A92D5B24AAC7DCF5CED9AE2ECC0BBA7F444AC9BE4DD1AACB856F5445AD575AFE84C76CA15E73D39E6887C774085DC27A2C8BED74FBD6C85B2AFE23A43A73D6A9D0044D931C183223F21D7BC9D12C24DB68AC67BE912D1D93680413C9C7315548C5F4E5A3EE60997C34729B9684EE53B161D067960B80563FB72E882232CD946D27D7AF57AC452926900E83CD821C94A7CFAE68497D459D0DE28CBB7BB50D2176367DD051FBAE33BCB10BB004E3FF611D5024C18C1BB18ADA61C49189760D7E4A2AF0C14CC4C6DB7AEC7A06BF043B44412EC4A9CBC9EFEF344D8E7A9A97932002C8C6B9E53BB54A7069D0D1804B316FDEFBECFE9390BF082AE20DC0C1D778C7B144FD4AF1302BF0C36A8D6067DC9EC000A32D0ECF8015E83F9307F5CBAB1FB5ED147A5312D0A4AC17B3B21092B652AD83C3DD882FBF85337AED90CEEB8BBA380D6C2F311949738E2A38AAF054AC40CCD5CA6F5BE81126FD520432D7CAE02AC3DE2FB5591A09F9A20D369F5C05A035531AE7B1DA195001C58C452F6784055081EE1A632496796E550AA70E8099D7418DDA6F4F1C5D37A4E8C72D4098B0A8E2C7D9E7793C7E4CF20315E83322D6AD11642F7A50821D2EAF1D82673C4C095203DCB69AFA42C6136D33DD85113115B2C670F43708ED515A3E124C407CAABEB943D5523B59EDE9119213D66DF1A05A0E476CCD924A875B54B6DCF4452E72E462AC2494531A2E6B50A5DDD92C46F9107A09712FF2612098D2E9B09762C0A5B3BA5546EB35760A80389B02632019BC8AA'
    # list1 = 'EADEFC92220EB5112539CCB81D66B5E52A2B15C9F4FE133EFAAB9FC695CC6B6D737D08D0B641E791BE725880C66FC39EE4E4C222A85907CF70978618787A356180F62BF0F73727BB6D7683242DED65261B279646BBB11BFF346A45C9B981F25293F67D535BEB5539CBB9320F9A9CA2935C44EF8862B659B6505FA96DDD8900672AA033174F753DF7BEA2423090A85A3648FF8480EDE92AF3907C88A0AB81517F2D9EFE7820A376C6C41EA10D369253C88EBDA8BB47C94927F9F8E28597C809B4AE12DFCCF0A58C6FD6AD704E804AB7E68FCD151AE5E80C8B6106758107DA7CB5EB8411D4BD175FDC1F4D728B185C9A9BBF6A22E78971304ADFA9CA15CD7DCE4ACE0CD52FC29470B244BF78E92A3D87E8BDA587284E135C2BD8643476D7DCFC8D4049B976FC5FD69B22591E0A26B9FCC0B378C462452C56549950BFCAD7A9B9AE88F94A029A5AD8B406ED4F65261A03BF983E9BAF503541BC1C4D31C8EB410FE456B82390C3001CB565FA5576E6537B70518D985A63AC8A8114CB9F10564036A626DA8A134063A1A552960EE68A1436F149B130B831E9EFDC00F9CDB2AD62F546B976F50162D847E71D934E6AD3ED36A63E646CECEBC51C491D5BFBE6A30BED1E3550C2A1FDCFAE0D51C663EA66EFFE24AC3C855652C88A3B43C5AD1E5F51C97880E9651F5D06C7DE0A8D3E61958E53178266A990BD3859DD331905957BA55523B05D25BB0708781859203F9489D6308F462F045A9EB1951934ADAA9C4F6846D996B9FDD425A78151C3E8A4367689E1FA3F6D4BA68624C9F745992B9F92CF38DB080EBB0D64D5EEDB8EEC39DAD90FDF6F17F3C3B6A01189818550CD9A4301E4C5BE84375485670052F11E1FD1807779BBF02DAB904197CAC3A2AAC456E3163E28791101515BDA4A652DF2782D8A6ADEC8C5E24EEF9672A8167EBE626CCAF1506BACB0FDF87AA3F44393EAACD86ADF56878260A4B045E592F4EE355E4D28AA4A2D57DFDC2618C7034E7E26C03FAA700AA7CD709BD0D9FD6C1926630642926E895A76940F3BB14E07D7FB3ABD89EEDECB33C39728ED17C969A18ED6EAD75B9D33935FFD79082DBF94A8198033CCEE5831F496A9C4AB25DA8377466AC2683A6FE485A8CC9BDD6BA7CE6E248351D70C56A6E9591A296CF48A828CE8E6773C18250E1237A365AA816E3FB347F879712C1F8265E008AEFD4BE8D2EA6185AD243B9628A5411F6D3B31CD2D07ED788254FF41F4757D0AEBD0E9230E07F3A192A820B677054A072286B50B6337D155A410C64183D0CF34CF41F5102FBC294CCF41728CFE5C9E17AA9ABD131700E4C7CE9A804B023716A555E3397463EFB9FB992AB7628FB094254450CCCBA04042617428F737592B80407990B2DA5A2EDAB05568F6156855ECDC8C9B1AD425E0BEEB41791C3414BCEC6B0AFC119A0D9851F1AFC94E21F9DA72BE9774569C998CBCD9A9BB5049A8B69DE93E550488E8A209626F5E10CC357704070318D50E44DC1A28F8A8AFC1F04C91B11C3C0F4D3B117674773482F2C29E7DD3378AC08EE743F7E8B563B05C56659A5F8D592B70E327C3645C5794FEF85D7B983372F00E6F4ED4D9860D4FB899AAA9F0D0646FE06FBAE69D4F1046DE325BB0C062F5012A86FE7679B965DB691B9BC50B3857C9A7AEF81EA0DBE20CE0E7351931D518A864CDA2EA28E01294502429B5BAD7D54579325DEBDB37F144F27D91D8CA866EE22E3AEC2DC3A88EED546DB8BAA3D1156BDFA9B18599C0B0C77CBE1F11C38E62D21BE08E9BBE41817C90DFD3338AC6ED41340F7BEA9DD97F7F1034DB37A26A92E49774D0633D1A4C74E9138983A8B79EA6BDD6763C6864BBD42142EB900779642623D7A57A7E5D6A73E2B6478F2A798DCB6509FBCBA3E8009FACAC2F788713772D0365B6A30D431649EC8E3C2C578941929BC662243446463F7481D71D22FF11DC9F37F0D0F7113E2AC6FAAF5A02034942C1E891419EAE171798103806BFE27D4B411C624FED811B07301D0A086A261039AE7C22608BB6C166CC713CFC4EB4111036E66C0B91B685D526A18ED8A215D722DCEF724A1F6A51FB7C35473FE45C4FF297EA2C5125119F617D078C417E584F0527E48558CF5BE32F52C03FA9B2C8B537BB1597E733A609C28F47A9CC0EA09BEC0F7DEBBC7D80E8E60AB1498B87A058A7E0CE2FBCF5D8D13BC012A433F09101319341EA4DA332A2C1E4BCD02848BF05B66CE88D1FCD0CE8D9C69469E66D1624EE38AC82A3C47866F7EF8B6D6A2BA115CBDC6C15E7265B4A29832E55996783069E0BBFC74A0DB064BEA9E532E86F33B9B6424D4EEB2EED86AF783B8BABE296607CB089BAE4E9F7FD084394FFB8C337090BD0316377B4455918EE43C126837C40721B3C21A06B10109B91268A5F4B59384F3BA92C738C9AFA98A35D6BBEB7F73770E6CB34820ABA3E11D913E539061C33CD1CBE6A29976E8562FB69B9BFB1DC122943A4A069CFFA4A9B38CBB3E6A7E9B6E3D892CC2BF1C771A350F3C88277A8FF7D4D2B2378707F27B31A9540BA92A6693CFC6919FDFEF37854B99A8C021BCCEBFE54F83BDE10776AEFCFCB4BFA665D96C34EC2903D70A3291EF89138091250EEE554CD58FA91E230C8E80194551CE32193E4AF0E700357C5E7ED812471E0CECEC9A1B58B99907984A70BA2C159ED68E651B83665CA3D43AB70B6B89415F3C2F2AF93835603C5E78B0BAEF0B119B9F216D8782DB1C2C0B2ABC11331DEE477442C7177A8B5FEE7536CB6BFD1656BB09004148CF6E51F364D5A4B3CF7DDE98A2F542B64D103D6DB90331866147354564170A72C746FA23BE9FE4F30E70E43FDAAF038041A5C7B657E98883EBD98F8F760310EED44951F7827B94A668353DDCA91A80B7E4C3CE2E012AAB8055FA4F4D72E5DE09EA623F8B584AD3A754E04A5C3B33C659928AAEC0B46417B36CE10683EC77ADD2406DCA87CBFBF3759C2793E17DE23E8CE4C2E56787B04543270C529270A476B9318D06D3CC1E46DB5801682196F8CA11F9535095042DD59D5A9D2896561052AA1E9843FDF09B1D408AF83AEED33D2C9F5AEFBCD4348A0688D5FE08ECDAF22A8D9E773C9C742BCD6699675B52A7A233D9A59A65FD18D525440A1FE191C7F930FA3A17E0F1A08386F3F384258E02881458297B64A1766948A1B20741492D3F86AF9E64A9F13A2258BAF968F931CA965646C45351427708F905F183ADC36F9D51EAF7CDD586991B629B0E6377A24640B64738D2BD37DE2B68CF1B46DB21414C85206251CE49385C1CB445BDC7EEC59131B59B25D65404101D6FED1C1E8C26BD98F195C9FCD5C057D3880DD00405CC082CD6BE2C9EBFB77A18D01AFEAE31049F985BF644D778F004C56C48F1F942B4503E63CE564F6C207892E30F8F71C78558A3A9D09D1B1749BC44F69CA0E0E8D354B46282248F4C896934D317EF25CD0C7E06890FC86CCA2D1C0D8FBDF200EFA91A15223BC885CA3EEF9286FFE04D9413993F15176A1A34E785D534F3166FED41A94B1DF67D28990F35B6E26FC44992D8F2B3F5CA9E0566714C1402BEDC8DAA573714690B6310F2A3FA3E327EF99CFFE7478FC6986E728179387881DC7964997EC1369BE2965334430F2A3550FE2350A00193D16EE8F9C971BFDCED90552CFBC9293B271B8F27274126E8A975117C23EB33C3BE4ED59229C075AFA4AF1114C3B75583F9E6FEF77CEFB2CA3B3AF399D1B71E469E687CB5B4554E1CC6742FE431E19B83F31B583FD36943F645D3D1BFB0B273073A179A387CB44C557FA0E4D6B2297E5AF69B6AF17E1B7797510328B662400B3B91B28E718C5C7A356D54835469A02F63F240FEA08509D19F2C7B2AD17B13B9650AD8DB0DDC959628AACF8462E8A88C78AA7E3D9ED5EAF68B7EE7B279B48BF3D1A3C615A0A3A630909A60BEC0EACDE584570380B33F51DEB8D4F1CD7204A827F99A9ABC559877F3AA53A7832E8BA5B3AECFC13699DF25CF487F91A04041B8B39F02ACC196ED7E4C3D9259C0477C7174B74356F5AF5989179EB72C800D5C93303602D0C289860EF59383976C15AD386D402ECB0BB2F9F40F7A115C736E0E4980366970E3060C2F3BF2AE3AB3B0480881211D951F7E59F508C70B2F78D66F3A1007790A2A19CC7F456E7F969A933950496CB1C169A6924E0BA16314A96DC9EE0417F22EDCF09905F4D22E22AD14822907980FCF90C5173F5E8A40CE0B5CA028C3346923DF3EA9F8A83255DAB1ED90346D37B4F0BC28DB02A3BA6387436497EDC960ED169EF36F66DD5D2D4E40F5918707414A62BB24DAFB24136EFB66ABEEFBE15903F4A6A355166ED0E051708CD64A446966DEBE308945807F0814149B159D6146BC84C5A7F32EEB731CECB09AE9E97D39D8DB45521AFCE7AD665BCC39626DE6BDC53BEBE23151495C9EDC7DAAF5712C8CEA71A48D86F8FFFA5B742A51E9DB4C3A826E6A6D82A6AC0419B782477FBBBEA7D30725802D4C10A32F6A7E6B662BBD02D41FAE3A03DF0E73266DFB9FE9F3BECBE073809AAC0655B180808D197931F5FAD9EDA9649D6100BF03E714282BEFF0ADB88165618BC654D57B3600C3C7C4CD737521D8AF7763E1D32FBB263B6FC88EC993B5B7098E7BA5D9D094C23516DBB7B7DC3BCC2407581929C261AFFEAD26EA348D227551B25E4B4A2B45F8600DBB720AFF5E4479659867B7705CA61F04680A5A964AD33DC83705316AF553DF693FE6B60DEF56AE608EAA24EF669D11DCCE617773BA6B22C2E8958452886C6DEA1EAC72AA30CB6E81486719D038D2B59C87FA8F1CE14FC467A714E66912CD076963A6BF96297CA37D769243BAF6DAFB9E4DE3C7A900959B2A3ED919F3ECD163E9A4E1378DD092A3729B3BE85E3882A1CAAC71CF04660A4A46E6DCCC80EE49B1B493B2BC9D185E434E7016640B32DCF6A1FEF81678BBF6A448163DEB0975D5F834DF67D703DFA4A6679C2B0DC62EAA37CDE1C93CCBD125583EACFAEDCC38858FBBFEB7174D6D369BEAA69C2E6932C1030F3B93382DA4199CE5F7E38A9E488F19322C29E9CE0AE383061D5B50CB8985011DEC39EC8E425EC267A7E8E1462DB701B5478F6D58414F73076F5F630345E28D4F13BABD0D47BBC32FA0B7B080C00AB6D1C09DCA6BB2949C8B571BCE0445665176DDF02CD62A2C2C42B80DF640B077824145D3AAA571DD3B24526B5136D2EB87C70F124E5021DA110590031B6DCA9058E9C4380F3DD8EB800A2223AC906DF5F952C1900FF97DAD2757950E1DE4D68F301E8F699DA242C8E80FCFCFEEE2D7E5451A6B1ADEF4D10F12384F0EE27F14B9D73CE9FB6404E3CE6F7CE33D1A8C6E8DBE86137D331B7FC1B7F960E0CD86D2A2704978CDDFFB3473FFF313BE02CA28AF740E72FCC83F94DAE07C4CE0DCA6BA50A5A6291A0D8D90FA16391A3D1A486983EEA6764A3E460A9152E483C953184E46BDBF2D49C2F0EB7DC4C186A1C498B3840521D802C3E4FF037E9DB78E537A584B18F4CEB8CDFB566E8AA11498997906E78635093C0DDC9CCD07CF6B0024C252B9927D202E0AA97FE131655E53186BBF9AB673A0AF012943AB338515E78E8EBC4885469872BBA5CE3CAE52799950E42D61A93CD2BA5F5F32AD7E03B6F00D0552D20C07C2233323EA1BA07B1D13C1F53E55FF13D52A758082B69D88C7FA33F4144DCEA9881927DA27DA96AF453799C393EC720EB130E943ABB5334FF0EDCD241E6769428BD64C12C42831D7D62C70090DB02F7F4627786E5EE4C30E69592937460FC0360CD0506CADB066AA7728CB6816D418A90BC0C1D6AF45A8622E317C7B2DE07BA07BD9E39EAF79909AE9DE4F82872A6A9804A779FC3AAEC56DA1538DA314BB668F5F2F19F6587B1E7A5FEAB1506D4714802E7E3F0E056E4264039B65F6A299185E2716350C33CC474B2745AF47DFA4C1CAFB289014918CDF2DDFE3724909BE895CC15841D0D68536F1FE7A17B60CF6EE68BCF5C58D32EA9E60A6DF2E5DC635FD98F43A6E4965F71954A7DE1BB1C704168DE79AE447E5E297CBBA6A9495E9811621558726F5B62C85B9A95BFCB9F871B38B355B70DDEE5BC32E8281BB18B6F622BEDEAB421D035521F070656F9566BBC834C46E1C424B4A9E677BDD6FA9177112734CA927DF113F9793E7053EDC3430FE55BF96BB0456AE0ED5CAC7D3D236AAAA03A4DF579ABEDC382F8876CA15C74FD3E04454D66FC0DD2F873D685EB032EA5FE69D54DB04B596E0C24FB4E1F86026FB6F9AF19E9E0944DFBFDC64018985ECBC3D37BA20ADB67069BA87EDCEDB36100B6BC353C79343401C7B7085AB228B1577812F6249B31061060D638D7BABA7795D49F3E1AE1BC6BE2F8284D97B52E856EEC972583BB03C6782C07952AD8750744881220F660FA9F2D43D3006E9CB2A8359AD4E4B321C1FB767733FC981BD99929FBDBF537EBA9FC243266A9312DF6FE80060939B3A6DECD6D8903E36DC11E893D34B6F3EBD657FFDBA2225E1BED2F03A250168FFCEB1BBCAE756782F25DDAAF237CB202C5685D704CCF6CDAC51DA1BEEC07E1053F58D28C40E64EE0064B134D17391C9DCD2DEB6128F615A72EF2CFA2DE345768EC510A807F987648E05B98B8A460032D71D6A445E31A1D64A32FABC6C24C1303CFE057DEE8C1FAD184D7846114083097F4D93C3F15B6A39D094199E4B73299C1E85DA2A32E0D28C4AE6512F078BE4E238B58B9FF3395BD78248228CA1CD5EB610D21F318D15E917C56658E23BAC8C527E9A3C4BAF7FC477E436BB283EB904C9D2570A805BA1715FC4A4A641E8FD1FFFB31F2E56BE00A93793432EBC9C9B2F01EE9A291CBDA31EE98A16D87ABD9389011CBE390C1FA4AE734CDD8243D8E13C05B9B78224FF22EEE65391FD231C74262EF2E796E99D902021622754AA5E4328206CE54CBF5DAFB95BA32AD3734B0D87895B2B888154EFC4D01291EF8AC1D69CCDF59BE911663674526BCEB0B78E1C97521E6617FB1937AB65B51E5DE790959222B34D22C4B8FE9AE6EA166826F6105CC7BBA47C7359783BC54AF12A5663928C3E7F00C4207291F00DF86A0DCE6C01B74F52871EA51333B0D127CF060A7D5712100152A46B5285130AD111CACC1A1CFF3E8F9C5D46220AD9D224F70127D6F779959A5B0F278A4A7B6F786412192C28682904E7B1ACAA3E47B175A9C09AA05C257A5B91D1F75E86A0DA6683D82FACB19939778E6CDFAE17F03EEDA4A35A44D62554B0094FFE246599491099377D5BF31587D8EF8AE66EFF15805268CD5AAB9DCE87F871C99815E08048534D8EBB6AD7AFC5688AA5235F2CC66B6B28FD9CEB87589FBC1C25F0E6FAE9EB9FB38F0ABD2CB890065278A091D1F65D36A8C71BAE77DE8C67264E7E47A440ACAEEFE875B8D7B71EB44BB7BCB231CD2828C39613F922A0CF2F352DE31E033A4008FA3AA22ABCC47A72BF7F7AB7AC2053424438A8ADD6FCA4BF34527AEDF628A1AD312EC0B366F5D49EF828E4A9BA9CDE242C49E7BCBFF57CD8F09BB36E36E23A46E4A2ADE572A9454236BA79B8D428767A11824AB7149C37BABE1BABE21F2A76EB42A6C475975EDB9F37439250D9E25348A9E25F1EB9E960D4E1AF2033F00A12172274D5237D145CB422497EEBF22247640E12CF9B2ECD39ED140379A8120BE1D3CAB5E63B25406ED9CDE5E0E576EA17EFB0A9E400F0782D9C447ADD9FD017936B8D1C71AB9082438464354A9FEF77AD937D736CC4006BFF18274A0121DE49E3670F42ACF02DBB57E7518780C35E60BF7FC1C7F810F51052ACB1462E30B4636527720279F8FB44895A419DB9D577AEDBA2A3655B9B3E802A7136459086377AC12572667960B9F7B5640BD5D993B60B56B7A1B7B05BA7EB83401BBC13D1DDF1EDD93B4A0F001E8C17D4EC82932F4EF97F2CECD2ACC903FAD9D37CBABB54D1602DF618139392BE047522AED0724EE16798235493D9C5A57AB10F174FE139AA86EF0201773B8EFF1D30FA93B83FC26107461078CEDA700D537676A4B56A18781ED7AF6B6D840B4AAAB4F7C1709A3797E7AF6E76976FC32062B070BA79F740532A01892A3B477849F08B619FAA55A8D92E1F8F341C228A01D41623494B6E7D6FFCF328A907B07AFB4B3E3A44391CD834E24D28863A5D63422A153DDFC3059CB8C1488E6222B0228F6884881CAB66CE3B6EB9691EA60FAF8795E15F2E4C38512DE2FD289C4D1C9C4D45846CA50ECB3D73685189CBE93AA1937311CD55F256E9F0C32418A21F4A1C98FE11F4FAA4466A106BE4AAB0373510EF66AF37AC6D3AC9B98F8528A1D6DCEC3C042DBE3CD0FF3636881532E884FE7642DBFF82D039E31303E034252BEEF9FAEFA27658258ED7FB77B400CACBAE992DF8632AC6D40684597C8BC78FC2F36065C302C2B35441E45836D0814FA9568144D91AC6FF443349054D73D25FF009A316301F88524924D4CDB1612730E5376057EA87E7D62D0D353474EAF0BA27D5DE97320A98396367BBE79976F2F81863FED71E4A06CC4D4CAC68942E6CC62A9C68E314BAE06CEA60AA8544B03719FFF9E4D506C17EA3A1735E78C8EE6FEF767830DEDEF57EAAFF9FB36808D808C2BCC29A7331C0B6EC7640CA348192E379E702FD036DDE5503769142E0743CF1A48BF8542FA02520FB45983558BC35721CDCAB097F9945127AD40EB578377BBECE0D8B2B3CD622B9B75AF57DA7DCCE9035FF5239D4B58188EB3A74D0047E1E5A1B61C90EDD7A56C45419B91A40552F7FB2BB469661B0DCD3EE6E5D5E2124BE787A77B2B8DA2E31E61896AB62A6E144001176E7C3D9031998165E16E6F0FA6F68753551DC125839C6F60D9E8A2619F617306A31C6C2E58D4C23065C6AE0FEFEC445EE25B32E4E1B706C92527B6EECCD924BABF996C167D26EE44844184AD21F514F40D589E716170F0945E8E50AC57C29A207983ABBB979BB68E5EF156ADC33A3C01D4537D03099727FC17B85BA0C642D99D58F28F2966647DAFC30A29C8D675383969730B45CCD8B94C4B597B3C2FE5442A7446A6DB9ED233BEC0F969839FDA45635E70AA4201E27DD3A2088B7A3CE10956B676C45615FEC4EA36730FA49919494AAD5795AAFDBF86D53981955BAC2F5DA7C2D78875DC1A56CA962B783664EA7983F1C892C89062924784D5CD25889AEFDD58D15D78C197A9C088682B3934F6EF9EB25002C2F1F5F95EB28D65262103C627F0466A6529CF0C40322D1CD6A8BF26AC806AE432D5B8BBC6EE3B204A766BB30D9C671848B2BD89EE88A4EDB8CEA518D1DECCE6DEC9C7724BF0FDDC3864C728B79101BD602FA70AE87986864570DB15B65EBAF8059BDDBF7E4BA2AEFA154DC593AD2D232323A6A3D355C1C9B8D742946E3122F1EFA1A0C1BA2AB1890AE3BCE02BCE9B9F4A03960FB5D7B2FF9321280AE7DAAAA33ED4E43080367269F2DBD3D951FE518D50EF5E0AEE31CCBFE3D32EA66405C8930392EA3D7BA980F389EF4F123B1848E16CCE36DCA5202FC1D9C7CC6860AA6DB52B36A02F697DAD3065955DB1D5B225237CD10ECA560A3D83E0B5F4C8BC092FAF946FB540B6C6DC9AFE68B76ADF16EC41D5DECAFD349C97FD980C9BC47A8D5F89D9338BA356431D369F5D3D4651324C5B51B4EC01C9B75C1D6C74D6F9D9356FD1685419507832B0EE1F578368443B2638646991842CA84331BF5E028179018EC1785B6372EFD1D2C96E3C91954ECAEA7C584AC45E5E3CA96857D26169A14D5A25690C260D93A144DE8165CFEC117AEC5F5C841870D4531F4990135BA52BD99133E072356C5A4ECD4740CB3E58C3DD8E123284108E495A0346A336F68042B3173B04064F3061087F0745A1EFDC4D5EAA54A08E3E0DAD811ED335C99D06D24765B00BBFE412E8046526DE9D594851EF4E2B1C7A97A9AAF74F237CFB853C9D8330C3590D5B0270B2DAE2B5F7EC66F1B18FAB1052DD2CA6C0D6546F454BDBBC43BD1BD89EBE69B85DF6E18B8A7FBC6F0250A9D1A8ADAF8D47D8DACB5356A9A96D279B64BA49C4840E41975EB7BEDCD0BC03E292F49E75066F4E0744A9F7BBF30318FCAF57C3FAC0755BA470E834ED98A3D52F137617F3E0AE237C4A4E9E9D7157CEF48A7C392F10F28ACF8063ACC9CCC5F2208CBEE66AEF3DAD615F763354A3EA9CF8C99F86DFB781A5FD6154DF00B15B8746665EFB6BBAE68149C876EB3C863EE9EC0BFDDC4CD2E2B7839C8DB4EA5DDF2577981DB4AAE54182850E6CBC36C89BD44B0857CA1689E19FB06784A4F62BF6B7AA2849818294164ED3ECF32BD279696559FEA2969FAA2BA94E1226D028CE2A85DFA3E1614A51652664E932194B48BB0A8086C84F99737AD5B4BC78DCDF4A9288E84F9B45AFED3CC793F2C2AACD6CF12ADE600BC7570FC73866843D39BBA5B1DE937A085189B16971EBCCBA08F462408E7CDA473FEDDF53DAC995BC3F2675B4D6F3AE4B2D423CF2B6B3204EBF3A184BDEAEFD8BB2A408EF0F8ACA52777BBD5D053550BADA214D169FBE3A63BD83C877CEAF9F2437AD91536291178A48FBE870F0A845127CE3FC93FE4A547074643A83DB9F96CC0D6E1D2717C627D6A1A8A8BBA73E2EC26BB7D6186DDE97CB0AC5404AF17A7287915727F3889B0BF671577C45A33F4DE7A8D9002EB3D3E6C2A0DAF1F994AF26F75BBCDF4E0539F61A25AE59F7C72FDF46CBA87F2327B8F9E3A03813BB9B547B6A08A85EDCBD720D8ED54D4F4AE5363FA3888D705E7DE55AA6DC175DDF1B4E69F84D7D8CF16DBBA5F192F996B9AA93CBCB45C9C5186787B59E2CA9111F90A87E4ED0A45CAA03CBC3AEBF401298A71720390D0D90A6E90E4C71D9A7E20960C89D8CF0FA8203E07D04212CA95E222B861EB4377D74695B881E4647870700E4E40DEFA0DD2D39FCCFC41AE937A5EB13D2D5192CCE855A5AD3EABAA13566921BBDF1D3EC2B261DC8D8E9E736304AA5E05D42C196DAC8C43B04324150A73D9CA5DD7DF335A10B5F6DD912C991F9ACA6C90ECE4AFFA6C34C286D5426366F7C4AB99045663F7C81D8BDC3F51246EB22313E85DF4EBF4F61043E43A734FD863A61D6FB2962101DB45BEB79C1FC1CB2313B4557998F9AF535DE82A767B954A46200F7AEB8A3182EA6B2B21D290630388FA14168C1B2C4DE065C79CA09BBC51288B0FAC8D52E1B11C0BB49C938F6E5DFE7420EDE3015D720FF25537428AC63E5D4BC8F28ACE752E4C060B6A79C8042ECC6620918FF30626ACD1AD09CB4E91E99434638357B88B847F8EFF84E9667DCA4A4EAF867C63F2A34160BCB200215AE50A77E4BE670093B7223B113056EFEBEAF2F4376D10B62A43342B9F868F93DA27229D1544D30368C20D4103F179E5A0150CED5431E49CD5825DCFA4E66A05CBE8DB3007776CD58AC7D12826E0832CB49509483B65AD732F90B5561CAE0FF599095D9DD7DE1EC1D7E9F9FBA046179FC982F5CF5D6610379FCAEFA056AEF14258B4F73ED760F6AE8CAFB4E56966D8072B8EC1935952F6ABA8A07649C8EB4D805344CE3B00F291177B66826B91FF44F0175182A84D00D5A0DB18A0AA577CDA5A5DEF37CC96CA121DB7AD532C918E43707D5DCB07F3B5CD8B5D3C59FA874838719D55ED5D9664EFD987105ABEA58EC466FB3B7DD5B53DF0AAE0BAE3AE76D05940A8E7B3D3B59615400ACB11A147D5B6C12B29D6A516DBB4E0A25864F21ED1C25BA59EA8120FDC86D1AEA477E0994A3DF9992F806CFAF07462D3AC9E1E62CD92968955D5342F6405B8CA980DF7FF5CB7BFCB954798657B8C8B31C526B8489C2CF1E8308DEE744522DCCD3B6E2331AAA80614BF682CD8FC4C86872FC980B10BF834CA7C58CA08CF21652C124E9E74CD3589C07D2710FF89E96473CFBD87C8A65EAD4B53158DD6FE9B2AE926343DFC8B0F6BC0AAB433599BB832A04842B0AFDFFAE35D9D5AA31545162AE415BCD85DD416CEA8466F9878BC6112814C83C03DC5C2967E9EDA79B470D1D72C39327B3BDB4ACA24C1766417650D9E4AA293C1AC38393CFCCCA5E071182780584B0169E0344FEF01A3D3AE7911D462142150626B08D851D4B579B8048FFD9345739A49B4807BE66485B54A9B8A5042E71E8771A9BC8185F39729E99E18C62C9BD7AEA722055246285268C94F0965CD1A70C309064C1E1AD2BE64A3B2F9CA4610A45DDCB41417A7A56D3ABDB435EFA538E226989BE186971C98131394361B787EC952E0518E6E690FA2A9FDE31959185C8E23BCE8229E57193DA12E828CFCF5583D661F207FE81CB0F40226AC8F014FAF0EA01AD025841D767E2F2DB0BBEBA5475688CC59EC519B533A90C2D519432A2AD4C04F2255228D0985EAE47F5AE05E5C8F3FD1DEDCFB01D57408AF24D63917D9F66EA9D7C05B1D2BAF5AF2A33753F654D1F29B3697283EFE710CCC0C5DD79DFEB95F8F7B3B23F0F021A676E9A4B8048EFDEFC16CCD6CE39D3F783DD5B1242755B7F2445065AD7EF9F9BF611954CBD69AEC234245994FA16DAAD4AD2425C9627D680758F7C95C598898E95226F30D1F0833A273E38D200238E79B35949EB53DE9ED4C3569DB5FCDCA42CE11AA8B71AE7DBED65A361B79BA15455D525A0A32960350E6CF8ED6537093C86FA03E6334EEB0CC328541F2F4C1EAC807B3D9DAFA3D6C2D91074158BFC87F97F699026EF2D76CE453B3A9210DAE041CE32337D5D3A91EDE22859A81B910640B9F1BABA3B843A51ACA56F36BA5EC4D1460887D24484E6E683313145E996AC1D09A02D547557F261411214EF3FF51CF3D6A67E0B085524A942B9BE13D6D9CB0935BD6100A278607854EDEFA4E2BB9EF64F827B313EE366656745C3DA858B2B57647CD9EAAFA59D4B8EEEF835B055C94F9099141B4134980A56B70E47AEFA6930B16D11FA23E9B97FF8FA344796B49A5360DE659FB882973150645D14A15F8A16BA1403A096DCD85DE70DA880558178AACC52CE11082B67605A695D21DEC1DF16DD0E82805C965EED2FBF1B817E4627A2DDE9C9BD663F9445B80B1BC7A9F6DE6D2AFD1071AEAD3CCA85BF0F99285BCD89DACA8143B2B59E34BF0F8B9BBB76E649AECE2D1D75458F71D54B17299793975C5C7700A3BAEA4933288338BDC43316653B6A3C275F47419E9C73F599EC0E0DA720D7DA95A143252CB7CBCC9F1C80E8199B90A4711B412C214CC9A58259A4009BCC4BA0D4F86F8BC4AF273393443DBA743BE18B004979'
    list = str.lower(list1)


    # pc = PrpCrypt('sycmsycmsycmsycm')  # 初始化密钥
    # d = pc.decrypt(list)  # 解密
    # print(d)


    return render(request, 'test.html', {'data': json.dumps(list)})



@csrf_exempt
def parsingData(request):

    form3 = UploadFileForm3()
    return render(request, 'test.html', {'form': form3})


@csrf_exempt
def showpage(request):

    form = UploadFileForm()
    form2 = UploadFileForm2()
    form4 = UploadFileForm4()
    form5 = UploadFileForm5()
    return render(request, 'index.html', {'form': form , 'form2': form2, 'form4': form4 , 'form5': form5})


@csrf_exempt
def excel_expoet(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            storagefile=Storagefilelocal()
            storagefile.excelfile=form.cleaned_data['file']
            (filepath, tempfilename) = os.path.split(storagefile.excelfile.path)
            (shotname, extension) = os.path.splitext(tempfilename)
            print(shotname, extension)
            if IdentifyFileExist(storagefile.excelfile.path):
                return HttpResponse("文件已经上传完毕！请检查", content_type="application/json")
            try:
                storagefile.save()
            except Exception as err:
                return HttpResponse(err, content_type="application/json")
            msg = handle_uploaded_file(storagefile.excelfile, shotname)
            return HttpResponse(msg, content_type="application/json")
        else:
            return HttpResponse("表单有问题", content_type="application/json")

    else:
        form = UploadFileForm()

    return render(request, 'index.html')

@csrf_exempt
def getExcel_comexpoet(request):
    if request.method == 'POST':
        form = UploadFileForm5(request.POST, request.FILES)
        print(request.POST, request.FILES)
        if form.is_valid():
            storagefile=Storagefilelocal()
            storagefile.excelfile=form.cleaned_data['file1']
            (filepath, tempfilename) = os.path.split(storagefile.excelfile.path)
            (shotname, extension) = os.path.splitext(tempfilename)
            # fileobj = storagefile.objects.filter(storagefile=)

            if IdentifyFileExist(storagefile.excelfile.path):
                return HttpResponse("文件已经上传完毕！请检查", content_type="application/json")
            try:
                storagefile.save()
            except Exception as err:
                return HttpResponse(err, content_type="application/json")
            msg = handle_uploaded_file(storagefile.excelfile, '竞品数据')
            # msg='ok'
            return HttpResponse(msg, content_type="application/json")
        else:
            return HttpResponse("表单有问题", content_type="application/json")

    else:
        form = UploadFileForm()

    return render(request, 'index.html')


@csrf_exempt
def getExcel_mingexpoet(request):
    if request.method == 'POST':
        form = UploadFileForm4(request.POST, request.FILES)
        print(request.POST, request.FILES)
        if form.is_valid():
            storagefile=Storagefilelocal()
            storagefile.excelfile=form.cleaned_data['file1']
            (filepath, tempfilename) = os.path.split(storagefile.excelfile.path)
            (shotname, extension) = os.path.splitext(tempfilename)
            # fileobj = storagefile.objects.filter(storagefile=)

            if IdentifyFileExist(storagefile.excelfile.path):
                return HttpResponse("文件已经上传完毕！请检查", content_type="application/json")
            try:
                storagefile.save()
            except Exception as err:
                return HttpResponse(err, content_type="application/json")
            msg = handle_uploaded_file(storagefile.excelfile, '阿明数据')
            # msg='ok'
            return HttpResponse(msg, content_type="application/json")
        else:
            return HttpResponse("表单有问题", content_type="application/json")

    else:
        form = UploadFileForm()

    return render(request, 'index.html')


@csrf_exempt
def getExcel_keyWords(request):
    print('走着了')
    if request.method == 'POST':
        form = UploadFileForm2(request.POST, request.FILES)
        print(request.POST, request.FILES)
        if form.is_valid():
            storagefile=Storagefilelocal()
            storagefile.excelfile=form.cleaned_data['file1']
            (filepath, tempfilename) = os.path.split(storagefile.excelfile.path)
            (shotname, extension) = os.path.splitext(tempfilename)
            # fileobj = storagefile.objects.filter(storagefile=)

            if IdentifyFileExist(storagefile.excelfile.path):
                return HttpResponse("文件已经上传完毕！请检查", content_type="application/json")
            try:
                storagefile.save()
            except Exception as err:
                return HttpResponse(err, content_type="application/json")
            msg = handle_uploaded_file(storagefile.excelfile, '直通车关键词')
            # msg='ok'
            return HttpResponse(msg, content_type="application/json")
        else:
            return HttpResponse("表单有问题", content_type="application/json")

    else:
        form = UploadFileForm()

    return render(request, 'index.html')


def IdentifyFileExist(fileName):
    (filepath, tempfilename) = os.path.split(fileName);
    (shotname, extension) = os.path.splitext(tempfilename);
    newfilepath = filepath + "/"+"excelUpFile"+"/"+shotname+extension
    print("检查文件："+newfilepath)
    if os.path.exists(newfilepath):
        return True
    else:
        return False




def handle_uploaded_file(f, rootFile):
    print('开始解析Excel')



    if rootFile =="阿明数据" or rootFile =="竞品数据" or rootFile=="直通车关键词":
        try:
            csy_reader = csv.reader(open(f.path, encoding='utf-8'))
        except Exception as err:
            os.remove(f.path)
            print(err)
        res = filter_cvs(csy_reader, f.path, rootFile)
        if res == 'ok':
            res = '上传成功'
        else:
            os.remove(f.path)
        return res
    else:
        try:
            data = xlrd.open_workbook(f.path)
        except Exception as err:
            os.remove(f.path)
            print(err)
        res = filter_excel(data, rootFile)
        if res == 'ok':
            res = '上传成功'
        else:
            os.remove(f.path)
        return res



def filter_cvs(cvs_reader, fpath, datatype):

    try:
        listFile = filter_cvs_sort(cvs_reader)
    except Exception as err:
        return err


    rander_reader = csv.reader(open(fpath, encoding='utf-8'))
    table_header = []
    for i, rows in enumerate(rander_reader):
        if i == 0:
            table_header = rows

            if datatype=='阿明数据':
                table_header[0] = '关键词'
            elif datatype=='直通车关键词':

                table_header[0] = '日期'
            else:
                table_header[0] = '商品标题'
            break
    print(table_header)
    resCom = compareHead(table_header, datatype)
    if not resCom['status'] == 'ok':
        return resCom['status']

    rander_reader1 = csv.reader(open(fpath, encoding='utf-8'))

    excel_list = []
    for j, rows in enumerate(rander_reader1):  # 也就是从Excel第二行开始，第一行表头不算
        if j == 0 :
            continue
        Tempdate = ''
        if rows:
            row_object = {}
            i = 0
            for node in rows:
                key = table_header[i]
                newkey = getkeyvalue(resCom['data'], key)
                row_object[newkey] = node  # 表头与数据对应
                i = i + 1
            excel_list.append(row_object)
    print(excel_list)
    outlist = []
    outlist = changeList(excel_list, datatype)
    if len(outlist)==0:
        errMsg = '本次上传数据为空---' + datatype
        return errMsg
    if datatype == '阿明数据':
        try:
            models.Mingdatalist.objects.bulk_create(outlist)
        except Exception as err:
            print(err)
    elif datatype == '直通车关键词':
        try:
            models.KeywordsPutonEffect.objects.bulk_create(outlist)
        except Exception as err:
            print(err)
    else:
        try:
            models.Competitiveproducts.objects.bulk_create(outlist)
        except Exception as err:
            print(err)

    return 'ok'


def filter_cvs_sort(cvs_reader):
    table_header = []
    for i, rows in enumerate(cvs_reader):
        if i == 1:
            table_header = rows
            break
    print(table_header)

    excel_list = []
    for j, rows in enumerate(cvs_reader):  # 也就是从Excel第二行开始，第一行表头不算
        if rows:
            row_object = {}
            i = 0
            for node in rows:
                key = table_header[i]
                row_object[key] = node  # 表头与数据对应
                i = i + 1
            excel_list.append(row_object)
    print(excel_list)
    return excel_list


def filter_excel(workbook, type,column_name=0):
    table = workbook.sheets()[0]
    table_header = table.row_values(0)
    resCom = compareHead(table_header, type)
    if not resCom['status'] == 'ok':
        return resCom['status']
    print(table_header)

    listFile = []

    if type=='直通车关键词':
        listFile = filter_excel_effect(workbook, fileName=type, resCom=resCom)
    elif type=='阿明数据':
        listFile = filter_excel_effect(workbook, fileName=type, resCom=resCom)
    elif type=='竞品数据':
        listFile = filter_excel_effect(workbook, fileName=type, resCom=resCom)
    else:
        listFile = filter_excel_sort(workbook, fileName=type, resCom=resCom)



    # print(listFile)

    outlist=[]
    outlist = changeList(listFile, type)
    if type=='直通车关键词':
        try:
            models.KeywordsPutonEffect.objects.bulk_create(outlist)
        except Exception as err:
            print(err)

    elif type == '阿明数据':
        try:
            models.Mingdatalist.objects.bulk_create(outlist)
        except Exception as err:
            print(err)
    elif type == '竞品数据':
        try:
            models.Competitiveproducts.objects.bulk_create(outlist)
        except Exception as err:
            print(err)
    else:
        try:
            models.KeywordsOperation.objects.bulk_create(outlist)
        except Exception as err:
            print(err)

    return 'Ok'




def filter_excel_effect(workbook, column_name=0, resCom=[], fileName=''):

    table = workbook.sheets()[0]  # 获得表格
    # print(table)
    total_rows = table.nrows  # 拿到总共行数
    columns = table.row_values(column_name)  # 某一行数据 ['姓名', '用户名', '联系方式', '密码']
    table_header = table.row_values(0)
    # print(columns)
    excel_list = []
    for one_row in range(1, total_rows):  # 也就是从Excel第二行开始，第一行表头不算
        row = table.row_values(one_row)
        if row:
            row_object = {}
            loc = []
            for i in range(0, len(columns)):
                # print(loc)
                # key = columns[i]
                key = getkeyvalue(resCom['data'], columns[i])
                # print(key)
                if fileName=='阿明数据' or fileName=='竞品数据'  or fileName=='直通车关键词':
                    row_object[key] = row[i]
                else:
                    if key == 'Date':
                        row_object[key] = changeKeyWordsTimeToDate(row[i])
                    else:
                        row_object[key] = row[i]
                        # print(row[i])
                  # 表头与数据对应

            excel_list.append(row_object)
    return excel_list


def filter_excel_sort(workbook, column_name=0, resCom=[], fileName=''):

    excel_lists = []

    for table in workbook.sheets():
        # table = workbook.sheets()[0]  # 获得表格
        total_rows = table.nrows  # 拿到总共行数
        columns = table.row_values(column_name)  # 某一行数据 ['姓名', '用户名', '联系方式', '密码']
        table_header = table.row_values(0)
        integrationList=integrationOfData(total_rows, fileName, table)
        excel_lists += integrationList


    sortedlist=sorted(excel_lists, key=lambda excel_lists: excel_lists[0])

    calculated=[]
    for item in sortedlist:
        changeNewKeyWordsList(item, totalList=sortedlist)


    # print(sortedlist,len(sortedlist))



    return excel_lists


def integrationOfData(data=0, fileName='', table=[]):
    newlist=[]
    for row_col in range(1, data):
        list1 = []
        row = table.row_values(row_col)
        list1.append(changeXlrdTimeToDate(row[0])) #日期
        list1.append(fileName) #计划名称
        list1.append(changeType(row[1]))#操作类型
        str1=row[2]
        tmp = str1.split('\"')
        putStr = tmp[1]
        keyWords = tmp[3]
        list1.append(putStr)#操作单元
        list1.append(keyWords)#关键词
        list1.append(putPriceType(row))#出价类型 默认：0   无线：1   移动：2  自定义：3
        list1.append(matchingType(tmp))#匹配类型 无：0   广泛 1   精确 2
        list1.append(getPrice(row)[0])#操作前价格
        list1.append(getPrice(row)[1])#操作后价格
        list1.append(row[-1])#操作人
        newlist.append(list1)
    return newlist


def getPrice(row):
    str1 = row[2]
    tmp = str1.split('\"')
    if row[1] == '删除关键词':
        return ['0', '0']
    elif row[1] == '添加关键词':
        li = ['0', '0']
        for i in range(len(tmp)):
            if '移动出价' in tmp[i]:
                li[0] = '0'
                li[1] = tmp[i+1]
            elif '自定义出价' in tmp[i]:
                li[0] = '0'
                li[1] = tmp[i+2]
        return li
    elif row[1] == '更新关键词' or row[1] == '更新关键词出价':
        l = ['0', '0']
        for i in range(len(tmp)):
            if '元更新为' in tmp[i]:
                if i == len(tmp)-1:
                    l[0] = '0'
                    l[1] = '0'
                else:
                    l[0] = tmp[i-1]
                    l[1] = tmp[i+1]
        return l
    else:
        return ['0', '0']



def matchingType(tmp):
    tmpstr=tmp[-1]

    if tmpstr=='精确':
        return '2'
    elif tmpstr=='广泛':
        return '1'
    else:
        return '0'


def changeType(type):

    if type=='更新关键词':
        return '1'
    elif type=='更新关键词出价':
        return '2'
    elif type=='添加关键词':
        return '3'
    elif type=='删除关键词':
        return '4'
    else:
        return '0'

def putPriceType(row):
    tmpstr=row[2]
    if row[1]=='删除关键词':
        return '0'
    elif row[1]=='添加关键词':
        if '移动出价' in tmpstr:
            return '2'
        elif '自定义出价' in tmpstr:
            return '3'
        else:
            return '0'
    elif row[1]=='更新关键词' or row[1]=='更新关键词出价':
        if '无线出价' in tmpstr:
            return '1'
        else:
            return '0'
    else:
        return '0'


def changeNewKeyWordsList(data=[],resCom=[], fileName='', totalList=[]):
    print(data)
    newList=[]
    beList=[]#距离上次操作 的数据
    afList=[]#距离下次操作 的数据
    currentList=[]
    be_date='0'#距离上次操作 的时间
    af_date='0'#距离下次操作 的时间

    # 找出当前计划内 操作过该推广单元 该关键字的数据 放进数组
    for tmpList in totalList:
        if tmpList[3]==data[3] and tmpList[4]==data[4]:
            newList.append(tmpList)

    tempitem = data.pop()

    #找出本次操作 的上次操作 和 下次操作
    '''
    分几种情况：数组里 只有本次操作  两次时间为0
    只有上次 和本次  如果 上次和本次相差不超过3天 
    只有本次和下次
    都有
    '''
    # print(newList)

    bnum=0
    anum=0
    for i in range(0, len(newList)):
        if newList[i][0]==data[0]:
            bl = bedate(newList, i, data)
            al = afdate(newList, i, data)
            be_date = bl[0]
            bnum=bl[1]
            af_date = al[0]
            anum=al[1]

    # start_date = datetime.datetime.strptime(data[0], "%Y-%m-%d %H:%M:%S")
    # currentdate = start_date.strftime('%Y-%m-%d')

    # print(be_date,af_date,anum,bnum)

    start_date = datetime.datetime.strptime(data[0], "%Y-%m-%d %H:%M:%S")
    currentdate = start_date.strftime('%Y-%m-%d')

    obj=KeywordsPutonEffect.objects.filter(keywords=data[4], promotionplanname=data[1], babyname=data[3])

    print(list(obj.values()))
    print('********************')
    objlist = list(obj.values())

    for val in objlist:
        tmpDate=val['date']
        if be_date < tmpDate and tmpDate < currentdate:
            beList.append(val)
        elif af_date > tmpDate and tmpDate > currentdate:
            afList.append(val)
        elif tmpDate == currentdate:
            currentList.append(val)

    print(beList,len(beList))
    print(afList, len(afList))
    print(currentList, len(currentList))
    beclick = 0.0
    beshow = 0.0
    becount = 0.0
    bemoney = 0.0
    becost = 0.0
    afclick = 0.0
    afshow = 0.0
    afcount = 0.0
    afmoney = 0.0
    afcost = 0.0


    if len(beList)>0:
        for be in beList:
           n = 0.0
           s = 0.0
           c = 0.0
           m = 0.0
           co = 0.0
           num = 0.0
           if be['showamount']:
               s = float(be['showamount'])

           beshow += s

           if be['clickquantity']:
               c = float(be['clickquantity'])

           beclick += c

           if be['totalclinchdealcount']:
               num = float(be['totalclinchdealcount'])

           becount += num


           if be['cost']:
               co = float(be['cost'])
           becost += co


           if be['totalclinchdealmoney']:
               m = float(be['totalclinchdealmoney'])
           bemoney += m

        day=1
        if bnum > 2:
            day = bnum-1
        data.append(beshow/day)
        data.append(beclick/day)
        data.append(becount/day)
        if beclick/day > 0:
            data.append((becount/day)/(beclick/day))
        else:
            data.append(0.0)
        data.append(becost/day)
        data.append(bemoney/day)
        if bemoney/day > 0:
            data.append((becost/day)/(bemoney/day))
        else:
            data.append(0.0)
    else:
        for i in range(0, 7):
            data.append(0.0)

    if len(afList)>0:
        for af in afList:
           n = 0.0
           s = 0.0
           c = 0.0
           m = 0.0
           co = 0.0
           num = 0.0
           if af['showamount']:
               s = float(af['showamount'])

           afshow += s

           if af['clickquantity']:
               c = float(af['clickquantity'])

           afclick += c

           if af['totalclinchdealcount']:
               num = float(af['totalclinchdealcount'])

           afcount += num


           if af['cost']:
               co = float(af['cost'])
           afcost += co


           if af['totalclinchdealmoney']:
               m = float(af['totalclinchdealmoney'])
           afmoney += m

        day=1
        if anum > 2:
            day = anum-1
        data.append(afshow/day)
        data.append(afclick/day)
        data.append(afcount/day)
        if beclick/day > 0:
            data.append((afcount/day)/(afclick/day))
        else:
            data.append(0.0)
        data.append(afcost/day)
        data.append(afmoney/day)
        if bemoney/day > 0:
            data.append((afcost/day)/(afmoney/day))
        else:
            data.append(0.0)
    else:
        for i in range(0, 7):
            data.append(0.0)


    data.append(tempitem)

    print('+++++++++++++++++++++++')
    print(data)

    return newList

# 求下次操作的日期 无 或 小于 1天
def afdate(total=[],i=0,current=[]):
    start_date = datetime.datetime.strptime(current[0], "%Y-%m-%d %H:%M:%S")
    # offsetday = datetime.timedelta(days=1)
    currentdate = start_date.strftime('%Y-%m-%d')


    # b = datetime.datetime.strptime(be_date, '%Y-%m-%d')
    c = datetime.datetime.strptime(currentdate, '%Y-%m-%d')


    if i > len(total)-1:
        return [currentdate, 0]
    elif i+1 > len(total)-1:
        return [currentdate, 0]
    else:

        # currentdate = datetime.datetime(start_date + offsetday)

        afterdate = datetime.datetime.strptime(total[i+1][0], "%Y-%m-%d %H:%M:%S")
        # offsetday1 = datetime.timedelta(days=-1)
        afdate1 = afterdate.strftime('%Y-%m-%d')
        # afdate1 = datetime.datetime(start_date + offsetday1)
        a = datetime.datetime.strptime(afdate1, '%Y-%m-%d')
        days = (a - c).days
        print(a, c, afdate1, currentdate, days)
        print('<<<<<<<<<<<<<<<<<<<<<<')
        if days > 2:
            return [afdate1, days]
        else:
            return [currentdate, days]

    #     取当前操作天数的上一天
    #     取当前操作数据的上条数据 天数的后一天 取差值看是否大于0  大于=0 赋值   小于零  i-1 调用该方法

def bedate(total=[], i=0, current=[]):
    start_date = datetime.datetime.strptime(current[0], "%Y-%m-%d %H:%M:%S")
    # offsetday = datetime.timedelta(days=1)
    currentdate = start_date.strftime('%Y-%m-%d')

    # b = datetime.datetime.strptime(be_date, '%Y-%m-%d')
    c = datetime.datetime.strptime(currentdate, '%Y-%m-%d')
    if i < 0:
        return [currentdate, 0]
    elif i-1 < 0:
        return [currentdate, 0]
    else:
        beforedate = datetime.datetime.strptime(total[i-1][0], "%Y-%m-%d %H:%M:%S")
        bedate1 = beforedate.strftime('%Y-%m-%d')

        b = datetime.datetime.strptime(bedate1, '%Y-%m-%d')
        days = (c - b).days
        print(c, b, bedate1, currentdate, days)
        print('>>>>>>>>>>>>>>>>>>>')
        if days > 2:
            return [bedate1, days]
        else:
            return [currentdate, days]


def get_date_list(date_str):
    return time.strptime(date_str, "%Y-%m-%d %H:%M:%S")
def get_datetime(date_list):
    return datetime.datetime(date_list[0], date_list[1], date_list[2])
def get_delta_days(start_date, end_date):
    return (end_date - start_date).days


def changeList(excel_list, datatype):

    newlist=[]
    if datatype == '直通车关键词':
        for val in excel_list:
            newObj=models.KeywordsPutonEffect(date=val['Date'], \
                                              promotionplanname=val['PromotionPlanName'], \
                                              babyname=val['BabyName'], \
                                              keywords=val['Keywords'], \
                                              trafficsources=val['TrafficSources'], \
                                              searchtype=val['SearchType'], \
                                              showamount=val['ShowAmount'], \
                                              clickquantity=val['ClickQuantity'], \
                                              cost=val['Cost'], \
                                              clickrate=val['ClickRate'], \
                                              averageshowrank=val['AverageShowRank'], \
                                              averageclickcost=val['AverageClickCost'], \
                                              thousandshowcost=val['ThousandShowCost'], \
                                              clickconversion=val['ClickConversion'], \
                                              directlyclinchdealmoney=val['DirectlyClinchdealMoney'], \
                                              directlyclinchdealcount=val['DirectlyClinchdealCount'], \
                                              indirectclinchdealmoney=val['IndirectClinchdealMoney'], \
                                              indirectclinchdealcount=val['IndirectClinchdealCount'], \
                                              totalclinchdealmoney=val['TotalClinchdealMoney'], \
                                              totalclinchdealcount=val['TotalClinchdealCount'], \
                                              babycollectioncount=val['BabyCollectionCount'], \
                                              storecollectioncount=val['StoreCollectionCount'], \
                                              totalcollectioncount=val['TotalCollectionCount'], \
                                              roi=val['ROI'], \
                                              directlyshoppingcart=val['DirectlyShoppingCart'], \
                                              indirectshoppingcart=val['IndirectShoppingCart'], \
                                              totalshoppingcart=val['TotalShoppingCart']
                                              )
            newlist.append(newObj)
    elif datatype == '阿明数据':
        for val in excel_list:
            clickRate = ''
            payRate = ''
            if '%' in val['ClickRate']:
                tmpstr = val['ClickRate'][:-1]
                f1 = float(tmpstr)/100
                clickRate = ('%.4f' % f1)
            else:
                clickRate = float(val['ClickRate'])

            if '%' in val['PayRate']:
                tmpstr1 = val['PayRate']
                payRate = ('%.4f' % ((float(tmpstr1[:-1]))/100))
            else:
                payRate = float(val['PayRate'])

            print(clickRate, payRate)

            newObj1=models.Mingdatalist(keyword=val['KeyWord'], \
                                             date=val['Date'], \
                                             rank=val['Rank'], \
                                             searchnum=val['SearchNum'], \
                                             clicknum=val['ClickNum'], \
                                             clickrate=clickRate, \
                                             payrate=payRate, \
                                             paynum=val['PayNum'], \
                                             category=MCategory
                                             )
            newlist.append(newObj1)
    elif datatype == '竞品数据':
        for val in excel_list:
            print(val.values())
            if '' in val.values():
                continue

            goodType = ""

            if val['GoodsId'] == '523920366379' or val['GoodsId'] == '556833996282':
                goodType = '本店商品'
            else:
                goodType = val['GoodsType']


            payRate = ''

            if '%' in val['PayRate']:
                tmpstr1 = val['PayRate']
                payRate = ('%.4f' % ((float(tmpstr1[:-1]))/100))
            else:
                payRate = float(val['PayRate'])


            newObj1=models.Competitiveproducts(title=val['Title'], \
                                             goodsid=val['GoodsId'], \
                                             goodstype=goodType, \
                                             date=val['Date'], \
                                             category=CCategory, \
                                             keyword=val['KeyWord'], \
                                             payrate=payRate, \
                                             visiorsnum=val['VisiorsNum'], \
                                             paycount=val['PayCount'], \
                                               )
            newlist.append(newObj1)
    else:
        for val in excel_list:
            newObj1=models.KeywordsOperation(operationdate=val['OperationDate'], \
                                             projectname=val['ProjectName'], \
                                             operationtype=val['OperationType'], \
                                             promotecell=val['PromoteCell'], \
                                             keywords=val['KeyWords'], \
                                             operatingcontent=val['OperatingContent'], \
                                             roi=val['ROI'], \
                                             conversionrate=val['ConversionRate'], \
                                             operatingeffect=val['OperatingEffect'], \
                                             operationpeople=val['OperationPeople']
                                             )
            newlist.append(newObj1)


    return newlist


def getkeyvalue(keylist,oldkey):
    # print(keylist, oldkey)
    for node in keylist:
        if node['download_column'] == oldkey:
            return node['mysql_column']
    return 'null'


# 替换时间
def changeXlrdTimeToDate(xlrdTime):
    newdate = xldate_as_tuple(xlrdTime, 0)
    month = '0'
    day = '0'
    hour = '0'
    minute = '0'
    sec = '0'
    if newdate[1] < 10:
       month='0'+str(newdate[1])
    else:
       month=str(newdate[1])

    if newdate[2]<10:
        day='0'+str(newdate[2])
    else:
        day=str(newdate[2])

    if newdate[-3]<10:
        hour='0'+str(newdate[-3])
    else:
        hour=str(newdate[-3])

    if newdate[-2]<10:
        minute='0'+str(newdate[-2])
    else:
        minute=str(newdate[-2])

    if newdate[-1]<10:
        sec='0'+str(newdate[-1])
    else:
        sec=str(newdate[-1])


    return str(str(newdate[0])+"-" +month+"-"+day+" "+hour+":"+minute+":"+sec)
    # return str(str(newdate[0])+"-" +month+"-"+day)







# 替换时间
def changeKeyWordsTimeToDate(xlrdTime):
    print(xlrdTime)
    newdate = xldate_as_tuple(xlrdTime, 0)
    month = '0'
    day = '0'

    if newdate[1] < 10:
       month='0'+str(newdate[1])
    else:
       month=str(newdate[1])

    if newdate[2]<10:
        day='0'+str(newdate[2])
    else:
        day=str(newdate[2])

    return str(str(newdate[0])+"-" +month+"-"+day)



def compareHead(srource,type):
    if type=='直通车关键词':
        obj = models.DownloadMysql.objects.filter(download_table=type)
        print(obj.__len__())
        print(len(srource))
        print(obj.values(), type, srource)
        if not obj.exists():
            msg = {'status': "在download_table未发现内容"}
            return msg
        if not obj.__len__() == len(srource):
            msg = {'status': "上传表的字段和表定义字段数量不合"}
            return msg
        for line in obj:
            print(line)
            if not line.download_column in srource:
                if not line.download_column in ['主键ID', ]:
                    msg = {'status': "【" + line.download_column + "】" + '该字段为在表中定义'}
                    return msg
        data = list(obj.values())
        msg = {'status': 'ok', 'data': data}
        return msg
    elif type=='阿明数据':
        print('阿明')
        obj = models.DownloadMysql.objects.filter(download_table=type)
        print(obj.__len__())
        print(len(srource))
        print(obj.values(), type, srource)
        if not obj.exists():
            msg = {'status': "在download_table未发现内容"}
            return msg
        if not obj.__len__() == len(srource):
            msg = {'status': "上传表的字段和表定义字段数量不合"}
            return msg
        for line in obj:
            print(line)
            if not line.download_column in srource:
                if not line.download_column in ['主键ID', ]:
                    msg = {'status': "【" + line.download_column + "】" + '该字段为在表中定义'}
                    return msg
        data = list(obj.values())
        msg = {'status': 'ok', 'data': data}
        return msg
    elif type=='竞品数据':
        print(type)
        obj = models.DownloadMysql.objects.filter(download_table=type)
        print(obj.__len__())
        print(len(srource))
        print(obj.values(), type, srource)
        if not obj.exists():
            msg = {'status': "在download_table未发现内容"}
            return msg
        if not obj.__len__() == len(srource):
            msg = {'status': "上传表的字段和表定义字段数量不合"}
            return msg
        for line in obj:
            print(line)
            if not line.download_column in srource:
                if not line.download_column in ['主键ID', ]:
                    msg = {'status': "【" + line.download_column + "】" + '该字段为在表中定义'}
                    return msg
        data = list(obj.values())
        msg = {'status': 'ok', 'data': data}
        return msg
    else:
        obj = models.DownloadMysql.objects.filter(download_table='关键词操作')
        data = list(obj.values())
        msg = {'status': 'ok', 'data': data}
        return msg



# 获取天的数据 店铺或产品分类
def getDayData(request):
    pass


# 获取周的数据  店铺或产品 分类
def getWeekData(request):
    pass


def home(request):
     requestDayData()
     return render(request, 'index.html', context={'log': '报表开始'})



def saveKeyWords(request):
    pass



@csrf_exempt
def searchRecommend(request):

    list1 =request.body.decode('utf-8')
    print(type(list1))
    totalData = json.loads(list1)
    print(totalData)
    msg = {}
    mainP = totalData['searchid']
    recommendType = totalData['RecommendType']
    dateT = totalData['datetime']
    page = totalData['pageNo']

    try:
        caregory = Mainproduct.objects.filter(searchid=mainP).values('category')
    except Exception as err:
        print(err)

    c = list(caregory)[0]['category']

    try:
        rObjs = Recommendedkeywords.objects.filter(rankgroup=page, recommendtype=recommendType, date=dateT, category=c).values()
    except Exception as err:
        print(err)
        msg['status'] = 'failure'
        msg['data'] = []
        msg['msg'] = '数据库执行错误'
        return JsonResponse(msg)


    print(rObjs)

    if len(list(rObjs)) == 0:
        msg['status'] = 'success'
        msg['data'] = []
        msg['msg'] = '没有查到该数据'
        return JsonResponse(msg)

    DataList = []
    for robj in rObjs:
        try:
            rSum = Recommendwordssummary.objects.filter(keywords=robj['keyword'], datetime=dateT).values()
        except Exception as err:
            msg['status'] = 'failure'
            msg['data'] = []
            msg['msg'] = '数据库执行错误'
            return JsonResponse(msg)

        for r in rSum:
            DataList.append(r)

    dict = {}
    dict['total'] = len(DataList)
    dict['pageNoArray'] = len(DataList)
    dict['data'] = DataList
    dict['pageSize'] = page
    dict['pageNo'] = page
    print(dict)
    msg['status'] = 'success'
    msg['msg'] = '查询成功'
    msg['data'] = dict
    return JsonResponse(msg)




import datetime
@csrf_exempt
def keyWordsTotalData(request):
    list1 = request.body.decode('utf-8')
    logger_supplement.info(type(list1))
    totalData = json.loads(list1)
    logger_supplement.info(totalData)
    msg = {}
    mainP = totalData['searchid']
    startTime = ""
    endTime = ""
    pageNo = totalData['pageNo']

    if len(totalData['startTime']) > 0 and len(totalData['endTime']) > 0:
        startTime = totalData['startTime']
        endTime = totalData['endTime']
        print(startTime)
        print(endTime)
    else:
        d = datetime.datetime.now()
        e = d + timedelta(days=-1)
        startTime = e.strftime('%Y-%m-%d')
        endTime = startTime

    page = int(totalData['pageNo'])
    pageSize = 15
    if "pageSize" in totalData.keys():
        pageSize = int(totalData['pageSize']) if int(totalData['pageSize']) > 0 else 15

    if len(mainP) > 0:
        print(mainP)
    else:
        msg['status'] = 'failure'
        msg['data'] = []
        msg['msg'] = '产品不能为空'
        return JsonResponse(msg)

    sP = (int(pageNo) - 1) * pageSize

    eP = sP + pageSize

    try:
        caregory = Mainproduct.objects.filter(searchid=mainP).values('category')
    except Exception as err:
        print(err)

    c = list(caregory)[0]['category']

    try:
        count = Keywordssummary.objects.filter(datetime__gte=startTime, datetime__lte=endTime, searchid=mainP).values(
            'keywords').annotate(industrysearchpopularity=Sum('visitorstosearch')).count()
    except Exception as err:
        print(err)

    print(count)

    try:
        tmpList1 = Keywordssummary.objects.filter(datetime__gte=startTime, \
                                                  datetime__lte=endTime, \
                                                  searchid=mainP).values('keywords').annotate(
            industrysearchpopularity=Sum('industrysearchpopularity'), \
            visitorstosearch=Sum('visitorstosearch'), \
            searchclinchdeal=Sum('searchclinchdeal'), \
            click=Sum('click'), \
            spending=Sum('spending'), \
            amount=Sum('amount'), \
            totalcount=Sum('totalcount'), \
            msearchnum=Sum('msearchnum'), \
            mclicknum=Sum('mclicknum'), \
            mpaynum=Sum('mpaynum'), \
            showcount=Sum('showcount')

            )[sP:eP]
    except Exception as err:
        print(err)
    TmpList = []
    for t in tmpList1:
        print(t)
        try:
            AMZH = Competitiveproducts.objects.filter(date__gte=startTime, date__lte=endTime, \
                                                      keyword=t['keywords'], \
                                                      category=c, \
                                                      goodstype__contains='本店商品').values('visiorsnum',
                                                                                         'paycount')
        except Exception as err:
            print(err)

        try:
            JPZH = Competitiveproducts.objects.filter(date__gte=startTime, date__lte=endTime, \
                                                      keyword=t['keywords'], category=c, \
                                                      goodstype__contains='竞品').values('visiorsnum', 'paycount')
        except Exception as err:
            print(err)
        # 权重分
        WeightPoints = 0.0

        # 行业搜索人气
        IndustrySearchPopularity = 0
        # 行业转化
        IndustryTransformation = 0.0
        # 搜索访客
        VisitorsToSearch = 0
        # 搜索成交
        SearchClinchDeal = 0
        # 搜索转化
        SearchConversion = 0.0
        # 阿明转化
        MingConversion = 0.0
        # 竞品转化
        CompetingConversion = 0.0
        # 展现量
        ShowCount = 0
        # 点击
        Click = 0
        # 点击率
        Click_Rate = 0.0
        # 花费
        Spending = 0
        # PPC
        PPC = 0.0
        # 笔数
        TotalCount = 0
        # 转化
        Conversion = 0.0
        # 金额
        Amount = 0
        # ROI
        ROI = 0.0
        # UV价值
        UV = 0.0
        # 客单价
        GuestUnitPrice = 0.0

        # 搜索人数
        MSearchNum = 0
        # 阿明点击人数
        MclickNum = 0
        # 阿明点击率
        # 阿明支付转化率
        Mpaytate = 0.0
        # 阿明支付人数
        MpayNum = 0
        # 本店 访客人数 支付人数
        amvisiorsnum = 0
        ampaycount = 0
        # 竞品访客人数 支付人数
        jpvisiorsnum = 0
        jppaycount = 0
        AM = 0.0
        JP = 0.0
        print(['*'] * 10)
        for m in AMZH:
            amvisiorsnum += float(m['visiorsnum'])
            ampaycount += float(m['paycount'])

        for c in JPZH:
            jpvisiorsnum += float(c['visiorsnum'])
            jppaycount += float(c['paycount'])

        if len(AMZH) > 0:
            MingConversion = (ampaycount / amvisiorsnum) / len(AMZH)

        if len(JPZH) > 0:
            CompetingConversion = (jppaycount / jpvisiorsnum) / len(JPZH)
        IndustrySearchPopularity += int(t['industrysearchpopularity'])
        VisitorsToSearch += int(t['visitorstosearch'])
        SearchClinchDeal += int(t['searchclinchdeal'])
        Click += int(t['click'])
        Spending += int(t['spending'])
        Amount += int(t['amount'])
        TotalCount += int(t['totalcount'])
        ShowCount += int(t['showcount'])
        MSearchNum += int(t['msearchnum'])
        MclickNum += int(t['mclicknum'])
        MpayNum += int(t['mpaynum'])

        Mpaytate = (MpayNum / IndustrySearchPopularity) if MSearchNum <= 0 else MpayNum / MSearchNum

        SearchConversion = 0.0 if VisitorsToSearch <= 0 else SearchClinchDeal / VisitorsToSearch

        Click_Rate = Click if ShowCount <= 0 else Click / ShowCount
        Conversion = TotalCount if Click <= 0 else TotalCount / Click
        ROI = Amount if Spending <= 0.0 else Amount / Spending
        PPC = Click if Click <= 0.0 else Spending / Click
        GuestUnitPrice = TotalCount if TotalCount <= 0.0 else Amount / TotalCount
        UV = GuestUnitPrice * Conversion

        t['industrytransformation'] = ('%.2f' % (Mpaytate * 100)) + "%"
        t['searchconversion'] = ('%.2f' % (SearchConversion * 100)) + "%"
        t['mingconversion'] = ('%.2f' % (MingConversion * 100)) + "%"
        t['competingconversion'] = ('%.2f' % (CompetingConversion * 100)) + "%"
        t['click_rate'] = ('%.2f' % (Click_Rate * 100)) + "%"
        t['ppc'] = ('%.2f' % (PPC / 100))
        t['conversion'] = ('%.2f' % (Conversion * 100))
        t['roi'] = ('%.2f' % (ROI * 100))
        t['uv'] = str(round(UV, 2))
        t['guestunitprice'] = ('%.2f' % GuestUnitPrice)
        TmpList.append(t)
    dict = {}
    dict['total'] = count
    dict['pageNoArray'] = len(TmpList)
    dict['data'] = TmpList
    dict['pageSize'] = pageSize
    dict['pageNo'] = int(pageNo)
    logger_supplement.info(dict)
    msg['status'] = 'success'
    msg['msg'] = '查询成功'
    msg['data'] = dict
    return JsonResponse(msg)


import datetime
# def write_excel(request):
def write_excel():
    """
    导出excel表格
    """
    d = datetime.datetime.now()
    e = d + timedelta(days=-1)
    s = d + timedelta(days=-7)

    # startTime = s.strftime('%Y-%m-%d')
    # endTime = e.strftime('%Y-%m-%d')

    startTime = "2019-05-29"
    endTime = "2019-06-04"
    dayNum = 7

    productName = Mainproduct.objects.all().values('productname', 'searchid', 'category')

    print(productName)

    for item in productName:
        searchKeys = Keywordssummary.objects.filter(datetime__gte=startTime, datetime__lte=endTime, searchid=item['searchid']).values('keywords')

        data = []
        for searchKey in searchKeys:
            data.append(searchKey['keywords'])

        li = list(set(data))
        li.sort(key=data.index)

        print(item['productname'], li)

        List = []
        CategoryList = []
        try:
            tmpList1 = Keywordssummary.objects.filter(datetime__gte=startTime, \
                                                      datetime__lte=endTime, \
                                                      searchid=item['searchid']).values('keywords').annotate(
                industrysearchpopularity=Sum('industrysearchpopularity'), \
                visitorstosearch=Sum('visitorstosearch'), \
                searchclinchdeal=Sum('searchclinchdeal'), \
                click=Sum('click'), \
                spending=Sum('spending'), \
                amount=Sum('amount'), \
                totalcount=Sum('totalcount'), \
                msearchnum=Sum('msearchnum'), \
                mclicknum=Sum('mclicknum'), \
                mpaynum=Sum('mpaynum'), \
                showcount=Sum('showcount')

            )
        except Exception as err:
            print(err)
        TmpList = []
        for t in tmpList1:
            print(t)
            keyList = []
            try:
                AMZH = Competitiveproducts.objects.filter(date__gte=startTime, date__lte=endTime, \
                                                          keyword=t['keywords'], \
                                                          category=item['category'], \
                                                          goodstype__contains='本店商品').values('visiorsnum',
                                                                                             'paycount')
            except Exception as err:
                print(err)

            try:
                JPZH = Competitiveproducts.objects.filter(date__gte=startTime, date__lte=endTime, \
                                                          keyword=t['keywords'], category=item['category'], \
                                                          goodstype__contains='竞品').values('visiorsnum', 'paycount')
            except Exception as err:
                print(err)

            # 权重分
            WeightPoints = 0.0

            # 行业搜索人气
            IndustrySearchPopularity = 0
            # 行业转化
            IndustryTransformation = 0.0
            # 搜索访客
            VisitorsToSearch = 0
            # 搜索成交
            SearchClinchDeal = 0
            # 搜索转化
            SearchConversion = 0.0
            # 阿明转化
            MingConversion = 0.0
            # 竞品转化
            CompetingConversion = 0.0
            # 展现量
            ShowCount = 0
            # 点击
            Click = 0
            # 点击率
            Click_Rate = 0.0
            # 花费
            Spending = 0
            # PPC
            PPC = 0.0
            # 笔数
            TotalCount = 0
            # 转化
            Conversion = 0.0
            # 金额
            Amount = 0
            # ROI
            ROI = 0.0
            # UV价值
            UV = 0.0
            # 客单价
            GuestUnitPrice = 0.0

            # 行业转化权重
            IndustryConversionWeigh = 0.0
            # 搜索转化权重
            SearchConversionWeight = 0.0
            # 阿明转化权重
            MingConversionWeight = 0.0
            # 竞品转化权重
            CompetingConversionWeight = 0.0
            # 转化总分
            ConversionTotalScore = 0.0
            # 主商品
            MainP = ''
            # 搜索id
            searchId = ''
            #搜索人数
            MSearchNum = 0
            #阿明点击人数
            MclickNum = 0
            #阿明点击率
            #阿明支付转化率
            Mpaytate = 0.0
            #阿明支付人数
            MpayNum = 0
            #本店 访客人数 支付人数
            amvisiorsnum = 0
            ampaycount = 0
            #竞品访客人数 支付人数
            jpvisiorsnum = 0
            jppaycount = 0

            AM = 0.0
            JP = 0.0
            print(['*'] * 10)
            for m in AMZH:
                amvisiorsnum += float(m['visiorsnum'])
                ampaycount += float(m['paycount'])

            for c in JPZH:
                jpvisiorsnum += float(c['visiorsnum'])
                jppaycount += float(c['paycount'])

            if len(AMZH) > 0:
                MingConversion = (ampaycount / amvisiorsnum) / len(AMZH)

            if len(JPZH) > 0:
                CompetingConversion = (jppaycount / jpvisiorsnum) / len(JPZH)
            IndustrySearchPopularity = int(t['industrysearchpopularity'])
            VisitorsToSearch = int(t['visitorstosearch'])
            SearchClinchDeal = int(t['searchclinchdeal'])
            Click = int(t['click'])
            Spending = int(t['spending'])
            Amount = int(t['amount'])
            TotalCount = int(t['totalcount'])
            ShowCount = int(t['showcount'])
            MSearchNum = int(t['msearchnum'])
            MclickNum = int(t['mclicknum'])
            MpayNum = int(t['mpaynum'])

            Mpaytate = (MpayNum / IndustrySearchPopularity) if MSearchNum <= 0 else MpayNum / MSearchNum

            SearchConversion = 0.0 if VisitorsToSearch <= 0 else SearchClinchDeal / VisitorsToSearch

            Click_Rate = Click if ShowCount <= 0 else Click / ShowCount
            Conversion = TotalCount if Click <= 0 else TotalCount / Click
            ROI = Amount if Spending <= 0.0 else Amount / Spending
            PPC = Click if Click <= 0.0 else Spending / Click
            GuestUnitPrice = TotalCount if TotalCount <= 0.0 else Amount / TotalCount
            UV = GuestUnitPrice * Conversion
            keyList.append(t['keywords'])
            keyList.append(IndustrySearchPopularity/dayNum)
            keyList.append(Mpaytate/dayNum)
            keyList.append(MSearchNum/dayNum)
            keyList.append(MclickNum/dayNum)
            keyList.append(Mpaytate/dayNum)
            keyList.append(MpayNum/dayNum)
            keyList.append(VisitorsToSearch/dayNum)
            keyList.append(SearchClinchDeal/dayNum)
            keyList.append(round(SearchConversion/dayNum, 4))
            keyList.append(MingConversion)
            keyList.append(CompetingConversion)
            keyList.append(Click/dayNum)
            keyList.append(round(Click_Rate/dayNum, 4))
            keyList.append(Spending/dayNum)
            keyList.append(round(PPC/dayNum, 4))
            keyList.append(TotalCount/dayNum)
            keyList.append(round(Conversion/dayNum, 4))
            keyList.append(Amount/dayNum)
            keyList.append(round(ROI/dayNum, 4))
            keyList.append(round(UV/dayNum, 2))
            keyList.append(GuestUnitPrice/dayNum)
            newObject = models.Recommendwordssummary(
                datetime=endTime, \
                weightpoints=str(WeightPoints), \
                keywords=t['keywords'], \
                industrysearchpopularity=str(int(IndustrySearchPopularity)), \
                industrytransformation=('%.2f' % (Mpaytate * 100)) + "%", \
                visitorstosearch=str(VisitorsToSearch), \
                searchclinchdeal=str(SearchClinchDeal), \
                searchconversion=('%.2f' % (SearchConversion * 100))+"%", \
                mingconversion=('%.2f' % (MingConversion * 100)) + "%", \
                competingconversion=('%.2f' % (CompetingConversion * 100)) + "%", \
                click=str(Click), \
                click_rate=('%.2f' % (Click_Rate * 100)) + "%", \
                spending=str(int(Spending)),
                ppc=('%.2f' % (PPC /100)), \
                totalcount=str(TotalCount), \
                conversion=('%.2f' % (Conversion * 100)) + "%", \
                amount=str(Amount), \
                roi=('%.2f' % (ROI * 100)), \
                uv=str(round(UV, 2)), \
                guestunitprice=('%.2f' % GuestUnitPrice), \
                industryconversionweight=('%.2f' % (IndustryConversionWeigh * 100)) + "%", \
                searchconversionweight=('%.2f' % (SearchConversionWeight * 100)) + "%", \
                mingconversionweight=('%.2f' % (MingConversionWeight * 100)) + "%", \
                competingconversionweight=('%.2f' % (CompetingConversionWeight * 100)) + "%", \
                conversiontotalscore=('%.2f' % (ConversionTotalScore * 100)) + "%", \
                productname=item['productname'], \
                searchid=item['searchid'], \
                showcount=int(ShowCount),
            )

            CategoryList.append(newObject)
            List.append(keyList)

        # try:
        #     Recommendwordssummary.objects.bulk_create(CategoryList)
        # except Exception as err:
        #     print(err)

        name = item['category']+endTime + ".xlsx"
        ws = xlsxwriter.Workbook(name)
        w = ws.add_worksheet('关键词汇总')
        excel_row = 0
        for index in List:
            for i in range(22):
                w.write(excel_row, i, index[i],)
            excel_row += 1
        ws.close()


        # wb = openpyxl.Workbook()
        # ws = wb.active # 创建一个sheet
        # ws.title = "关键词汇总"
        # excel_row = 0
        #
        # for i in range(22):
        #     for index in List:
        #         ws.append({i+1: index[i]})
        #
        # # for index in List:
        # #     for i in range(22):
        # #         ws.append(excel_row, i, index[i],)
        # #     excel_row += 1
        # # ws.close()
        # fileName = os.path.split(os.path.realpath(__file__))[0] + "/" + "dataSource" + "/" + item['category'] + endTime + ".xlsx"
        # wb.save(fileName)



        return HttpResponse('11111')



@csrf_exempt
# def keyWordsResult(request):
def requestKeyRecommend(data):

    # url = 'http://47.97.51.185:9090'
    url = 'http://192.168.63.104:9090'



    headers = {
        "Content-Type": "application/json; charset=UTF-8",
    }

    ret = requests.post(url, json.dumps(data), headers=headers)

    # requests.post()

    totalData = json.loads(ret.text)

    print(totalData)
    # recommendList = totalData['retinfo']['key_words_list']
    #
    # tmplist = []
    # for item in recommendList:
    #     if "current" not in item:
    #         tmplist.append(item)
    #
    # d = datetime.datetime.now()
    #
    # e = d + timedelta(days=-1)
    # date = e.strftime('%Y-%m-%d')
    #
    # valuestr = tmplist.pop()[1:-1]
    # valueList = valuestr.split(", ")
    # print(valueList)
    # OBJ = []
    # for index in range(len(tmplist)):
    #     str1 = tmplist[index][1:-1]
    #     print(type(str1))
    #     wordsList = str1.split(", ")
    #     print(wordsList)
    #     for i in range(len(wordsList)):
    #         word = wordsList[i][1:-1]
    #         obj = models.Recommendedkeywords(
    #             date=date, \
    #             keyword=word, \
    #             rankgroup=str(index+1), \
    #             category=totalData['id'], \
    #             recommendtype=totalData['reward_type'], \
    #             rankvalue=valueList[index],
    #         )
    #         OBJ.append(obj)
    #
    # try:
    #     Recommendedkeywords.objects.bulk_create(OBJ)
    # except Exception as err:
    #     print(err)


    # return render(request, 'catId.html')


def requestKeyRecommendResut(data, date):
    # url = 'http://47.97.51.185:9090'
    # url = 'http://192.168.63.104:9090'
    #
    # headers = {
    #     "Content-Type": "application/json; charset=UTF-8",
    # }
    #
    # ret = requests.post(url, json.dumps(data), headers=headers)
    #
    # totalData = json.loads(ret.text)

    totalData = {'actiontime': '2019-06-05 15:43:36', 'reward_type': 4, 'id': 'probiotics', 'action_id': 2, 'retcode': 0, 'num_timesteps': 1000000, 'process_id': 6, 'retinfo': {'isstarted': True, 'run_process': "['益生菌', '益生菌大人 调理 肠胃', '益生菌粉', '益生菌粉', '益生菌调理肠胃', '肠道益生菌', '益生菌冻干粉', '益生菌 成人', '复合益生菌', '复合益生菌冻干粉', '复合益生菌冻干粉', '益生菌大人', '益生菌大人调理肠胃肠道', '益生菌大人调理肠胃', '姿美堂益生菌', '儿童益生菌', '益生菌成人', '儿童益生菌 调理肠胃', '调理肠胃', '顺丰速达 妙语益生菌成人儿童大人女性肠胃肠道调理益生元冻干粉']", 'iscompleted': True, 'key_words_list': ['current rank words:', "['益生菌', '益生菌大人 调理 肠胃', '益生菌粉', '益生菌调理肠胃', '乐力益生菌', '肠道益生菌', '益生菌冻干粉', '乐力', '益生菌 成人', '益生菌 成人', '复合益生菌', '复合益生菌冻干粉', '妙语益生菌', '益生菌大人调理肠胃肠道', '益生菌大人调理肠胃', '益生菌儿童 调理 肠胃', '益生菌成人', '儿童益生菌 调理肠胃', '调理肠胃', '顺丰速达 妙语益生菌成人儿童大人女性肠胃肠道调理益生元冻干粉']", "['益生菌', '益生菌大人 调理 肠胃', '益生菌粉', '乐力益生菌', '肠道益生菌', '益生菌冻干粉', '乐力', '益生菌 成人', '益生菌 成人', '复合益生菌', '复合益生菌冻干粉', '妙语益生菌', '益生菌大人', '益生菌大人调理肠胃肠道', '益生菌大人调理肠胃', '儿童益生菌', '益生菌成人', '儿童益生菌 调理肠胃', '调理肠胃', '顺丰速达 妙语益生菌成人儿童大人女性肠胃肠道调理益生元冻干粉']", "['益生菌', '益生菌大人 调理 肠胃', '益生菌粉', '乐力益生菌', '肠道益生菌', '益生菌冻干粉', '乐力', '益生菌 成人', '益生菌 成人', '复合益生菌', '复合益生菌冻干粉', '妙语益生菌', '益生菌大人', '益生菌大人调理肠胃肠道', '益生菌大人调理肠胃', '儿童益生菌', '益生菌成人', '儿童益生菌 调理肠胃', '调理肠胃', '顺丰速达 妙语益生菌成人儿童大人女性肠胃肠道调理益生元冻干粉']", "['益生菌', '益生菌大人 调理 肠胃', '益生菌粉', '乐力益生菌', '肠道益生菌', '益生菌冻干粉', '益生菌 成人', '复合益生菌', '复合益生菌冻干粉', '妙语益生菌', '益生菌大人', '益生菌大人调理肠胃肠道', '益生菌大人调理肠胃', '姿美堂益生菌', '姿美堂益生菌', '儿童益生菌', '益生菌儿童 调理 肠胃', '儿童益生菌 调理肠胃', '调理肠胃', '顺丰速达 妙语益生菌成人儿童大人女性肠胃肠道调理益生元冻干粉']", "['益生菌', '益生菌大人 调理 肠胃', '益生菌粉', '益生菌调理肠胃', '乐力益生菌', '肠道益生菌', '益生菌冻干粉', '乐力', '复合益生菌', '复合益生菌冻干粉', '妙语益生菌', '益生菌大人', '益生菌大人调理肠胃肠道', '益生菌大人调理肠胃', '姿美堂益生菌', '益生菌儿童 调理 肠胃', '益生菌成人', '益生菌成人', '儿童益生菌 调理肠胃', '顺丰速达 妙语益生菌成人儿童大人女性肠胃肠道调理益生元冻干粉']", "['益生菌', '益生菌粉', '益生菌调理肠胃', '乐力益生菌', '乐力益生菌', '肠道益生菌', '益生菌冻干粉', '乐力', '益生菌 成人', '复合益生菌', '复合益生菌冻干粉', '益生菌大人', '益生菌大人调理肠胃肠道', '益生菌大人调理肠胃', '姿美堂益生菌', '儿童益生菌', '益生菌儿童 调理 肠胃', '益生菌成人', '儿童益生菌 调理肠胃', '顺丰速达 妙语益生菌成人儿童大人女性肠胃肠道调理益生元冻干粉']", "['益生菌', '益生菌大人 调理 肠胃', '益生菌粉', '益生菌调理肠胃', '乐力益生菌', '益生菌冻干粉', '乐力', '益生菌 成人', '复合益生菌', '复合益生菌冻干粉', '妙语益生菌', '益生菌大人', '益生菌大人调理肠胃肠道', '益生菌大人调理肠胃', '姿美堂益生菌', '儿童益生菌', '儿童益生菌', '益生菌儿童 调理 肠胃', '儿童益生菌 调理肠胃', '调理肠胃']", "['益生菌', '益生菌大人 调理 肠胃', '益生菌粉', '益生菌调理肠胃', '肠道益生菌', '益生菌冻干粉', '乐力', '乐力', '益生菌 成人', '复合益生菌', '复合益生菌冻干粉', '妙语益生菌', '益生菌大人', '益生菌大人调理肠胃肠道', '姿美堂益生菌', '儿童益生菌', '益生菌儿童 调理 肠胃', '儿童益生菌 调理肠胃', '调理肠胃', '顺丰速达 妙语益生菌成人儿童大人女性肠胃肠道调理益生元冻干粉']", "['益生菌', '益生菌大人 调理 肠胃', '益生菌粉', '益生菌调理肠胃', '乐力益生菌', '肠道益生菌', '益生菌冻干粉', '益生菌 成人', '复合益生菌', '复合益生菌冻干粉', '益生菌大人', '益生菌大人调理肠胃肠道', '益生菌大人调理肠胃', '益生菌大人调理肠胃', '益生菌大人调理肠胃', '姿美堂益生菌', '益生菌儿童 调理 肠胃', '益生菌成人', '调理肠胃', '顺丰速达 妙语益生菌成人儿童大人女性肠胃肠道调理益生元冻干粉']", "['益生菌', '益生菌大人 调理 肠胃', '益生菌粉', '益生菌粉', '益生菌调理肠胃', '肠道益生菌', '益生菌冻干粉', '益生菌 成人', '复合益生菌', '复合益生菌冻干粉', '复合益生菌冻干粉', '益生菌大人', '益生菌大人调理肠胃肠道', '益生菌大人调理肠胃', '姿美堂益生菌', '儿童益生菌', '益生菌成人', '儿童益生菌 调理肠胃', '调理肠胃', '顺丰速达 妙语益生菌成人儿童大人女性肠胃肠道调理益生元冻干粉']", 'current rank value:', '[2770.6259034720774, 2765.139531232997, 2762.89156238525, 2739.9839108853043, 2738.753416515552, 2725.1228332096775, 2718.9683853547153, 2626.8206220719117, 2625.937416810049, 2625.0716107348917]'], 'os_id': 0}}


    print(totalData)

    if totalData['retinfo']:
        if totalData['retinfo']['iscompleted'] == True:
            recommendList = totalData['retinfo']['key_words_list']

            tmplist = []
            if len(recommendList) >0:
                for item in recommendList:
                    if "current" not in item:
                        tmplist.append(item)

                # d = datetime.datetime.now()
                #
                # e = d + timedelta(days=-1)
                # date = e.strftime('%Y-%m-%d')



                valuestr = tmplist.pop()[1:-1]
                valueList = valuestr.split(", ")
                print(valueList)
                OBJ = []
                for index in range(len(valueList)):
                    str1 = tmplist[index][1:-1]
                    print(type(str1))
                    wordsList = str1.split(", ")
                    print(wordsList)
                    for i in range(len(wordsList)):
                        word = wordsList[i][1:-1]
                        obj = models.Recommendedkeywords(
                            date=date, \
                            keyword=word, \
                            rankgroup=str(index + 1), \
                            category=totalData['id'], \
                            recommendtype=totalData['reward_type'], \
                            rankvalue=valueList[index],
                        )
                        OBJ.append(obj)

                try:
                    Recommendedkeywords.objects.bulk_create(OBJ)
                except Exception as err:
                    print(err)


def requestR():

    data = {"id":'probiotics',"action_id" : 1,"process_id" : 1, "reward_type": 1,"num_timesteps" : 1000000 ,"assert_file" : "probiotics2019-05-29.xlsx"}

    requestKeyRecommend(data)

    time.sleep(3)

    data1 = {"id":'probiotics',"action_id" : 1,"process_id" : 1, "reward_type": 2,"num_timesteps" : 1000000 ,"assert_file" : "probiotics2019-05-29.xlsx"}

    requestKeyRecommend(data1)

    time.sleep(3)

    data2 = {"id":'probiotics',"action_id" : 1,"process_id" : 1, "reward_type": 3,"num_timesteps" : 1000000 ,"assert_file" : "probiotics2019-05-29.xlsx"}

    requestKeyRecommend(data2)

    time.sleep(3)
    data3 = {"id":'probiotics',"action_id" : 1,"process_id" : 1, "reward_type": 4,"num_timesteps" : 1000000 ,"assert_file" : "probiotics2019-05-29.xlsx"}

    requestKeyRecommend(data3)



def resultR():
    date = '2019-05-29'

    # data1 = {"id":'probiotics',"action_id" : 2,"process_id" : 3, "reward_type": 1,"num_timesteps" : 1000000 ,"assert_file" : "probiotics2019-05-29.xlsx"}
    # #
    # requestKeyRecommendResut(data1, date)

    # time.sleep(3)
    # data2 = {"id":'probiotics',"action_id" : 2,"process_id" : 4, "reward_type": 2,"num_timesteps" : 1000000 ,"assert_file" : "probiotics2019-05-29.xlsx"}
    # #
    # requestKeyRecommendResut(data2, date)
    # time.sleep(3)
    # data3 = {"id":'probiotics',"action_id" : 2,"process_id" : 5, "reward_type": 3,"num_timesteps" : 1000000 ,"assert_file" : "probiotics2019-05-29.xlsx"}
    # #
    # requestKeyRecommendResut(data3, date)
    # time.sleep(3)
    data4 = {"id":'probiotics',"action_id" : 2,"process_id" : 6, "reward_type": 4,"num_timesteps" : 1000000 ,"assert_file" : "probiotics2019-05-29.xlsx"}
    #
    requestKeyRecommendResut(data4, date)




if __name__ == "__main__":

    startTime = "2019-06-04"
    endTime = "2019-06-04"

    # IntegrationData(endTime)
    write_excel()
    # requestR()
    # resultR()
    # getKey()














