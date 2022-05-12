from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class AuthMiddlewareMixin(MiddlewareMixin):
    """ 中间件1 """

    def process_request(self, request):

        # 1、排除哪些不需要登录就能访问的页面
        # request.path_info获取当前用户请求的url
        if request.path_info in  ["/login/", '/image_code/']:
            return None

        # 2、读取当前访问的用户的session信息，如果能读到，说明已登录，可继续访问动作
        info_dict = request.session.get('info')
        if info_dict:
            return

        # 3、如果没有登陆过，重定向回登录页面
        return redirect('/login/')







