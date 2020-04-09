from django.conf.urls import url
from django.contrib import admin
from . import views
urlpatterns = [
    url('reg', views.reg_view),
    url('login', views.login_view),
    url('logout', views.logout),

]