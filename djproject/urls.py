"""djproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
import datetime
import re

import pymysql
from django.contrib import admin
from django.shortcuts import render
from django.urls import path

from showDATA import views


urlpatterns = [
    path('admin/', admin.site.urls),#系统默认创建的
    path('login/',views.login),#用于打开登录页面
    path('register/',views.register),#用于打开注册页面
    # path('register/save',views.save),#输入用户名密码后交给后台save函数处理
    # path('login/query',query),  #输入用户名密码后交给后台query函数处理
    # path('register/query',views.query),  #输入用户名密码后交给后台query函数处理
    path('login/savedata/',views.savedata), #输入用户名密码后交给后台query函数处理
    path('showdata/',views.group),  #输入用户名密码后交给后台query函数处理
    path('addelem/',views.addelem),  #输入用户名密码后交给后台query函数处理
    path('addelem2/',views.addelem2),  #输入用户名密码后交给后台query函数处理
    path('editelem2/',views.editelem2), #输入用户名密码后交给后台query函数处理
    path('showuser/',views.showuser)  #输入用户名密码后交给后台query函数处理

]
