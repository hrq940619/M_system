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

from app import views

urlpatterns = [
    # 部门管理
    path('depart_list/', views.depart_list),
    path('depart_add/', views.depart_add),
    path('depart_deleted/', views.depart_deleted),
    path('depart_edit/<int:nid>/', views.depart_edit),

    # 用户管理
    path('user_list/', views.user_list),
    path('user_add/', views.user_add),
    path('user_model_form_add/', views.user_model_form_add),
    path('user_edit/<int:nid>/', views.user_edit),
    path('user_deleted/<int:nid>/', views.user_deleted),

    # 靓号管理
    path('pretty_list/', views.pretty_list),
    path('pretty_add/', views.pretty_add),
    # path('pretty_edit/<int:nid>', views.pretty_edit),
    path('pretty_edit/<int:nid>/', views.pretty_edit),
    path('pretty_deleted/<int:tid>/', views.pretty_deleted),

]
