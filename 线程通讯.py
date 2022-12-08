import threading
import time
import inspect
import ctypes

lock = threading.Lock()
lock_r = threading.RLock()


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)



class thread(threading.Thread):
    def __init__(self, threadname):
        threading.Thread.__init__(self, name='线程' + str(threadname))
        self.threadname = threadname
        self.kill = False

    def run(self):  #run 为start主方法 关键字
        print('%s:Now timestamp is %s'%(self.name, time.time()))
        lock.acquire()
        for i in range(100):
            if self.kill:
                break
        lock.release()


    def stop(self):
        self.kill = True

# threads = []
# for a in range(5):  # 线程个数
#     a:str
#     threads.append(thread(a))
# for t in threads:
#     a = getattr(t,'threadname',None)
#     t.setName('172.18.17.224')
#     # t.start()
#
#     # print(a)
#     # print('线程id',t.native_id)
#     if t.is_alive():
#         print(t.ident == t.native_id)
#         print(t.ident,'被杀死了')
#         # stop_thread(t)
#         t.stop()
#     print(t.is_alive()) #返回此线程是否活着
# for t in threads:
#     t.join()  # 阻塞线程


#定义线程要调用的方法，*add可接收多个以非关键字方式传入的参数
def action(*add):
    for arc in add:
        #调用 getName() 方法获取当前执行该程序的线程名
        print(threading.current_thread().getName() +" "+ arc)
#定义为线程方法传入的参数
my_tuple = ("http://c.biancheng.net/python/",\
            "http://c.biancheng.net/shell/",\
            "http://c.biancheng.net/java/")
#创建线程
threads = threading.Thread(target=action, args=my_tuple)

threads.start()
