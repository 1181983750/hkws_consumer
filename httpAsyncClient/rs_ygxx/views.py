# Creation time: 2022/5/31 15:08
# The author: Tiger_YC
from django.db import transaction
from django.http import JsonResponse
from rest_framework.viewsets import ViewSet

from httpAsyncClient.models import rs_ygxx
from httpAsyncClient.rs_ygxx.rs_ygxx_services import RSYGXXServices
from httpAsyncClient.serializers import rs_ygxxModelSerializer
from public.utils.response_result import ResponseResult


class RSYGXXView(ViewSet):
    def __init__(self):
        super(RSYGXXView, self).__init__()
        self.service = RSYGXXServices(rs_ygxx)

    def get_ygxx_query(self, request):
        """
        查询充值员工信息 没离职的
        :param request: queryString
        :return:
        """
        result_response = self.service.get_ygxx_wlz_or_by_query(request.data.get('queryString'), rs_ygxxModelSerializer)
        return JsonResponse(result_response.__call__())

    def get_ygxx_ygdm(self, request):
        """
        根据 ygdm 查询 员工信息
        :param request:
        :return:
        """
        if not all([request.data.get('ygdm')]):
            return JsonResponse(ResponseResult(msg='ygdm必传').__call__())
        result_response = self.service.get_ygxx_by_ygdm(request.data['ygdm'], rs_ygxxModelSerializer)
        return JsonResponse(result_response.__call__())

    def get_NoFace_ygxx(self, request):
        """
        获取需要采集人脸的员工信息
        :param request:
        :return:
        """

        result_response = self.service.get_noface_ygxx(request.GET.get('queryString'))
        return JsonResponse(result_response.__call__())

    def get_all_ygxx(self, request):
        """
        获取需要所有的员工信息
        :param request:
        :return:
        """
        result_response = self.service.get_all_ygxx(request.data.get('queryString'))
        return JsonResponse(result_response.__call__())


