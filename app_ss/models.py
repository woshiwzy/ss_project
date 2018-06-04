# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):

    alias_name = models.CharField(max_length=50, verbose_name=u'别名', default='')
    app_version=models.CharField(max_length=15,verbose_name=u"app version",default='')
    ip=models.CharField(max_length=20,verbose_name="注册时的IP",default="")

    brand=models.CharField(max_length=50,verbose_name="手机型号",default='')
    imei=models.CharField(max_length=50,verbose_name="imei",default='')
    system_version=models.CharField(max_length=20,verbose_name="操作系统版本",default="")

    enable = models.BooleanField(default=True, verbose_name="是否可用")
    disableMessage=models.CharField(max_length=100,verbose_name="不可用时提示",default='')
    installationId=models.CharField(max_length=50,verbose_name="VPN Service ID",default='')

    country=models.CharField(max_length=10,verbose_name="国家代码",default='')
    mac=models.CharField(max_length=50,verbose_name="网卡mac地址",default='')

    remaining_bytes=models.IntegerField(default=0,verbose_name="剩余流量(KB)")
    total_bytes=models.IntegerField(default=0,verbose_name="总流量(KB)")
    usedByte = models.IntegerField(default=0, verbose_name="已经使用总流量(KB)")

    create_time = models.DateTimeField(u'create time', auto_now=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

class Host(models.Model):

    enable=models.BooleanField(default=True,verbose_name="是否可用")

    type=models.IntegerField(default=1,verbose_name="1：自建立服务器，2.其他服务器")
    alias=models.CharField(max_length=30,verbose_name="别名")
    available_band=models.IntegerField(verbose_name="可用的带宽",default=0)
    total_band=models.IntegerField(verbose_name="总带宽",default=500)
    name = models.CharField(max_length=30, default="显示名称")

    oneline=models.IntegerField(default=0,verbose_name="在线人数")

    method=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    ip=models.CharField(max_length=20,default='')
    port=models.IntegerField()
    create_time = models.DateTimeField(u'create time', auto_now=True)

    def __unicode__(self):
        return self.toHostString()

    def toHostString(self):
        # return "host:"+self.serverurl+" Port:"+str(self.port)
        return "ss://"+self.method+":"+self.password+"@"+self.ip+":"+str(self.port)

    def to_dict(self):
        data = {}
        for f in self._meta.concrete_fields:
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