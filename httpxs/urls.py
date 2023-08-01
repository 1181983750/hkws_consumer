"""httpxs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from httpAsyncClient import urls, Reporturls, Userurls, BatchSubsidyurls, imageurls
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', include(urls)), #充值 扣费 补贴 退款
    path('Report/', include(Reporturls)), #All POST     查询各类明细 及附带条件
    path('User/', include(Userurls)), #All POST     查询各类明细 及附带条件
    path('BatchSubsidy/', include(BatchSubsidyurls)), #All POST 批量补贴总路由
    path('image/', include(imageurls)),  # All POST 图片处理
    # path('Celery/', include(Celery_urls)) # 定时任务
<<<<<<< HEAD
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> master
