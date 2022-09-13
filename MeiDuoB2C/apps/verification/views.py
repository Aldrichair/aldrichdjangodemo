from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import HttpResponse, JsonResponse
from libs.yuntongxun.sms import CCP
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

"""
短信验证
"""


class InfoCodeView(APIView):
    """
    短信验证
    接受经点击按钮传回的uuid和手机号码
    uuid用于校验redis当前已经存储的uuid验证码信息
    手机号码用于发送短信
    测试过程中需将手机号码是否重复验证关闭
    """
    # 1.接受前端消息 发送手机短信
    def get(self, request, mobile):
        import random
        ccp = CCP()
        num = ''
        for i in range(0, 5):
            num += str(random.randint(1, 11))
        # mobile = request.data.get('mobile')
        from django_redis import get_redis_connection
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')
        if not all([uuid, image_code]):
            return Response({
                'code': 400,
                'errmsg': '参数不全'
            })
        redis_cil = get_redis_connection('code')
        redis_image_code = redis_cil.get(uuid)
        # print('ric:'+redis_image_code)
        # print('ic:'+image_code)
        if redis_image_code is None:
            return Response({
                'code': 400,
                'errmsg': '验证码已过期',
            })
        # print('ric:'+redis_image_code)
        # print('ic:'+image_code)
        # image_code = redis_cil.get(str(request.data.get('image_code_id')))  # uuid
        # print('2')
        # print(f'image_code:{0}', request.data.get('image_code'))
        # print(f'im_id_code{0}', redis_cil.get(str(request.data.get('image_code_id'))))
        # if request.data.get('image_code') == image_code:
        if redis_image_code.decode().lower() == image_code.lower():
            send_flag = redis_cil.get('send_flag_%s' % mobile)
            if send_flag is not None:
                return Response({
                    'code': 400,
                    'errmsg': '频繁发送信息错误'
                })
            ccp.send_template_sms(mobile, [num, 5], 1)
            redis_cil.setex(mobile, 500, num)
            # 添加一个发送标记,有效期60秒
            # 新建一个管道
            pipeline = redis_cil.pipeline()
            # 管道收集指令
            pipeline.setex('send_flag_%s' % mobile, 60, 1)
            # 管道执行指令
            pipeline.execute()
            # redis_cil.setex('send_flag_%s' % mobile, 60, 1)
            return JsonResponse({
                'code': 0,
                'errmsg': 'ok'
            })
        else:
            return Response({
                'message': '图片验证码有误'
            }, status=400)


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
        print(text)
        redis_cli.setex(uuid, 1000, text)
        # 4.返回图片二进制
        # content_type 响应体数据类型 语法 大类/小类
        # return Response(image, content_type='image/jpeg')
        return HttpResponse(image, content_type='image/jpeg')