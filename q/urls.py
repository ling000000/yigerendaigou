from django.conf.urls import include, url
from q import views
from django.contrib import admin
app_name = 'q'
admin.autodiscover()

urlpatterns = [
    url(r'^index/',views.index,name='index'),
    url(r'^an_pa/(?P<an_id>[0-9]+)$', views.an_pa, name='an_pa'),#公告详情
    url(r'^help_pa/(?P<help_id>[0-9]+)$', views.help_pa, name='help_pa'),  # 帮助详情
    url(r'^index/',views.hl,name='hl'),
    url(r'^do_reg/', views.regist,name='do_reg'),
    url(r'^login/',views.do_login,name='login'),
    url(r'^logout/',views.do_logout,name='logout'),
    url(r'^r_pass',views.r_pass,name='r_pass'),
    url(r'^userindex', views.userindexs, name='userindex'),
    url(r'^top_up_a',views.top_up_a,name='top_up_a'),
    url(r'^top_up_b',views.top_up_b,name='top_up_b'),
    url(r'^paylist',views.paylist,name='paylist'),
    url(r'^addurl',views.addurl,name='addurl'),
    # url(r'^trys',views.trys,name='trys'),
    url(r'^getproduct',views.getproduct,name='getproduct'),
    url(r'^daicai',views.daicai,name='daicai'),
    url(r'^deld_dci/$',views.deld_dci,name='deld_dci'), #删除购物车商品
    url(r'^jiesuan',views.jiesuan,name='jiesuan'),
    url(r'^daigouorderlist',views.daigouorderlist,name='daigouorderlist'),
    url(r'^addzyorder',views.addzyorder,name='addzyorder'),#代运主页
    url(r'^addzy', views.addzy, name='addzy'),#代运功能
    url(r'^waybill',views.waybill,name='waybill'),#我的运单
    url(r'^deld_as/$',views.deld_as,name='deld_as'), #删除地址
    url(r'^useraddress',views.useraddress,name='useraddress'),
    url(r'^address',views.address,name='address'),
    url(r'^ad_re',views.ad_re,name='ad_re'),
    url(r'^feedback',views.feedback,name='feedback'),
    url(r'^packeagesearch',views.packagesearch,name='packagesearch'),#包裹查询
    url(r'^usersongcar',views.usersongcar,name='usersongcar'),#我的包裹
    url(r'^wcgnmd',views.wcgnmd,name='wcgnmd'),
    url(r'^wcnmd2',views.wcnmd2,name='wcnmd2'),
    url(r'^content-80', views.content_80, name='content-80'),
    url(r'^content-49', views.content_49, name='content-49'),
    url(r'^content-51', views.content_51, name='content-51'),
    url(r'^content-54', views.content_54, name='content-54'),
    url(r'^content-56', views.content_56, name='content-56'),
    url(r'^content-57', views.content_57, name='content-57'),
    url(r'^content-58', views.content_58, name='content-58'),
    url(r'^content-59', views.content_59, name='content-59'),
    url(r'^content-68', views.content_68, name='content-68'),
    url(r'^content-65', views.content_65, name='content-65'),
    url(r'^content-70', views.content_70, name='content-70'),
    url(r'^content-71', views.content_71, name='content-71'),
    url(r'^content-72', views.content_72, name='content-72'),
    url(r'^content-73', views.content_73, name='content-73'),
    url(r'^content-74', views.content_74, name='content-74'),
    url(r'^content-75', views.content_75, name='content-75'),
    url(r'^content-77', views.content_77, name='content-77'),
    url(r'^content-78', views.content_78, name='content-78'),
    url(r'^content-79', views.content_79, name='content-79'),
    url(r'^content-53', views.content_53, name='content-53'),
    url(r'^content-85', views.content_85, name='content-85'),
    url(r'^content-86', views.content_86, name='content-86'),
    url(r'^content-87', views.content_87, name='content-87'),
    url(r'^content-88', views.content_88, name='content-88'),
    url(r'^content-89', views.content_89, name='content-89'),



    # url(r'^newindex',views.newindex,name='newindex'),
    # url(r'^p1',views.p1,name='p1'),
    # url(r'^p2',views.p2,name='p2'),
    url(r'^kong',views.kong,name='kong'),
    ]