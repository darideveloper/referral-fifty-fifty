from django.contrib import admin
from users import models

@admin.register(models.User)
class UserAdmin (admin.ModelAdmin):
    list_display = ['id', 'name', 'last_name', 'email', 'phone', 'active']
    ordering = ['id', 'name', 'last_name', 'email', 'phone', 'active']
    list_filter = ['active', 'created_at', 'updated_at']

@admin.register(models.Store)
class StoreAdmin (admin.ModelAdmin):
    list_display = ['id', 'name']
    ordering = ['id', 'name']
    
@admin.register(models.ReferralLink)
class ReferralLinkAdmin (admin.ModelAdmin):
    list_display = ['id', 'user', 'store', 'link']
    ordering = ['id', 'user__name', 'store__name', 'link']
    list_filter = ['user', 'store']