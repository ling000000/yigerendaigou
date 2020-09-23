# coding: utf-8

from itertools import chain
import os
import requests
from urllib import parse
import json
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
from django.contrib import auth
from django.db.models import Q
from django.core import serializers
import gzip
import urllib.request
import re
from django.views.decorators.csrf import csrf_exempt


class UserForm(forms.Form):
    email = forms.EmailField(label='邮    箱')
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密    码', widget=forms.PasswordInput())

#主页
def index(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        a = models.Announcement.objects.all().order_by('-update_time')
        b = models.Help.objects.all().order_by('-update_time')
        c = models.Announcement.objects.all().order_by('-update_time')[:1]
        print(c)
        return render(request, 'yj/index1.html', {'a': a ,'b':b ,'c':c,'u1':u1})
    else:
        a = models.Announcement.objects.all().order_by('-update_time')
        b = models.Help.objects.all().order_by('-update_time')
        c = models.Announcement.objects.all().order_by('-update_time')[:1]
        print(c)
        return render(request, 'yj/index.html', {'a': a,'b':b,'c':c})

#新闻页面
def an_pa(request,an_id):
    print(an_id)
    article = models.Announcement.objects.get(pk=an_id)
    print(article)
    return render(request, 'yj/Article.html',{'a':article})

def help_pa(request,help_id):
    article = models.Help.objects.get(pk=help_id)
    return render(request,'yj/Content.html',{'a':article})

#货币汇率
def hl(request):
    if request.method == 'POST':
        MYR = request.POST.get('MYR')
        CNY = request.POST.get('CNY')
        SGD = request.POST.get('SGD')
        print(MYR,CNY,SGD)
        print(type(MYR))
        if CNY != "":
            # url = 'http: // api.jisuapi.com / exchange / convert?appkey=cad7ad4129f744bd&from=CNY&to=MYR&amount=' + CNY
            appid = "29a963bfdfc5a266af7dcc14fdc00d0a"
            url = "https://api.shenjian.io/exchange/currency/?appid=" + appid + "&form=CNY&to=MYR"
            request_i = urllib.request.Request(url,
                                           headers={
                                               "Accept-Encoding": "gzip",
                                           })

            response = urllib.request.urlopen(request_i)
            gzipFile = gzip.GzipFile(fileobj=response)
            b = gzipFile.read().decode('UTF-8')
            c = eval(b)
            url1 ="https://api.shenjian.io/exchange/currency/?appid=" + appid + "&form=CNY&to=SGD"
            request_i1 = urllib.request.Request(url1,
                                            headers={
                                                "Accept-Encoding": "gzip",
                                            })
            response1 = urllib.request.urlopen(request_i1)
            gzipFile1 = gzip.GzipFile(fileobj=response1)
            b1 = gzipFile1.read().decode('UTF-8')
            c1 = eval(b1)
            a = c['data']['rate']
            a1 = c1['data']['rate']
            a2=float(CNY)
            a3=float(a)
            a4=float(a1)
            d = {'MYR':a2*a3,'SGD':a2*a4,'CNY':a2}
            print(d)
            a = models.Announcement.objects.all().order_by('-update_time')
            help = models.Help.objects.all().order_by('-update_time')
            return render(request, "yj/index.html", {'d': d ,'a':a,'b':help})
        elif MYR != "":
            appid = "29a963bfdfc5a266af7dcc14fdc00d0a"
            url = "https://api.shenjian.io/exchange/currency/?appid=" + appid + "&form=MYR&to=CNY"
            request_i = urllib.request.Request(url,
                                           headers={
                                               "Accept-Encoding": "gzip",
                                           })
            response = urllib.request.urlopen(request_i)
            gzipFile = gzip.GzipFile(fileobj=response)
            b = gzipFile.read().decode('UTF-8')
            c = eval(b)
            print(c)
            url1 = "https://api.shenjian.io/exchange/currency/?appid=" + appid + "&form=MYR&to=SGD"
            request_i1 = urllib.request.Request(url1,
                                            headers={
                                                "Accept-Encoding": "gzip",
                                            })
            response1 = urllib.request.urlopen(request_i1)
            gzipFile1 = gzip.GzipFile(fileobj=response1)
            b1 = gzipFile1.read().decode('UTF-8')
            c1 = eval(b1)
            print(c1)
            a = c['data']['rate']
            a3 = float(a)
            a1 = c1['data']['rate']
            a2 = float(MYR)
            a4 = float(a1)
            a5=a2 * a3
            a6=a2 * a4
            d = {'CNY': a5, 'SGD': a6,'MYR':a2}
            print(d)
            a = models.Announcement.objects.all().order_by('-update_time')
            help = models.Help.objects.all().order_by('-update_time')
            return render(request, "yj/index.html", {'d': d ,'a':a,'b':help})
        elif SGD != "":
            appid = "29a963bfdfc5a266af7dcc14fdc00d0a"
            url = "https://api.shenjian.io/exchange/currency/?appid=" + appid + "&form=SGD&to=CNY"
            request_i = urllib.request.Request(url,
                                           headers={
                                               "Accept-Encoding": "gzip",
                                           })
            response = urllib.request.urlopen(request_i)
            gzipFile = gzip.GzipFile(fileobj=response)
            b = gzipFile.read().decode('UTF-8')
            c = eval(b)
            url1 = "https://api.shenjian.io/exchange/currency/?appid=" + appid + "&form=SGD&to=MYR"
            request_i1 = urllib.request.Request(url1,
                                            headers={
                                                "Accept-Encoding": "gzip",
                                            })
            response1 = urllib.request.urlopen(request_i1)
            gzipFile1 = gzip.GzipFile(fileobj=response1)
            b1 = gzipFile1.read().decode('UTF-8')
            c1 = eval(b1)
            a = c['data']['rate']
            a1 = c1['data']['rate']
            a2 = float(SGD)
            a3 = float(a)
            a4 = float(a1)
            d = {'CNY': a2 * a3, 'MYR': a2 * a4,'SGD':a2}
            print(d)
            a = models.Announcement.objects.all().order_by('-update_time')
            help = models.Help.objects.all().order_by('-update_time')
            return render(request, "yj/index.html", {'d': d,'a':a,'b':help})
        else:
            a = models.Announcement.objects.all().order_by('-update_time')
            help = models.Help.objects.all().order_by('-update_time')
            return render(request,'yj/index.html',{'a':a,'b':help})
    a = models.Announcement.objects.all().order_by('-update_time')
    help = models.Help.objects.all().order_by('-update_time')
    return render(request, 'yj/index.html',{'a':a,'b':help})

def regist(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        cp = request.POST.get('cp')
        print(email, username, password, cp)
        if all ([email , username , password , cp ]):
            str = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
            if re.match(str, email):
                try:#验证邮箱是否使用
                    a = models.User.objects.filter(email__exact=email)
                except Exception as e:
                    a = None
                if a:
                    return render(request, 'yj/register.html', {'error1': '邮箱被使用'})
                try:
                    b = models.User.objects.filter(username__exact=username)
                except Exception as e:
                    b = None
                if b:
                    return render(request,'yj/register.html',{'error2':'用户名已存在'})
                if len(password) < 6:
                    return render(request,'yj/register.html',{'error3':'密码过短'})
                if password != cp:
                    return render(request,'yj/register.html',{'error4':'两次密码不一致'})
                print(email,username,password,cp)
                c = models.User.objects.create(email=email,username=username,password=password,r_money=0.0)
                if c==False:
                    return render(request,'yj/register.html',{'error4':'注册错误'})
                return render(request,'yj/login.html')
            else:
                return render(request, 'yj/register.html', {'error1': '邮箱错误'})
        elif not email:
            return render(request, 'yj/register.html', {'error1':'请输入邮箱'})
        elif not username:
            return render(request,'yj/register.html',{'error2':'请输入用户名'})
        elif not password:
            return render(request, 'yj/register.html', {'error3': '请输入密码'})
        elif not cp:
            return render(request,'yj/register.html',{'error4':'请确认密码'})
    else:
        return render(request,'yj/register.html')

# def regist(request):
#     if request.method == 'POST':
#         uf = UserForm(request.POST)  # 包含用户名和密码
#         if uf.is_valid():
#             # 获取表单数据
#             email = uf.cleaned_data['email']
#             username = uf.cleaned_data['username']  # cleaned_data类型是字典，里面是提交成功后的信息
#             password = uf.cleaned_data['password']
#             str = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
#             print(username,password,email)
#             if re.match(str, email):
#                 registAdd = User.objects.create(username=username, password=password, email=email, r_money=0.00)
#                 print(type(registAdd))
#                 if registAdd == False:
#                     return render(request, 'yj/share1.html', {'registAdd': registAdd, 'username': username})
#                 else:
#                     return render(request, 'yj/share1.html', {'registAdd': registAdd})
#             else:
#                 print('邮箱错误')
#                 return render(request,'yj/registe1.html',{'error':'邮箱错误'})
#     else:
#         uf = UserForm()
#     return render(request, 'yj/register.html', {'uf': uf})

#登录
def do_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        b = models.User.objects.distinct().values("username")
        print(b.values('username'))
        # c = []
        c = list()
        for i in b.values('username'):
            c.append(i['username'])
        print(c)
        if username in c:
            a = models.User.objects.get(username=username)
            if a.password == password:
                u = a.toJSON()
                print(u)
                u1 = eval(u)
                request.session['user111'] = u1
                request.session['is_login'] = True
                id = u1.get('id')
                return render(request, 'yj/userindexs.html', {'user': u1})
            else:  # 数据库里不存在与之对应的数据
                return render(request, 'yj/login.html', {'login_error': '用户名或密码错误'})
        else:  # 数据库里不存在与之对应的数据
            return render(request, 'yj/login.html', {'login_error': '用户名或密码错误'})
    return render(request, 'yj/login.html')


def do_logout(request):
    request.session.clear()
    a = models.Announcement.objects.all().order_by('-update_time')
    help = models.Help.objects.all().order_by('-update_time')
    c = models.Announcement.objects.all().order_by('-update_time')[:1]
    return render(request, 'yj/index.html',{'a':a,'b':help,'c':c})

#重置密码
def r_pass(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        id = u1.get('id')
        a = models.User.objects.get(id=id)
        if request.method=="POST":
            password = request.POST.get('password')
            n_pass = request.POST.get('new_password')
            r_n = request.POST.get('r_new_password')
            if all([password,n_pass,r_n]):
                if password !=a.password:
                    return render(request, 'yj/r_password.html', {'error': '密码错误','user':a})
                if password == n_pass:
                    return render(request, 'yj/r_password.html', {'error': '新旧密码不可相同','user':a})
                if len(n_pass) < 6 :
                    return render(request, 'yj/r_password.html', {'error': '新密码过短','user':a})
                if n_pass != r_n:
                    return render(request, 'yj/r_password.html', {'error': '请确认两次密码相同','user':a})
                else:
                    models.User.objects.filter(id =id ).update(password=n_pass)
                    return render(request, 'yj/login.html')
            else:
                return render(request,'yj/r_password.html',{'error':'请输入完整','user':a})
        return render(request, 'yj/r_password.html', { 'user': a})
    return render(request,'yj/login.html')


#用户中心
def userindexs(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        id =u1.get('id')
        c = models.User.objects.get(id = id)
        # articles = models.User.objects.all()
        print(u1)
        return render(request,'yj/userindexs.html',{'user':c})
    else:
        return render(request,'yj/login.html')


#充值
def top_up_a(request):
    u1 = request.session.get('user111')
    return render(request,'yj/deposit.html',{'user':u1})



def top_up_b(request):
        u1 = request.session.get('user111')
        if request.method == 'POST':
            money = request.POST.get('money')
            # imgurl = request.FILES.get('imgurl')
            img = request.FILES.get('img')
            payment_id = request.POST.get('payment_id')
            id = u1.get('id')
            beizhu = request.POST.get('beizhu')
            u = models.User.objects.get(id=id)
            print(money, img,  u)
            if all([money,img,payment_id]):
                models.Top_up.objects.create(money=money, img=img, u=u, payment_id=payment_id,beizhu=beizhu, state=0)
                u1 = request.session.get('user111')
                print(u1)
                return render(request, 'yj/userindexs.html', {'user': u1})
            else:
                return render(request,'yj/deposit.html',{'user':u1})
        else:
            return render(request, 'yj/login.html')

#充值记录
def paylist(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        id = u1.get('id')
        a = models.User.objects.get(id=id)
        b = models.Top_up.objects.filter(u = id)
        return render(request,'yj/paylist.html',{'user':a,'b':b})
    return render(request,'yj/login.html')

#代购
def addurl(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        # articles = models.User.objects.all()
        print(u1)
        a = request.POST.get('goods_url')
        print(a)
        if a:
            scanUrl = parse.quote_plus(a)
            print(scanUrl)
            appid = "4aa033a06bce9b555fa82509f381866f"
            url = "https://api.shenjian.io/?appid=" + appid + "&scanUrl=" + scanUrl
            request_i = urllib.request.Request(url,
                                               headers={
                                                   "Accept-Encoding": "gzip",
                                               })
            response = urllib.request.urlopen(request_i)
            gzipFile = gzip.GzipFile(fileobj=response)
            b = gzipFile.read().decode('UTF-8')
            c = eval(b)
            print(c)
            if c['error_code'] == 0:
                name = c['data']['product_details']['name']
                print(name)
                img = c['data']['product_details']['images'][1]['image_url'].replace('\\', '')
                print(img)
                u1 = request.session.get('user111')
                id = u1.get('id')
                print(name, id)
                u = models.User.objects.get(id=id)
                b13 = c['data']['product_details']
                print(b13)
                b113 = b13['sku']
                try:
                    b133=b113[0]['values']
                    for b111 in b133:
                        print(2)
                        print(b111)
                        b112=b111['desc']
                        print(3)
                        print(b112)
                    return render(request, 'yj/getproduct.html', {'b': b13,'b11':b113, 'user': u1, 'a': a})
                except Exception as e:
                    xxxxxx=None
                return render(request, 'yj/getproduct.html', {'b': b13, 'b11': b113, 'user': u1, 'a': a})
            else:
                return render(request,'yj/addurl.html',{'user':u1})
        else:
            return render(request, 'yj/addurl.html',{'user':u1})
    else:
        a = models.Announcement.objects.all().order_by('-update_time')
        help = models.Help.objects.all().order_by('-update_time')
        return  render(request,'yj/index.html',{'a':a,'b':help})



def getproduct(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        url = request.POST.get('info_url')
        name=request.POST.get('good_name')
        img2=request.POST.get('pic_url')
        img1=eval(img2)
        img = img1['image_url'].replace('\\', '')
        price1 = request.POST.get('price')
        yunfei1 = request.POST.get('yunfei')
        shuliang1 = request.POST.get('shuliang')
        feilei = request.POST.get('fenlei')
        u1 = request.session.get('user111')
        id = u1.get('id')
        print(price1,yunfei1,shuliang1,id)
        u = models.User.objects.get(id=id)
        print(u)
        if all([price1,yunfei1,shuliang1]):
            price = float(price1)
            yunfei = float(yunfei1)
            shuliang = int(shuliang1)
            zongjia = float(price * shuliang)+yunfei
            print(zongjia)
            models.Buy.objects.create(dj = price,num=shuliang,u=u,feilei=feilei, gn_yunfei=yunfei,gy_yunfei=0, zongjia=zongjia, url=url, name=name, img=img,state=1,payment_id=1,gy_py=1)
            a = models.Buy.objects.filter(u=id)
            print(a)
            # return HttpResponse("添加成功")
            messages.success(request, "添加成功")
            return render(request,'yj/daicai.html',{'user':u1,'a':a})
        elif not yunfei1 or not shuliang1:
            print(2233)
            messages.success(request,"添加失败")
            # return render(request,'yj/deposit.html',{'error':'请输入运费'})
        return render(request,'yj/daicai.html',{'user':u1})

#购物车
def daicai(request):
    if request.session.get('is_login', None):
        # if request.method=='POST':
            u1 = request.session.get('user111')
            id = u1.get('id')
            c = models.Buy.objects.filter(u=id , payment_id=1).values()
            add = models.Address.objects.filter(u=id)
            return render(request, 'yj/daicai.html', {'a': c,'user':u1,'b':add})
    else:
        a = models.Announcement.objects.all().order_by('-update_time')
        help = models.Help.objects.all().order_by('-update_time')
        return render(request,'yj/index.html',{'a':a,'b':help})

#删除购物车商品
def deld_dci(request):
    print(23)
    if request.method=='POST':
        print(1)
        id = request.POST.get('s_id')
        print(id)
        models.Buy.objects.filter(id=id).delete()
        u1 = request.session.get('user111')
        a = u1.get('id')
        c = models.User.objects.get(pk=a)
        print(u1)
        b = models.Buy.objects.filter(payment_id=1,u=c)
        add = models.Address.objects.filter(u=a)
        return render(request,'yj/daicai.html',{'a':b , 'user':u1,'b':add})

#结算
def jiesuan(request):
    u1 = request.session.get('user111')
    id = u1.get('id')
    a = models.User.objects.get(id = id)
    print(a)
    b = serializers.serialize("json", User.objects.filter(id=id))
    print(b)
    c=json.loads(b)
    print(c)
    d = models.Buy.objects.filter(payment_id=1,u=id)
    e = serializers.serialize("json", Buy.objects.filter(u=id))
    print(type(e))
    f = json.loads(e)
    print(type(f))
    sum = 0
    for i in f:
        # print(i)
        sum = sum + int(i['fields']['zongjia'])
    print(sum)
    if sum==0:
        add = models.Address.objects.filter(u=id)
        return render(request, 'yj/daicai.html', {'a': d, 'user': u1,'b':add})
    for i in c:
        print(i['fields']['r_money'])
        x=int(i['fields']['r_money'])
        if x<sum:
            messages.success(request, "余额不足，请充值")
            return render(request,'yj/deposit.html',{'user':u1})
        else:
            y=int(x)-int(sum)
            models.User.objects.filter(id=id).update(r_money=y)
            models.Buy.objects.filter(u=id).update(payment_id=2)
            return render(request,'yj/yue2.html')
    return render(request,'yj/daicai.html',{'a':d , 'user':u1})

#我的订单
def daigouorderlist(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        id = u1.get('id')
        u = models.User.objects.get(id = id)
        r_money = u.r_money
        print(r_money)
        d = models.Buy.objects.filter(payment_id=2, u=id)
        gy_py1 = request.POST.get('gy_py')
        b_id = request.POST.get('b_id')
        gy_yunfei1 = request.POST.get('gy_yunfei')
        print(gy_yunfei1)
        print(type(gy_yunfei1))
        if all([gy_yunfei1,gy_py1]):
            gy_yunfei=float(gy_yunfei1)
            print(gy_yunfei)
            c = models.Buy.objects.get(id=b_id)
            c1 = c.gy_py
            print(c1)
            if gy_yunfei>r_money:
                return render(request,'yj/yue1.html')
            else:
                r_money2 = r_money - gy_yunfei
                print(r_money2)
                gy_py = int(gy_py1)
                print(gy_py)
                if c1 !=gy_py:
                    models.User.objects.filter(id = id).update(r_money=r_money2)
                    models.Buy.objects.filter(id=b_id).update(gy_py=gy_py)
                    return render(request,'yj/yue2.html')
                return render(request, 'yj/daigouorderlist.html', {'a': d, 'user': u1})
        return render(request,'yj/daigouorderlist.html',{'a':d , 'user':u1})
    else:
        a = models.Announcement.objects.all().order_by('-update_time')
        help = models.Help.objects.all().order_by('-update_time')
        return render(request,'yj/index.html',{'a':a,'b':help})

#代运
def addzyorder(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        id = u1.get('id')
        b = models.Address.objects.filter(u = id)
        return render(request, 'yj/addzyorder.html',{'user':u1 , 'b' : b})
    else:
        a = models.Announcement.objects.all().order_by('-update_time')
        help = models.Help.objects.all().order_by('-update_time')
        return render(request,'yj/index.html',{'a':a,'b':help})

def addzy(request):
        if request.method=="POST":
            u1 = request.session.get('user111')
            id = u1['id']
            print(id)
            u = models.User.objects.get(id=id)
            a = request.POST.get('a')#快递号
            b = request.POST.get('b')#物品名称
            c = request.POST.get('c')#数量
            d = request.POST.get('d')#单价
            e = request.POST.get('e')#快递备注
            f = request.POST.get('f')#快递公司
            g = request.POST.get('goodtype')#货物类型
            x = request.POST.get('postway')#运输类型
            y1 = request.POST.get('1')#特殊服务
            y2 = request.POST.get('2')
            y3 = request.POST.get('3')
            y4 = request.POST.get('4')
            z = request.POST.get('txtremark')#备注
            ad = request.POST.get('addr')#地址id
            print(ad)
            if not ad:
                return render(request, 'yj/addzyorder.html', {'error': '请选择收货人地址', 'user': u1})
            addr=models.Address.objects.get(id=ad)
            add = models.Address.objects.filter(u=id)
            if y1==None:
                y1=""
            if y2==None:
                y2=""
            if y3==None:
                y3=""
            if y4==None:
                y4=""
            y=y1+y2+y3+y4
            print(a, b, c, d,  f, g, x, y, addr)
            if all([a,b,c,d,f,g,x,addr]):
                models.Transport.objects.create(ddnum=a, ddname=b, ddsu=c, dddanjia=d, ddbeizhu=e, ddgongsi=f,
                                                lx=g, yslx=x, dsfw=y, beizhu=z, yunfei=0.0, state=1, payment_id=1, u=u, ad=addr)
                w = models.Transport.objects.all()
                return render(request, 'yj/waybill.html', {'x': w, 'user': u1 ,'b':add})
            return render(request,'yj/addzyorder.html',{'error':'请将信息填入完整','user':u1 , 'b' : add})


#我的运单
def waybill(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        id = u1.get('id')
        u = models.User.objects.get(id=id)
        r_money = u.r_money
        yunfei1=request.POST.get('yunfei')
        t_id = request.POST.get('t_id')
        gy_py1 = request.POST.get('py')
        print(gy_py1)
        d = models.Transport.objects.all()
        if all([yunfei1,gy_py1]):
            yunfei = float(yunfei1)
            if yunfei > r_money:
                return render(request, 'yj/yue1.html')
            else:
                r_money2 = r_money - yunfei
                print(r_money2)
                gy_py = int(gy_py1)
                print(gy_py)
                print(t_id)
                c = models.Transport.objects.get(id=t_id)
                c1 = c.payment_id
                if c1 != gy_py:
                    models.User.objects.filter(id=id).update(r_money=r_money2)
                    models.Transport.objects.filter(id=t_id).update(payment_id=gy_py)
                    return render(request, 'yj/yue2.html')
                return render(request, 'yj/waybill.html', {'x': d, 'user': u1})
        return render(request, 'yj/waybill.html',{'x':d, 'user':u1})
    else:
        a = models.Announcement.objects.all().order_by('-update_time')
        help = models.Help.objects.all().order_by('-update_time')
        return render(request,'yj/index.html',{'a':a,'b':help})


#删除地址
def deld_as(request):
    u1 = request.session.get('user111')
    id = request.POST.get('id')
    print(id)
    models.Address.objects.filter(id=id).delete()
    a = models.Address.objects.all()
    return render(request,'yj/useraddress.html',{'a':a, 'user':u1})

#地址管理
def useraddress(request):
    u1 = request.session.get('user111')
    id = request.POST.get('id')
    a=models.Address.objects.filter(u = id)
    print(a)
    return render(request,'yj/useraddress.html',{'a':a , 'user':u1})

def address(request):
    return render(request, 'yj/address.html')

def ad_re(request):
    if request.session.get('is_login', None):
        if request.method == 'POST':
            u1 = request.session.get('user111')
            id = u1['id']
            print(id)
            u = models.User.objects.get(id=id)
            a = request.POST.get('difang')
            b = request.POST.get('name')
            c = request.POST.get('email')
            d = request.POST.get('mailnum')
            e = request.POST.get('phone')
            print(a, b, c, d, e)
            if all([a,b,c,d,e]):
                models.Address.objects.create(u=u, difang=a, name=b, email=c, mailnum=d, phone=e)
                f = models.Address.objects.all()
                print(f)
                return render(request, 'yj/useraddress.html', {'a': f ,'user':u1})
            else:
                return render(request, 'yj/address.html',{'error':'请输入完全'})
    else:
        a = models.Announcement.objects.all().order_by('-update_time')
        help = models.Help.objects.all().order_by('-update_time')
        return render(request,'yj/index.html',{'a':a,'b':help})

@csrf_exempt
#意见投诉
def feedback(request):
    if request.session.get('is_login',None):
        u1 = request.session.get('user111')
        username = u1['username']
        id = u1['id']
        u = models.User.objects.get(id = id)
        if request.method=='POST':
                name = request.POST.get('username')
                phone = request.POST.get('usertel')
                title = request.POST.get('title')
                content = request.POST.get('fcontent')
                print(name,phone,title,content)
                if all([name,phone,title,content]):
                    models.Toushu.objects.create(name=name,phone=phone,title=title,content=content,u=u)
                    return HttpResponse("true")
                    # return render(request,'yj/sbb.html')
                elif not name:
                    return messages.success(request, "请输入姓名")
                elif not phone:
                    return messages.success(request, "请输入电话")
                elif not title:
                    return messages.success(request, "请输入标题")
                elif not content:
                    return messages.success(request, "请输入内容")
                return render(request,'yj/feedback.html',{'user':u1})
        return render(request, 'yj/feedback.html', {'user': u1})
        # return render(request, 'yj/feedback.html', {'user': u1})
    else:
        a = models.Announcement.objects.all().order_by('-update_time')
        help = models.Help.objects.all().order_by('-update_time')
        return render(request,'yj/index.html',{'a':a,'b':help})

# 包裹查询
def packagesearch(request):
    if request.session.get('is_login',None):
        u1 = request.session.get('user111')
        username = u1['username']
        id = u1['id']
        u = models.User.objects.get(id = id)
        if request.method == 'POST':
            a = request.POST.get('number')
            print(a)
            if a!=None:
                number = parse.quote_plus(a)
                type = parse.quote_plus("")
                appid = "6ae76851af0bdcd989061ea7551d15cb"
                # appid = "2d27616d803384b8c0c3438e6a91beb4"
                url = "https://api.shenjian.io/express/query/?appid=" + appid + "&number=" + number + "&type=" + type
                request_i = urllib.request.Request(url,
                                                 headers={
                                                     "Accept-Encoding": "gzip",
                                                 })
                response = urllib.request.urlopen(request_i)
                gzipFile = gzip.GzipFile(fileobj=response)
                b = gzipFile.read().decode('UTF-8')
                print('4=%s'%b)
                b1 =eval(b)
                print(b1)
                try:
                    c = b1['data']['result']['list']
                except Exception as e:
                    return render(request, 'yj/packagesearch.html', {'error':'查询失败', 'user': u1})
                return render(request, 'yj/packagesearch.html', {'c': c,'user':u1})
        else:
            return render(request, 'yj/packagesearch.html', { 'user': u1})
    else:
        return render(request,'yj/login.html')

#我的包裹
def usersongcar(request):
    return render(request,'yj/usersongcar.html')

def wcgnmd(request):
    return render(request,'yj/wcgnmd.html')

def wcnmd2(request):
    return render(request,'yj/wcnmd2.html')

def content_45(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-45.html',{'user':u1})
    else:
        return render(request, 'yj/content-45.html',{'u':'gun'})
def content_46(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-46.html',{'user':u1})
    else:
        return render(request, 'yj/content-46.html',{'u':'gun'})
def content_49(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-49.html',{'user':u1})
    else:
        return render(request, 'yj/content-49.html',{'u':'gun'})
def content_51(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-51.html',{'user':u1})
    else:
        return render(request, 'yj/content-51.html',{'u':'gun'})
def content_53(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-53.html',{'user':u1})
    else:
        return render(request, 'yj/content-53.html',{'u':'gun'})
def content_54(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-54.html',{'user':u1})
    else:
        return render(request, 'yj/content-54.html',{'u':'gun'})
def content_56(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-56.html',{'user':u1})
    else:
        return render(request, 'yj/content-56.html',{'u':'gun'})
def content_57(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-57.html',{'user':u1})
    else:
        return render(request, 'yj/content-57.html',{'u':'gun'})
def content_58(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-58.html',{'user':u1})
    else:
        return render(request, 'yj/content-58.html',{'u':'gun'})
def content_59(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-59.html',{'user':u1})
    else:
        return render(request, 'yj/content-59.html',{'u':'gun'})
# def content_60(request):
#     u1 = request.session.get('user111')
#     return render(request,'yj/content-60.html',{'user':u1})

def content_65(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-65.html',{'user':u1})
    else:
        return render(request, 'yj/content-65.html',{'u':'gun'})
def content_68(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-68.html',{'user':u1})
    else:
        return render(request, 'yj/content-68.html',{'u':'gun'})
def content_70(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-70.html',{'user':u1})
    else:
        return render(request, 'yj/content-70.html',{'u':'gun'})
def content_71(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-71.html',{'user':u1})
    else:
        return render(request, 'yj/content-71.html',{'u':'gun'})
def content_72(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-72.html',{'user':u1})
    else:
        return render(request, 'yj/content-72.html',{'u':'gun'})
def content_73(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-73.html',{'user':u1})
    else:
        return render(request, 'yj/content-73.html',{'u':'gun'})
def content_74(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-74.html',{'user':u1})
    else:
        return render(request, 'yj/content-74.html',{'u':'gun'})

def content_75(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-75.html',{'user':u1})
    else:
        return render(request, 'yj/content-75.html',{'u':'gun'})

def content_77(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-77.html',{'user':u1})
    else:
        return render(request, 'yj/content-77.html',{'u':'gun'})

def content_78(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-78.html',{'user':u1})
    else:
        return render(request, 'yj/content-78.html',{'u':'gun'})

def content_79(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-79.html',{'user':u1})
    else:
        return render(request, 'yj/content-79.html',{'u':'gun'})

def content_80(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-80.html',{'user':u1})
    else:
        return render(request, 'yj/content-80.html',{'u':'gun'})

def content_85(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-85.html',{'user':u1})
    else:
        return render(request, 'yj/content-85.html',{'u':'gun'})
def content_86(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-86.html',{'user':u1})
    else:
        return render(request, 'yj/content-86.html',{'u':'gun'})
def content_87(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-87.html',{'user':u1})
    else:
        return render(request, 'yj/content-87.html',{'u':'gun'})
def content_88(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-88.html',{'user':u1})
    else:
        return render(request, 'yj/content-88.html',{'u':'gun'})
def content_89(request):
    if request.session.get('is_login', None):
        u1 = request.session.get('user111')
        return render(request, 'yj/content-89.html',{'user':u1})
    else:
        return render(request, 'yj/content-89.html',{'u':'gun'})
#ss
# def newindex(request):
#     return render(request,'yj/newindex.html')
@csrf_exempt
def kong(request):
    if request.method=='POST':
        # return HttpResponse("OK")
        name = request.POST.get('name')
        phone = request.POST.get('iphone')
        title = request.POST.get('title')
        content = request.POST.get('content')
        print(name,phone,title,content)
        if all([name, phone, title, content]):
            return HttpResponse("提交成功")
        elif not name:
            return HttpResponse( "请输入姓名")
        elif not phone:
            return HttpResponse( "请输入电话")
        elif not title:
            return HttpResponse( "请输入标题")
        elif not content:
            return HttpResponse("请输入内容")
    else:
        return render(request,'yj/kong.html')

#运费计算
def yunfei(request):
    dm = request.POST.get('dm')#东马
    xm = request.POST.get('xm')#西马
    xjp = request.POST.get('xjp')#新加坡
    quankong = request.POST.get('quankong')#全抛空运
    bankong =request.POST.get('bankong')#半抛空运
    haix = request.POST.get('haix')#海运小包
    hai =request.POST.get('hai')#海运
    chang = request.POST.get('chang')
    kuang = request.POST.get('kuang')
    gao = request.POST.get('gao')
    tiji = (chang * kuang * gao) / 6000  # 体积重
    shiji = request.POST.get('shiji')  # 实际重量
    if dm == 1:#东马
        if quankong == 1:
            if tiji > shiji:
                return tiji
            elif tiji == shiji:
                return tiji
            else:
                return shiji
        elif bankong == 1:
            zhong = (shiji + tiji) / 2
            return zhong
        elif haix == 1:
            if tiji > shiji:
                return tiji
            elif tiji == shiji:
                return tiji
            else:
                return shiji
        elif hai == 1:
            zhong1 = (chang * kuang * gao) / 1000000
    elif xm == 1:#西马
        if quankong == 1:
            if tiji > shiji:
                return tiji
            elif tiji == shiji:
                return tiji
            else:
                return shiji
        elif bankong == 1:
            zhong = (shiji + tiji) / 2
            return zhong
        elif haix == 1:
            if tiji > shiji:
                return tiji
            elif tiji == shiji:
                return tiji
            else:
                return shiji
        elif hai == 1:
            zhong1 = (chang * kuang * gao) / 1000000
    elif xjp == 1:#新加坡
        if quankong == 1:
            if tiji > shiji:
                return tiji
            elif tiji == shiji:
                return tiji
            else:
                return shiji
        elif bankong == 1:
            zhong = (shiji + tiji) / 2
            return zhong
        elif haix == 1:
            if tiji > shiji:
                return tiji
            elif tiji == shiji:
                return tiji
            else:
                return shiji
        elif hai == 1:
            zhong1 = (chang * kuang * gao) / 1000000






