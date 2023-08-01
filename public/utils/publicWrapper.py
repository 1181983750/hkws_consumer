# Creation time: 2022/5/31 21:36
# The author: Tiger_YC
import datetime
import re
import time
import traceback

from django.http import JsonResponse

from httpAsyncClient.models import hkws_xf_xfmx
from public.utils.response_result import ResponseResult

def nonce_valid(func):
    """
    验证时间 防止前端充值、扣款、补贴、退款、高并发 导致明细混乱
    :param func:
    :return: 装饰器  被装饰的方法必须继承DRF视图才可使用
    """
    def wrapper(self, request, *args, **kwargs):
        data: dict = request.data
        if data.get('nonce'):
            nonce = datetime.datetime.strptime(data.get('nonce'), '%Y-%m-%d %H:%M:%S')
            last_sjrq = hkws_xf_xfmx.objects.filter(ygid=data.get('ygid')).order_by('-sjrq').only('sjrq').first()
            if last_sjrq:
                i_nonce = int(datetime.datetime.timestamp(nonce))
                time_result = i_nonce - int(datetime.datetime.timestamp(last_sjrq.sjrq))
                if abs(time_result) < 1:
                    return JsonResponse(ResponseResult(msg='请勿重复点击').__call__())
        else:
            return JsonResponse(ResponseResult(msg='时效码未更新').__call__())
        print('执行后的日期格式', data)
        result = func(self, request, *args, **kwargs)
        return result
    return wrapper


def datetime_format(func):
    """
    日期时间 格式处理装饰器  防止前端不穿 时分秒导致无法搜索datetime字段
    :param func:
    :return: 装饰器  被装饰的方法必须继承DRF视图才可使用
    """
    def wrapper(self, request, *args, **kwargs):
        data: dict = request.data
        now = datetime.datetime.now()
        pattern = re.compile(r' \d{1,2}:\d{1,2}:\d{1,2}$')
        if data.get('dateStart') and pattern.search(data.get('dateStart')):
            try:
                datetime.datetime.strptime(data.get('dateStart', 'None'), '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    datetime.datetime.strptime(data.get('dateStart', 'None'), '%Y/%m/%d %H:%M:%S')
                except:
                    print('dateStart系统替换')
                    data.update(dateStart=now.date().strftime('%Y-%m-%d') + " 00:00:00")
        elif data.get('dateStart') and not pattern.search(data.get('dateStart')):
            try:
                datetime.datetime.strptime(data.get('dateStart', 'None'), '%Y-%m-%d')
            except ValueError:
                try:
                    datetime.datetime.strptime(data.get('dateStart', 'None'), '%Y/%m/%d')
                except:
                    print('dateStart系统替换')
                    data.update(dateStart=now.date().strftime('%Y/%m/%d') + " 00:00:00")
            else:
                data.update(dateStart=data['dateStart'].strip() + " 00:00:00.000")

        if data.get('dateEnd') and pattern.search(data.get('dateEnd')):
            try:
                datetime.datetime.strptime(data.get('dateEnd', 'null'), '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    datetime.datetime.strptime(data.get('dateEnd', 'None'), '%Y/%m/%d %H:%M:%S')
                except:
                    print('dateEnd系统替换')
                    data.update(dateEnd=now.date().strftime('%Y-%m-%d') + " 23:59:59.999")
        elif data.get('dateEnd') and not pattern.search(data.get('dateEnd')):
            try:
                datetime.datetime.strptime(data.get('dateEnd', 'null'), '%Y-%m-%d')
            except ValueError:
                try:
                    datetime.datetime.strptime(data.get('dateEnd', 'None'), '%Y/%m/%d')
                except:
                    print('dateEnd系统替换')
                    data.update(dateEnd=now.date().strftime('%Y/%m/%d') + " 23:59:59.999")
                else:
                    data.update(dateEnd=data['dateEnd'].strip() + " 23:59:59.999")
            else:
                data.update(dateEnd=data['dateEnd'].strip() + " 23:59:59.999")

        print('执行后的日期格式', data)
        result = func(self, request, *args, **kwargs)
        return result
    return wrapper