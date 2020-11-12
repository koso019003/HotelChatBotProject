from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # path('dialogflow', views.webhook_dialogflow),
    path('chat', views.chat),
    url(r'^$', TemplateView.as_view(template_name='checkin/checkin.html'), name='checkin_main'),
    url(r'^search/$', views.locate_search, name='ajax-search'),
    url(r'^submit_reg/$', views.submit_reg, name='ajax-submit_reg'),
    url(r'^reg_show_sign/$', views.show_sign, name='ajax-reg_show_sign'),
    url(r'^reg_show_term/$', views.show_term, name='ajax-reg_show_term'),
    url(r'^ready/$', views.ready, name='ajax-ready'),
]
