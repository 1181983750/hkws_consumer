from django.http import JsonResponse
from rest_framework.viewsets import ViewSet

from httpAsyncClient.imageUpload.model import ImageFileds
from httpAsyncClient.imageUpload.uploads_services import UploadServices
from httpAsyncClient.models import hkws_xf_sbygxx
from public.utils.onlineTime import getBeijinTime
from public.utils.response_result import ResponseResult


class SingleFileUploadView(ViewSet):
    def __init__(self):
        super(SingleFileUploadView, self).__init__()
        self.service = UploadServices(ImageFileds)

    def singleFileUpload(self, request):
        """
        单一图片文件上传
        :param request:
        :return:
        """
        ygid = request.data.get('ygid')
        file = request.data.get('file')
        type_list = ['image/jpeg', 'image/bmp', 'image/tiff', 'image/jpg', 'image/png']
        if not all([ygid, file]):
            return JsonResponse(ResponseResult('不全啊数据')())
        if file.content_type not in type_list:
            return JsonResponse(ResponseResult('格式不对')())
        if file.size > 3333333:
            return JsonResponse(ResponseResult(msg='文件大小不能超过3M').__call__())
        #生成不重复文件名
        # now = getBeijinTime()[0]
        # file.name = f"{ygid}-{now.get('year')}-{now.get('month')}-{now.get('day')}.{file.name.split('.')[1]}"
        file.name = f"{ygid}.jpg"
        result_response = self.service.upload_image(file)
        # 删除下发记录 重新下发本地文件人脸
        hkws_xf_sbygxx.objects.filter(ygid=ygid).delete()
        return JsonResponse(result_response.__call__())

    def base64PicUpload(self, request):
        """
        base64编码上传
        :param request:
        :return:
        """
        now = getBeijinTime()[0]
        ygid = request.data.get('ygid')
        base64_file = request.data.get('base64pic')
        if not all([ygid, base64_file]):
            return JsonResponse(ResponseResult('不全啊数据')())
        # 生成不重复文件名
        filename = f"{ygid}.jpg"
        result_response = self.service.upload_base64_image(base64_file, filename)
        return JsonResponse(result_response.__call__())


