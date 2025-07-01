# Creation time: 2022/6/2 15:21
# The author: Tiger_YC


from django.urls import path

from httpAsyncClient.hkws_xf_btmd.views import HKWSXFBTMDView

urlpatterns = [
    path('addBatchSubsidy/', HKWSXFBTMDView.as_view({'post': 'addBatchSubsidy'})), #POST  根据搜索条件 和日期范围 查询 消费明细
    path('delBatchSubsidy/', HKWSXFBTMDView.as_view({'post': 'delBatchSubsidy'})),  # POST  根据搜索条件 和日期范围 查询 充值明细
    path('selBatchSubsidy/', HKWSXFBTMDView.as_view({'post': 'selBatchSubsidy'})),  # POST  根据搜索条件 和日期范围 查询 退款明细
    path('selBatchSubsidyByMonth/', HKWSXFBTMDView.as_view({'post': 'selBatchSubsidyByMonth'})),  # POST  根据搜索条件 和日期范围 查询 批量补贴明细
    path('updateBatchSubsidy/', HKWSXFBTMDView.as_view({'post': 'updateBatchSubsidy'})),  # POST  根据搜索条件 和日期范围 查询 单一补贴明细
    path('execBatchSubsidy/', HKWSXFBTMDView.as_view({'get': 'execBatchSubsidy'})),  # POST  根据搜索条件 和日期范围 查询 全部补贴明细
]