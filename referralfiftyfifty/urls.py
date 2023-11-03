from django.contrib import admin
from django.urls import path, include
from apps.users import urls as users_urls

admin.site.site_header = "Referral Fifty Fifty"
admin.site.site_title = 'Referral Fifty Fifty'
admin.site.site_url = '/'
admin.site.index_title = "Referral Fifty Fifty"

urlpatterns = [
    path('', include(users_urls), name='users'),
    path('admin/', admin.site.urls),
]
