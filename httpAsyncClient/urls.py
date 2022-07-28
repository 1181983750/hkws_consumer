
from django.urls import path

from httpAsyncClient.hkws_xf_xfmx.views import HKWSXFMXView
from httpAsyncClient.hkws_xf_ygye.views import HKWSXFYGYEView

urlpatterns = [
    path('Recharge/', HKWSXFMXView.as_view()), #POST 员工充值
    path('Deduction/', HKWSXFMXView.as_view()),  # POST 员工扣费
    path('Refund/', HKWSXFMXView.as_view()),  # POST 员工退款
    path('Subsidy/', HKWSXFMXView.as_view()),  # POST 员工补贴
    path('ygye/',HKWSXFYGYEView.as_view({'get':'get_query_ygye'})), #GET 通过query ygid 查询员工余额
    path('fix_ygye/', HKWSXFYGYEView.as_view({'get': 'fix_query_ygye'})),  # GET 通过query ygid 修复员工明细余额
]
