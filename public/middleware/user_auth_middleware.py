import datetime

import jwt
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

<<<<<<< HEAD
=======
from httpAsyncClient.models import hkws_xf_user
>>>>>>> master
from httpxs.settings import CG_ERP_KEY, api_settings

def jwt_decode_handler(token):
    """
    token解密
    :param token:
    :return:
    """
    options = {
        'verify_exp': api_settings.JWT_VERIFY_EXPIRATION,
    }
    return jwt.decode(
        token,
        api_settings.JWT_PUBLIC_KEY or api_settings.JWT_SECRET_KEY,
        api_settings.JWT_VERIFY,
        options=options,
        leeway=api_settings.JWT_LEEWAY,
        audience=api_settings.JWT_AUDIENCE,
        issuer=api_settings.JWT_ISSUER,
        algorithms=[api_settings.JWT_ALGORITHM]
    )





class TokenAuthMiddleware(MiddlewareMixin):
    def process_request(self, request, salt=CG_ERP_KEY):
        # 如果为下面的两个请求不做任何处理 return可以终止函数
        # print(request.path)

        if request.path == '/user/login/' or request.path == '/docs/' or '/static_files/file/' in request.path:
            pass
        else:
            # 从cookies中找ticket
            print('token 拦截中间件执行')
            try:
                # ticket = jwt.encode(payload={
                #     "id": "29490",
                #     "username": "童羿诚",
                #     "exp": 9653468700.589272
                # }, key=salt, headers={
                #     "alg": "HS256",
                #     "typ": "JWT"
                # })
                ticket = request.headers.get('Authorization').split('Bearer ')[1]
            except Exception as e:
                return JsonResponse({"message": "没有登录：%s" % e, "code": -1, "data": {}})
            # 判断取出的内容是否有效

            # 判断cookies中有没有ticket
            try:
                info = jwt_decode_handler(ticket)
            except jwt.ExpiredSignatureError:
                return JsonResponse({"message": 'Token过期', "code": -1, "data": {}})
            except jwt.DecodeError:
                return JsonResponse({"message": 'Token不合法', "code": -1, "data": {}})
            except jwt.InvalidTokenError as e:
                return JsonResponse({"message": "出现了无法预料的view视图错误：%s" % e, "code": -1, "data": {}})
            info.update(username=info['id'])
<<<<<<< HEAD
            print(info)
            request.info = info
=======
            qx_query = hkws_xf_user.objects.filter(username=info.get('username'))
            if not qx_query:
                return JsonResponse({"message": "你没有该权限", "code": -1, "data": {}})
            request.info = info

>>>>>>> master
