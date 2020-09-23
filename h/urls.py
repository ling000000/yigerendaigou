from django.conf.urls import include, url
from h import views
from django.contrib import admin
app_name = 'h'
admin.autodiscover()

urlpatterns = [
#url(r'^article/(?P<help_id>[0-9]+)$',views.help_page,name='help_page'),
    url(r'^sign_up',views.sign_up,name='sign_up'),#注册
    url(r'^sign_in',views.sign_in,name='sign_in'),#登录
    url(r'^h_logout',views.h_logout,name='h_logout'),#退出登录
    url(r'^usermanagement',views.usermanagement,name='usermanagement'),#用户管理
    url(r'^help_h',views.help_h,name='help_h'),#帮助管理
    url(r'^deld_hp/$', views.deld_hp, name='deld_hp'),  # 删除
    url(r'^help_page/(?P<help_id>[0-9]+)$', views.help_page, name='help_page'),
    url(r'^addhelp/(?P<help_id>[0-9]+)$',views.addhelp,name='addhelp'),
    url(r'^add_action',views.add_action,name='add_action'),
    url(r'^announcement', views.announcement,name='announcement'),#公告管理
    url(r'^deld_ac/$', views.deld_ac, name='deld_ac'),#删除公告
    url(r'^a_p/(?P<a_id>[0-9]+)$',views.a_p, name='a_p'),
    url(r'^ad_ac/(?P<a_id>[0-9]+)$', views.ad_ac, name='ad_ac'),
    url(r'^add_ac', views.add_ac, name='add_ac'),
    url(r'^top_up/', views.top_up, name='top_up'),#充值管理
    url(r'^top_up_c', views.top_up_c, name='top_up_c'),
    url(r'^b_shop', views.b_shop, name='b_shop'),#代购
    url(r'^b_cancel',views.b_cancel,name='b_cancel'),
    url(r'^b_pay',views.b_pay,name='b_pay'),
    url(r'^gjyf',views.gjyf,name='gjyf'),
    url(r'^b_complete',views.b_complete,name='b_complete'),
    url(r'^b_delivery',views.b_delivery,name='b_delivery'),
    url(r'^t_shop', views.t_shop, name='t_shop'),#代运
    url(r'^yf',views.yf,name='yf'),
    url(r'^t_cancel', views.t_cancel, name='t_cancel'),
    url(r'^t_pay', views.t_pay, name='t_pay'),
    url(r'^t_complete', views.t_complete, name='t_complete'),
    url(r'^t_delivery', views.t_delivery, name='t_delivery'),
    url(r'^toushu',views.toushu,name='toushu'),#意见投诉
    url(r'^ts_p/(?P<ts_id>[0-9]+)$', views.ts_p, name='ts_p'),#查看详细
    url(r'^de_ts/$', views.de_ts, name='de_ts'),  # 删除投书
    url(r'^op',views.op,name='op'),#操作日志
    url(r'^r_password',views.r_password,name='r_password'),#系统设置
    url(r'^search/$', views.search, name='search'),#投诉搜索
    url(r'^search_u/$', views.search_u, name='search_u'),  # 搜索用户
    url(r'^search_h/$', views.search_h, name='search_h'),  # 搜索帮助
    url(r'^search_a/$', views.search_a, name='search_a'),  # 搜索公告
]