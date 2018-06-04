# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from app_ss.models import Host
from app_ss.models import BMessage
from app_ss.models import VPLOG
from app_ss.models import User

# Register your models here.



# class TagInline(admin.TabularInline):
#     model = Host

class HostAdmin(admin.ModelAdmin):
    list_display = ("enable",'oneline','name','ip','port','method','available_band','total_band',"create_time")
    # inlines = [TagInline]  # Inline
    search_fields = ('name','port','method')
    fieldsets = (
        ['Main',{
            'fields':('enable','oneline','name','ip','port','method','available_band','total_band'),
        }],
        ['Advance',{
            'classes':('collapse',),
            'fields':('alias',),
        }

        ]

    )

class VPLogAdmin(admin.ModelAdmin):
    list_display = ('brand','mac','ip','user','create_time')
    # inlines = [TagInline]  # Inline
    search_fields = ('brand','mac','ip','user')

admin.site.register(User)
admin.site.register(Host,HostAdmin)
admin.site.register(BMessage)
admin.site.register(VPLOG,VPLogAdmin)