from django.contrib import admin
from django.urls import path, include
from apps.users import urls as users_urls
from apps.users import views

admin.site.site_header = "Referral Fifty Fifty"
admin.site.site_title = 'Referral Fifty Fifty'
admin.site.site_url = '/'
admin.site.index_title = "Referral Fifty Fifty"

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('users/', include(users_urls)),
]
