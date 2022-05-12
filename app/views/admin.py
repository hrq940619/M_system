from django.shortcuts import render,redirect

from app import models
from app.utils.pagination import Pagination


def admin_list(request):
    """ 管理员列表 """

    # 获取当前已登录的用户信息
    # info_dict = request.session['info']
    # print(info_dict['id'])
    # print(info_dict['name'])

    # 检查用户是否已经登录
    # 用户发来请求，获取Cookie随机字符串，拿着随机字符串看看session中有没有对应数据
    # request.session['info']
    info = request.session.get('info')
    if not info:
        return redirect('/login/')

    # 1、根据自己的情况去筛选自己的数据
    data_dict = {}
    search_data = request.GET.get('q', '')

    if search_data:
        data_dict = {"username__contains": search_data}
    queryset = models.Admin.objects.filter(**data_dict)

    # 2、实例化分页对象
    page_object = Pagination(request, queryset)
    context = {
        "search_data": search_data,
        'queryset': page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }

    return render(request, 'app/admin_list.html', context)


from django import forms
from django.core.exceptions import ValidationError
from app.utils.form import BootStrapModelForm
from app.utils.encrypt import md5

class AdminModelForm(BootStrapModelForm):

    # 如果不想两次密码输入错误后被清空，需要加上参数render_value=True
    confirm_password = forms.CharField(label="确认密码",widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = models.Admin
        fields = ["username", "password"]
        # 如果不想两次密码输入错误后被清空，需要加上参数render_value=True
        widgets = {'password': forms.PasswordInput(render_value=True)}

    # 密码md5加密存储
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        # 所有通过验证的数据都可以通过form.cleaned_data的方法得到
        # print(self.cleaned_data)

        pwd = self.cleaned_data.get("password")
        print(pwd)
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("两次输入的密码不一致")

        # 函数返回什么，此字段以后保存到数据库就是什么
        return confirm

class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']

class AdminResetPasswordModelForm(BootStrapModelForm):
    # 如果不想两次密码输入错误后被清空，需要加上参数render_value=True
    confirm_password = forms.CharField(label="确认密码", widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']
        widgets = {'password': forms.PasswordInput(render_value=True)}

    # 密码md5加密存储
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)

        # 去数据库校验当前密码和新输入的密码是否一致
        exists = models.Admin.objects.filter(id=self.instance.pk,password=md5_pwd).exists()
        if exists:
            raise ValidationError("密码不能与之前的相同")
        return md5_pwd

    def clean_confirm_password(self):

        # 所有通过验证的数据都可以通过form.cleaned_data的方法得到
        # print(self.cleaned_data)

        pwd = self.cleaned_data.get("password")
        # print(pwd)
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if not pwd:
            raise ValidationError("密码不能与之前的相同")

        elif confirm != pwd:
            raise ValidationError("两次输入的密码不一致")

        # 函数返回什么，此字段以后保存到数据库就是什么
        return confirm

def admin_add(request):
    """ 添加管理员 """

    title = "新建管理员"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, 'app/change.html', {'form': form, 'title': title})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        form.save()
        return redirect('/admin_list/')

    return render(request, 'app/change.html', {'form': form, 'title': title})


def admin_edit(request, nid):
    """ 编辑管理员 """

    # 对象/None
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'app/error.html', {'msg': "数据不存在"})

    title = "编辑管理员信息"

    if request.method == "GET":
        # 显示默认值
        form = AdminEditModelForm(instance=row_object)
        return render(request, 'app/change.html', {'form': form, 'title': title})

    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin_list/')
    return render(request, 'app/change.html', {'form': form, 'title': title})


def admin_deleted(request, nid):
    """ 删除管理员 """
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin_list/')

def admin_reset_password(request, nid):
    """ 重置密码 """
    # 对象/None
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin_list/')
    title = "重置密码 - {}".format(row_object.username)

    if request.method == "GET":
        # 不希望前端能看到密码的加密文本值，需要去掉参数：instance=row_object
        form = AdminResetPasswordModelForm()
        return render(request, 'app/change.html', {'form': form, 'title': title})

    form = AdminResetPasswordModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin_list/')
    return render(request, 'app/change.html', {'form': form, 'title': title})
