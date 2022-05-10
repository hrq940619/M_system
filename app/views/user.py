from django.shortcuts import render, redirect
from app import models
from app.utils.pagination import Pagination
from app.utils.form import UserModelForm,PrettyModelForm,PrettyEditModelForm

# =============================== 用户管理 =====================================

def user_list(request):
    """ 用户管理 """

    """ for obj in queryset:
        # obj.gender  # 只能获取到：1/2
        # obj.get_gender_display()  # 固定写法： get_字段名称_display()
        print(obj.id,obj.name,obj.account,obj.create_time.strftime("%Y-%m-%d"),obj.get_gender_display(),obj.depart.title)
        # obj.depart.title # 根据id自动去关联的表中获取那一行数据depart对象
    """
    queryset = models.UserInfo.objects.all()

    page_object = Pagination(request, queryset)
    context = {
        'queryset': page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }


    return render(request, 'app/user_list.html', context)


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



def user_model_form_add(request):
    """ 添加用户（ModelForm版本） """
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'app/user_model_form_add.html', {"form": form})

    # 用户POST 提交数据，校验数据
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        form.save()
        return redirect('/user_list/')

    # 校验失败(在页面上显示错误信息)
    return render(request, 'app/user_model_form_add.html', {"form": form})


def user_edit(request, nid):
    """ 编辑用户 """
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        # 根据id去数据库获取需要编辑的数据
        form = UserModelForm(instance=row_object)
        return render(request, 'app/user_edit.html', {"form": form})

    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要在用户输入以外增加一点值
        # form.instance.字段名 = 值
        form.save()
        return redirect('/user_list/')
    return render(request, 'app/user_edit.html', {'form': form})


def user_deleted(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user_list/')