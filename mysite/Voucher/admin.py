from django.contrib import admin
from .models import Subject, SubjectDetail,Account, AccountDetail
from django import forms
from django.db import models
from django.urls import reverse
from . import forms as user_forms
import datetime
# Register your models here.

#admin.site.register(Subject)
#admin.site.register(SubjectDetail)


class SubjectDetailInline(admin.StackedInline):
    model = SubjectDetail


class AccountDetailInline(admin.TabularInline):
    model = AccountDetail



class SubjectAdmin(admin.ModelAdmin):
    inlines = [SubjectDetailInline,]
    list_display = ('name', 'code', 'category', )
    #list_editable = ( 'code', 'category')
    list_filter = ('category', )
    list_per_page = 5
    ordering = ('code',)
    search_fields = ['name', 'code']
    view_on_site = True
    def view_on_site(self, obj):
        url = reverse('voucher:home')
        return url






class MyAdminSite(admin.AdminSite):
    site_header = 'finance system'


admin_site = MyAdminSite()



class AccountAdmin(admin.ModelAdmin):
    date_hierarchy = 'account_date'
    #fields = ( ('producer','account_date'), 'audit')
    list_display =  ('producer','account_date', 'audit')
    #inlines = [AccountDetailInline,]
    form = user_forms.AccountForm 

    def get_changeform_initial_data(self, request):
        return {'account_date':datetime.date.today()}

admin.site.register(Account, AccountAdmin)
admin.site.register(Subject, SubjectAdmin)
