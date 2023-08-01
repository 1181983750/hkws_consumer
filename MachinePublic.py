import logging
import os
<<<<<<< HEAD

from django.db import transaction

from public.utils.BaseOrm import DictToModel

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'httpxs.settings')
import django

django.setup()
from MachineLogging import logger

import datetime
from decimal import Decimal
from httpAsyncClient.hkws_xf_xfmx.hkws_xf_xfmx_services import HKWSXFMXServices
from httpAsyncClient.hkws_xf_ygye.HKWSXFYGYEORM import HKWSXFYGYEORM
from public.utils.onlineTime import getBeijinTime
from httpAsyncClient.models import hkws_xf_sbmx, hkws_yg_sbqy, hkws_xf_xfmx, hkws_xf_ygye
=======
import platform
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'httpxs.settings')
import django
from django.db import transaction
from public.utils.BaseOrm import DictToModel

django.setup()

logger = logging.getLogger('error')

import datetime

from decimal import Decimal

from httpAsyncClient.hkws_xf_xfmx.hkws_xf_xfmx_services import HKWSXFMXServices

from httpAsyncClient.hkws_xf_ygye.HKWSXFYGYEORM import HKWSXFYGYEORM
from public.utils.onlineTime import getBeijinTime
from httpAsyncClient.rs_ygxx.RSYGXXORM import RSYGXXORM
from httpAsyncClient.models import hkws_xf_sbmx, hkws_yg_sbqy, hkws_xf_xfmx, hkws_xf_ygye, rs_ygxx
>>>>>>> master
from public.utils import EmployeesToBanlanceConstruction as EC
from httpAsyncClient.Config import Config
from httpAsyncClient.hkws_yg_sbqy.HKWSYGSBQYORM import HKWSYGSBQYORM
import json
import threading
import time
from typing import Any
import httpx
import requests
from requests.auth import HTTPDigestAuth

XML = 1
JSON = 2
IMAGE = 3
end = b"\r\n"
boundary = b"--MIME_boundary"
ContentT = b"Content-Type: "
ContentL = b"Content-Length: "


class ParseData:

    def __init__(self, ip: str, username: str, password: str):
        self.ip = ip
        self.content_type = None
        self.content_length = None
        self.content = b''
        self.auth = httpx.DigestAuth(username, password)
        self.http_x = httpx
        self.HKWSYGSBQYORM = HKWSYGSBQYORM(hkws_yg_sbqy)
        self.HKWSXFMXServices = HKWSXFMXServices(hkws_xf_xfmx)
        self.HKWSXFYGYEORM = HKWSXFYGYEORM(hkws_xf_ygye)
<<<<<<< HEAD
=======
        self.RSYGXXORM = RSYGXXORM(rs_ygxx)
>>>>>>> master
        self.DictToModel = DictToModel

    def fileinput(self, data: bytes, img_dict: dict):
        with open(
                f"{Config.xf_path}{img_dict['TransactionRecordEvent'].get('employeeNoString')}{img_dict['TransactionRecordEvent'].get('name')}-{img_dict['TransactionRecordEvent'].get('serialNo')}.jpg",
                "wb", ) as file:
            file.write(data)
            file.close()

    def handle_transaction_event(self, data: dict):
        response_refund = None  # 是否退款事件处理了
        response_transaction = None  # 是否消费事件处理了
        dateTime = data.get('dateTime')
        activePostCount = data.get('activePostCount')
        detail = data.get('TransactionRecordEvent')
        type = detail.get('type')
        serialNo = detail.get('serialNo')
        employeeNoString = detail.get('employeeNoString')
        modeType = detail.get('modeType')
        verifyMode = detail.get('verifyMode')
        # mode = detail.get('mode')
        refundPayment = detail.get('refundPayment')
        name = detail.get('name')
<<<<<<< HEAD
        if type == "refund":
            # 消费退款
            refundPayment = detail.get('refundPayment')
            result_list = self.HKWSYGSBQYORM.get_xfmx_by_serialNo(int(serialNo))
=======
        result_list = self.HKWSYGSBQYORM.get_xfmx_by_serialNo(int(serialNo), str(self.ip))
        if type == "refund":
            # 消费退款
            refundPayment = detail.get('refundPayment')
>>>>>>> master
            if not result_list:
                response_refund = self.parse_transactionRecord(amount=Decimal(refundPayment) / Decimal(100),
                                                               Etype=EC.REFUND,
                                                               ygid=int(employeeNoString),
                                                               deviceInfo=
                                                               self.HKWSYGSBQYORM.QueryDeviceInformationByIp(self.ip)[
                                                                   0],
                                                               ygmc=name, xfrq=dateTime, serialNo=serialNo,
                                                               verifyMode=verifyMode,
                                                               username=name)
            else:
                # 已经处理过的单号 返回成功信息
                response_refund = True
<<<<<<< HEAD
        elif type == "transaction":
            actualPayment = detail.get('actualPayment')
            result_list = self.HKWSYGSBQYORM.get_xfmx_by_serialNo(int(serialNo))
=======
        if type == "transaction":
            actualPayment = detail.get('actualPayment')
>>>>>>> master
            if not result_list:
                # 没有该serialNo记录 开始处理 消费
                response_transaction = self.parse_transactionRecord(amount=Decimal(actualPayment) / Decimal(100),
                                                                    Etype=EC.DEDUCTION,
                                                                    ygid=int(employeeNoString),
                                                                    deviceInfo=
                                                                    self.HKWSYGSBQYORM.QueryDeviceInformationByIp(
                                                                        self.ip)[0],
                                                                    ygmc=name, xfrq=dateTime, serialNo=serialNo,
                                                                    verifyMode=verifyMode,
                                                                    username=name)
            else:
                # 有serialNo此单了 返回成功信息
                response_transaction = True
        if response_transaction is not None:
            json_data_t = {'TransactionRecordEventConfirm': {}}
            json_data_t['TransactionRecordEventConfirm']['serialNo'] = int(serialNo)
            json_data_t['TransactionRecordEventConfirm']['result'] = 'success' if response_transaction else 'failed'
            response_t = self.http_x.put(f"http://{self.ip}/ISAPI/Consume/transactionRecordEventConfirm",
                                         auth=self.auth,
                                         params={'format': 'json'}, json=json_data_t)
<<<<<<< HEAD
            logging.warning(f"交易确认回执{response_t.text}")
        elif response_refund is not None:
            response_c = {'TransactionRecordEventConfirm': {}}
            response_c['TransactionRecordEventConfirm']['serialNo'] = int(serialNo)
            response_c['TransactionRecordEventConfirm']['result'] = 'success' if response_refund else 'failed'
            response_c = self.http_x.put(f"http://{self.ip}/ISAPI/Consume/transactionRecordEventConfirm",
                                         auth=self.auth,
                                         params={'format': 'json'}, json=response_c)
            logging.warning(f"退款确认回执{response_c.text}")

    def handle_consumption_event(self, data: dict):
        """在线消费事件、 这一步只做余额是否够扣款判断 存储在交易确认事件中"""
=======
            # print(f"交易确认回执{response_t.text}流水号:{serialNo}")
            logger.warning(f"交易确认回执{response_t.text}流水号:{serialNo}")
        if response_refund is not None:
            json_data_c = {'TransactionRecordEventConfirm': {}}
            json_data_c['TransactionRecordEventConfirm']['serialNo'] = int(serialNo)
            json_data_c['TransactionRecordEventConfirm']['result'] = 'success' if response_refund else 'failed'
            response_c = self.http_x.put(f"http://{self.ip}/ISAPI/Consume/transactionRecordEventConfirm",
                                         auth=self.auth,
                                         params={'format': 'json'}, json=json_data_c)
            logger.warning(f"退款确认回执{response_c.text}流水号:{serialNo}")

    def handle_consumption_event(self, data: dict):
>>>>>>> master
        # date_time = data.get('dateTime')
        # activePostCount = data.get('activePostCount')
        detail = data.get('ConsumptionEvent')
        # minor = detail.get('minor')
        # cancel = detail['cancel']
        serialNo = detail.get('serialNo')
        employeeNoString = detail.get('employeeNoString')
        name = detail.get('name')
        type = detail.get('type')
        # mode = detail.get('mode')
        totalPayment = detail.get('totalPayment')
<<<<<<< HEAD
=======
        result = 'success'
>>>>>>> master
        # 扣款前 先看看余额是否足够
        ye: Decimal = self.HKWSXFYGYEORM.get_ye_by_ygid(employeeNoString).ye
        handel_ye: Decimal = (ye if ye else Decimal(0)) * Decimal(100)
        if handel_ye >= Decimal(totalPayment):
            result = 'success'
        else:
            result = "balanceNotEnough"
<<<<<<< HEAD
            # 小数点处理
=======
        # 小数点处理
>>>>>>> master
        balanceBeforeDeduct = str(handel_ye).split(".")[0]
        # 处理完提交数据:
        json_data = {'ConsumptionEventConfirm': {}}
        json_data['ConsumptionEventConfirm'].update(serialNo=serialNo,
                                                    result=result,
                                                    mode="amount",
                                                    actualPayment=totalPayment,
                                                    balanceBeforeDeduct=balanceBeforeDeduct,
                                                    name=name,
                                                    employeeNoString=employeeNoString)

        response = self.http_x.put(f"http://{self.ip}/ISAPI/Consume/consumptionEventConfirm", auth=self.auth,
                                   params={'format': 'json'}, json=json_data)
<<<<<<< HEAD
        logging.warning(f'消费事件回执：{response.text}', )
=======
        # print(f'{serialNo}消费事件回执：{response.text}', )
        logger.warning(f'{serialNo}消费事件回执：{response.text}', )
>>>>>>> master

    def parse_transactionRecord(self, amount: Decimal, Etype: EC, ygid: int, deviceInfo: dict, ygmc: str,
                                xfrq: datetime.datetime, serialNo: int, verifyMode: str, username: str) -> bool:
        # 自动计算余额 如果没有该ygid 则新建为0
        if Etype == EC.REFUND:
            result = self.HKWSXFMXServices.auto_calc_xfmx_ye(ygid=ygid, amount=amount, xflx=4)
            data_dict = {"sbip": deviceInfo.get('sbip'), "ygid": ygid, "ygmc": ygmc, "xfje": amount, "ye": result,
                         "sbxh": 2, "xfrq": xfrq, "serialNo": serialNo, "verifyMode": verifyMode, "username": username}
            with transaction.atomic():  # 禁止自动提交,保证该函数中的所有数据库操作在同一个事物中，第一个数据库操作1即使成功保存到数据库中，只要第2个数据操作失败，那么所有该段代码所有设计的都会更改回滚到原来
                sid = transaction.savepoint()  # 开启事务设置事务保存点 可以设置多个保存点
                try:
                    data_dict.update(**Etype, sjrq=getBeijinTime()[1])
                    dict_to_model = self.DictToModel(dict_data=data_dict,
                                                     model_class=hkws_xf_xfmx).format_dict_data_to_model()
                    self.HKWSXFMXServices.add(dict_to_model)  # 添加退款明细
                    self.HKWSXFYGYEORM.update_ygye(ygid, result)  # 更新余额
                except:
                    transaction.savepoint_rollback(sid)  # 失败回滚事务(如果数据库操作发生异常，回滚到设置的事务保存点)
                    return False
                else:
                    transaction.savepoint_commit(sid)  # 如果没有异常，成功提交事物
                    return True
        elif Etype == EC.DEDUCTION:
            result = self.HKWSXFMXServices.auto_calc_xfmx_ye(ygid=ygid, amount=amount, xflx=2)
            data_dict = {"sbip": deviceInfo.get('sbip'), "ygid": ygid, "ygmc": ygmc, "xfje": -amount, "ye": result,
                         "sbxh": 2, "xfrq": xfrq, "serialNo": serialNo, "verifyMode": verifyMode}
            with transaction.atomic():  # 禁止自动提交,保证该函数中的所有数据库操作在同一个事物中，第一个数据库操作1即使成功保存到数据库中，只要第2个数据操作失败，那么所有该段代码所有设计的都会更改回滚到原来
                sid = transaction.savepoint()  # 开启事务设置事务保存点 可以设置多个保存点
                try:
                    data_dict.update(**Etype, sjrq=getBeijinTime()[1])
                    data_dict.update(**Etype, sjrq=getBeijinTime()[1])
                    dict_to_model = self.DictToModel(dict_data=data_dict,
                                                     model_class=hkws_xf_xfmx).format_dict_data_to_model()
                    self.HKWSXFMXServices.add(dict_to_model)  # 添加消费明细
                    self.HKWSXFYGYEORM.update_ygye(ygid, result)  # 更新余额
                except:
                    transaction.savepoint_rollback(sid)  # 失败回滚事务(如果数据库操作发生异常，回滚到设置的事务保存点)
                    return False
                else:
                    transaction.savepoint_commit(sid)  # 如果没有异常，成功提交事物
                    return True

<<<<<<< HEAD
=======
    def handle_query_ye_event(self, data: dict):
        employeeNo = data.get('ConsumptionQuery').get('employeeNo')
        queryUUID = data.get('ConsumptionQuery').get('queryUUID')
        ye: Decimal = self.HKWSXFYGYEORM.get_ye_by_ygid(employeeNo).ye
        try:
            name = self.RSYGXXORM.get_ygxx_by_ygid(employeeNo).first().ygmc
        except Exception:
            logger.warning('查无此人')
            name = '查无此人'
        query_ye: Decimal = (ye if ye else Decimal(0)) * Decimal(100)
        # 小数点处理
        balanceBeforeDeduct = str(query_ye).split(".")[0]
        # 处理完提交数据:
        json_data = {'queryUUID': queryUUID, 'queryResult': 'success', 'name': name, 'employeeNo': employeeNo,
                     'balance': balanceBeforeDeduct, 'remainingTimes': 1}
        response = self.http_x.put(f"http://{self.ip}/ISAPI/Consume/localQueryResult", auth=self.auth,
                                   params={'format': 'json'}, json=json_data)
        logger.warning(response.read())

>>>>>>> master
    def parse_data(self, da: bytes):
        if self.content_type is None:
            self.__init_data(da)
        else:
            self.append_data(da)

    def __init_data(self, da: bytes):
        if ContentT in da:
            start_index = da.find(ContentT)
            start_content_length = da.find(ContentL)
            end_content_length = da.find(end, start_content_length)

            if b'Content-Type: application/json' in da[start_index:start_content_length]:
                self.content_type = 'JSON'
            elif b'Content-Type: image/jpeg' in da[start_index:start_content_length]:
                self.content_type = 'IMAGE'
            else:
<<<<<<< HEAD
                logging.warning('content_type未处理的格式')
=======
                logger.warning('content_type未处理的格式')
>>>>>>> master
            content_length_temp = da[start_content_length:end_content_length]

            self.content_length = int(
                content_length_temp.split(ContentL).pop().decode(encoding='utf-8', errors='strict').strip())

            if self.content_type == 'JSON':
                offset = 2
                left_temp = da[end_content_length + len(end) + offset:len(da)]
<<<<<<< HEAD
                # 开始读取内容到self.content
                self.append_data(left_temp)
            elif self.content_type == 'IMAGE':
                offset = da.find(b'\r\n\r\n', start_index + len(end)) + len(b'\r\n\r\n')
                # left_temp = da[offset:len(da)][:-18]
=======

                self.append_data(left_temp)
            elif self.content_type == 'IMAGE':
                offset = da.find(b'\r\n\r\n', start_index + len(end)) + len(b'\r\n\r\n')
                # left_temp = da[offset:len(da)][:-17]
>>>>>>> master
                left_temp = da[offset:len(da)]
                # 开始读取内容到self.content
                self.append_data(left_temp)

        else:
            self.content += da

    def append_data(self, da: bytes):
<<<<<<< HEAD
=======
        self.content = self.content.replace(b'--MIME_boundary\r\n', b'')
>>>>>>> master
        count = 0
        for i in da:
            if len(self.content) < self.content_length:
                self.content += bytes([i])
                count += 1
            else:
                break
        da = da[count:len(da)]
        # 拼接结束
<<<<<<< HEAD
        if len(self.content) >= self.content_length:
            # 处理content
            if self.content_type == 'IMAGE':
                self.fileinput(self.content, self.image_dict)
            elif self.content_type == 'JSON':
                de_json = json.loads(self.content.decode(encoding='utf-8'))
                if de_json['eventType'] == 'videoloss':
                    print('视频丢失 pass')
                    print(de_json)
                elif de_json['eventType'] == 'TransactionRecordEvent':
                    print('交易事件确认')
                    print(de_json)
                    self.image_dict = de_json
                    self.handle_transaction_event(de_json)
                elif de_json['eventType'] == 'AccessControllerEvent':
                    logger.warning(f"{de_json.get('ipAddress')}访问消费机")
                elif de_json['eventType'] == 'ConsumptionEvent':
                    print('消费事件确认')
                    print(de_json)
                    self.image_dict = de_json
                    self.handle_consumption_event(de_json)
                else:
                    logging.warning(f'其他json事件{de_json}')
            else:
                de_json = json.loads(self.content.decode(encoding='utf-8'))
                logging.warning(f'未处理的格式{de_json}')
            print('*' * 100)
=======

        if len(self.content) >= self.content_length:
            # 处理content
            if self.content_type == 'IMAGE':
                pass
            # self.fileinput(self.content, self.image_dict)
            elif self.content_type == 'JSON':
                logger.info(f'我是:{self.ip}')
                # print(self.content)
                # print(len(self.content))
                de_json = json.loads(self.content.decode(encoding='utf-8'))
                if de_json['eventType'] == 'videoloss':
                    pass
                elif de_json['eventType'] == 'TransactionRecordEvent':

                    self.image_dict = de_json
                    self.handle_transaction_event(de_json)
                elif de_json['eventType'] == 'AccessControllerEvent':
                    pass
                # print('访问控制器', de_json)
                elif de_json['eventType'] == 'ConsumptionEvent':

                    self.image_dict = de_json
                    self.handle_consumption_event(de_json)
                elif de_json['eventType'] == 'ConsumptionQuery':
                    print('余额查询')
                    self.handle_query_ye_event(de_json)
                else:
                    print(f'其他json事件{de_json}')
                    logger.warning(f'其他json事件{de_json}')
            else:
                de_json = json.loads(self.content.decode(encoding='utf-8'))
                logger.warning(f'未处理的格式{de_json}')
            #            print('*' * 100)
>>>>>>> master
            # 处理content结束

            # 处理剩下的内容
            self.content = b''
            self.content_type = None
<<<<<<< HEAD
            print('left_temp', da)
=======
            # print('left_temp', da)
>>>>>>> master
            if len(da) == 0 or da.find(ContentT) == -1:
                self.content_length = None
            else:
                self.parse_data(da)
<<<<<<< HEAD
            # 处理剩下的内容
=======
    # 处理剩下的内容
>>>>>>> master


class LongLink(threading.Thread):
    """开启长链接"""

    def __init__(self, ip, username, password, ids):
        super(LongLink, self).__init__(name='线程' + ip)
        self.ip = ip
        self.username = username
        self.password = password
        self.ids = ids
        self.parse_data = ParseData(ip=self.ip, username=self.username, password=self.password)
        self.http_x = httpx
<<<<<<< HEAD
        self.auth = httpx.DigestAuth(self.username, self.password)
=======
        self.auth = self.http_x.DigestAuth(self.username, self.password)
>>>>>>> master
        self.requests = requests
        self.requests_auth = HTTPDigestAuth(self.username, self.password)
        self.kill = False
        self.mt = MachineThread().get_instance()
        self.HKWSYGSBQYORM = HKWSYGSBQYORM(hkws_yg_sbqy)
<<<<<<< HEAD
        self.timeout = 3
=======
        self.timeout = 2
        self.token = ''
>>>>>>> master

    def run(self):
        self.start_long_link()

    def start_long_link(self):
        self.mt.threads[self.ids].update(LongLink=self)  # 更新成在线状态
<<<<<<< HEAD
        with self.http_x.stream("GET", f"http://{self.ip}/ISAPI/Event/notification/alertStream", auth=self.auth,
                                timeout=None) as r:
            for data in r.iter_bytes():
                print("我是:", self.name, threading.get_ident())
                self.parse_data.parse_data(data)
                if self.parse_data.content_type is None:
                    if self.kill:
                        print('停止成功')
                        break
            # 清空所有数据，退出线程并且清空在线设备容器
            del self.mt.threads[self.ids]['LongLink']
            self.reset_parse_data()
            # 被动断网 保持重连
            # logger.warning('被动断网 即将重连')
            time.sleep(1)
            if not self.kill:
                # logger.warning('重连中')
                self.run()
=======
        try:
            with self.http_x.stream("GET", f"http://{self.ip}/ISAPI/Event/notification/alertStream",
                                    auth=self.http_x.DigestAuth(self.username, self.password),
                                    timeout=50) as r:
                for data in r.iter_bytes():
                    self.parse_data.parse_data(data)
                    if self.parse_data.content_type is None:
                        if self.kill:
                            logger.warning('停止成功')
                            break
                self.reset_parse_data()
                print(self.ip, '# 被动断网 保持重连', self.kill, )
                time.sleep(0.5)
                if not self.kill:
                    self.run()
                else:
                    del self.mt.threads[self.ids]['LongLink']
                    return '停止成功'
        except RecursionError:
            logger.info('重连次数超过递归最大限制，退出重启！！！！！！！！！！！！')
            self.exit()
        except httpx.ReadTimeout:
            print('长时间未读取到数据')
            # 清空所有数据，退出线程并且清空在线设备容器
            self.reset_parse_data()
            # 被动断网 保持重连
            time.sleep(1)
            if not self.kill:
                logger.warning(f'{self.ip}长时间未读取到数据，被动断网 即将重连')
                self.run()
            else:
                del self.mt.threads[self.ids]['LongLink']
                return '停止成功'
        except Exception as e:
            # traceback.print_exc()
            logger.warning(e)
            print('其他异常', str(e), self.ids, self.kill)
            time.sleep(1)
            self.reset_parse_data()
            # 被动断网 保持重连
            if not self.kill:
                logger.warning(f'{self.ip}异常 即将重连:{str(e), self.kill}')
                self.run()

            else:
                del self.mt.threads[self.ids]['LongLink']
                return '停止成功'
>>>>>>> master

    def reset_parse_data(self):
        """重置消息处理类属性"""
        self.parse_data.content = b''
        self.parse_data.content_type = None
        self.parse_data.content_length = None

<<<<<<< HEAD
=======
    @staticmethod
    def exit():
        pid = os.getpid()
        sys_name = platform.system()
        if sys_name == 'Windows':
            os.system('taskkill /f /t /im {pid}'.format(pid=pid))
        elif sys_name == 'Linux':
            os.system('kill -9 {pid}'.format(pid=pid))

>>>>>>> master
    def stop(self):
        # logger.warning('开始杀死该线程')
        self.kill = True

    def addStaff(self):
        """获得当前设备要下发的人脸下发到设备"""
        sbid: int = self.ids
        result: list = self.HKWSYGSBQYORM.sel_add_staff_bysbid(sbid)
<<<<<<< HEAD
=======

        if not result:
            return
>>>>>>> master
        try:
            login_res = self.http_x.post(f"{Config.pic_url}/login/", json={
                "name": "zcc",
                "password": "12345"
            }, timeout=self.timeout, verify=False)
<<<<<<< HEAD
        except httpx.ReadTimeout:
            logger.warning(f"接口:{Config.pic_url}/login/获取token超时")
        else:
            self.token = login_res.json().get("token")
        for item in result:
            ygid = item.get("ygid")
            ygmc = item.get("ygmc")
            picpath = f'{Config.rl_path}{ygid}.jpg'
            try:
                img_res = self.http_x.get(f"{Config.pic_url}/return_pic_bytes/%s" % ygid,  headers={'Authorization': self.token}, timeout=self.timeout, verify=False)
            except httpx.ReadTimeout:
                logger.warning(f"接口:{Config.pic_url}/return_pic_bytes/获取%s超时" % ygid)
            except Exception as e:
                logger.warning(f"接口:{Config.pic_url}/return_pic_bytes/获取%s时：{str(e)}" % ygid)
            else:
                if img_res.status_code > 210:
                    logger.warning(f"接口:{Config.pic_url}/return_pic_bytes/没有%s的图片" % ygid)
                    continue
                with open(picpath, "wb") as f:
                    f.write(img_res.text.encode(encoding='ISO-8859-1'))
            pic_list = os.listdir(Config.rl_path)
            pic = None
            if f"{ygid}.jpg" in pic_list:
                pic = self.mt.getPicByPath(picpath)
            if pic:
                if self.handel_set_face_event(ygid, ygmc, pic):  # 无论成功都增加明细记录
                    logger.warning(f"设备id：{sbid}下发成功的员工{ygid, ygmc}")
                    self.HKWSYGSBQYORM.add_staff_record(ygid, sbid, 1)
                else:
                    logger.error(f"设备id：{sbid}下发失败的员工{ygid, ygmc}")
                    # 下发失败的员工设备 把 isSuccess 改为0
                    self.HKWSYGSBQYORM.add_staff_record(ygid, sbid, 0)
            else:
                logger.error(f'{ygid, ygmc}有需要下发的人脸，但是获取不到图片')
=======
            if b'token' not in login_res.read():
                logger.warning('没有获取到token')
        except httpx.ReadTimeout:
            logger.warning(f"接口:{Config.pic_url}/login/获取token超时")
        except Exception as e:
            #            print('获取token接口不对', e)
            logger.warning('获取token接口不对')
        else:
            self.token = login_res.json().get("token", self.token)
        for item in result:
            print("开始下发人脸")
            ygid = item.get("ygid")
            ygmc = item.get("ygmc")
            picpath = f'{Config.rl_path}{ygid}.jpg'
            if f"{ygid}.jpg" not in os.listdir(Config.rl_path):
                try:
                    img_res = self.http_x.get(f"{Config.pic_url}/return_pic_bytes/%s" % ygid,
                                              headers={'Authorization': self.token}, timeout=self.timeout, verify=False)
                except httpx.ReadTimeout:
                    logger.warning(f"接口:{Config.pic_url}/return_pic_bytes/获取%s超时" % ygid)
                except Exception as e:
                    logger.warning(f"接口:{Config.pic_url}/return_pic_bytes/获取%s时：{str(e)}" % ygid)
                else:
                    if img_res.status_code != 200:
                        logger.warning(f"接口:{Config.pic_url}/return_pic_bytes/没有%s的图片" % ygid)
                        continue
                    if img_res.read() != b'' and b'data' not in img_res.read() and b'!DOCTYPE' not in img_res.read():
                        with open(picpath, "wb") as f:
                            f.write(img_res.text.encode(encoding='ISO-8859-1'))
                            f.close()
            if f"{ygid}.jpg" in os.listdir(Config.rl_path):
                pic = self.mt.getPicByPath(picpath)
                if pic:
                    if self.handel_set_face_event(ygid, ygmc, pic):  # 无论成功都增加明细记录
                        logger.info(f"设备id：{sbid}下发成功的员工{ygid, ygmc}")
                        self.HKWSYGSBQYORM.add_staff_record(ygid, sbid, 1)
                    else:
                        logger.error(f"设备id：{sbid}下发失败的员工{ygid, ygmc}")
                        # 下发失败的员工设备 把 isSuccess 改为0
                        self.HKWSYGSBQYORM.add_staff_record(ygid, sbid, 0)
                    os.remove(f"{Config.rl_path}/{ygid}.jpg")
                else:
                    logger.error(f'{ygid, ygmc}有需要下发的人脸，但是获取不到图片设备id：{sbid}')
            else:
                print(f"{ygid - ygmc}.jpg not in Config.rl_path the {Config.rl_path}")
>>>>>>> master

    def delStaff(self):
        """通过ygid删除人脸"""
        sbid: int = self.ids
        result: list = self.HKWSYGSBQYORM.sel_del_staff_bysbid(sbid)
        for item in result:
            ygid = item.get("ygid")
            if self.handel_del_face_event(ygid):  # 无论成功都增加明细记录
<<<<<<< HEAD
                logger.warning(f"设备id：{sbid}删除成功的员工{ygid}")
=======
                logger.info(f"设备id：{sbid}删除成功的员工{ygid}")
>>>>>>> master
                self.HKWSYGSBQYORM.del_staff_record(ygid, sbid)
            else:
                logger.error(f"设备id：{sbid}删除失败的员工{ygid}")

    def handel_set_face_event(self, ygid: int, ygmc: str, Pic: bytes) -> bool:
        """
        此台消费机下发人脸
        :param ygid:
<<<<<<< HEAD
        :param sbid:
        :param isSuccess:
        :param kwargs:
=======
        :param ygmc:
        :param Pic:
>>>>>>> master
        :return:
        """
        boundary = "-------------tyctyctyctyctyctyctyc"
        byte_pic = Pic.decode('ISO-8859-1')
        headers = {
            "Content-Type": "multipart/form-data; boundary=" + boundary,
            "Accept": "text/html, application/xhtml+xml",
            "Accept-Language": "zh-CN",
            "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "Keep-Alive",
            "Cache-Control": "no-"
        }
        send_json = json.dumps({
            "UserInfoAndRight": {
                "employeeNo": f"{ygid}",
                "deleteUser": False,
                "name": f"{ygmc}",
                "userType": "normal",
                "Valid": {
                    "enable": False,
                    "beginTime": "1970-01-01T00:00:00+00:00",
                    "endTime": "2037-12-31T23:59:59+00:00",
                },
                "password": "123456",
                "RightPlan": [
                    {
                        "doorNo": 1
                    }
                ],
                "localUIRight": False,
                "userVerifyMode": "face",
                "FaceInfo": {
                    "List": [
                        {
                            "FDID": "1",
                            "faceID": 1,
                            "faceName": "FacePicture"
                        }
                    ],
                }
            },
        })
        payload = "--" + boundary + "\r\n" \
                  + "Content-Disposition: form-data; name=\"uploadStorageCloud\";\r\n" \
                  + "Content-Type: application/json\r\n" \
                  + "Content-Length: " + str(len(send_json)) + "\r\n\r\n" \
                  + send_json + "\r\n" \
                  + "--" + boundary + "\r\n" \
                  + "Content-Disposition: form-data; name=\"FacePicture\";\r\n" \
                  + "Content-Type: image/jpeg\r\n" \
                  + "Content-Length: " + str(len(byte_pic)) + "\r\n\r\n" \
                  + byte_pic + "\r\n" \
                  + "--" + boundary + "--\r\n"
        response = self.requests.post(f"http://{self.ip}/ISAPI/AccessControl/userInfoAndRight/setup?format=json",
<<<<<<< HEAD
                                      auth=self.requests_auth,
                                      data=payload,
                                      verify=False,
                                      headers=headers,
                                      timeout=self.timeout)
        logger.warning(response.text)
=======
                                      auth=HTTPDigestAuth(self.username, self.password),
                                      verify=False,
                                      data=payload,
                                      headers=headers,
                                      timeout=self.timeout)

        logger.info(response.text)
        #        print(response.text)
>>>>>>> master
        if response.text.find("user info proc success") != -1 and response.text.find("face proc success") != -1:
            return True
        return False

    def handel_del_face_event(self, ygid: int, ) -> bool:
        """
        此台消费机删除人脸
        :param ygid:
<<<<<<< HEAD
        :param ygmc:
=======
>>>>>>> master
        :return:
        """
        byte_pic = "null"
        boundary = "-------------tyctyctyctyctyctyctyc"
        headers = {
            "Content-Type": "multipart/form-data; boundary=" + boundary,
            "Accept": "text/html, application/xhtml+xml",
            "Accept-Language": "zh-CN",
            "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "Keep-Alive",
            "Cache-Control": "no-"
        }
        send_json = json.dumps({
            "UserInfoAndRight": {
                "employeeNo": f"{ygid}",
                "deleteUser": True,
                "name": "",
                "userType": "normal",
                "Valid": {
                    "enable": False,
                    "beginTime": "1970-01-01T00:00:00+00:00",
                    "endTime": "2037-12-31T23:59:59+00:00",
                },
                "password": "123456",
                "RightPlan": [
                    {
                        "doorNo": 1
                    }
                ],
                "localUIRight": False,
                "userVerifyMode": "face",
                "FaceInfo": {
                    "List": [
                        {
                            "FDID": "1",
                            "faceID": 1,
                            "faceName": "FacePicture"
                        }
                    ],
                }
            },
        })
        payload = "--" + boundary + "\r\n" \
                  + "Content-Disposition: form-data; name=\"uploadStorageCloud\";\r\n" \
                  + "Content-Type: application/json\r\n" \
                  + "Content-Length: " + str(len(send_json)) + "\r\n\r\n" \
                  + send_json + "\r\n" \
                  + "--" + boundary + "\r\n" \
                  + "Content-Disposition: form-data; name=\"FacePicture\";\r\n" \
                  + "Content-Type: image/jpeg\r\n" \
                  + "Content-Length: " + str(len(byte_pic)) + "\r\n\r\n" \
                  + byte_pic + "\r\n" \
                  + "--" + boundary + "--\r\n"
<<<<<<< HEAD
        response = self.requests.post(f"http://{self.ip}/ISAPI/AccessControl/userInfoAndRight/setup?format=json",
                                      auth=self.requests_auth,
                                      data=payload,
                                      verify=False,
                                      headers=headers,
                                      timeout=5)
        logger.warning(response.text)
=======
        try:
            response = self.requests.post(f"http://{self.ip}/ISAPI/AccessControl/userInfoAndRight/setup?format=json",
                                          auth=HTTPDigestAuth(self.username, self.password),
                                          data=payload,
                                          verify=False,
                                          headers=headers,
                                          timeout=5)
        except self.requests.ConnectTimeout:
            return False
        logger.info(response.text)
        #        print(response.text)
>>>>>>> master
        if response.text.find("\"deleteUser\": true,") != -1:
            return True
        return False


class MachineThread:
    """
       设备任务管理容器对象，该类为单例模式，确保任何时候获取该对象时都是同一个对象，从而保证放入该容器的对象可以正常获取
    """
    poll_time = Config.poll_time  # 单位秒
    # _instance = None  hasattr
    lock_r = threading.RLock()
    _first_init = True

    def __new__(cls, *args, **kwargs) -> object:
        if not hasattr(cls, "_instance"):  # 返回Boolean
            with cls.lock_r:
                instance = super(__class__, cls).__new__(cls)
                setattr(cls, "_instance", instance)  # 设置属性 cls._instance = object  同理
        return getattr(cls, "_instance")

    def __init__(self):
        """存放每台在线消费机实例所有信息"""
        if getattr(self, "_first_init"):
            self.sbinfo = {}
            self.threads = {}
            # 防止每次初始化
            self.__class__._first_init = False

<<<<<<< HEAD
    # classmethod确保被装饰的方法可以不实例化 直接调用
=======
>>>>>>> master
    @classmethod
    def get_instance(cls):
        """
        获取容器对象实例
        # 用法：
        mt = MachineThread.get_instance()
        mt.add_obj_to_container('user_id_' + str(user_id), self.room)
        Returns:

        """
        if not getattr(cls, '_instance', None):
            return getattr(cls, '_instance')
        else:
            return MachineThread()

    def task_loop(self):
<<<<<<< HEAD
        i = 0
        while i < self.poll_time:
            i += 1
            time.sleep(1)
            if i == self.poll_time:
                """执行其他任务"""
                # 执行下发、删除人脸
                self.task_face()
                # 打印存活线程
                logger.warning(f'存活的线程{self.get_online_thread()}')
                # print('有', threading.active_count(), '个线程正在运行', threading.enumerate())
                self.task_loop()

    def task_face(self):
        for obj in self.threads:
            _lk: LongLink = self.threads[obj].get('LongLink')
            if _lk:
                _lk.addStaff()
                _lk.delStaff()
=======
        """开启时先调用一次，后面按轮询时间来"""
        while True:
            """执行其他任务"""
            # 刷新设备列表
            try:
                self.refresh_machine()
            except:
                pass
            print('未停用的', self.threads)
            # 将停用的设备停止运行
            for _ in self.get_deactivate_machine():
                self.kill_thread(list(_.keys())[0])
            # 检查是否新增设备，有的话启动新线程
            self.start_all_thread()
            # 执行下发、删除人脸
            try:
                logger.info('开始下发人脸')
                self.task_face()
            except:
                traceback.print_exc()
                logger.error('下发人脸异常')
            # 打印存活线程
            # logger.info(f'共计：{threading.active_count()}个线程正在运行，存活的线程{self.get_online_thread()}')
            print('有', threading.active_count(), '个线程正在运行', threading.enumerate())
            if threading.active_count() == 1:
                LongLink.exit()
            time.sleep(Config.poll_time)

    def task_face(self):
        for obj in self.threads:
            try:
                _lk: LongLink = self.threads[obj]['LongLink']
            except Exception as e:
                logger.error('本该在线的长连接LongLink，却不在线')
            else:
                _lk.addStaff()
                _lk.delStaff()
        return True
>>>>>>> master

    def add_machine(self, key: str, obj: Any):
        """
        添加对象到线程容器中
        Args:
            key: 键
            obj: 对象 | 值
        Returns:

        """
        if key not in self.threads.keys():
            self.threads[key] = obj
        else:
<<<<<<< HEAD
            logging.error("已存在无法添加到线程容器")
=======
            logger.warning("已存在无法添加到线程容器")
>>>>>>> master

    def refresh_machine(self):
        """刷新获取所有消费机设备 并且放入容器"""
        query_all = hkws_xf_sbmx.objects.filter(sblxid=4)
        for obj in query_all:
            # 设备类型id 为 4是人脸消费机
            d = obj.__dict__
            del d['_state']
<<<<<<< HEAD
            self.sbinfo[obj.id] = {'query_obj': d}
=======
            if self.sbinfo.get(obj.id) and self.sbinfo[obj.id].get('query_obj'):
                self.sbinfo[obj.id]['query_obj'] = d
            else:
                self.sbinfo[obj.id] = {'query_obj': d}
>>>>>>> master
        return self.sbinfo

    def get_all_machine(self):
        """
        获得容器所有设备
        :return:
        """
        return self.sbinfo

    def start_all_thread(self):
        """启动未停用并且未在线的消费机"""
        if not self.sbinfo:
            logger.warning('请先获取设备，或执行refresh_machine')
            return False
        for i in self.sbinfo.keys():
            item = self.sbinfo[i]
            if not item.get('query_obj').get('ty'):
                if self.threads.get(i) and 'LongLink' in self.threads.get(i):
                    continue
                self.add_machine(i, {"query_obj": item.get('query_obj')})
                i_: LongLink = LongLink(ip=item.get('query_obj').get('sbip'),
                                        username=item.get('query_obj').get('userid'),
                                        password=item.get('query_obj').get('password'),
                                        ids=item.get('query_obj').get('id'))
<<<<<<< HEAD
                i_.setDaemon(True)
=======
                # i_.setDaemon(True)
>>>>>>> master
                i_.start()

    def get_activate_machine(self):
        """
        获得未停用的设备
        :return:list
        """
        activate_machines = []
        for machine in self.sbinfo:
<<<<<<< HEAD
            if self.sbinfo[machine]['query_obj']['ty'] == False:
=======
            if self.sbinfo[machine]['query_obj']['ty'] is False:
>>>>>>> master
                activate_machines.append({machine: self.sbinfo[machine]})
        return activate_machines

    def get_deactivate_machine(self):
        """
        获得停用的设备
        :return: list
        """
        deactivate_machines = []
        for machine in self.sbinfo:
<<<<<<< HEAD
            if self.sbinfo[machine]['query_obj']['ty'] == True:
=======
            if self.sbinfo[machine]['query_obj']['ty'] is True or self.sbinfo[machine]['query_obj']['sbip'] != \
                    self.get_online_thread()[machine]['query_obj'].get('sbip'):
>>>>>>> master
                deactivate_machines.append({machine: self.sbinfo[machine]})
        return deactivate_machines

    def get_online_thread(self):
        """
        获得所有在线设备的线程
        :return:
        """
        return self.threads

    def kill_thread(self, ids: int):
        """查看停用设备是否在在线设备列表，在的话就杀死线程   172.17.11.12"""
<<<<<<< HEAD
        tl: LongLink = self.threads[ids]['LongLink']
        tl.stop()
=======
        try:
            tl: LongLink = self.threads[ids]['LongLink']
            tl.stop()
            logger.info(f'{self.threads[ids]}停用设备关闭成功')
        except Exception as e:
            logger.info(f'停用设备，不在线了 设备id:{ids}')
>>>>>>> master

    def getPicByPath(self, picpath) -> bytes:
        """
        通过图片地址获取 文件二进制
        :param picpath:
        :return:
        """
        files = None
        if picpath:
            with open(picpath, "rb") as file:
                files = file.read()
        return files


def main():
    print("我是谁", os.getpid())
    with open("pid.txt", 'w') as files:
        files.write(str(os.getpid()))
    mt = MachineThread().get_instance()
    print('写入文件的process id:', os.getpid())
    try:
        mt.refresh_machine()
        mt.start_all_thread()
        mt.task_loop()
    except KeyboardInterrupt:
        print("主动关闭报错")
<<<<<<< HEAD
        print('获取在线的线程', mt.get_online_thread())
        exit()
=======
        exit()
    except RecursionError:
        print("关闭进程，重启服务")
>>>>>>> master


if __name__ == '__main__':
    main()

<<<<<<< HEAD
    # mt.kill_thread(2) #杀死对象key为2的线程
=======
# mt.kill_thread(2) #杀死对象key为2的线程
>>>>>>> master
