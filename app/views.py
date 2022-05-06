from django.shortcuts import render, redirect

# Create your views here.
from app import models


def depart_list(request):
    """ 部门列表 """
    queryset = models.Department.objects.all()
    return render(request, 'app/depart_list.html', {'queryset': queryset})


def depart_add(request):
    """ 添加部门 """
    if request.method == "GET":
        return render(request, 'app/depart_add.html')
    # 获取用户POST提交过来的数据
    title = request.POST.get("title")
    # 保存到数据库
    models.Department.objects.create(title=title)
    # 重定向回部门列表
    return redirect("/depart_list/")


def depart_deleted(request):
    # 获取id
    depart_id = request.GET.get('nid')
    # 删除
    models.Department.objects.filter(id=depart_id).delete()
    # 重定向回部门列表
    return redirect("/depart_list/")


def depart_edit(request, nid):
    """ 修改部门 """
    # 根据nid，获取数据
    if request.method == "GET":
        row_object = models.Department.objects.filter(id=nid).first()
        # print(row_object.id,row_object.title)

        return render(request, 'app/depart_edit.html', {"row_object": row_object})

    # 获取用户提交的标题
    title = request.POST.get("title")
    # 根据id找到数据库中的数据并更新
    models.Department.objects.filter(id=nid).update(title=title)
    # 重定向回部门列表
    return redirect("/depart_list/")


def user_list(request):
    """ 用户管理 """
    queryset = models.UserInfo.objects.all()

    """ for obj in queryset:
        # obj.gender  # 只能获取到：1/2
        # obj.get_gender_display()  # 固定写法： get_字段名称_display()
        print(obj.id,obj.name,obj.account,obj.create_time.strftime("%Y-%m-%d"),obj.get_gender_display(),obj.depart.title)
        # obj.depart.title # 根据id自动去关联的表中获取那一行数据depart对象
    """

    return render(request, 'app/user_list.html', {'queryset': queryset})


def user_add(request):
    """ 添加用户（原始方法） """
    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.all()
        }
        return render(request, 'app/user_add.html', context)

    # 获取用户提交的数据
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('ac')
    ctime = request.POST.get('ctime')
    gender_id = request.POST.get('gd')
    depart_id = request.POST.get('dp')

    # 添加到数据库
    models.UserInfo.objects.create(name=user, password=pwd, age=age, account=account, create_time=ctime,
                                   gender=gender_id, depart_id=depart_id)

    # 返回用户列表页面
    return redirect('/user_list/')

# =============================== ModelForm示例 =====================================

from django import forms
class UserModelForm(forms.ModelForm):
    # 重写可以做更多的校验
    name = forms.CharField(min_length=2,label="用户名")

    class Meta:
        model = models.UserInfo
        # 这样写只能判断是否为空
        fields = ['name','password','age','account','create_time','gender','depart']
        # 解决样式问题
        # 方法一（不推荐，因为要一个一个字段地添加）
        # widgets = {
        #     "name":forms.TextInput(attrs={"class": "form-control"}),
        #     "password":forms.PasswordInput(attrs={"class": "form-control"})
        # }

        # 方法二 重新定义init方法
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        # 循环找到所有的插件，添加class样式
        for name,field in self.fields.items():
            if name == 'name':
                field.widget.attrs = {'placeholder': field.label}
                continue
            field.widget.attrs = {'class': "form-control", 'placeholder': field.label}
            # field.widget.attrs = {'class': "form-control"}


def user_model_form_add(request):
    """ 添加用户（ModelForm版本） """
    if request.method == "GET":
        form = UserModelForm()
        return render(request,'app/user_model_form_add.html',{"form":form})

    # 用户POST 提交数据，校验数据
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        form.save()
        return redirect('/user_list/')

    # 校验失败(在页面上显示错误信息)
    return render(request, 'app/user_model_form_add.html', {"form": form})


def user_edit(request,nid):
    """ 编辑用户 """
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        # 根据id去数据库获取需要编辑的数据
        form = UserModelForm(instance=row_object)
        return render(request,'app/user_edit.html', {"form": form})

    form = UserModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要在用户输入以外增加一点值
        # form.instance.字段名 = 值
        form.save()
        return redirect('/user_list/')
    return render(request, 'app/user_edit.html', {'form':form})


def user_deleted(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user_list/')

# =============================== 靓号管理 =====================================

def pretty_list(request):
    """ 靓号列表 """

    queryset = models.PrettyNum.objects.all().order_by('-level')
    return render(request,'app/pretty_list.html', {'queryset': queryset})

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class PrettyModelForm(forms.ModelForm):
    # 重写以做更多的输入校验
    # 验证：方式一
    # mobile = forms.CharField(
    #     label="手机号码",
    #     validators=[RegexValidator(r'^133\d{8}$', '手机号格式错误')],
    # )

    class Meta:
        model = models.PrettyNum
        # fields = ['mobile','price','level','status']

        # 表示所有字段
        fields = "__all__"

        # 排除哪个字段
        # exclude = ['level']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有的插件，添加class样式
        for name, field in self.fields.items():
            if name == 'mobile':
                field.widget.attrs = {'placeholder': field.label}
                continue
            field.widget.attrs = {'class': "form-control", 'placeholder': field.label}
            # field.widget.attrs = {'class': "form-control"}

    # 验证：方式二 (钩子方法)
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']

        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError('手机号已存在')
        elif len(txt_mobile) != 11:
            # 验证不通过
            raise ValidationError('格式错误')

        # 验证通过，则返回用户输入的数据
        return txt_mobile

def pretty_add(request):
    """ 添加靓号 """
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request,'app/pretty_add.html',{'form':form})

    form = PrettyModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect('/pretty_list/')

    return render(request,'app/pretty_add.html', {'form': form})


class PrettyEditModelForm(forms.ModelForm):
    # 设置为不可编辑，或者直接在fields中去掉mobile
    # mobile = forms.CharField(disabled=True,label="手机")

    # 重写以做更多的输入校验
    # 验证：方式一
    mobile = forms.CharField(
        label="手机号码",
        validators=[RegexValidator(r'^133\d{8}$', '手机号格式错误')],
    )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile','price','level','status']

        # 表示所有字段
        # fields = "__all__"

        # 排除哪个字段
        # exclude = ['level']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有的插件，添加class样式
        for name, field in self.fields.items():
            if name == 'mobile':
                field.widget.attrs = {'placeholder': field.label}
                continue
            field.widget.attrs = {'class': "form-control", 'placeholder': field.label}
            # field.widget.attrs = {'class': "form-control"}

    # 验证：方式二 (钩子方法)
    def clean_mobile(self):
        # 当前编辑数据的id
        # print(self.instance.pk)

        txt_mobile = self.cleaned_data['mobile']

        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError('手机号已存在')
        elif len(txt_mobile) != 11:
            # 验证不通过
            raise ValidationError('格式错误')

        # 验证通过，则返回用户输入的数据
        return txt_mobile

def pretty_edit(request,nid):
    """ 编辑靓号 """
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_object)
        return render(request, 'app/pretty_edit.html', {'form': form})

    form = PrettyEditModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要在用户输入以外增加一点值
        # form.instance.字段名 = 值
        form.save()
        return redirect('/pretty_list/')
    return render(request, 'app/pretty_edit.html', {'form': form})


def pretty_deleted(request, tid):
    models.PrettyNum.objects.filter(id=tid).delete()
    return redirect('/pretty_list/')