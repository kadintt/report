# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Clinchdeal(models.Model):
    primary_key_id = models.AutoField(db_column='Primary_key_ID', primary_key=True)  # Field name made lowercase.
    module = models.CharField(max_length=128)
    starttime = models.CharField(db_column='startTime', max_length=256)  # Field name made lowercase.
    endtime = models.CharField(db_column='endTime', max_length=256)  # Field name made lowercase.
    updatetime = models.CharField(db_column='updateTime', max_length=256)  # Field name made lowercase.
    good_me = models.CharField(max_length=256, blank=True, null=True)
    jz_shop_name = models.CharField(max_length=256, blank=True, null=True)
    js_shop_goodid = models.CharField(db_column='js_shop_goodID', max_length=256, blank=True, null=True)  # Field name made lowercase.
    uv = models.IntegerField()
    keyword = models.CharField(max_length=256)
    datetype = models.CharField(db_column='dateType', max_length=256)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ClinchDeal'


class Competingdrainage(models.Model):
    primary_key_id = models.AutoField(db_column='Primary_key_ID', primary_key=True)  # Field name made lowercase.
    module = models.CharField(max_length=128)
    starttime = models.CharField(db_column='startTime', max_length=256)  # Field name made lowercase.
    endtime = models.CharField(db_column='endTime', max_length=256)  # Field name made lowercase.
    updatetime = models.CharField(db_column='updateTime', max_length=256)  # Field name made lowercase.
    good_me = models.CharField(max_length=256, blank=True, null=True)
    jz_shop_name = models.CharField(max_length=256, blank=True, null=True)
    js_shop_goodid = models.CharField(db_column='js_shop_goodID', max_length=256, blank=True, null=True)  # Field name made lowercase.
    uv = models.IntegerField()
    keyword = models.CharField(max_length=256)
    datetype = models.CharField(db_column='dateType', max_length=256)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CompetingDrainage'


class Downloadoperationhistory(models.Model):
    operationdate = models.CharField(db_column='operationDate', max_length=128)  # Field name made lowercase.
    operationmoulename = models.CharField(db_column='operationMouleName', max_length=258)  # Field name made lowercase.
    downloadcount = models.IntegerField(db_column='downLoadCount')  # Field name made lowercase.
    searchid = models.CharField(max_length=256)
    competinggoodsname = models.CharField(db_column='competingGoodsName', max_length=256)  # Field name made lowercase.
    competingstorename = models.CharField(db_column='competingStoreName', max_length=256)  # Field name made lowercase.
    competinggoodsid = models.CharField(db_column='competingGoodsId', max_length=256)  # Field name made lowercase.
    datetype = models.CharField(db_column='dateType', max_length=256)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DownLoadOperationHistory'


class KeywordsPutonEffect(models.Model):
    primary_key_id = models.AutoField(db_column='Primary_key_ID', primary_key=True)  # Field name made lowercase.
    date = models.CharField(db_column='Date', max_length=255, blank=True, null=True)  # Field name made lowercase.
    promotionplanname = models.CharField(db_column='PromotionPlanName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    babyname = models.CharField(db_column='BabyName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    keywords = models.CharField(db_column='Keywords', max_length=255, blank=True, null=True)  # Field name made lowercase.
    trafficsources = models.CharField(db_column='TrafficSources', max_length=255, blank=True, null=True)  # Field name made lowercase.
    searchtype = models.CharField(db_column='SearchType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    showamount = models.CharField(db_column='ShowAmount', max_length=255, blank=True, null=True)  # Field name made lowercase.
    clickquantity = models.CharField(db_column='ClickQuantity', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cost = models.CharField(db_column='Cost', max_length=255, blank=True, null=True)  # Field name made lowercase.
    clickrate = models.CharField(db_column='ClickRate', max_length=255, blank=True, null=True)  # Field name made lowercase.
    averageshowrank = models.CharField(db_column='AverageShowRank', max_length=255, blank=True, null=True)  # Field name made lowercase.
    averageclickcost = models.CharField(db_column='AverageClickCost', max_length=255, blank=True, null=True)  # Field name made lowercase.
    thousandshowcost = models.CharField(db_column='ThousandShowCost', max_length=255, blank=True, null=True)  # Field name made lowercase.
    clickconversion = models.CharField(db_column='ClickConversion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    directlyclinchdealmoney = models.CharField(db_column='DirectlyClinchdealMoney', max_length=255, blank=True, null=True)  # Field name made lowercase.
    directlyclinchdealcount = models.CharField(db_column='DirectlyClinchdealCount', max_length=255, blank=True, null=True)  # Field name made lowercase.
    indirectclinchdealmoney = models.CharField(db_column='IndirectClinchdealMoney', max_length=255, blank=True, null=True)  # Field name made lowercase.
    indirectclinchdealcount = models.CharField(db_column='IndirectClinchdealCount', max_length=255, blank=True, null=True)  # Field name made lowercase.
    totalclinchdealmoney = models.CharField(db_column='TotalClinchdealMoney', max_length=255, blank=True, null=True)  # Field name made lowercase.
    totalclinchdealcount = models.CharField(db_column='TotalClinchdealCount', max_length=255, blank=True, null=True)  # Field name made lowercase.
    babycollectioncount = models.CharField(db_column='BabyCollectionCount', max_length=255, blank=True, null=True)  # Field name made lowercase.
    storecollectioncount = models.CharField(db_column='StoreCollectionCount', max_length=255, blank=True, null=True)  # Field name made lowercase.
    totalcollectioncount = models.CharField(db_column='TotalCollectionCount', max_length=255, blank=True, null=True)  # Field name made lowercase.
    roi = models.CharField(db_column='ROI', max_length=255, blank=True, null=True)  # Field name made lowercase.
    directlyshoppingcart = models.CharField(db_column='DirectlyShoppingCart', max_length=255, blank=True, null=True)  # Field name made lowercase.
    indirectshoppingcart = models.CharField(db_column='IndirectShoppingCart', max_length=255, blank=True, null=True)  # Field name made lowercase.
    totalshoppingcart = models.CharField(db_column='TotalShoppingCart', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KeyWords_PutOn_Effect'


class Keywordssummary(models.Model):
    primary_key_id = models.AutoField(db_column='Primary_key_ID', primary_key=True)  # Field name made lowercase.
    datetime = models.CharField(db_column='DateTime', max_length=255, blank=True, null=True)  # Field name made lowercase.
    weightpoints = models.CharField(db_column='WeightPoints', max_length=255, blank=True, null=True)  # Field name made lowercase.
    keywords = models.CharField(db_column='Keywords', max_length=255, blank=True, null=True)  # Field name made lowercase.
    industrysearchpopularity = models.CharField(db_column='IndustrySearchPopularity', max_length=255, blank=True, null=True)  # Field name made lowercase.
    industrytransformation = models.CharField(db_column='IndustryTransformation', max_length=255, blank=True, null=True)  # Field name made lowercase.
    visitorstosearch = models.CharField(db_column='VisitorsToSearch', max_length=255, blank=True, null=True)  # Field name made lowercase.
    searchclinchdeal = models.CharField(db_column='SearchClinchDeal', max_length=255, blank=True, null=True)  # Field name made lowercase.
    searchconversion = models.CharField(db_column='SearchConversion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mingconversion = models.CharField(db_column='MingConversion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    competingconversion = models.CharField(db_column='CompetingConversion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    click = models.CharField(db_column='Click', max_length=255, blank=True, null=True)  # Field name made lowercase.
    click_rate = models.CharField(db_column='Click_Rate', max_length=255, blank=True, null=True)  # Field name made lowercase.
    spending = models.CharField(db_column='Spending', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ppc = models.CharField(db_column='PPC', max_length=255, blank=True, null=True)  # Field name made lowercase.
    totalcount = models.CharField(db_column='TotalCount', max_length=255, blank=True, null=True)  # Field name made lowercase.
    conversion = models.CharField(db_column='Conversion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    amount = models.CharField(db_column='Amount', max_length=255, blank=True, null=True)  # Field name made lowercase.
    roi = models.CharField(db_column='ROI', max_length=255, blank=True, null=True)  # Field name made lowercase.
    uv = models.CharField(db_column='UV', max_length=255, blank=True, null=True)  # Field name made lowercase.
    guestunitprice = models.CharField(db_column='GuestUnitPrice', max_length=255, blank=True, null=True)  # Field name made lowercase.
    industryconversionweight = models.CharField(db_column='IndustryConversionWeight', max_length=255, blank=True, null=True)  # Field name made lowercase.
    searchconversionweight = models.CharField(db_column='SearchConversionWeight', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mingconversionweight = models.CharField(db_column='MingConversionWeight', max_length=255, blank=True, null=True)  # Field name made lowercase.
    competingconversionweight = models.CharField(db_column='CompetingConversionWeight', max_length=255, blank=True, null=True)  # Field name made lowercase.
    conversiontotalscore = models.CharField(db_column='ConversionTotalScore', max_length=255, blank=True, null=True)  # Field name made lowercase.
    productname = models.CharField(db_column='ProductName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    searchid = models.CharField(db_column='SearchId', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KeywordsSummary'


class Mainproduct(models.Model):
    primary_key_id = models.AutoField(db_column='Primary_key_ID', primary_key=True)  # Field name made lowercase.
    productname = models.CharField(db_column='ProductName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    searchid = models.CharField(db_column='SearchId', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MainProduct'


class SearchRanklist(models.Model):
    module = models.CharField(max_length=128)
    starttime = models.CharField(max_length=256)
    endtime = models.CharField(max_length=256)
    searchid = models.CharField(max_length=256)
    clickhits = models.IntegerField(db_column='clickHits')  # Field name made lowercase.
    clickrate = models.CharField(db_column='clickRate', max_length=256, blank=True, null=True)  # Field name made lowercase.
    hotsearchrank = models.IntegerField(db_column='hotSearchRank')  # Field name made lowercase.
    ordernum = models.IntegerField(db_column='orderNum')  # Field name made lowercase.
    p4prefprice = models.CharField(db_column='p4pRefPrice', max_length=256, blank=True, null=True)  # Field name made lowercase.
    payrate = models.CharField(db_column='payRate', max_length=256, blank=True, null=True)  # Field name made lowercase.
    seipvuvhits = models.IntegerField(db_column='seIpvUvHits')  # Field name made lowercase.
    searchword = models.CharField(db_column='searchWord', max_length=256)  # Field name made lowercase.
    soarrank = models.CharField(db_column='soarRank', max_length=256)  # Field name made lowercase.
    tmclickrate = models.CharField(db_column='tmClickRate', max_length=256, blank=True, null=True)  # Field name made lowercase.
    primary_key_id = models.AutoField(db_column='Primary_key_ID', primary_key=True)  # Field name made lowercase.
    datetype = models.CharField(db_column='dateType', max_length=256)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Search_RankList'


class Trafficsources(models.Model):
    primary_key_id = models.AutoField(db_column='Primary_key_ID', primary_key=True)  # Field name made lowercase.
    module = models.CharField(max_length=128)
    starttime = models.CharField(db_column='startTime', max_length=256)  # Field name made lowercase.
    endtime = models.CharField(db_column='endTime', max_length=256)  # Field name made lowercase.
    goodid = models.CharField(db_column='goodId', max_length=256)  # Field name made lowercase.
    pagename = models.CharField(db_column='pageName', max_length=256)  # Field name made lowercase.
    datetype = models.CharField(db_column='dateType', max_length=256)  # Field name made lowercase.
    uv = models.IntegerField()
    crtbyrcnt = models.CharField(db_column='crtByrCnt', max_length=256)  # Field name made lowercase.
    crtrate = models.CharField(db_column='crtRate', max_length=256)  # Field name made lowercase.
    pv = models.CharField(max_length=256)
    ratio = models.CharField(max_length=256)
    jpselfuv = models.CharField(db_column='jpSelfUv', max_length=256)  # Field name made lowercase.
    jpuv = models.CharField(db_column='jpUv', max_length=256)  # Field name made lowercase.
    cltcnt = models.CharField(db_column='cltCnt', max_length=256)  # Field name made lowercase.
    cartbyrcnt = models.CharField(db_column='cartByrCnt', max_length=256)  # Field name made lowercase.
    payitmcnt = models.CharField(db_column='payItmCnt', max_length=256)  # Field name made lowercase.
    paybyrcnt = models.CharField(db_column='payByrCnt', max_length=256)  # Field name made lowercase.
    payrate = models.CharField(db_column='payRate', max_length=256)  # Field name made lowercase.
    directpaybyrcnt = models.CharField(db_column='directPayByrCnt', max_length=256)  # Field name made lowercase.
    cltitmpaybyrcnt = models.CharField(db_column='cltItmPayByrCnt', max_length=256)  # Field name made lowercase.
    fanspaybyrcnt = models.CharField(db_column='fansPayByrCnt', max_length=256)  # Field name made lowercase.
    orditmpaybyrcnt = models.CharField(db_column='ordItmPayByrCnt', max_length=256)  # Field name made lowercase.
    itemid = models.CharField(db_column='itemId', max_length=256)  # Field name made lowercase.
    ppageid = models.CharField(db_column='pPageId', max_length=256)  # Field name made lowercase.
    pageid = models.CharField(db_column='pageId', max_length=256)  # Field name made lowercase.
    pagelevel = models.CharField(db_column='pageLevel', max_length=256)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TrafficSources'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DownloadMysql(models.Model):
    download_table = models.CharField(db_column='Download_table', max_length=255, blank=True, null=True)  # Field name made lowercase.
    download_column = models.CharField(db_column='Download_column', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mysql_table = models.CharField(max_length=255, blank=True, null=True)
    mysql_column = models.CharField(max_length=255, blank=True, null=True)
    primary_key_id = models.AutoField(db_column='Primary_key_ID', primary_key=True)  # Field name made lowercase.
    import_time = models.DateTimeField(db_column='Import_time')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'download_mysql'


class Storagefilelocal(models.Model):
    excelfile = models.CharField(db_column='excelFile', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'storagefilelocal'
