"""report URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from electricityReport import views
from django.conf.urls import include,url


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^chandle/showpage', views.showpage),
    url(r'^chandle/excel_expoet', views.excel_expoet, name='excel_expoet'),
    url(r'^chandle/getExcel_keyWords', views.getExcel_keyWords, name='getExcel_keyWords'),
    url(r'^chandle/getExcel_mingexpoet', views.getExcel_mingexpoet, name='getExcel_mingexpoet'),
    url(r'^chandle/getExcel_comexpoet', views.getExcel_comexpoet, name='getExcel_comexpoet'),
    url(r'^chandle/parsingData', views.parsingData, name='parsingData'),
    url(r'^chandle/getKey', views.getKey, name='getKey'),
    url(r'^chandle/popKey', views.popKey, name='popKey'),
    url(r'^search_tm_data', views.search_tm_data, name='search_tm_data'),
    url(r'^search_tm_hotRank', views.search_tm_hotRank, name='search_tm_hotRank'),
    url(r'^search_tm_Competition', views.search_tm_Competition, name='search_tm_Competition'),
    url(r'^search_tm_Source ', views.search_tm_Source, name='search_tm_Source '),
    url(r'^requeryMainProduct', views.requeryMainProduct, name='requeryMainProduct'),
    url(r'^IntegrationData', views.IntegrationData, name='IntegrationData'),
    url(r'^requeryKeyWordData', views.requeryKeyWordData, name='requeryKeyWordData'),
    url(r'^requeryItemsGraph', views.requeryItemsGraph, name='requeryItemsGraph'),
    url(r'^requeryItemDetail', views.requeryItemDetail, name='requeryItemDetail'),
    url(r'^write_excel', views.write_excel, name='write_excel'),
    url(r'^keyWordsResult', views.keyWordsResult, name='keyWordsResult'),
    url(r'^keyWordsTotalData', views.keyWordsTotalData, name='keyWordsTotalData'),
    url(r'^searchRecommend', views.searchRecommend, name='searchRecommend'),
    url(r'mcategory', views.mcategory, name='mcategory'),
    url(r'ccategory', views.ccategory, name='ccategory'),

]
