from django import forms


class BootStrap:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有的插件，添加class样式
        # 循环ModelForm中的所有字段，给每个字段的插件设置
        for name, field in self.fields.items():

            # 字段中有属性的话，要保留原来的属性
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs ={
                    "class": "form-control",
                    "placeholder": field.label
                }
                # if name == 'name':
                #     field.widget.attrs = {'placeholder': field.label}
                #     continue
                # field.widget.attrs = {'class': "form-control", 'placeholder': field.label}


class BootStrapModelForm(BootStrap, forms.ModelForm):
    pass


# class BootStrapForm(BootStrap, forms.ModelForm):
class BootStrapForm(BootStrap, forms.Form):
    pass
