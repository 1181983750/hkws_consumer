# Creation time: 2022/6/16 10:20
# The author: Tiger_YC
"""
                   _ooOoo_
                  o8888888o
                  88" . "88
                  (| -_- |)
                  O\  =  /O
               ____/`---'\____
             .'  \\|     |//  `.
            /  \\|||  :  |||//  \
           /  _||||| -:- |||||-  \
           |   | \\\  -  /// |   |
           | \_|  ''\---/''  |   |
           \  .-\__  `-`  ___/-. /
         ___`. .'  /--.--\  `. . __
      ."" '<  `.___\_<|>_/___.'  >'"".
     | | :  `- \`.;`\ _ /`;.`/ - ` : | |
     \  \ `-.   \_ __\ /__ _/   .-` /  /
======`-.____`-.___\_____/___.-`____.-'======
                   `=---='
             佛祖保佑       永无BUG
"""
# 使用方法 celery -A Celery_Tasks.celery_config worker  --pool=solo --loglevel=INFO -c 8 (这条命令必须在 E:\httpxs> 所在的目录执行)

#读取Django的配置,

from celery import Celery
import os

#worker代理人：指定 rabbitmq作为消息队列
broker_url = "redis://127.0.0.1:6379/10"
os.environ["DJANGO_SETTINGS_MODULE"] = "httpxs.settings"
# 创建celery对象,并指定代理配置
app = Celery("tasks", broker=broker_url, backend="redis://127.0.0.1:6379/11")
# 加载可用的任务目录
app.autodiscover_tasks([
    'Celery_Tasks.tasks',
])



