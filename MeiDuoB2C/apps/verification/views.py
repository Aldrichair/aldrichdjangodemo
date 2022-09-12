from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import HttpResponse
# Create your views here.

"""
前端 
    拼接一个url,然后给img img会发起请求
    url = http://www.meiduo.site:8000/image_codes/b44ec53c-7b9d-49d7-a63e-f0a8ecec2310/
    url = http://ip:port/image_codes/uuid
    
后端
    请求      接收路由中的uuid
    业务逻辑   生成图片验证码和图片二进制 通过redis把图片验证码保存下来
    响应      返回图片二进制
    路由:   GET  image_codes/uuid
    步骤:     
            1. 接受路由uuid
            2.生成验证码和二进制
            3.通过redis把图片验证码保存起来
            4.返回图片二进制
"""


class ImageCodeView(APIView):
    def get(self, request, uuid):
        # 1. 接受路由uuid
        from libs.captcha.captcha import captcha
        # 2.生成验证码和二进制
        # text是验证码内容 image是二进制
        text, image = captcha.generate_captcha()
        # 3.通过redis把图片验证码保存起来
        from django_redis import get_redis_connection
        redis_cli = get_redis_connection('code')
        # setex(name,time,value)    键名 过期时间 键值
        redis_cli.setex(uuid, 100, text)
        # 4.返回图片二进制
        # content_type 响应体数据类型 语法 大类/小类
        # return Response(image, content_type='image/jpeg')
        return HttpResponse(image, content_type='image/jpeg')