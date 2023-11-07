# mysite/urls.py
from users import views
from django.urls import path

urlpatterns = [
    path ('', views.Index.as_view(), name='index'),
    path ("referral/", views.Referral.as_view(), name="referral"),
    path ("register/", views.Register.as_view(), name="register"),
    path ("activate/<hash>", views.Activate.as_view(), name="activate"),
    path ("404", views.error404Preview, name="404"),
]