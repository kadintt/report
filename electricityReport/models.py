# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Amingconversion(models.Model):
    primary_key_id = models.AutoField(db_column='Primary_key_ID', primary_key=True)  # Field name made lowercase.
    keywords = models.CharField(db_column='Keywords', max_length=255, blank=True, null=True)  # Field name made lowercase.
    visitors = models.CharField(db_column='Visitors', max_length=255, blank=True, null=True)  # Field name made lowercase.
    number = models.CharField(db_column='Number', max_length=255, blank=True, null=True)  # Field name made lowercase.
    numberconversion = models.CharField(db_column='NumberConversion', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AmingConversion'


class Competingconversion(models.Model):
    primary_key_id = models.AutoField(db_column='Primary_key_ID', primary_key=True)  # Field name made lowercase.
    keywords = models.CharField(db_column='Keywords', max_length=255, blank=True, null=True)  # Field name made lowercase.
    visitors = models.CharField(db_column='Visitors', max_length=255, blank=True, null=True)  # Field name made lowercase.
    number = models.CharField(db_column='Number', max_length=255, blank=True, null=True)  # Field name made lowercase.
    numberconversion = models.CharField(db_column='NumberConversion', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CompetingConversion'


class Industrydata(models.Model):
    keywords = models.CharField(db_column='KeyWords', max_length=255, blank=True, null=True)  # Field name made lowercase.
    date = models.CharField(db_column='Date', max_length=255, blank=True, null=True)  # Field name made lowercase.
    rank = models.CharField(db_column='Rank', max_length=255, blank=True, null=True)  # Field name made lowercase.
    searchnumber = models.CharField(db_column='SearchNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.
    clicknumber = models.CharField(db_column='ClickNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.
    clickrate = models.CharField(db_column='ClickRate', max_length=255, blank=True, null=True)  # Field name made lowercase.
    paymentconversionrate = models.CharField(db_column='PaymentConversionRate', max_length=255, blank=True, null=True)  # Field name made lowercase.
    paynumber = models.CharField(db_column='PayNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.
    primary_key_id = models.AutoField(db_column='Primary_key_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'IndustryData'


class Keywordsdescribe(models.Model):
    primary_key_id = models.AutoField(db_column='Primary_key_ID', primary_key=True)  # Field name made lowercase.
    keywords = models.CharField(db_column='Keywords', max_length=255, blank=True, null=True)  # Field name made lowercase.
    markword = models.CharField(db_column='MarkWord', max_length=255, blank=True, null=True)  # Field name made lowercase.
    noteword = models.CharField(db_column='NoteWord', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KeywordsDescribe'


class Keywordssummary(models.Model):
    primary_key_id = models.AutoField(db_column='Primary_key_ID', primary_key=True)  # Field name made lowercase.
    weightpoints = models.CharField(db_column='WeightPoints', max_length=255, blank=True, null=True)  # Field name made lowercase.
    keywords = models.CharField(db_column='Keywords', max_length=255, blank=True, null=True)  # Field name made lowercase.
    markword = models.CharField(db_column='MarkWord', max_length=255, blank=True, null=True)  # Field name made lowercase.
    noteword = models.CharField(db_column='NoteWord', max_length=255, blank=True, null=True)  # Field name made lowercase.
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

    class Meta:
        managed = False
        db_table = 'KeywordsSummary'


class Selfsearchdata(models.Model):
    date = models.CharField(db_column='Date', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sourcename = models.CharField(db_column='SourceName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    visitors = models.CharField(db_column='Visitors', max_length=255, blank=True, null=True)  # Field name made lowercase.
    views = models.CharField(db_column='Views', max_length=255, blank=True, null=True)  # Field name made lowercase.
    browseproportion = models.CharField(db_column='BrowseProportion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    stationjump = models.CharField(db_column='StationJump', max_length=255, blank=True, null=True)  # Field name made lowercase.
    stationout = models.CharField(db_column='StationOut', max_length=255, blank=True, null=True)  # Field name made lowercase.
    collections = models.CharField(db_column='Collections', max_length=255, blank=True, null=True)  # Field name made lowercase.
    purchasedrepeat = models.CharField(db_column='PurchasedRepeat', max_length=255, blank=True, null=True)  # Field name made lowercase.
    orders = models.CharField(db_column='Orders', max_length=255, blank=True, null=True)  # Field name made lowercase.
    orders_rate = models.CharField(db_column='Orders_Rate', max_length=255, blank=True, null=True)  # Field name made lowercase.
    paypackages = models.CharField(db_column='PayPackages', max_length=255, blank=True, null=True)  # Field name made lowercase.
    paybuyer = models.CharField(db_column='PayBuyer', max_length=255, blank=True, null=True)  # Field name made lowercase.
    paymentconversionrate = models.CharField(db_column='PaymentConversionRate', max_length=255, blank=True, null=True)  # Field name made lowercase.
    directpayment = models.CharField(db_column='DirectPayment', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fanspay = models.CharField(db_column='FansPay', max_length=255, blank=True, null=True)  # Field name made lowercase.
    collectionspay = models.CharField(db_column='CollectionsPay', max_length=255, blank=True, null=True)  # Field name made lowercase.
    repeatbuy = models.CharField(db_column='RepeatBuy', max_length=255, blank=True, null=True)  # Field name made lowercase.
    primary_key_id = models.AutoField(db_column='Primary_key_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SelfSearchData'


class Valueofkeywords(models.Model):
    primary_key_id = models.AutoField(db_column='Primary_key_ID', primary_key=True)  # Field name made lowercase.
    keywords = models.CharField(db_column='KeyWords', max_length=255, blank=True, null=True)  # Field name made lowercase.
    show = models.CharField(db_column='Show', max_length=255, blank=True, null=True)  # Field name made lowercase.
    click = models.CharField(db_column='Click', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ctr = models.CharField(db_column='CTR', max_length=255, blank=True, null=True)  # Field name made lowercase.
    spending = models.CharField(db_column='Spending', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ppc = models.CharField(db_column='PPC', max_length=255, blank=True, null=True)  # Field name made lowercase.
    totalcount = models.CharField(db_column='TotalCount', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cvr = models.CharField(db_column='CVR', max_length=255, blank=True, null=True)  # Field name made lowercase.
    amount = models.CharField(db_column='Amount', max_length=255, blank=True, null=True)  # Field name made lowercase.
    roi = models.CharField(db_column='ROI', max_length=255, blank=True, null=True)  # Field name made lowercase.
    uv = models.CharField(db_column='UV', max_length=255, blank=True, null=True)  # Field name made lowercase.
    guestunitprice = models.CharField(db_column='GuestUnitPrice', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ValueOfKeyWords'


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
