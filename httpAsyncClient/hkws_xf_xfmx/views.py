import datetime
from decimal import Decimal

<<<<<<< HEAD
from django.db import transaction
=======

>>>>>>> master
from django.http import JsonResponse
from rest_framework.views import APIView

from httpAsyncClient.hkws_xf_xfmx.hkws_xf_xfmx_services import HKWSXFMXServices
from httpAsyncClient.models import hkws_xf_xfmx
from httpAsyncClient.serializers import hkws_xf_xfmxModelSerializer
from public.utils import EmployeesToBanlanceConstruction as EC
<<<<<<< HEAD
from public.utils.publicWrapper import datetime_format, nonce_valid
=======
from public.utils.publicWrapper import datetime_format
>>>>>>> master
from public.utils.response_result import ResponseResult
from public.utils.standard import CheckException, Standard


class HKWSXFMXView(APIView, Standard):
    def __init__(self, **kwargs):
        super(HKWSXFMXView, self).__init__()
        self.service = HKWSXFMXServices(hkws_xf_xfmx)
        self.nonce = ''

    # 主方法
<<<<<<< HEAD
    @transaction.atomic
=======
>>>>>>> master
    def post(self, request):
        print('访问的path:', request.path)
        if request.path == '/Recharge/':
            """我就是员工充值"""
            return self.recharge(request)
        elif request.path == '/Deduction/':
            """员工扣款"""
            return self.deduction(request)
        elif request.path == '/Subsidy/':
            """员工补贴"""
            return self.subsidy(request)
        elif request.path == '/Refund/':
            """员工退款"""
            return self.refund(request)
        elif request.path == '/Report/GetXfmxbyQuerystring/':
            """根据搜索条件 和日期范围 查询 消费明细"""
            return self.get_xfmx_by_query(request)
        elif request.path == '/Report/GetCzmxbyQuerystring/':
            """根据搜索条件 和日期范围 查询 充值明细"""
            return self.get_czmx_by_query(request)
        elif request.path == '/Report/GetTkmxbyQuerystring/':
            """根据搜索条件 和日期范围 查询 退款明细"""
            return self.get_tkmx_by_query(request)
        elif request.path == '/Report/GetBtmxbyQuerystring/':
            """根据搜索条件 和日期范围 查询 补贴明细"""
            return self.get_btmx_by_query(request)
        elif request.path == '/Report/GetSingleBtmxbyQuerystring/':
            """根据搜索条件 和日期范围 查询 单一补贴明细"""
            return self.get_single_btmx_by_query(request)
        elif request.path == '/Report/GetAllBtmxbyQuerystring/':
            """根据搜索条件 和日期范围 查询 批量补贴明细"""
            return self.get_all_btmx_by_query(request)
        elif request.path == '/Report/GetAllRecordByQuerystring/':
            """根据搜索条件 和日期范围 查询 全部明细"""
            return self.get_all_mx_by_query(request)
        elif request.path == '/Report/GetCzmxStatistics/':
            """获取 每日 充值 统计 情况"""
            return self.get_czmx_statistics(request)
<<<<<<< HEAD
        return JsonResponse(ResponseResult(msg='此请求地址有误').__call__())

    # @nonce_valid
    def recharge(self, request):
        """这里开始是用工充值"""
=======
        elif request.path == '/Report/GetDaysCountCZmx/':
            """根据 日期范围 统计充值明细 """
            return self.getDaysCountCZmx(request)
        return JsonResponse(ResponseResult(msg='此请求地址有误').__call__())

    def recharge(self, request):
        """这里开始是用工充值"""

>>>>>>> master
        data: dict = request.data
        data.update({'sbip': request.META['REMOTE_ADDR']})
        data.update(czy=request.info.get('username', None))
        data.update(EC.RECHARGE)  # 1代表  消费类型为充值
        # 入参检查
        try:
            self.check(data, {'1': ['sbip', 'ygid', 'amount', 'nonce', 'czy', 'xflx', 'xflxmc']})
        except CheckException as e:
            return JsonResponse(ResponseResult(msg=str(e), data={}).__call__())
        if Decimal(data['amount']) <= 0:
            return JsonResponse(ResponseResult(msg='不能充值负数值', data={}).__call__())
        data['amount'] = abs(Decimal(data['amount']))  # 取绝对值 并且改为Decimal类型
        result_response = self.service.add_money(data, hkws_xf_xfmxModelSerializer)
        return JsonResponse(result_response.__call__())

    def deduction(self, request):
        """
        员工扣费    - 法
        :param request:
        :return:
        """
        data: dict = request.data
        data.update({'sbip': request.META['REMOTE_ADDR']})
        data.update(czy=request.info.get('username', None))
        data.update(xfrq=datetime.datetime.now())  #消费日期
        data.update(EC.DEDUCTION)   # 2代表  消费类型为扣费
        try:
            self.check(data, {'1': ['sbip', 'ygid', 'amount', 'nonce', 'czy', 'xflx', 'xflxmc', 'xfrq']})
        except CheckException as e:
            return JsonResponse(ResponseResult(msg=str(e)).__call__())
        data['amount'] = abs(Decimal(data['amount']))  # 取绝对值
        result_response = self.service.deduction_money(data, hkws_xf_xfmxModelSerializer)
        return JsonResponse(result_response.__call__())

    def refund(self, request):
        """
        员工退款   现金退款   -法
        :param request:
        :return:
        """
        data: dict = request.data
        data.update(sbip=request.META['REMOTE_ADDR'])
        data.update(czy=request.info['username'])
        data.update(EC.CASHREFUND)   # 5代表  类型为现金退款
        try:
            self.check(data, {'1': ['sbip', 'ygid', 'amount', 'nonce', 'czy', 'xflx', 'xflxmc']})
        except CheckException as e:
            return JsonResponse(ResponseResult(msg=str(e)).__call__())
        data['amount'] = abs(Decimal(data['amount']))  # 取绝对值
        result_response = self.service.refund_money(data, hkws_xf_xfmxModelSerializer)
        return JsonResponse(result_response.__call__())

    def subsidy(self, request):
        """
        员工补贴 3  可能为正  可能为负  amount
        :param request:
        :return:
        """
        data: dict = request.data
        data.update({'sbip': request.META['REMOTE_ADDR']})
        data.update(czy=request.info['username'])
        data.update(EC.SUBSIDY)
        try:
            self.check(data, {'1': ['sbip', 'ygid', 'amount', 'nonce', 'czy', 'xflx', 'xflxmc', 'sfbt']})
        except CheckException as e:
            return JsonResponse(ResponseResult(msg=str(e)).__call__())
        data['amount'] = Decimal(data.get('amount', 0))
        result_response = self.service.subsidy_money(data, hkws_xf_xfmxModelSerializer)
        return JsonResponse(result_response.__call__())

    @datetime_format
    def get_xfmx_by_query(self, request):
        """根据搜索条件 和日期范围 查询 消费明细"""
        data: dict = request.data
        # try:
        #     data['dateStart'] = datetime.datetime.strptime(data.get('dateStart', 'None'), '%Y-%m-%d')
        #     data['dateEnd'] = datetime.datetime.strptime(data.get('dateEnd', 'null'), '%Y-%m-%d')
        # except:
        #     return JsonResponse(ResponseResult(msg='查询日期格式不对，YYYY-MM-DD', data=[])())
        result_response = self.service.get_xfmx(data, hkws_xf_xfmxModelSerializer)
        return JsonResponse(result_response.__call__())

    @datetime_format
    def get_czmx_by_query(self, request):
        """根据搜索条件 和日期范围 查询 充值明细"""
        data: dict = request.data
        # try:
        #     data['dateStart'] = datetime.datetime.strptime(data.get('dateStart', 'None'), '%Y-%m-%d')
        #     data['dateEnd'] = datetime.datetime.strptime(data.get('dateEnd', 'null'), '%Y-%m-%d')
        # except:
        #     return JsonResponse(ResponseResult(msg='查询日期格式不对，YYYY-MM-DD', data=[])())
        result_response = self.service.get_czmx(data, hkws_xf_xfmxModelSerializer)
        return JsonResponse(result_response.__call__())

    @datetime_format
<<<<<<< HEAD
=======
    def getDaysCountCZmx(self, request):
        """根据日期范围统计充值明细"""
        data: dict = request.data
        result_response = self.service.get_czmx_by_rangeDate(data, hkws_xf_xfmxModelSerializer)
        return JsonResponse(result_response.__call__())

    @datetime_format
>>>>>>> master
    def get_tkmx_by_query(self, request):
        """根据搜索条件 和日期范围 查询 消费退款与现金退款"""
        data: dict = request.data
        result_response = self.service.get_tkmx(data, hkws_xf_xfmxModelSerializer)
        return JsonResponse(result_response.__call__())

    @datetime_format
    def get_btmx_by_query(self, request):
        """根据搜索条件 和日期范围 查询 正负 批量 补贴明细"""
        data: dict = request.data
        # try:
        #     datetime.datetime.strptime(data.get('dateStart', 'None'), '%Y-%m-%d')
        #     datetime.datetime.strptime(data.get('dateEnd', 'null'), '%Y-%m-%d')
        #     print('通过了')
        # except:
        #     return JsonResponse(ResponseResult(msg='查询日期格式不对，YYYY-MM-DD', data=[])())
        result_response = self.service.get_btmx(data, hkws_xf_xfmxModelSerializer)
        return JsonResponse(result_response.__call__())

    @datetime_format
    def get_single_btmx_by_query(self, request):
        """根据搜索条件 和日期范围 查询 正负 单一 补贴明细"""
        data: dict = request.data
        # try:
        #     datetime.datetime.strptime(data.get('dateStart', 'None'), '%Y-%m-%d')
        #     datetime.datetime.strptime(data.get('dateEnd', 'null'), '%Y-%m-%d')
        # except:
        #     return JsonResponse(ResponseResult(msg='查询日期格式不对，YYYY-MM-DD', data=[])())
        result_response = self.service.get_single_btmx(data, hkws_xf_xfmxModelSerializer)
        return JsonResponse(result_response.__call__())

    @datetime_format
    def get_all_btmx_by_query(self, request):
        """根据搜索条件 和日期范围 查询 补贴明细"""
        data: dict = request.data
        # try:
        #     datetime.datetime.strptime(data.get('dateStart', 'None'), '%Y-%m-%d')
        #     datetime.datetime.strptime(data.get('dateEnd', 'null'), '%Y-%m-%d')
        # except:
        #     return JsonResponse(ResponseResult(msg='查询日期格式不对，YYYY-MM-DD', data=[])())

        result_response = self.service.get_all_btmx(data, hkws_xf_xfmxModelSerializer)
        return JsonResponse(result_response.__call__())

    @datetime_format
    def get_all_mx_by_query(self, request):
        """根据搜索条件 和日期范围 查询 全部明细"""
        data: dict = request.data
        # try:
        #     datetime.datetime.strptime(data.get('dateStart', 'None'), '%Y-%m-%d')
        #     datetime.datetime.strptime(data.get('dateEnd', 'null'), '%Y-%m-%d')
        # except:
        #     return JsonResponse(ResponseResult(msg='查询日期格式不对，YYYY-MM-DD', data=[])())
        result_response = self.service.get_all_mx(data, hkws_xf_xfmxModelSerializer)
        return JsonResponse(result_response.__call__())

    @datetime_format
    def get_czmx_statistics(self, request):
        """根据日期范围 查询 获取 每日 充值 统计 情况"""
        data: dict = request.data
        result_response = self.service.get_everyday_czmx_count(data, hkws_xf_xfmxModelSerializer)
        return JsonResponse(result_response.__call__())


