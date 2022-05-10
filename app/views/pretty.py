from django.shortcuts import render, redirect
from app import models
from app.utils.pagination import Pagination
from app.utils.form import UserModelForm,PrettyModelForm,PrettyEditModelForm

# =============================== 靓号管理 =====================================

def pretty_list(request):
    """ 靓号列表 """
    # 判断请求是否有筛选条件
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict = {"mobile__contains": search_data}

    # 获取数据
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by('-level')

    # 分页回显处理
    page_object = Pagination(request, queryset)
    count_queryset = page_object.total_page_count

    context = {
        "search_data": search_data,
        'queryset': page_object.page_queryset, # 分完页的数据
        "page_string": page_object.html(), # 页码
        'count_queryset': count_queryset
    }

    return render(request, 'app/pretty_list.html', context)


def pretty_add(request):
    """ 添加靓号 """
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, 'app/pretty_add.html', {'form': form})

    form = PrettyModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect('/pretty_list/')

    return render(request, 'app/pretty_add.html', {'form': form})


def pretty_edit(request, nid):
    """ 编辑靓号 """
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_object)
        # print(form)
        return render(request, 'app/pretty_edit.html', {'form': form})

    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要在用户输入以外增加一点值
        # form.instance.字段名 = 值
        form.save()
        return redirect('/pretty_list/')
    return render(request, 'app/pretty_edit.html', {'form': form})


def pretty_deleted(request, tid):
    models.PrettyNum.objects.filter(id=tid).delete()
    return redirect('/pretty_list/')

