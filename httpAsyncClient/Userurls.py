# Creation time: 2022/5/31 14:47
# The author: Tiger_YC

from django.urls import path

from httpAsyncClient.rs_ygxx.views import RSYGXXView

urlpatterns = [
    path('getYgxx/',RSYGXXView.as_view({'post': 'get_ygxx_query'})), #POST 查询充值员工信息  未离职的 可选queryString
    path('getYgxxByYgdm/', RSYGXXView.as_view({'post': 'get_ygxx_ygdm'})),  # POST 通过ygdm取得员工信息 未离职的 可选queryString
    path('getNoFaceYgxx/', RSYGXXView.as_view({'get': 'get_NoFace_ygxx'})), #GET 获取需要采集人脸的员工信息 queryString
    path('getAllYgxx/', RSYGXXView.as_view({'post': 'get_all_ygxx'})), #POST 获取所有的员工信息 queryString
]

