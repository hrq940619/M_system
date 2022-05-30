from django.http import JsonResponse
from django.shortcuts import render


def chart_list(request):
    """ 数据统计 """
    return render(request, 'app/chart_list.html')


def chart_bar(request):
    """ 构造柱状图的数据 """
    legend = ['张飞', '赵云']

    series_list = [
        {
            'name': '张飞',
            'type': 'bar',
            'data': [5, 20, 36, 10, 10, 20]
        },
        {
            'name': '赵云',
            'type': 'bar',
            'data': [56, 30, 16, 5, 40, 35]
        }
    ]

    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月']

    result = {
        'status': True,
        'data': {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


def chart_pie(request):
    """ 构造饼图的数据 """

    db_data_list = [
        {'value': 1048, 'name': 'IT部门'},
        {'value': 735, 'name': '新媒体'},
        {'value': 580, 'name': '运营'},
    ]
    result = {
        "status": True,
        "data": db_data_list
    }
    return JsonResponse(result)


def chart_line(request):
    legend = ['蜀国', '魏国']

    series_list = [
        {
            'name': '蜀国',
            'type': 'line',
            "stack": "Total",
            'data': [5, 20, 36, 10, 10, 20]
        },
        {
            'name': '魏国',
            'type': 'line',
            "stack": "Total",
            'data': [56, 30, 16, 5, 40, 35]
        }
    ]

    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月']

    result = {
        'status': True,
        'data': {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)

def chart_highcharts(request):
    """ highcharts示例 """

    return render(request, 'app/highcharts.html')
