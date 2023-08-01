# Creation time: 2022/6/7 9:46
# The author: Tiger_YC
from django.urls import path

from httpAsyncClient.imageUpload.views import SingleFileUploadView

urlpatterns = [
    path('post/', SingleFileUploadView.as_view({'post': 'singleFileUpload'})), #POST 单一文件上传
    path('postBase64/', SingleFileUploadView.as_view({'post': 'base64PicUpload'})), #POST base64编码上传
]

