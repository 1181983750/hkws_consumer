import threading

from django.db import transaction
from django.http import JsonResponse
from rest_framework.viewsets import ViewSet

from public.utils.response_result import ResponseResult
from public.utils.standard import Standard, CheckException


class HKWSYGSBQYView(ViewSet, Standard):
    def __init__(self):
        super(HKWSYGSBQYView, self).__init__()
        self.service = None

    @transaction.atomic
    def set_face(self, request):
        """
         区域 下发人脸
        :param request:
        :return:
        """
        threading.Lock()
        data = request.data
        try:
            self.check(data, {'1': ['ygid']})
        except CheckException as e:
            return JsonResponse(ResponseResult(msg=str(e)).__call__())
        result_response = self.service(data, None)
        return JsonResponse(result_response.__call__())

