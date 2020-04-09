from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [

    # url('link/', views.link),
    # url('send/', views.send),
    # url('to_sendmsg/', views.to_recmsg),
    # url('to_recmsg/', views.to_sendmsg),
    #
    # url('to_chat/', views.to_chat),
    # url('chat/', views.chat),
    # url('msg_send/', views.msg_send),
    url('to_chat', views.to_chat),
    url('chat', views.chat),
    url('msg_send', views.msg_send),
    url('tiao', views.tiao),
]
