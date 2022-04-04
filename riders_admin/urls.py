from . import views
from django.urls import path

urlpatterns = [
    path('', views.login),
    path('dashboard', views.dashboard,name='dashboard'),
]
