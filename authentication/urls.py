from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib import admin
admin.site.site_header = 'Skin Cancer Prediction Web-app Admin'
admin.site.site_title = 'Admin Skin Cancer Prediction Web-app'
admin.site.index_title = 'Developed by tim-G'

urlpatterns = [
    path('sign-up', views.SignUpView.as_view(), name='sign-up'),
    path('sign-in', views.SignIn.as_view(), name='sign-in'),
    path('sign-out', views.SignOut.as_view(), name='sign-out'),
]