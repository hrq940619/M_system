from django.shortcuts import render

# Create your views here.
from app import models


def depart_list(request):
    """ 部门列表 """
    queryset = models.Department.objects.all()
    return render(request,'app/depart_list.html', {'queryset':queryset})