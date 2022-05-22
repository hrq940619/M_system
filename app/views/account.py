from io import BytesIO
from django import forms
from django.http import HttpResponse
from django.shortcuts import render,redirect

# 用Form组件实现
from app import models
from app.utils.bootstrap import BootStrapForm
from app.utils.encrypt import md5
from app.utils.code import check_code


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label='用户名',
        # attrs={'class': "form-control"}该参数表示给字段添加上class样式
        widget=forms.TextInput,
        # 必填校验
        required=True

    )

    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(render_value=True),
        # 必填校验
        required=True
    )

    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput,
        # 必填校验
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

# 用ModelForm组件实现
# class LoginModelForm(forms.ModelForm):
#     class Meta:
#         model = models.Admin
#         fields = ['username', 'password']



def login(request):
    """ 登录 """


    if request.method == "GET":
        form = LoginForm()
        return render(request, 'app/login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证成功，获取到的用户名和密码
        # print(form.cleaned_data)

        # 验证码的校验
        # get()和pop()都返回项目，但 pop() 将它们从源字典中删除，而 get() 将它们保留在那里。
        # user_input_code = form.cleaned_data.get('code')

        # 先取消验证码校验逻辑
        user_input_code = form.cleaned_data.pop('code')
        # code = request.session.get('image_code', '')
        # if code.upper() != user_input_code.upper():
        #     form.add_error("code","验证码错误")
        #     return render(request, 'app/login.html', {'form': form})

        # 去数据库校验用户名和密码是否正确，获取用户对象
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        # 如果用户名或密码错误
        if not admin_object:
            # 添加错误提示
            form.add_error("password","用户名或密码错误")
            # form.add_error("username","用户名或密码错误")
            return render(request, 'app/login.html', {'form': form})

        # 用户名和密码输入正确
        # 网站生成随机字符串，写到用户浏览器的cookie中，再写入到session中，数据存储在django_session表中
        request.session['info'] = {'id': admin_object.id, 'name': admin_object.username}
        # 重新设置session超时时间（三天免登陆）
        request.session.set_expiry(60 * 60 * 72)


        return redirect("/admin_list/")
    return render(request, "app/login.html", {'form': form})


def logout(request):
    """ 注销（退出登录） """
    request.session.clear()
    return redirect('/login/')


def image_code(request):
    """ 生成图片验证码 """

    # 调用pillow函数，生成图片
    img, code_string = check_code()

    # 写入到自己的session中（以便于后续获取验证码再进行校验）
    request.session['image_code'] = code_string
    # 给session设置60s超时
    request.session.set_expiry(60)

    # 创建一个内存中的文件
    stream = BytesIO()
    img.save(stream, 'png')

    return HttpResponse(stream.getvalue())