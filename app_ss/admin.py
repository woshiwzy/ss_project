# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from app_ss.models import BMessage, RewardHistory
from app_ss.models import Host
from app_ss.models import User
from app_ss.models import VPLOG


# Register your models here.

# class TagInline(admin.TabularInline):
#     model = Host

class HostAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'type', "enable", 'online', 'ip', "base64str", 'password', 'port', 'method', 'available_band',
        'total_band',
        "create_time")
    # inlines = [TagInline]  # Inline
    search_fields = ('name', 'port', 'method')

    fieldsets = (
        ['Main', {
            'fields': (
                'name', 'type', 'enable', 'online', 'ip', "base64str", 'password', 'port', 'method', 'available_band',
                'total_band'),
        }],
        ['Advance', {
            'classes': ('collapse',),
            'fields': ('alias',),
        }
         ]
    )


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'alias_name', 'uuid',
                    'app_version', 'brand', "system_version", 'enable',
                    'country', 'mac', 'remaining_bytes', 'total_bytes', 'usedByte')

    search_fields = ('uuid' 'brand', 'country', 'app_version')

    fieldsets = (
        ['Main', {
            'fields': (
                'uuid', 'alias_name','enable', 'brand', "system_version", 'usedByte', 'remaining_bytes',
                'is_superuser'),
        }],
        ['Advance', {
            'classes': ('collapse',),
            'fields': ('system_version', 'disableMessage', 'disableMessageCn', 'country', 'mac'),
        }
         ]

    )


class RewardHisAdmin(admin.ModelAdmin):
    # uuid=models.CharField(max_length=60,default='',verbose_name="用户UUID")
    # descption=models.CharField(default="",max_length=100,verbose_name="奖励描述")
    # reward_size=models.IntegerField(default=0,verbose_name="奖励M数")
    # create_time = models.DateTimeField(u'create time', auto_now=True)

    list_display = ('uuid', 'username', 'descption', 'reward_size')
    search_fields = ('uuid', 'descption', 'reward_size', 'username')


class VPLogAdmin(admin.ModelAdmin):
    list_display = ('brand', 'mac', 'ip', 'user', 'create_time')
    # inlines = [TagInline]  # Inline
    search_fields = ('brand', 'mac', 'ip', 'user')


admin.site.register(User, UserAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(BMessage)
admin.site.register(VPLOG, VPLogAdmin)
admin.site.register(RewardHistory, RewardHisAdmin)
