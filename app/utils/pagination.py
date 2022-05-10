"""
    自定义的分页组件,使用步骤如下

在视图函数中
def pretty_list(request):
    # 1、根据自己的情况去筛选自己的数据
    # data_dict = {}
    # search_data = request.GET.get('q', '')
    #
    # if search_data:
    #     data_dict = {"mobile__contains": search_data}
    # queryset = models.PrettyNum.objects.filter(**data_dict).order_by('-level')

    queryset = models.PrettyNum.objects.all()

    # 2、实例化分页对象
    page_object = Pagination(request, queryset)
    context = {
        "search_data": search_data,
        'queryset': page_object.page_queryset, # 分完页的数据
        "page_string": page_object.html()      # 生成页码
    }

    return render(request, 'app/pretty_list.html', context)

在HTML页面中
{% for obj in queryset %}
    {{ obj.xx }}
{% endfor %}
      <div class="clearfix">
            <ul class="pagination">
                {{ page_string }}
            </ul>
        </div>
"""
from django.utils.safestring import mark_safe
import copy

class Pagination(object):

    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        """
        :param request: 请求的对象
        :param queryset: 查询的符合条件的数据（根据这个数据给他进行分页处理）
        :param page_size: 每页显示多少条数据
        :param page_param: 在URL中传递的获取分页的参数，例如：http://127.0.0.1:8000/pretty_list/?page=1
        :param plus: 显示当前页的 前几页或后几页（根据页码）
        """

        from django.http.request import QueryDict

        quety_dict = copy.deepcopy(request.GET)
        quety_dict._mutable = True
        self.quety_dict = quety_dict
        self.page_param = page_param

        page = request.GET.get(page_param, "1")
        # isdecimal() 方法检查字符串是否只包含十进制字符
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start: self.end]

        # 计算总页码
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        # 计算出，当前页显示的前5页、后5页
        if self.total_page_count <= 2 * self.plus + 1:
            # 数据库中的数据比较少，都没有达到11页
            start_page = 1
            end_page = self.total_page_count
        else:
            # 当前页 < 5时
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                # 当前页 > 5时
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 页码
        page_str_list = []


        self.quety_dict.setlist(self.page_param, [1])
        page_str_list.append('<li ><a href="?{}">首页</a></li>'.format(self.quety_dict.urlencode()))

        # 上一页
        if self.page > 1:
            self.quety_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li ><a href="?{}">上一页</a></li>'.format(self.quety_dict.urlencode())
        else:
            # self.quety_dict.setlist(self.page_param, [1])
            prev = '<li ><a href="?{}">上一页</a></li>'.format(self.quety_dict.urlencode())
        page_str_list.append(prev)

        # 页面
        for i in range(start_page, end_page + 1):
            self.quety_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.quety_dict.urlencode(), i)
            else:
                ele = '<li ><a href="?{}">{}</a></li>'.format(self.quety_dict.urlencode(), i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            self.quety_dict.setlist(self.page_param, [self.page + 1])
            prev = '<li ><a href="?{}">下一页</a></li>'.format(self.quety_dict.urlencode())
        else:
            self.quety_dict.setlist(self.page_param, [self.total_page_count])
            prev = '<li ><a href="?{}">下一页</a></li>'.format(self.quety_dict.urlencode())
        page_str_list.append(prev)
        # 尾页
        self.quety_dict.setlist(self.page_param, [self.total_page_count])

        page_str_list.append('<li ><a href="?{}">尾页</a></li>'.format(self.quety_dict.urlencode()))

        search_string = """
            <li>
                <form style="float: left;margin-left: -1px" method="get">
                    <input type="text" name="page" class="form-control" placeholder="页码"
                           style="position: relative;float: left;display: inline-block;width: 80px;border-radius: 0;">
                    <button style="border-radius: 0;border: 0px;background: rgba(0,0, 0, 0);" class="btn btn-default" type="submit">跳转</button>
                </form>
            </li>
            """
        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))
        return page_string
