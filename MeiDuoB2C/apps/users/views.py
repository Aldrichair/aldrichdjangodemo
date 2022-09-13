import re
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# Create your views here.


"""
需求分析:根据页面的功能(从上到下,从左到右),哪些功能需要和后端配合
如何确定 哪些功能需要进行交互?
1.经验  2.关注类似网站问题
"""
"""
判断用户名是否重复的功能
前端:     当用户输入用户名之后,失去焦点,发送一个axios(ajax)请求

后端:
    请求:     接受用户名
    业务逻辑:  根据用户名查询数据库,如果查询结果数量等于0,说明没有注册 等于1则有注册       
    响应:     JSON{
                code:0, count: 0/1, errmsg: ok  
                # code表示状态码 errmsg表示错误信息 count为记录用户数
                }
    路由       GET   usernam34e/(?<username>[a-zA-z0-9_-]{5,20}/count/  # 用户名的数量 
    步骤:
        1. 接受用户名
        2. 根据用户名查询数据库
        3.返回响应
"""
from rest_framework.views import APIView
from apps.users.models import User
from django.http.response import JsonResponse
from .serializer import UserSerializer


class UsernameCountView(APIView):
    def get(self, request, username):
        # 1. 接受用户名
        # re.match 尝试从字符串的起始位置匹配一个模式，
        # 如果不是起始位置匹配成功的话，match() 就返回 none。
        # if not re.match('[a-zA-z0-9_-]{5,20}', username):      # 合法性验证
        #     return JsonResponse({'code': 200, 'errmsg': '用户名不满足需求'})
        # # 2. 根据用户名查询数据库
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})


class MobileCountView(APIView):
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()

        return JsonResponse({
            'code': 0,
            'count': count,
            'errmsg': 'ok',
        })


"""
用户注册
前端:     当用户输入完信息后 前端会发送axios请求至后端
后端:   
        code: 0成功 1失败
        请求: 接收数据(JSON),获取数据
        业务逻辑: 对前端数据进一步验证(无问题则入库)
        响应:{'code':0,'errmsg':'ok'}
        路由: POST
        步骤:
            1.接受数据(POST----JSON)
                验证数据
            2.获取数据
                用户名不可重复
            3.验证数据 
            4.数据入库 
            5.返回响应
"""

import json


class RegisterView(APIView):
    # @csrf_exempt
    def post(self, request):
        # body_bytes = request.data
        # # body_str = body_bytes.decode()
        # body_dict = json.loads(str(body_bytes))
        # # username = body_dict['']
        # username = body_dict.get('username')  # 最好这样用
        # password = body_dict.get('password')
        # password2 = body_dict.get('password2')
        # mobile = body_dict.get('mobile')
        # allow = body_dict.get('allow')
        print(request.data)
        username = request.data.get('username')
        password = request.data.get('password')
        password2 = request.data.get('password2')
        mobile = request.data.get('mobile')
        allow = request.data.get('allow')
        if not all([username, password, password2, mobile, allow]):
            return JsonResponse({
                'code': 400,
                'errmsg': '参数不全',
            }, json_dumps_params={'ensure_ascii': False}, safe=True)
        if not re.match('[a-zA-Z_-]{5,20}', username):
            return JsonResponse({'code': 400,
                                 'errmsg': '用户名不满足规则'}, safe=False
                                , json_dumps_params={'ensure_ascii': False})
        if password != password2:
            return JsonResponse({
                'code': 400,
                'errmsg': '两次输入密码不一致',
            }, safe=False, json_dumps_params={'ensure_ascii': False})
        if len(mobile) != 11:
            return JsonResponse({
                'code': 400,
                'errmsg': '电话长度不匹配',
            }, safe=False, json_dumps_params={'ensure_ascii': False})
        """写的很冗余"""
        if allow == 'True':
            allow = True
        else:
            allow = False
        if not allow:
            return JsonResponse({
                'code': 400,
                'errmsg': '未同意注册协议',
            }, safe=False, json_dumps_params={'ensure_ascii': False})
        """
        这里我想用反序列化器 但是我感觉我有重复判断的嫌疑 
        而且我不清楚我可选字段选了所有,不确定是否会报错
        """
        # user = User.objects.filter(username=request.query_params.get('username'))
        # serializer = UserSerializer(instance=user, many=True)
        # serializer.is_valid(ra-ise_exception=True)
        # serializer.save()
        # 未加密
        # User.objects.create(username=username, password=password, mobile=mobile)
        # 加密
        user = User.objects.create_user(username=username, password=password, mobile=mobile)
        from django.contrib.auth import login
        login(request, user)
        return JsonResponse({'code': 0,
                             'errmsg': 'ok'}, safe=False, json_dumps_params={'ensure_ascii': False})


"""
实现状态保持
    在客户端存储信息时使用cookie
    在服务端存储信息时使用session
"""