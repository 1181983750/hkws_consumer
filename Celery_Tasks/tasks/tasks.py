# Creation time: 2022/6/16 10:28
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

from time import sleep

# import MachinePublic
from Celery_Tasks.celery_config import app
import time

"""
可用任务需要使用 装饰器@app.task
"""


@app.task
def send(a, b):
    time_now = time.strftime("%H:%M:%S", time.localtime())  # 刷新
    while True:
        if time_now == "00:00:00":  # 此处设置每天定时的时间
            print("开始调用send方法")
            # exit(MachinePublic.main())
            print("调用结束")

