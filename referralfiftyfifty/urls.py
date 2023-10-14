from django.contrib import admin
from django.urls import path

admin.site.site_header = "Referral Fifty Fifty"
admin.site.site_title = 'Referral Fifty Fifty'
admin.site.site_url = '/'
admin.site.index_title = "Referral Fifty Fifty"

urlpatterns = [
    path('admin/', admin.site.urls),
]
