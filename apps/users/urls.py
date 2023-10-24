# mysite/urls.py
from users import views
from django.urls import path

urlpatterns = [
    path ('', views.index, name='index'),
    path ("referral-by-phone/", views.ReferralByPhone.as_view(), name="referral-by-phone"),
]