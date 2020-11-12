from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # path('dialogflow', views.webhook_dialogflow),
    path('chat', views.chat),
    url(r'^$', TemplateView.as_view(template_name='checkout/checkout.html'), name='checkout_main'),
    url(r'^ready/$', views.ready, name='ajax-ready'),
    url(r'^search/$', views.stay_detail_search, name='ajax-search'),
    url(r'^submit_bill/$', views.submit_bill, name='ajax-submit_bill'),
    url(r'^reg_show_sign/$', views.show_sign, name='ajax-reg_show_sign'),
    # url(r'^reg_show_sign_payment/$', views.show_sign_payment, name='ajax-reg_show_sign_payment'),
]
