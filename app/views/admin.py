from django.shortcuts import render,redirect

from app import models
from app.utils.pagination import Pagination


def admin_list(request):
    """ 管理员列表 """

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
        print(self.cleaned_data)

        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
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
    title = "编辑管理员信息"
    return render(request, 'app/change.html', {'title': title})
