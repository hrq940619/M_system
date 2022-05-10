from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app import models
from django import forms
from app.utils.bootstrap import BootStrapModelForm


class UserModelForm(BootStrapModelForm):
    # 重写可以做更多的校验
    name = forms.CharField(min_length=2, label="用户名")
    # name = forms.CharField(
    #     min_length=2,
    #     label="用户名",
    #     widget=forms.TextInput(attrs={"class": "form-control"})
    # )

    class Meta:
        model = models.UserInfo
        # 这样写只能判断是否为空
        fields = ['name', 'password', 'age', 'account', 'create_time', 'gender', 'depart']
        # 解决样式问题
        # 方法一（不推荐，因为要一个一个字段地添加）
        # widgets = {
        #     "name":forms.TextInput(attrs={"class": "form-control"}),
        #     "password":forms.PasswordInput(attrs={"class": "form-control"})
        # }

        # 方法二 重新定义init方法

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有的插件，添加class样式
        # 循环ModelForm中的所有字段，给每个字段的插件设置
        for name, field in self.fields.items():

            # if name == 'name':
            #     field.widget.attrs = {'placeholder': field.label}
            #     continue
            # field.widget.attrs = {'class': "form-control", 'placeholder': field.label}
            # field.widget.attrs = {'class': "form-control"}

            # 字段中有属性的话，要保留原来的属性
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                if name == 'name':
                    field.widget.attrs = {'placeholder': field.label}
                    continue
                field.widget.attrs = {'class': "form-control", 'placeholder': field.label}


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
        fields = ['mobile', 'price', 'level', 'status']

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
