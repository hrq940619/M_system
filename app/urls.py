"""Demo4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from app.views import depart,user,pretty,admin

urlpatterns = [
    # 部门管理
    path('depart_list/', depart.depart_list),
    path('depart_add/', depart.depart_add),
    path('depart_deleted/', depart.depart_deleted),
    path('depart_edit/<int:nid>/', depart.depart_edit),

    # 用户管理
    path('user_list/', user.user_list),
    path('user_add/', user.user_add),
    path('user_model_form_add/', user.user_model_form_add),
    path('user_edit/<int:nid>/', user.user_edit),
    path('user_deleted/<int:nid>/', user.user_deleted),

    # 靓号管理
    path('pretty_list/', pretty.pretty_list),
    path('pretty_add/', pretty.pretty_add),
    # path('pretty_edit/<int:nid>', views.pretty_edit),
    path('pretty_edit/<int:nid>/', pretty.pretty_edit),
    path('pretty_deleted/<int:tid>/', pretty.pretty_deleted),

    # 管理员管理
    path('admin_list/', admin.admin_list),
    path('admin_add/', admin.admin_add),
    path('admin_edit/<int:nid>/', admin.admin_edit),

]
