# Creation time: 2022/6/9 11:30
# The author: Tiger_YC
import threading
import traceback
from typing import Type, Optional

from httpAsyncClient.models import hkws_yg_sbqy
from public.utils.BaseOrm import BaseORM
from public.utils.sqlserver import SqlServerObject


class HKWSYGSBQYORM(BaseORM):
    def __init__(self, model: Type[hkws_yg_sbqy]):
        super(HKWSYGSBQYORM, self).__init__(model)
        self.model = model
        self.sql_orm = SqlServerObject()

    def sel_add_staff_bysbid(self, sbid: int) -> list:
        """
        查询 需要增加到消费机设备员工信息   是否有人脸标识hkws_rlbs
        :param sbid: 必填
        :return: list
        """
        sql = f"""select e.id as sbid,e.sbip,a.ygid,b.ygmc from ykt_ickqy a
                        join rs_ygxx b on a.ygid = b.id
                        join ykt_csh_ickqy c on c.id = a.qyid
                        join hkws_xf_sbmx e on e.sbickqyid = a.qyid
                        left join hkws_xf_sbygxx f on f.ygid=a.ygid and f.sbid = e.id
                        where b.sflz = 0 and e.ty = 0 and e.sblxid = 4 and f.ygid is null and b.hkws_rlbs = 1 
                        and e.id = {sbid}"""
        result_set, column_list = self.sql_orm.query_data(sql)
        data_list = [dict(zip(column_list, row)) for row in result_set]
        return data_list

    def sel_del_staff_bysbid(self, sbid: int) -> list:
        """
         查询 需要删除消费机设备上的员工
        :param sbid:
        :return: list    字段： ygid
        """
        sql = f"""select * from (select ygid from hkws_xf_sbygxx where sbid = {sbid}) as a
                where a.ygid not in (
                select a.ygid  from ykt_ickqy a
                left join rs_ygxx b on a.ygid = b.id
                join ykt_csh_ickqy c on c.id = a.qyid
                join hkws_xf_sbmx e on e.sbickqyid = a.qyid
                where b.sflz = 0 and e.ty = 0 and e.id = {sbid})"""
        result_set, column_list = self.sql_orm.query_data(sql)
        data_list = [dict(zip(column_list, row)) for row in result_set]
        return data_list

    def add_staff_record(self, ygid: int, sbid: int, isSuccess: int) -> bool:
        """
        增加员工人脸信息设备成功or失败记录
        :param ygid:
        :param sbid:
        :param isSuccess:
        :return:
        """
        sql = "insert into hkws_xf_sbygxx values(%s,%s,%s)" % (ygid, sbid, isSuccess)
        try:
            self.sql_orm.insert_data(sql)  # 已经有事务回滚了
        except:
            traceback.print_exc()
            return False
        return True

    def del_staff_record(self, ygid: int, sbid: int) -> bool:
        """
        删除员工设备记录
        :param ygid:
        :param sbid:
        :param isSuccess:
        :return:
        """
        sql = "delete from hkws_xf_sbygxx where ygid = %s and sbid = %s" % (ygid, sbid)
        try:
            self.sql_orm.insert_data(sql)  # 已经有事务回滚了
        except:
            traceback.print_exc()
            return False
        return True

    def update_staff_record(self, ygid: int, sbid: int, isSuccess: int) -> bool:
        """
        更新员工设备失败记录
        :param ygid:
        :param sbid:
        :param isSuccess:
        :return:
        """
        sql = "update hkws_xf_sbygxx set isSuccess = %s where ygid = %s and sbid = %s" % (ygid, sbid, isSuccess)
        try:
            self.sql_orm.insert_data(sql)  # 已经有事务回滚了
        except:
            traceback.print_exc()
            return False
        return True

    def selTransactionRecordBySerialNo(self, serialNo: int) -> list:
        """
        根据流水号查询交易记录
        :param serialNo:
        :return:
        """
        sql = f"select * from hkws_xf_xfmx where serialNo = {serialNo}"
        result_set, column_list = self.sql_orm.query_data(sql)
        data_list = [dict(zip(column_list, row)) for row in result_set]
        return data_list

    def QueryDeviceInformationByIp(self, ipAddress: str) -> list:
        """
        按ip地址查询 所有未停用设备信息
        :param ipAddress:
        :return:
        """
        sql = f"select * from hkws_xf_sbmx where sblxid = 4 and ty=0 and sbip='%s'" % ipAddress
        result_set, column_list = self.sql_orm.query_data(sql)
        data_list = [dict(zip(column_list, row)) for row in result_set]
        return data_list

    def get_xfmx_by_serialNo(self, serialNo: int, ipAddress: str) -> list:
        """
        通过serialNo  消费机序列化获取所有消费明细
        :param serialNo:
        :return:
        """
        sql = "select * from hkws_xf_xfmx where serialNo = %s AND sbip='%s' " % (serialNo, ipAddress)
        result_set, column_list = self.sql_orm.query_data(sql)
        data_list = [dict(zip(column_list, row)) for row in result_set]
        return data_list