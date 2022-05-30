import random
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from app import models
from app.utils.bootstrap import BootStrapModelForm
from app.utils.pagination import Pagination

class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude = ["oid", 'admin']

def order_list(request):
    queryset = models.Order.objects.all().order_by('-id')
    form = OrderModelForm()
    page_object = Pagination(request, queryset)
    context = {
        "form": form,
        'queryset': page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }

    return render(request, 'app/order_list.html', context)

@csrf_exempt
def order_add(request):
    """ 新建订单（Ajax请求） """
    form = OrderModelForm(data=request.POST)
    if form.is_valid():

        # 随机生成订单号
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        form.instance.admin_id = request.session['info']['id']
        form.save()
        # 设置下单人  form.instance.admin_id = 当前登录系统的用户id


        return JsonResponse({"status": True})

    return JsonResponse({"status": False, "error": form.errors})


def order_delete(request):
    """ 删除订单 """
    uid = request.GET.get('uid')
    exists = models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({'status': False, 'error': '删除失败，数据不存在！'})

    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({'status': True, 'error': '数据成功！'})


def order_detail(request):
    """ 根据id获取订单详情"""
    # 实现方式一
    # uid = request.GET.get("uid")
    # row_object = models.Order.objects.filter(id=uid).first()
    # print(row_object)
    # if not row_object:
    #     return JsonResponse({'status': False, 'error': '数据不存在！'})
    #
    # # 从数据库获取到一个对象 row_object
    # result = {
    #     "status": True,
    #     "data": {
    #         "title": row_object.title,
    #         "price": row_object.price,
    #         "status": row_object.status,
    #     }
    # }
    #
    # return JsonResponse({"status": True, "data": result})

    # 实现方式二
    uid = request.GET.get("uid")
    # 如果想要去数据库获取数据时，可以通过values()的方法获取字典，不加的话获取的是对象
    row_dict = models.Order.objects.filter(id=uid).values("title","price","status").first()
    print(row_dict)
    if not row_dict:
        return JsonResponse({'status': False, 'error': '数据不存在！'})

    # 从数据库获取到一个对象 row_object
    result = {
        "status": True,
        "data": row_dict
    }

    return JsonResponse(result)

@csrf_exempt
def order_edit(request):
    """ 编辑订单 """
    uid = request.GET.get("uid")
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({'status': False, 'tips': '数据不存在！'})

    form = OrderModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({"status": False, "error": form.errors})
