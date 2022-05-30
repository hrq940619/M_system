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
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

from app.views import depart, user, pretty, admin, account, task, order, chart, upload, city

urlpatterns = [

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    # 部门管理
    path('depart_list/', depart.depart_list),
    path('depart_add/', depart.depart_add),
    path('depart_deleted/', depart.depart_deleted),
    path('depart_edit/<int:nid>/', depart.depart_edit),

    # 上传文件
    path('depart_multi/', depart.depart_multi),

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
    path('admin_deleted/<int:nid>/', admin.admin_deleted),
    path('admin_reset_password/<int:nid>/', admin.admin_reset_password),

    # 登录（用户认证）
    path('login/', account.login),
    # 退出登录（注销）
    path('logout/', account.logout),
    # 图片验证码
    path('image_code/', account.image_code),

    # 任务管理
    path('task_list/', task.task_list),
    path('task_ajax/', task.task_ajax),
    path('task_add/', task.task_add),

    # 订单管理
    path('order_list/', order.order_list),
    path('order_add/', order.order_add),
    path('order_delete/', order.order_delete),
    path('order_edit/', order.order_edit),
    path('order_detail/', order.order_detail),  # 实现将默认值展示到编辑页面的功能

    # 数据统计
    path('chart_list/', chart.chart_list),
    path('chart_bar/', chart.chart_bar),
    path('chart_pie/', chart.chart_pie),
    path('chart_line/', chart.chart_line),
    path('chart_highcharts/', chart.chart_highcharts),

    # 上传文件
    path('upload_list/', upload.upload_list),
    path('upload_form/', upload.upload_form),
    path('upload_modal_form/', upload.upload_modal_form),

    # 城市列表
    path('city_list/', city.city_list),
    path('city_add/', city.city_add),

]
