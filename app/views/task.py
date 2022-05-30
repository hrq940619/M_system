from django import forms
from django.http import HttpResponse
from django.shortcuts import render,redirect

from app import models
from app.utils.bootstrap import BootStrapModelForm
from app.utils.pagination import Pagination

class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            "detail": forms.TextInput
            # "detail": forms.Textarea
        }


def task_list(request):
    """ 任务列表 """
    queryset = models.Task.objects.all().order_by('-id')
    form = TaskModelForm()
    page_object = Pagination(request, queryset)

    context = {
        'form': form,
        'queryset': page_object.page_queryset,
        "page_string": page_object.html()
    }
    return render(request, 'app/task_list.html', context)


import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def task_ajax(request):
    print(request.GET)
    print(request.POST)
    data_dict = {"status": True, "data": [11, 22, 33, 44]}
    json_string = json.dumps(data_dict)
    return HttpResponse(json_string)

# ajax 发送post请求
@csrf_exempt
def task_add(request):
    # 获取Ajax请求发送过来的数据
    print(request.POST)

    # 1、对用户发送过来的数据进行校验
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()

        # 这里不能接return redirect，因为Ajax发送的是不刷新的请求，页面不会发生跳
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))

    # 错误信息
    print(type(form.errors)) # <class 'django.forms.utils.ErrorDict'>
    print(type(form.errors.as_json()))
    from django.forms.utils import ErrorDict
    data_dict = {"status": False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))