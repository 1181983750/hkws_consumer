from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

from Celery_Tasks.tasks import tasks


@require_http_methods(['GET'])
def test_view(request):
    # 需要将send 方法 使用消息队列就需要链式调用delay
    result = tasks.send.delay(2, 5)
    return HttpResponse(result)

