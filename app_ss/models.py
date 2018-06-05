# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from time import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from app_ss.EnTool import encopyt


class User(AbstractUser):
    uuid =models.CharField(max_length=50, verbose_name=u'UUID', default='',blank=True)
    alias_name = models.CharField(max_length=50, verbose_name=u'别名', default='',blank=True)
    app_version=models.CharField(max_length=15,verbose_name=u"app version",default='',blank=True)
    ip=models.CharField(max_length=20,verbose_name="注册时的IP",default="",blank=True)

    brand=models.CharField(max_length=50,verbose_name="手机型号",default='',blank=True)
    imei=models.CharField(max_length=50,verbose_name="imei",default='',blank=True)
    system_version=models.CharField(max_length=20,verbose_name="操作系统版本",default="",blank=True)

    enable = models.BooleanField(default=True, verbose_name="是否可用",blank=True)
    disableMessage=models.CharField(max_length=100,verbose_name="不可用时提示",default='',blank=True)
    disableMessageCn = models.CharField(max_length=100, verbose_name="不可用时提示CN", default='',blank=True)
    installationId=models.CharField(max_length=50,verbose_name="VPN Service ID",default='',blank=True)

    country=models.CharField(max_length=10,verbose_name="国家代码",default='',blank=True)
    mac=models.CharField(max_length=50,verbose_name="网卡mac地址",default='',blank=True)

    remaining_bytes=models.IntegerField(default=0,verbose_name="剩余流量(KB)",blank=True)
    total_bytes=models.IntegerField(default=0,verbose_name="总流量(KB)",blank=True)
    usedByte = models.IntegerField(default=0, verbose_name="已经使用总流量(KB)",blank=True)

    create_time = models.DateTimeField(u'create time', auto_now=True)

    def to_dict(self):
        data = {}
        for f in self._meta.concrete_fields:
            if f.name == 'enable'  or  f.name == 'usedByte' or f.name == 'total_bytes'or  f.name == 'disableMessage' or f.name=='uuid' or  f.name == 'disableMessageCn':
                     data[f.name] = f.value_from_object(self)
            if f.name == 'remaining_bytes':
                data[f.name] = f.value_from_object(self)
                data['remainingM']=f.value_from_object(self)/1024

        return data

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'




class Host(models.Model):

    enable=models.BooleanField(default=True,verbose_name="是否可用")

    type=models.IntegerField(default=1,verbose_name="类型:1自建 2.其他",)
    alias=models.CharField(max_length=30,verbose_name="别名")
    available_band=models.IntegerField(verbose_name="可用的带宽",default=0)
    total_band=models.IntegerField(verbose_name="总带宽",default=500)
    name = models.CharField(max_length=30, default="显示名称")

    online=models.IntegerField(default=0,verbose_name="在线人数")

    method=models.CharField(max_length=30,verbose_name="加密方式",default="aes-256-cfb")
    password=models.CharField(max_length=20)
    ip=models.CharField(max_length=20,default='',blank=True)
    base64str=models.CharField(max_length=60,default='',verbose_name='base64全路径:',blank=True)
    port=models.IntegerField(default=-1,blank=True)


    create_time = models.DateTimeField(u'create time', auto_now=True)

    def __unicode__(self):
        return self.toHostString()

    def toHostString(self):
        # return "host:"+self.serverurl+" Port:"+str(self.port)
        return "ss://"+self.method+":"+self.password+"@"+self.ip+":"+str(self.port)

    def to_dict(self):
        data = {}
        for f in self._meta.concrete_fields:
            if f.name!='create_time' and f.name != 'enable' and f.name != 'type' and f.name != 'alias':
                if f.name == 'password':
                     data[f.name] = encopyt(f.value_from_object(self))
                else:
                     data[f.name] = f.value_from_object(self)

        return data

class VPLOG(models.Model):
    ip = models.CharField(max_length=20, verbose_name="ip",default="")
    port = models.IntegerField()
    brand = models.CharField(max_length=50, verbose_name="手机型号",default="")
    country = models.CharField(max_length=10, verbose_name="国家代码",default="")
    mac = models.CharField(max_length=50, verbose_name="网卡mac地址",default="")
    user=models.ForeignKey(User)
    create_time = models.DateTimeField(u'create time', auto_now=True)


class BMessage(models.Model):
    type=models.IntegerField(default=1,verbose_name="消息类型")
    title=models.CharField(default="",max_length=100)
    content=models.CharField(max_length=200,default="")
    title_cn = models.CharField(default="", max_length=100)
    content_cn = models.CharField(max_length=200,default="")
    create_time = models.DateTimeField(u'create time', auto_now=True)


class RewardHistory(models.Model):
    uuid=models.CharField(max_length=60,default='',verbose_name="用户UUID")
    username=models.CharField(max_length=60,default='',verbose_name="用户名")
    descption=models.CharField(default="",max_length=100,verbose_name="奖励描述")
    reward_size=models.IntegerField(default=0,verbose_name="奖励M数")
    create_time = models.DateTimeField(u'create time', auto_now=True)