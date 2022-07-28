# Creation time: 2022/6/2 15:38
# The author: Tiger_YC
from decimal import Decimal

from django.db import transaction
from django.http import JsonResponse
from rest_framework.viewsets import ViewSet

from httpAsyncClient.hkws_xf_btmd.hkws_xf_btmd_services import HKWSXFBTServices
from httpAsyncClient.models import hkws_xf_btmd
from httpAsyncClient.serializers import hkws_xf_btmdModelSerializer
from public.utils.response_result import ResponseResult
from public.utils.standard import Standard, CheckException
from public.utils import EmployeesToBanlanceConstruction as EC


class HKWSXFBTMDView(ViewSet, Standard):
    def __init__(self):
        super(HKWSXFBTMDView, self).__init__()
        self.service = HKWSXFBTServices(hkws_xf_btmd)

    @transaction.atomic
    def addBatchSubsidy(self, request):
        """
        增加批量补贴名单 类型6
        :param request:  ygid, amount, bz 必填
        :return:
        """
        data: dict = request.data
        data.update(EC.BATCHSUBSIDY)
        if not all([data.get('ygid'), data.get('amount'), data.get('bz')]):
            return JsonResponse(ResponseResult("你这信息也不全啊").__call__())
        data['amount'] = Decimal(data.get('amount', 0))
        result_response = self.service.add_batch_subsidy(data, hkws_xf_btmdModelSerializer)
        return JsonResponse(result_response.__call__())

    @transaction.atomic
    def delBatchSubsidy(self, request):
        """
        删除批量补贴名单 类型6
        :param request:
        :return:
        """
        data: dict = request.data
        if not all([data.get('ygid')]):
            return JsonResponse(ResponseResult("你这员工id也没给啊").__call__())
        result_response = self.service.del_batch_subsidy(data, hkws_xf_btmdModelSerializer)
        return JsonResponse(result_response.__call__())

    def selBatchSubsidy(self, request):
        """
        查询所有批量补贴名单
        :param request:
        :return:
        """
        data: dict = request.data
        # if not all([data.get('queryString')]):
        #     return JsonResponse(ResponseResult("你这搜索条件也没给啊").__call__())
        result_response = self.service.sel_batch_subsidy(data.get('queryString'), hkws_xf_btmdModelSerializer)
        return JsonResponse(result_response.__call__())

    @transaction.atomic
    def selBatchSubsidyByMonth(self, request):
        """
        根据月份查询当月批量补贴名单
        :param request:
        :return:
        """
        data: dict = request.data
        if not all([data.get('month')]):
            return JsonResponse(ResponseResult("你这搜索条件month也没给啊").__call__())
        result_response = self.service.sel_batch_subsidy_by_month(data.get('month'), hkws_xf_btmdModelSerializer)
        return JsonResponse(result_response.__call__())

    def updateBatchSubsidy(self, request):
        """
        修改批量补贴名单
        :param request:
        :return:
        """
        data: dict = request.data
        try:
            self.check(data, {"1": ['ygid', 'amount', 'bz']})
        except CheckException as e:
            return JsonResponse(ResponseResult(str(e)).__call__())
        result_response = self.service.update_batch_subsidy(data, hkws_xf_btmdModelSerializer)
        return JsonResponse(result_response.__call__())

    @transaction.atomic
    def execBatchSubsidy(self, request):
        """
        执行批量补贴的名单
        :param request:
        :return:
        """
        data: dict = request.data
        data.update(sbip=request.META['REMOTE_ADDR'], czy=request.info['username'])
        result_response = self.service.exec_batch_subsidy(data, hkws_xf_btmdModelSerializer)
        return JsonResponse(result_response.__call__())



