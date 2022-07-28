# Creation time: 2022/6/27 16:16
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
import os
import time
from multiprocessing import Process
import schedule
import MachinePublic
import psutil


def my_job():
    print("I'm 正在重启进程...")
    with open("pid.txt", 'r') as f:
        pid = f.read()
    os.system('taskkill /f /t /im {pid}'.format(pid=pid))
    # os.kill(int(pid), -9)
    print("#" * 30)
    time.sleep(1)
    p1 = Process(target=MachinePublic.main, args=())
    p1.start()
    print("#" * 30)

def check_pid_alive():
    """
    如果想要kill 一个进程，可以向进程发送信9
    kill -9 pid
    如果发送的信号是0，系统并不会真的向进程发送信号，
    但还是会做错误检查，如果没有错误，说明进程存在，反之进程不存在
    :return:
    """
    print("检查进程是否存活")
    with open("pid.txt", "r") as f:
        pid = f.read()
    try:
        psutil.Process(int(pid))
        print("存活pid:", pid)
    except psutil.NoSuchProcess:
        my_job()
    except Exception as e:
        print("check_pid_alive函数报错", e)
        my_job()


if __name__ == '__main__':
    print("开始运行主进程", os.getpid())
    schedule.every(3).seconds.do(check_pid_alive)  # 每隔3秒检查进程是否存活
    schedule.every().day.at("04:30").do(my_job)  # 每天的04: 30
    while True:
        schedule.run_pending()  # run_pending：运行所有可以运行的任务
        time.sleep(1)
