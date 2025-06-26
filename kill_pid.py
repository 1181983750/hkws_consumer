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
import traceback
from multiprocessing import Process
import multiprocessing
import os
import threading
import time
import schedule
import MachinePublic
import psutil

import MachinePublic_old


# from wxPush import WeChatPush


class ScheduleJob:
    lock_r = threading.RLock()

    def __new__(cls, *args, **kwargs) -> object:
        if not hasattr(cls, "_instance"):  # 返回Boolean
            with cls.lock_r:
                instance = super(__class__, cls).__new__(cls)
                setattr(cls, "_instance", instance)  # 设置属性 cls._instance = object  同理
        return getattr(cls, "_instance")

    def __init__(self):
        self.machine_pid: int = 0
        self.machine_pid_old: int = 0
        # noinspection PyTypeChecker
        self.machine_process: psutil.Process = None
        self.machine_process_old: psutil.Process = None

    def is_zombie_process(self):
        # 判断是否是僵尸进程
        try:

            return  (
    self.machine_process.status() == psutil.STATUS_ZOMBIE
    and self.machine_process_old.status() == psutil.STATUS_ZOMBIE
)
        except psutil.NoSuchProcess:
            return False

    def kill_zombie_process(self):
        """
        杀死僵尸进程
        """
        if not self.is_zombie_process():
            return False
        try:
            self.machine_process.terminate()  # 或者使用 process.kill() 来强制终止进程
            self.machine_process_old.terminate()  # 或者使用 process.kill() 来强制终止进程
            return True
        except psutil.NoSuchProcess:
            return False

    def start_machine_process(self):
        """
        启动消费机工作进程
        """
        print("#" * 30)
        p1 = multiprocessing.Process(target=MachinePublic.main, args=())
        p2 = multiprocessing.Process(target=MachinePublic_old.main, args=())
        p1.start()
        p2.start()
        # 分别写入两个 PID 在各自脚本主方法里
        self.machine_pid = p1.pid
        self.machine_pid_old = p2.pid
        print("I'm 正在重启进程...", self.machine_process, 'pid:', self.machine_pid, 'pid_old:', self.machine_pid_old)


    def check_machine_alive(self):
        """
        如果想要kill 一个进程，可以向进程发送信9
        kill -9 pid
        如果发送的信号是0，系统并不会真的向进程发送信号，
        但还是会做错误检查，如果没有错误，说明进程存在，反之进程不存在
        :return:
        """
        with open("pid.txt", "r") as f:
            self.machine_pid = int(f.read())

        with open("pid_old.txt", "r") as z:
            self.machine_pid_old = int(z.read())
        try:

            self.machine_process = psutil.Process(self.machine_pid)
            self.machine_process_old = psutil.Process(self.machine_pid_old)
            if self.kill_zombie_process():
                # WeChatPush(server='已成僵尸进程, 准备重启').run()
                # 是僵尸进程就杀死当前僵尸进程，然后重新启动
                self.start_machine_process()

        except psutil.NoSuchProcess:
            # WeChatPush(server='进程意外退出').run()
            self.start_machine_process()
        except Exception as e:
            traceback.print_exc()
            print("check_pid_alive函数报错", e)
            self.start_machine_process()
        else:
            print("存活pid:", self.machine_pid, psutil.Process(self.machine_pid))
            print("存活pid:", self.machine_pid_old, psutil.Process(self.machine_pid_old))


def main():
    print("开始运行父进程", os.getpid())
    SJ = ScheduleJob()
    schedule.every(3).seconds.do(SJ.check_machine_alive)  # 每隔3秒检查进程是否存活
    # 每天的特定时间执行任务
    # schedule.every(1).day.at("08:00").do(WeChatPush(server='每日自检').check)
    while True:
        schedule.run_pending()  # run_pending：运行所有可以运行的任务
        time.sleep(1)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
