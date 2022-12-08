from django.db import transaction
from django.http import JsonResponse
from rest_framework.viewsets import ViewSet

from httpAsyncClient.hkws_xf_ygye.hkws_xf_ygye_services import HKWSXFYGYEServices
from httpAsyncClient.models import hkws_xf_ygye
from httpAsyncClient.serializers import hkws_xf_xfmxModelSerializer
from public.utils.response_result import ResponseResult
from public.utils.standard import Standard, CheckException


class HKWSXFYGYEView(ViewSet, Standard):
    def __init__(self):
        super(HKWSXFYGYEView, self).__init__()
        self.service = HKWSXFYGYEServices(hkws_xf_ygye)

    @transaction.atomic
    def get_query_ygye(self, request):
        """
        获取员工余额
        :return:
        """
        try:
            self.check(request.GET, {'1': ['ygid']})
        except CheckException as e:
            return JsonResponse(ResponseResult(msg=str(e)).__call__())
        result_response = self.service.get_ygye(request.GET['ygid'], hkws_xf_xfmxModelSerializer)
        return JsonResponse(result_response.__call__())

    @transaction.atomic
    def fix_query_ygye(self, request):
        """
        修复员工明细不准的脚本
        :param request:
        :return:
        """
        # data = abs(Decimal('-55.55'))  # 取绝对值
        result_response = self.service.fix_xfmx_ygye(request.GET['ygid'], hkws_xf_xfmxModelSerializer)
        return JsonResponse(result_response.__call__())

