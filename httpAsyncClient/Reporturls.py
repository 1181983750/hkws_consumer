from django.urls import path

from httpAsyncClient.hkws_xf_xfmx.views import HKWSXFMXView

urlpatterns = [
    path('GetXfmxbyQuerystring/', HKWSXFMXView.as_view()), #POST  根据搜索条件 和日期范围 查询 消费明细
    path('GetCzmxbyQuerystring/', HKWSXFMXView.as_view()),  # POST  根据搜索条件 和日期范围 查询 充值明细
    path('GetTkmxbyQuerystring/', HKWSXFMXView.as_view()),  # POST  根据搜索条件 和日期范围 查询 退款明细
    path('GetBtmxbyQuerystring/', HKWSXFMXView.as_view()),  # POST  根据搜索条件 和日期范围 查询 批量补贴明细
    path('GetSingleBtmxbyQuerystring/', HKWSXFMXView.as_view()),  # POST  根据搜索条件 和日期范围 查询 单一补贴明细
    path('GetAllBtmxbyQuerystring/', HKWSXFMXView.as_view()),  # POST  根据搜索条件 和日期范围 查询 全部补贴明细
    path('GetAllRecordByQuerystring/', HKWSXFMXView.as_view()),  # POST  根据搜索条件 和日期范围 查询 全部明细
    path('GetCzmxStatistics/', HKWSXFMXView.as_view()),     #POST 获取 每日 充值金额 统计 情况  param: dateStart,dateEnd
]