from django.contrib import admin
from core import models

@admin.register (models.Token)
class TokenAdmin (admin.ModelAdmin):
    ordering = ['id', 'token', 'is_active']
    list_display = ['id', 'token', 'is_active']
    list_filter = ['is_active']