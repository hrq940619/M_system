from django.http import HttpResponse
from django.shortcuts import render, redirect

from app import models


def city_list(request):
    queryset = models.City.objects.all()
    return render(request, 'app/city_list.html', {'queryset': queryset})

from app.utils.bootstrap import BootStrapModelForm, BootStrapForm

class UpModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img']
    class Meta:
        model = models.City
        fields = "__all__"


def city_add(request):
    """ 新建城市 """
    title = "新建城市"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'app/upload_form.html', {'form': form, "title": title})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 对于文件：自动保存
        #字段 + 上传路径写入到数据库
        form.save()
        return redirect('/city_list/')

    return render(request, 'app/upload_form.html', {'form': form, "title": title})