# mysite/urls.py
from users import views
from django.urls import path

urlpatterns = [
    path ('', views.index, name='index'),
    path ("referral/", views.Referral.as_view(), name="referral"),
    path ("register/", views.Register.as_view(), name="register"),
]