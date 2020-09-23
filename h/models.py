# coding:utf-8
from __future__ import unicode_literals
from tinymce.models import HTMLField
import tinymce
from django.db import models
from django.db.models.functions import datetime
#用户
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    r_money = models.FloatField()#余额
    email = models.EmailField()
    update_time = models.DateTimeField(auto_now=True)

    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            else:
                d[attr] = getattr(self, attr)

        import json
        return json.dumps(d)

#帮助
class Help(models.Model):
    title = models.CharField(max_length=322)
    content = tinymce.models.HTMLField(verbose_name="文章详细")
    update_time = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.title

#公告
class Announcement(models.Model):
    title = models.CharField(max_length=322)
    content = models.TextField(null=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

#充值
class Top_up(models.Model):
    u = models.ForeignKey(User,on_delete=models.CASCADE)
    choice =((1,'已充值'),(2,'已驳回'),(0,'未充值'))
    state = models.IntegerField(choices=choice)#支付状态
    money = models.FloatField()#充值金额
    img = models.ImageField(upload_to='static/img')
    beizhu = models.TextField(null=True)
    payment_id = models.CharField(max_length=255)#支付方式
    create_time = models.DateTimeField(auto_now=True)

    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            else:
                d[attr] = getattr(self, attr)

        import json
        return json.dumps(d)

#管理员
class Admin(models.Model):
    adminname = models.CharField(max_length=32)#用户名
    password = models.CharField(max_length=32)
    create_time=models.DateTimeField(auto_now=True)

    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            else:
                d[attr] = getattr(self, attr)

        import json
        return json.dumps(d)
#地址
class Address(models.Model):
    difang = models.CharField(max_length=255)
    name=models.CharField(max_length=32)
    email=models.EmailField()
    mailnum=models.CharField(max_length=10)
    phone=models.CharField(max_length=32)
    u = models.ForeignKey(User, on_delete=models.CASCADE)

#代购表
class Buy(models.Model):
    u = models.ForeignKey(User, on_delete=models.CASCADE)#连接用户表
    ad = models.ForeignKey(Address, on_delete=models.CASCADE)
    url = models.URLField()
    gn_yunfei = models.FloatField()#国内运费金额
    gy_yunfei = models.FloatField()#国外运费金额
    zongjia = models.FloatField()#商品价格
    dj = models.FloatField()#商品单价
    num = models.IntegerField()#商品数量
    feilei = models.CharField(max_length=20)#颜色分类
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='buyimg')
    a =((1,'未支付'),(2,'已支付'))
    b=((1,'未处理'),(2,'已处理'),(3,'未发货'),(4,'已发货'),(5,'已完成'),(6,'已取消'))
    state = models.IntegerField(choices=b)#订单状态
    payment_id = models.IntegerField(choices=a)#支付国内运费状态
    gy_py = models.IntegerField(choices=a)#支付国际运费状态
    create_time = models.DateTimeField(auto_now=True)

#代运表
class Transport(models.Model):
    u = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Address, on_delete=models.CASCADE)
    yunfei = models.FloatField()#运费
    ddnum = models.IntegerField()#订单号
    gongsi = ((1,'申通'),(2,'圆通'),(3,'中通'),(4,'韵达'),(5,'百世')
              ,(6,'天天'),(7,'顺丰'),(8,'邮政'),(9,'EMS'),(10,'优速')
              ,(11,'安能'),(12,'快捷')
              ,(13,'德邦'),(14,'宅急送'),(15,'速尔'),(16,'苏宁'),(17,'京东')
              ,(18,'加运美'),(19,'龙邦')
              ,(20,'万象物流'),(21,'联昊通'),(22,'全峰'),(23,'国通'),(24,'信丰')
              ,(25,'菜鸟快递'),(26,'如风达')
              ,(27,'京广物流'),(28,'运通物流'),(29,'其他物流'),(30,'新邦物流'))
    leixin = ((0,'普货'),(1,'敏感货')) #货物类型
    ys = ((72,'西马（空运）ABX派送单件>=30KG请咨询客服（急件勿选）'),
            (74,'西马（空运）Skynet派送单件>=40KG请咨询客服'),               #运输类型
            (77, '东马（空运）ABX派送单件>=25KG请咨询客服'),
            (82, '西马（空运）Gdex派送'),
            (83, '新加坡（空运）dragonlink/RaidereX 派送'),
            (89, '新加坡（海运）最低消费1立方'),
            (91,'西马（海运小包）（普/敏感）偏远地区咨询客服'),
            (93, '东马sabah（海运小包)（普货/敏感）偏远地区咨询客服'),
            (96, '西马（空运）poslaju派送'),
            (98,'西马(海运）最低消费0.3CBM偏远地区收取偏远费'),
            (99, '东马海运Sarawak最低消费0.5CBM（偏远地区收取偏远费）'),
            (102,'东马（空运）Poslaju派送'),
            (106, '东马SARAWAK（海运小包)（普货/敏感）偏远地区咨询客服'),
            (107,'东马海运Sabah最低消费0.5CBM（偏远地区收取偏远费）'),
            (111, '西马（海运小包）（普/敏感）6-10KG'),
            (112,'东马sabah（海运小包)（普货/敏感）6-10'),
            (113, '东马SARAWAK（海运小包)（普货/敏感）6-10'),
            (114,'单边超过140cm或重量超68KG收取120元超长费'),
            (115, '东马海运偏远地区+250元 最低消费0.5CBM'),
            (116,'东马海运（纳闽岛LABUAN）偏远地区，最低消费1CBM'),
            (117, '西马包税(skynet/gdex)下单备注'),
            (118,'西马（空运）Airpak派送（急件勿选）'),
            (1000, '其他'))
    ddgongsi = models.IntegerField(choices=gongsi)#快递公司
    ddname=models.CharField(max_length=32)#物品名称
    ddsu=models.IntegerField()#物品数量
    dddanjia=models.FloatField()#单价
    ddbeizhu=models.CharField(max_length=255)#订单备注
    a =((1,'未支付'),(2,'已支付'))
    b=((1,'未处理'),(2,'已处理'),(3,'未发货'),(4,'已发货'),(5,'已完成'),(6,'已取消'))
    lx = models.IntegerField(choices=leixin)#货物类型
    yslx = models.IntegerField(choices=ys)#运输类型
    dsfw = models.CharField(max_length=255)#特殊服务
    beizhu = models.TextField(null=True)#服务备注
    state = models.IntegerField(choices=b)#订单状态
    payment_id = models.IntegerField(choices=a)#支付状态
    create_time = models.DateTimeField(auto_now=True)

#投诉表
class Toushu(models.Model):
    u = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now=True)

# #搜索
# class Post(models.Model):
#     title = models.CharField(max_length=70)
#     # 正文
#     body = models.TextField()
#     # 其他属性
#
#     def __str__(self):
#         return self.title
