"""HotelChatBot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django .contrib.auth.decorators import login_required

from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_view

urlpatterns = [
    # url(r'^$', login_required(TemplateView.as_view(template_name='home.html')), name='home'),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),

    # path('checkin/webhook/', login_required(include('checkin.urls')), name='checkin_main'),
    path('checkin/', include('checkin.urls'), name='checkin_main'),
    # path('checkout/', login_required(include('checkout.urls')), name='checkout_main'),
    path('checkout/', include('checkout.urls'), name='checkout_main'),

    path('admin/', admin.site.urls, name='admin'),
    url(r'^accounts/login/$', auth_view.LoginView.as_view(template_name='login_out/login.html'), name='login'),
    url(r'^accounts/logout//$', auth_view.LogoutView.as_view(template_name='login_out/logged_out.html'), name='logout'),
]
