# 获取网络时间
import datetime
import logging
import threading
import time
import os
from copy import deepcopy

from future.backports.http.client import HTTPConnection #高并发用


def getBeijinTime():
    """获取北京时间www.beijing-time.org"""
    try:
        now = datetime.datetime.now()
        # conn = HTTPConnection("www.daojishiqi.com")
        # conn.request("GET", "/sj.asp", headers={
        #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"})
        # response = conn.getresponse()
        # # print(response.status, response.reason)
        # if response.status == 200:
        #     # 解析响应的消息
        #     result_copy = deepcopy(response.read().decode())
        #     t_ms1 = result_copy[10:13]
        #     result = float(result_copy[:10] + '.' + t_ms1) #获取到时间戳
        #     time_tuple = time.localtime(result) #时间戳转换为元组
        #     beijintime_str = time.strftime('%Y-%m-%d %H:%M:%S', time_tuple)#将元组（struct_time）转换为格式化时间字符串
        #     beijintime_str = f"{beijintime_str}.{t_ms1}"
        #     beijintime_dict = {'year':time_tuple.tm_year,'month':time_tuple.tm_mon, 'day':time_tuple.tm_mday, 'hours':time_tuple.tm_hour, 'minute':time_tuple.tm_min, 'second':time_tuple.tm_sec, 'wday':time_tuple.tm_wday+1}
        #     print('获取网络日期',beijintime_str)
        #     return beijintime_dict, beijintime_str
        beijintime_dict= {'year':now.year,'month':now.month, 'day':now.day, 'hours':now.hour, 'minute':now.minute, 'second':now.second, 'wday':now.weekday()+1}
        beijintime_str=f"{now.strftime('%Y-%m-%d ')}{now.time()}"
        return beijintime_dict, beijintime_str
    except:
        logging.exception("获取网络北京时间异常")
        # syncLocalTime()
        return None



def syncLocalTime():
    """同步本地时间"""
    t_ms1 = str(time.time())[str(time.time()).index('.'):]
    t_ms2 = str(time.time()).split('.')[1]
    print(time.localtime()[:6].__str__())
    print(f"电脑本地时间为: %d-%d-%d %d:%d:%d{t_ms1} 星期{time.localtime().tm_wday == 7 if 0 else time.localtime().tm_wday+1}" % time.localtime()[:6])
    beijinTime = getBeijinTime()
    if beijinTime is None:
        logging.error("获取北京时间失败，3秒后重新获取")
        timer = threading.Timer(3.0, syncLocalTime)
        timer.start()
        #失败，我就起一个线程，并且不关闭
    else:
        # logging.warning(f"获取到的北京时间为:{beijinTime[1]}" )
        year, month, day, hours, minute, second, wday = beijinTime[0].values()
        os.system("date %d-%d-%d" % (int(year), int(month),int(day)))  # 设置日期
        os.system("time %d:%d:%d" % (int(hours), int(minute),int(second)))  # 设置时间
        logging.warning("同步后电脑,现在本地时间: %d-%d-%d %d:%d:%d \n" % time.localtime()[:6])


