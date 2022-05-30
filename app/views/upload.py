from django.http import HttpResponse
from django.shortcuts import render
import os

from app import models


def upload_list(request):
    if request.method == "GET":
        return render(request, 'app/upload_list.html')
    # print(request.POST)  # 请求体中的数据
    # print(request.FILES)  # 请求发过来的文件

    file_object = request.FILES.get("avatar")
    # print(file_object.name)  # 文件名：WX20211117-222041@2x.png

    f = open(file_object.name, mode='wb')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()

    return HttpResponse("上传成功")


from django import forms
from app.utils.bootstrap import BootStrapModelForm, BootStrapForm


class UpForm(BootStrapForm):
    bootstrap_exclude_fields = ['img']

    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    img = forms.FileField(label="头像")


def upload_form(request):
    """ Form上传文件 """
    title = "Form上传"
    if request.method == "GET":
        form = UpForm()
        return render(request, 'app/upload_form.html', {"form": form, 'title': title})

    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 1、读取图片内容，写入到文件夹中并获取文件的路径。
        image_object = form.cleaned_data.get("img")

        # 拼接数据库存的路径，解决路径问题
        # db_file_path = os.path.join("app", "image", image_object.name)
        # file_path = "app/static/image/{}".format(image_object.name)

        # 将上传的文件存储到media文件夹
        from django.conf import settings
        # 绝对路径
        # media_path = os.path.join(settings.MEDIA_ROOT, image_object.name)
        # 相对路径
        media_path = os.path.join("media", image_object.name)

        # 3、拼接存在本地的路径
        f = open(media_path, mode='wb')
        for chunk in image_object.chunks():
            f.write(chunk)
        f.close()

        # 2、将图片文件路径写入到数据库
        models.Boss.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            img=media_path,
        )

        return HttpResponse('上传成功')
    return render(request, 'app/upload_form.html', {"form": form, 'title': title})


class UpModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img']
    class Meta:
        model = models.City
        fields = "__all__"


def upload_modal_form(request):
    """ 上传文件和数据（modelForm） """
    title = "ModelForm上传文件"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'app/upload_form.html', {'form': form, "title": title})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 对于文件：自动保存
        #字段 + 上传路径写入到数据库
        form.save()
        return HttpResponse('成功')

    return render(request, 'app/upload_form.html', {'form': form, "title": title})