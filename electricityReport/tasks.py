# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
#
# import os, django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "report.settings")# project_name 项目名称
# django.setup()
#
# from electricityReport.models import SuperRecommendation, ThroughTrain, DrillingExhibitionSingleProducts, DrillingExhibitionWholeStore, PromotionBalancePayments, PromotionDetails
#
# from django.db.models import Q
#
# import datetime
#
# import time
#
#
#
# def requestDayData():
#
#     print('开始查询上一天的报表数据')
#
#     #查询对照表
#
#     today = datetime.datetime.now()
#
#     offsetHour = datetime.timedelta(days=-1)
#
#     yesterday = (today + offsetHour).strftime('%Y-%m-%d')
#
#     # 分别查询 超级推荐  直通车  钻展单品  钻展全店 数据
#     try:
#         superList = SuperRecommendation.objects.values()
#     except Exception as err:
#         print(err)
#
#     # try:
#     #     throughList = ThroughTrain.objects.all()
#     # except Exception as err:
#     #     print(err)
#     #
#     #
#     # try:
#     #     drillSingleList = DrillingExhibitionSingleProducts.objects.all()
#     # except Exception as err:
#     #     print(err)
#     #
#     # try:
#     #     drillAllList = DrillingExhibitionWholeStore.objects.all()
#     # except Exception as err:
#     #     print(err)
#
#     print(len(list(superList)))
#     # print(throughList)
#     # print(drillAllList)
#     # print(drillSingleList)
#     #明细集合
#     detailsList = []
#     #收支集合
#     balanceList = []
#
#     #产品对照集合
#     sourceList = []
#
#
#     #1.先遍历数据  找推广细节表出需要的结果值 和 进行计算得出的结果值   及  收支表中需要值
#     for sData in superList:
#         print(sData['date'])
#         # sDetail = PromotionDetails.objects.create(channel='超级推荐', goodsname='', storename='', date='', \
#         #                                           showamount='', clickrate='', clickquantity='', cpc='',
#         #                                           cost='', conversionrate='', \
#         #                                           clinchdealquantity='', roi='', clinchdealamount='', uv='')
#         # detailsList.append(sDetail)
#         # #遍历产品对照集合 找出产品名称
#         # for source in sourceList:
#         #     if source.name in sData.unit:
#         #         sResult = PromotionBalancePayments.objects.create(channel='超级推荐', goodsname='', storename='',  \
#         #                                                           date='')
#
#
#
#
#
#
#     # for tData in throughList:
#     #     sResult = PromotionBalancePayments.objects.create(channel='超级推荐', goodsname='', storename='', \
#     #                                                       date='')
#     #     tDetail = PromotionDetails.objects.create(channel='超级推荐', goodsname='', storename='', date='', \
#     #                                               showamount='', clickrate='', clickquantity='', cpc='',
#     #                                               cost='', conversionrate='', \
#     #                                               clinchdealquantity='', roi='', clinchdealamount='', uv='')
#     #     detailsList.append(tDetail)
#     #
#     #
#     #
#     # for dsData in drillSingleList:
#     #     sResult = PromotionBalancePayments.objects.create(channel='超级推荐', goodsname='', storename='', \
#     #                                                       date='')
#     #     dsDetail = PromotionDetails.objects.create(channel='超级推荐', goodsname='', storename='', date='', \
#     #                                               showamount='', clickrate='', clickquantity='', cpc='',
#     #                                               cost='', conversionrate='', \
#     #                                               clinchdealquantity='', roi='', clinchdealamount='', uv='')
#     #     detailsList.append(dsDetail)
#     #
#     #
#     #
#     # for daData in drillAllList:
#     #     sResult = PromotionBalancePayments.objects.create(channel='超级推荐', goodsname='', storename='', \
#     #                                                       date='')
#     #     daDetail = PromotionDetails.objects.create(channel='超级推荐', goodsname='', storename='', date='', \
#     #                                               showamount='', clickrate='', clickquantity='', cpc='',
#     #                                               cost='', conversionrate='', \
#     #                                               clinchdealquantity='', roi='', clinchdealamount='', uv='')
#     #     detailsList.append(daDetail)
#
#
#
#     #
#     # for datail in detailsList:
#     #     print(datail)