# Creation time: 2022/6/2 15:54
# The author: Tiger_YC
import calendar
import datetime
from typing import Type, Union, Optional

from django.db.models import QuerySet

from httpAsyncClient.models import hkws_xf_btmd
from public.utils.BaseOrm import BaseORM
from public.utils.sqlserver import SqlServerObject


class HKWSXFBTORM(BaseORM):
    def __init__(self, model: Type[hkws_xf_btmd]):
        super(HKWSXFBTORM, self).__init__(model=model)
        self.model = model
        self.sql_orm = SqlServerObject()

    def get_batch_btmd_by_ygid_Sql(self, ygid: Union[int, str]) -> tuple:
        """
        通过员工id增加批量补贴记录  类型为6
        :param dateStart: 必填
        :param dateEnd: 必填
        :param queryStr: 可选
        :return: tuple
        """
        sql = f"""select a.ygid,b.ygdm,b.ygmc,a.btje,a.bz from hkws_xf_btmd  a
                left join rs_ygxx b on a.ygid = b.id
                where a.ygid = {ygid}"""
        result_set, column_list = self.sql_orm.query_data(sql)
        return result_set, column_list

    def del_batch_btmd_by_ygid(self, ygid: Union[int, str]) -> tuple:
        """
        通过员工id删除批量补贴记录
        :param ygid:
        :return:
        """
        return self.model.objects.filter(ygid=ygid).delete()

    def sel_batch_btmd_by_query_Sql(self, queryStr: Union[str, int]) -> tuple:
        """
        通过搜索条件 查询批量补贴名单
        :param queryStr:
        :return: tuple
        """

        sql = """select a.ygid,b.ygdm,b.ygmc,a.btje,a.bz,a.statusmsg from hkws_xf_btmd a 
                    left join rs_ygxx b on a.ygid = b.id order by a.id desc"""
        if queryStr:
            sql = f"""select a.ygid,b.ygdm,b.ygmc,a.btje,a.bz,a.statusmsg from hkws_xf_btmd a 
                left join rs_ygxx b on a.ygid = b.id 
                where a.ygid like '%{queryStr}%' or b.ygdm like '%{queryStr}%' or b.ygmc like '%{queryStr}%' or b.pym like '%{queryStr}%' order by a.id desc"""
        result_set, column_list = self.sql_orm.query_data(sql)
        return result_set, column_list

    def sel_batch_btmd_by_month_Sql(self, month: Union[str, int]) -> tuple:
        """
        通过月份 查询批量补贴名单
        :param month:
        :return: tuple
        """
        now = datetime.datetime.now()
        start = f"{now.year}-{month}-1"
        end = f"{now.year}-{month}-{calendar.monthrange(now.year, month)[1]}"
        sql = f"""select a.ygid,b.ygdm,b.ygmc,a.xfje,a.sjrq,a.czy,a.xflx,a.xflxmc,a.ye  from hkws_xf_xfmx a 
            left join rs_ygxx b on a.ygid = b.id
            where xflx = 6 and CONVERT(date, sjrq) >= '{start}' and CONVERT(date, sjrq) <= '{end}'
            """
        result_set, column_list = self.sql_orm.query_data(sql)
        return result_set, column_list

    def sel_batch_btmd_not_done(self,):
        """
        查询没有进行批量补贴的名单
        :return:
        """
        month = datetime.datetime.now().month
        sql = f"""select a.ygid,b.ygdm,b.ygmc,a.btje,a.bz,a.statusmsg  from hkws_xf_btmd a 
              left join rs_ygxx b on a.ygid = b.id where a.statusmsg <> '{month}' or a.statusmsg is null """
        result_set, column_list = self.sql_orm.query_data(sql)
        return result_set, column_list

    def update_batch_btmd(self, data_dict: dict) -> QuerySet:
        """
        修改批量补贴名单
        :param data_dict:
        :return:QuerySet
        """
        query = self.model.objects.filter(ygid=data_dict['ygid'])
        query.update(btje=data_dict['amount'], bz=data_dict.get('bz'))
        return query

    def update_batch_subsidy_status(self, ygid: Union[str, int], status: Union[str, int]) -> QuerySet:
        """
        修改补贴状态
        :param ygid:
        :param status:
        :return:
        """
        query = self.model.objects.filter(ygid=ygid)
        query.update(statusmsg=status)
        return query



