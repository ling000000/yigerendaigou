# coding: utf-8

from itertools import chain
import os
import requests
from urllib import parse
import json
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response,render,redirect,HttpResponseRedirect
from django.http import  HttpResponse,Http404
from h.forms import *
from h.models import *
from django.template import RequestContext
from django.contrib.auth import login,logout,authenticate
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from django.db.models import F
# from h.kuaidi import *
import time
from django.contrib.admin.views.decorators import staff_member_required  #装饰器
from h import models
from django.contrib import auth, messages
from django.db.models import Q
from django.core import serializers
import gzip
import urllib.request





#后台注册登录
class AdminForm(forms.Form):
    adminname = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密    码', widget=forms.PasswordInput())

def sign_up(request):
    if request.method == 'POST':
        uf = AdminForm(request.POST)  # 包含用户名和密码
        if uf.is_valid():
            # 获取表单数据
            adminname = uf.cleaned_data['adminname']  # cleaned_data类型是字典，里面是提交成功后的信息
            password = uf.cleaned_data['password']
            registAdd = Admin.objects.create(adminname=adminname, password=password)
            if registAdd == False:
                return render(request, 'dgfp_42_hr/share1.html', {'registAdd': registAdd, 'adminname': adminname})
            else:
                return render(request, 'dgfp_42_hr/share1.html', {'registAdd': registAdd})
    else:
        uf = AdminForm()
    return render(request, 'dgfp_42_hr/sign-up.html', {'uf': uf})

#登录
def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        if all([username,password]):
            try:
                a = models.Admin.objects.filter(adminname__exact=username)
            except Exception as e:
                a = None
            if  not a:
                return render(request, 'dgfp_42_hr/sign-in.html', {'error': '用户名或密码错误'})
            a = models.Admin.objects.get(adminname=username)
            if a.password == password:
                u = a.toJSON()
                print(u)
                u1 = eval(u)
                request.session['adminuser'] = u1
                request.session['sign_in'] = True
                u = models.User.objects.all()
                return render(request, 'dgfp_42_hr/usermanagement.html',{'a': u,'u':a})
            else:  # 数据库里不存在与之对应的数据
                return render(request, 'dgfp_42_hr/sign-in.html', {'error': '用户名或密码错误'})
        else:
            return render(request,'dgfp_42_hr/sign-in.html',{'error':'请输入用户名或密码'})
    return render(request, 'dgfp_42_hr/sign-in.html')

def h_logout(request):
    request.session.clear()
    return render(request, 'dgfp_42_hr/sign-in.html')

#后台-主页
def usermanagement(request):
    if request.session.get('sign_in', None):
        a = models.User.objects.all()
        u = request.session.get('adminuser')
        id = u['id']
        name = models.Admin.objects.get(id=id)
        print(name)
        # adminname=name['adminname']
        # print(adminname)
        return render(request, 'dgfp_42_hr/usermanagement.html', {'a': a,'u':name})
    else:
        return render(request, 'dgfp_42_hr/sign-in.html')

#搜索用户
def search_u(request):
    q = request.GET.get('q')
    error_msg = ''
    u = request.session.get('adminuser')
    id2 = u['id']
    name = models.Admin.objects.get(id=id2)
    if not q:
        error_msg = '请输入关键词'
        return render(request, 'dgfp_42_hr/usermanagement.html', {'error_msg': error_msg,'u':name})
    post_list = models.User.objects.filter(username__icontains=q)
    # print(q)
    # q1 = '%'+q+'%'
    # print(q1)
    # post_list = models.Toushu.objects.raw('SELECT * FROM h_toushu a LEFT JOIN  h_user b ON a.u_id=b.id WHERE a.title like %s',[q1])
    print(post_list)
    return render(request, 'dgfp_42_hr/usermanagement.html', {'error_msg': error_msg,'a': post_list,'u':name})

#删除
# def deld(request):
#     id = request.POST.get('id')
#     print(id)
#     models.Transport.objects.filter(id=id).delete()
#     return render(request,'yj/addzyorder.html')

#后台-充值
def top_up(request):
    if request.session.get('sign_in', None):
        d = models.Top_up.objects.raw(
            'SELECT * FROM h_top_up a LEFT JOIN h_user b ON a.u_id= b.id WHERE a.state = 0 ')
        u = request.session.get('adminuser')
        id2 = u['id']
        name = models.Admin.objects.get(id=id2)
        if request.method=='POST':
            state1 = request.POST.get('state')
            print(state1)
            id = request.POST.get('id')
            state_x = request.POST.get('state_x')
            je1 = request.POST.get('je')
            qr1 = request.POST.get('qr')
            print(state_x)
            if all([je1,qr1]):
                state = int(state1)
                a1 = request.POST.get('r_money')
                b1 = request.POST.get('money')
                a = float(a1)
                b = float(b1)
                je = float(je1)
                qr = float(qr1)
                if b==je and je ==qr:
                    r_money = a + b
                    u = models.Top_up.objects.get(id = id)
                    models.Top_up.objects.filter(id=id).update(state=state,money=0)
                    models.User.objects.filter(id = u.u.id).update(r_money=r_money)
                    messages.success(request, "成功")
                elif b!=je:
                    messages.success(request, "输入金额错误")
                else:
                    messages.success(request, "两次输入不同")
            elif not qr1 or not je1:
                messages.success(request, "输入金额")
            else:
                    models.Top_up.objects.filter(id=id).update(state=state_x)
            # return render(request,'dgfp_42_hr/top_up_c.html')
        return render(request,'dgfp_42_hr/top_up.html',{'top': d,'u':name})
    else:
        return render(request, 'dgfp_42_hr/sign-in.html')

#后台—充值完成
def top_up_c(request):
    if request.session.get('sign_in', None):
        u = request.session.get('adminuser')
        id2 = u['id']
        name = models.Admin.objects.get(id=id2)
        d = models.Top_up.objects.raw(
            'SELECT * FROM h_top_up a LEFT JOIN h_user b ON a.u_id= b.id WHERE a.state != 0 ')
        return render(request, 'dgfp_42_hr/top_up_c.html', {'top': d,'u':name})

    else:
        return render(request, 'dgfp_42_hr/sign-in.html')

#后台-代购
def b_shop(request):
    if request.session.get('sign_in', None):
        u = request.session.get('adminuser')
        id2 = u['id']
        name = models.Admin.objects.get(id=id2)
        a = models.Buy.objects.raw(
            'SELECT * FROM h_buy a LEFT JOIN  h_user b ON a.u_id=b.id WHERE a.state = 1 AND a.payment_id = 1')
        return render(request, 'dgfp_42_hr/b_shop.html', {'buy': a,'u':name})
    else:
        return render(request, 'dgfp_42_hr/sign-in.html')

#设置国际运费
def gjyf(request):
    if request.method=='POST':
        a = models.Buy.objects.raw(
            'SELECT * FROM h_buy a LEFT JOIN  h_user b ON a.u_id=b.id WHERE a.state = 1 AND a.payment_id = 2')
        id = request.POST.get('id')
        gjyf = request.POST.get('gjyf')
        u = request.session.get('adminuser')
        id2 = u['id']
        name = models.Admin.objects.get(id=id2)
        if gjyf:
            models.Buy.objects.filter(id=id).update(gy_yunfei=gjyf)  # 设置国际运费
            return render(request, 'dgfp_42_hr/b_pay.html', {'a': a,'u':name})
        else:
            return render(request, 'dgfp_42_hr/b_pay.html', {'a': a})


#未支付国际运费
def b_pay(request):
    if request.session.get('sign_in', None):
        a = models.Buy.objects.raw(
            'SELECT * FROM h_buy a LEFT JOIN  h_user b ON a.u_id=b.id WHERE a.state = 1 AND a.payment_id = 2')
        state1 = request.POST.get('state')
        id =request.POST.get('id')
        u = request.session.get('adminuser')
        id2 = u['id']
        name = models.Admin.objects.get(id=id2)
        if state1 !=None:
            state = int(state1)
            if state == 3:
                models.Buy.objects.filter(id=id).update(state=state)
        return render(request, 'dgfp_42_hr/b_pay.html', {'a': a,'u':name})
    else:
        return render(request,'dgfp_42_hr/sign-in.html')
#待发货
def b_delivery(request):
    if request.session.get('sign_in', None):
        a = models.Buy.objects.raw('SELECT * FROM h_buy a LEFT JOIN  h_user b ON a.u_id=b.id WHERE a.state = 3 ')
        state1 = request.POST.get('state')
        id = request.POST.get('id')
        u = request.session.get('adminuser')
        id2 = u['id']
        name = models.Admin.objects.get(id=id2)
        if state1 != None:
            state = int(state1)
            if state == 4:
                models.Buy.objects.filter(id=id).update(state=state)
        return render(request,'dgfp_42_hr/b_delivery.html',{'a':a,'u':name})
    else:
        return render(request,'dgfp_42_hr/sign-in.html')
#未完成
def b_cancel(request):
    if request.session.get('sign_in', None):
        a = models.Buy.objects.raw('SELECT * FROM h_buy a LEFT JOIN  h_user b ON a.u_id=b.id WHERE a.state = 4 AND a.gy_py=2')
        state1 = request.POST.get('state')
        id = request.POST.get('id')
        u = request.session.get('adminuser')
        id2 = u['id']
        name = models.Admin.objects.get(id=id2)
        if state1 != None:
            state = int(state1)
            if state == 5:
                models.Buy.objects.filter(id=id).update(state=state)
        return render(request,'dgfp_42_hr/b_cancel.html',{'a':a,'u':name})
    else:
        return render(request,'dgfp_42_hr/sign-in.html')
#已完成
def b_complete(request):
    if request.session.get('sign_in', None):
        a = models.Buy.objects.raw('SELECT * FROM h_buy a LEFT JOIN  h_user b ON a.u_id=b.id WHERE a.state = 5 AND a.gy_py=2')
        u = request.session.get('adminuser')
        id2 = u['id']
        name = models.Admin.objects.get(id=id2)
        return render(request,'dgfp_42_hr/b_complete.html',{'a':a,'u':name})
    else:
        return render(request,'dgfp_42_hr/sign-in.html')

#设置国际运费
def yf(request):
    if request.method=='POST':
        a = models.Transport.objects.raw(
            'SELECT * FROM h_transport a LEFT JOIN  h_user b ON a.u_id=b.id LEFT JOIN h_address c ON a.ad_id = c.id WHERE a.state =1 ')
        id = request.POST.get('id')
        yunfei = request.POST.get('yunf')
        u = request.session.get('adminuser')
        id2 = u['id']
        name = models.Admin.objects.get(id=id2)
        print(yunfei)
        print(type(yunfei))
        if yunfei :
            models.Transport.objects.filter(id=id).update(yunfei=yunfei)  # 设置国际运费
            return render(request, 'dgfp_42_hr/t_shop.html', {'a': a,'u':name})
        else:
            return render(request, 'dgfp_42_hr/t_shop.html', {'a': a,'u':name})

#后台-代运
def t_shop(request):
    if request.session.get('sign_in', None):
        a = models.Transport.objects.raw(
            'SELECT * FROM h_transport a LEFT JOIN  h_user b ON a.u_id=b.id LEFT JOIN h_address c ON a.ad_id = c.id WHERE a.state =1 ')
        id = request.POST.get('id')
        state1 = request.POST.get('state')
        print(id)
        print(state1)
        u = request.session.get('adminuser')
        id2 = u['id']
        name = models.Admin.objects.get(id=id2)
        if state1 != None:
            state = int(state1)
            if state == 3:
                models.Transport.objects.filter(id=id).update(state=state)
        return render(request, 'dgfp_42_hr/t_shop.html', {'a': a,'u':name})
    else:
        return render(request, 'dgfp_42_hr/sign-in.html')

def t_pay(request):
    if request.session.get('sign_in', None):
        u = request.session.get('adminuser')
        id2 = u['id']
        name = models.Admin.objects.get(id=id2)
        a = models.Transport.objects.raw(
            'SELECT * FROM h_transport a LEFT JOIN  h_user b ON a.u_id=b.id LEFT JOIN h_address c ON a.ad_id = c.id WHERE a.state =3 AND a.payment_id=1')
        return render(request,'dgfp_42_hr/t_pay.html',{'a':a,'u':name})
    else:
        return render(request,'dgfp_42_hr/sign-in.html')

def t_delivery(request):
    if request.session.get('sign_in', None):
        a = models.Transport.objects.raw(
            'SELECT * FROM h_transport a LEFT JOIN  h_user b ON a.u_id=b.id LEFT JOIN h_address c ON a.ad_id = c.id WHERE a.state =3 AND a.payment_id=2')
        id = request.POST.get('id')
        state1 = request.POST.get('state')
        u = request.session.get('adminuser')
        id2 = u['id']
        name = models.Admin.objects.get(id=id2)
        if state1 != None:
            state = int(state1)
            if state == 4:
                models.Transport.objects.filter(id=id).update(state=state)
        return render(request,'dgfp_42_hr/t_delivery.html',{'a':a,'u':name})
    else:
        return render(request,'dgfp_42_hr/sign-in.html')

def t_cancel(request):
    if request.session.get('sign_in', None):
        a = models.Transport.objects.raw(
            'SELECT * FROM h_transport a LEFT JOIN  h_user b ON a.u_id=b.id LEFT JOIN h_address c ON a.ad_id = c.id WHERE a.state =4 AND a.payment_id=2')
        id = request.POST.get('id')
        state1 = request.POST.get('state')
        u = request.session.get('adminuser')
        id2 = u['id']
        name = models.Admin.objects.get(id=id2)
        if state1 != None:
            state = int(state1)
            if state == 5:
                models.Transport.objects.filter(id=id).update(state=state)
        return render(request,'dgfp_42_hr/t_cancel.html',{'a':a,'u':name})
    else:
        return render(request,'dgfp_42_hr/sign-in.html')

def t_complete(request):
    if request.session.get('sign_in', None):
        u = request.session.get('adminuser')
        id2 = u['id']
        name = models.Admin.objects.get(id=id2)
        a = models.Transport.objects.raw(
            'SELECT * FROM h_transport a LEFT JOIN  h_user b ON a.u_id=b.id LEFT JOIN h_address c ON a.ad_id = c.id WHERE a.state =5 AND a.payment_id=2')
        return render(request,'dgfp_42_hr/t_complete.html',{'a':a,'u':name})
    else:
        return render(request,'dgfp_42_hr/sign-in.html')

#帮助管理
def help_h(request):
    if request.session.get('sign_in', None):
        print(965)
        articles = models.Help.objects.all().order_by('-update_time')
        u = request.session.get('adminuser')
        id2 = u['id']
        name = models.Admin.objects.get(id=id2)
        return render(request, 'dgfp_42_hr/help_h.html', {'articles': articles,'u':name})
    else:
        return render(request, 'dgfp_42_hr/sign-in.html')

#搜索帮助
def search_h(request):
    q = request.GET.get('q')
    error_msg = ''
    u = request.session.get('adminuser')
    id2 = u['id']
    name = models.Admin.objects.get(id=id2)
    if not q:
        error_msg = '请输入关键词'
        return render(request, 'dgfp_42_hr/help_h.html', {'error_msg': error_msg,'u':name})
    post_list = models.Help.objects.filter(title__icontains=q)
    # print(q)
    # q1 = '%'+q+'%'
    # print(q1)
    # post_list = models.Toushu.objects.raw('SELECT * FROM h_toushu a LEFT JOIN  h_user b ON a.u_id=b.id WHERE a.title like %s',[q1])
    print(post_list)
    return render(request, 'dgfp_42_hr/help_h.html', {'error_msg': error_msg,'articles': post_list,'u':name})

def help_page(request,help_id):
    print(help_id)
    article = models.Help.objects.get(pk=help_id)
    print(article)
    return render(request, 'dgfp_42_hr/help_page.html',{'article':article})

def addhelp(request,help_id):
    if str(help_id) == '0':
        return  render(request, 'dgfp_42_hr/addhelp.html')
    a = models.Help.objects.get(pk=help_id)
    return render(request, 'dgfp_42_hr/addhelp.html', {'article': a})
    # return render(request, 'dgfp_42_hr/addhelp.html')

def add_action(request):
    title = request.POST.get('title', 'TITLE')
    content = request.POST.get('content', 'CONTENT')
    help_id = request.POST.get('a_id','0')
    # models.Help.objects.create(title=title,content=content)
    articles = models.Help.objects.all().order_by('-update_time')
    u = request.session.get('adminuser')
    id2 = u['id']
    name = models.Admin.objects.get(id=id2)
    # return render(request,'dgfp_42_hr/help_h.html',{'articles':articles,'u':name})
    if not help_id:
        models.Help.objects.create(title=title,content=content)
        return render(request,'dgfp_42_hr/help_h.html',{'articles':articles,'u':name})
    try:
        article = models.Help.objects.get(pk=help_id)
    except Exception as e:
        return render(request,'dgfp_42_hr/help_h.html',{'articles':articles,'u':name})
    article.title = title
    article.content = content
    article.save()
    return render(request, 'dgfp_42_hr/help_h.html', {'articles': articles,'u':name})

#删除帮助
def deld_hp(request):
    if request.method=='POST':
        print(1)
        id = request.POST.get('id')
        print(id)
        models.Help.objects.filter(id=id).delete()
        a = models.Help.objects.all()
        u = request.session.get('adminuser')
        id2 = u['id']
        name = models.Admin.objects.get(id=id2)
        return render(request,'dgfp_42_hr/help_h.html',{'articles':a,'u':name})
    # return HttpResponse("chenggeng")

#删除公告
def deld_ac(request):
    print(23232)
    id = request.POST.get('id')
    print(id)
    models.Announcement.objects.filter(id=id).delete()
    a = models.Announcement.objects.all()
    u = request.session.get('adminuser')
    id2 = u['id']
    name = models.Admin.objects.get(id=id2)
    return render(request,'dgfp_42_hr/announcement.html',{'articles':a,'u':name})

#公告管理
def announcement(request):
    if request.session.get('sign_in', None):
        articles = models.Announcement.objects.all().order_by('-update_time')
        u = request.session.get('adminuser')
        id2 = u['id']
        name = models.Admin.objects.get(id=id2)
        return render(request, 'dgfp_42_hr/announcement.html', {'articles': articles,'u':name})
    else:
        return render(request, 'dgfp_42_hr/sign-in.html')

#搜索公告
def search_a(request):
    q = request.GET.get('q')
    error_msg = ''
    u = request.session.get('adminuser')
    id2 = u['id']
    name = models.Admin.objects.get(id=id2)
    if not q:
        error_msg = '请输入关键词'
        return render(request, 'dgfp_42_hr/help_h.html', {'error_msg': error_msg,'u':name})
    post_list = models.Announcement.objects.filter(title__icontains=q)
    # print(q)
    # q1 = '%'+q+'%'
    # print(q1)
    # post_list = models.Toushu.objects.raw('SELECT * FROM h_toushu a LEFT JOIN  h_user b ON a.u_id=b.id WHERE a.title like %s',[q1])
    print(post_list)
    return render(request, 'dgfp_42_hr/help_h.html', {'error_msg': error_msg,'articles': post_list,'u':name})

def a_p(request,a_id):
    article = models.Announcement.objects.get(pk=a_id)
    return render(request, 'dgfp_42_hr/a_p.html',{'article':article})

def ad_ac(request,a_id):
    print(1)
    if str(a_id) == '0':
        return  render(request, 'dgfp_42_hr/ad_ac.html')
    a = models.Announcement.objects.get(pk=a_id)
    return render(request, 'dgfp_42_hr/ad_ac.html', {'article': a})


def add_ac(request):
    title = request.POST.get('title', 'TITLE')
    content = request.POST.get('content', 'CONTENT')
    print(title,content)
    a_id = request.POST.get('a_id','0')
    u = request.session.get('adminuser')
    id2 = u['id']
    name = models.Admin.objects.get(id=id2)
    articles = models.Announcement.objects.all().order_by('-update_time')
    print(a_id)
    print(type(a_id))
    if not a_id:
        print(a_id)
        models.Announcement.objects.create(title=title,content=content)
        return render(request,'dgfp_42_hr/announcement.html',{'articles':articles,'u':name})
    article = models.Announcement.objects.get(pk=a_id)
    article.title = title
    article.content = content
    article.save()
    return render(request, 'dgfp_42_hr/announcement.html', {'articles': articles,'u':name})


#意见投诉
def toushu(request):
    if request.session.get('sign_in', None):
        u = request.session.get('adminuser')
        id2 = u['id']
        name = models.Admin.objects.get(id=id2)
        a = models.Transport.objects.raw(
            'SELECT * FROM h_toushu a LEFT JOIN  h_user b ON a.u_id=b.id ')
        return render(request, 'dgfp_42_hr/toushu.html', {'a': a, 'u': name})
    else:
        return render(request, 'dgfp_42_hr/sign-in.html')

#搜索投诉
def search(request):
    q = request.GET.get('q')
    error_msg = ''
    u = request.session.get('adminuser')
    id2 = u['id']
    name = models.Admin.objects.get(id=id2)
    if not q:
        error_msg = '请输入关键词'
        return render(request, 'dgfp_42_hr/toushu.html', {'error_msg': error_msg,'u':name})
    # post_list = models.Toushu.objects.filter(title__icontains=q)
    print(q)
    q1 = '%'+q+'%'
    print(q1)
    post_list = models.Toushu.objects.raw('SELECT * FROM h_toushu a LEFT JOIN  h_user b ON a.u_id=b.id WHERE a.title like %s',[q1])
    print(post_list)
    return render(request, 'dgfp_42_hr/toushu.html', {'error_msg': error_msg,'a': post_list,'u':name})

#查看详情
def ts_p(request,ts_id):
    a = models.Toushu.objects.get(pk=ts_id)
    return render(request,'dgfp_42_hr/ts_p.html',{'a':a})


#删除投诉
def de_ts(request):
    if request.method=='POST':
        id = request.POST.get('id')
        print(id)
        models.Toushu.objects.filter(id=id).delete()
        a = models.Toushu.objects.raw(
            'SELECT * FROM h_toushu a LEFT JOIN  h_user b ON a.u_id=b.id ')
        u = request.session.get('adminuser')
        id2 = u['id']
        name = models.Admin.objects.get(id=id2)
        return render(request, 'dgfp_42_hr/toushu.html', {'a': a, 'u': name})
    else:
        a = models.Toushu.objects.raw(
            'SELECT * FROM h_toushu a LEFT JOIN  h_user b ON a.u_id=b.id ')
        u = request.session.get('adminuser')
        id2 = u['id']
        name = models.Admin.objects.get(id=id2)
        return render(request, 'dgfp_42_hr/toushu.html', {'a': a, 'u': name})


#操作日志
def op(request):
    u = request.session.get('adminuser')
    id2 = u['id']
    name = models.Admin.objects.get(id=id2)
    return render(request,'dgfp_42_hr/operation.html',{'u':name})

#系统设置
def r_password(request):
    if request.session.get('sign_in', None):
        u = request.session.get('adminuser')
        id2 = u['id']
        name2 = models.Admin.objects.get(id=id2)
        if request.method == 'POST':
            name = request.POST.get('name')
            jmm = request.POST.get('jmm')
            xmm = request.POST.get('xmm')
            qd = request.POST.get('qd')
            if all([name, jmm, xmm, qd]):
                try:
                    a = models.Admin.objects.filter(adminname__exact=name)#a是否存在
                    print(2)
                except Exception as e:
                    a =None
                    print(23)
                if a == None:
                    return render(request, 'dgfp_42_hr/r_password.html', {'error1': '用户名错误', 'u': name2})
                b =models.Admin.objects.get(adminname=name)
                if b.password != jmm:
                    return render(request, 'dgfp_42_hr/r_password.html', {'error2': '密码错误', 'u': name2})
                if jmm == xmm:
                    return render(request,'dgfp_42_hr/r_password.html',{'error3':'两次密码不能相同'})
                if xmm !=qd:
                    return render(request, 'dgfp_42_hr/r_password.html', {'error4': '确认密码不相同', 'u': name2})
                models.Admin.objects.filter(adminname=name).update(password = xmm)
                return render(request,'dgfp_42_hr/sign-in.html')
            elif not name:
                return render(request, 'dgfp_42_hr/r_password.html', {'error1': '请输入用户名','u':name2})
            elif not jmm:
                return render(request, 'dgfp_42_hr/r_password.html', {'error2': '请输入原密码','u':name2})
            elif not xmm:
                return render(request, 'dgfp_42_hr/r_password.html', {'error3': '请输入新密码','u':name2})
            elif not qd:
                return render(request, 'dgfp_42_hr/r_password.html', {'error4': '请确认新密码','u':name2})

        return render(request, 'dgfp_42_hr/r_password.html')



