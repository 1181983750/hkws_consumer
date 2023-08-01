import datetime
from typing import Type, Union, Optional

from django.db.models import QuerySet, Q

from httpAsyncClient.models import hkws_xf_xfmx
from public.utils.BaseOrm import BaseORM
from public.utils.sqlserver import SqlServerObject


class HKWSXFMXORM(BaseORM):
    def __init__(self, model: Type[hkws_xf_xfmx]):
        super(HKWSXFMXORM, self).__init__(model=model)
        self.model = model
        self.sql_orm = SqlServerObject()

    def get_xfmx_by_serialNo(self, serialNo: int) -> QuerySet:
        """
        根据流水号查询交易记录  消费机用
        :param serialNo:
        :return:
        """
        query = self.model.objects.filter(serialNo=serialNo)
        return query

    def get_data_by_ygid(self, ygid: Union[str, int] = 0) -> QuerySet:
        """
        通过员工id查询消费明细所有数据
        :param ygid: int str
        :return: QuerySet
        """
        return self.model.objects.filter(ygid=ygid)

    def get_month_bt_gt_xfje_by_ygid(self, ygid: Union[str, int], month: int) -> QuerySet:
        """
        通过员工id和月份查询消费类型3或者6 并且xfje ’大于‘ 0的全部补贴明细: 查询当月是否有正数的补贴
        :param ygid:
        :param month:
        :return:
        """
        return hkws_xf_xfmx.objects.filter(Q(ygid=ygid, sjrq__year=datetime.datetime.now().year, sjrq__month=month, xfje__gt=0), (Q(xflx=3) | Q(xflx=6)))

    def get_month_bt_lt_xfje_by_ygid(self, ygid: Union[str, int], month: int) -> QuerySet:
        """
        通过员工id和月份查询消费类型3或者6 并且xfjex ’小于‘ 0的全部补贴明细: 查询当月是否有负数的补贴
        :param ygid:
        :param month:
        :return:
        """
        return self.model.objects.filter(Q(ygid=ygid, sjrq__year=datetime.datetime.now().year, sjrq__month=month, xfje__lt=0), (Q(xflx=3) | Q(xflx=6)))

    def get_xfmx_by_dateTime(self, dateStart, dateEnd) -> QuerySet:
        """
        通过起始时间 和 条件 搜索消费明细  类型 为2
        :param dateStart 必填
        :param dateEnd 必填
        :return:
        """
        return self.model.objects.filter(xfrq__range=[dateStart, dateEnd], xflx=2).order_by('-xfrq')

    def get_xfmx_by_queryAndTime_Sql(self, dateStart, dateEnd, queryStr: Optional[str] = None) -> tuple:
        """
        通过起止datetime 和 可选的 查询字符串 搜索消费明细  类型为2
        :param dateStart: 必填
        :param dateEnd: 必填
        :param queryStr: 可选
        :return: tuple
        """
        if queryStr:
            sql = f"""select a.ygid,b.ygdm,b.ygmc,b.pym,a.sbxh,a.xfje,a.ye,a.xfrq,a.czy,a.sbip from hkws_xf_xfmx a 
                                    left join rs_ygxx b on a.ygid = b.id 
                                    where  a.xfrq >= '{dateStart}' and  a.xfrq <= '{dateEnd}' and xflx = 2 
                                    and (b.ygdm like '%{queryStr}%' or b.id like '%{queryStr}%' or b.ygmc like '%{queryStr}%' or b.pym like '%{queryStr}%') ORDER BY a.xfrq desc"""
        else:
            sql = f"""select a.ygid,b.ygdm,b.ygmc,b.pym,a.sbxh,a.xfje,a.ye,a.xfrq,a.czy,a.sbip from hkws_xf_xfmx a 
                        left join rs_ygxx b on a.ygid = b.id 
                        where  a.xfrq >= '{dateStart}' and  a.xfrq <= '{dateEnd}' and xflx = 2 ORDER BY a.xfrq desc"""
        result_set, column_list = self.sql_orm.query_data(sql)

        return result_set, column_list

    def get_czmx_by_queryAndTime_Sql(self, dateStart, dateEnd, queryStr: Optional[str] = None) -> tuple:
        """
        通过起止datetime 和 可选的 查询字符串 搜索充值明细  类型为1
        :param dateStart: 必填
        :param dateEnd: 必填
        :param queryStr: 可选
        :return: tuple
        """
        if queryStr:
            sql = f"""select a.ygid,b.ygdm,b.ygmc,b.pym,a.sbip,a.sjrq,a.czy,a.xflx,a.xflxmc,a.xfje,a.ye from hkws_xf_xfmx a 
                                    left join rs_ygxx b on a.ygid = b.id 
                                    where a.sjrq >= '{dateStart}' and a.sjrq <= '{dateEnd}' and xflx = 1 
                                    and (b.ygdm like '%{queryStr}%' or b.id like '%{queryStr}%' or b.ygmc like '%{queryStr}%' or b.pym like '%{queryStr}%') ORDER BY a.sjrq desc"""
        else:
            sql = f"""select a.ygid,b.ygdm,b.ygmc,b.pym,a.sbip,a.sjrq,a.czy,a.xflx,a.xflxmc,a.xfje,a.ye from hkws_xf_xfmx a 
                        left join rs_ygxx b on a.ygid = b.id 
                        where a.sjrq >= '{dateStart}' and  a.sjrq <= '{dateEnd}' and xflx = 1 ORDER BY a.sjrq desc"""
        result_set, column_list = self.sql_orm.query_data(sql)
        return result_set, column_list

    def get_tkmx_by_queryAndTime_Sql(self, dateStart, dateEnd, queryStr: Optional[str] = None) -> tuple:
        """
        通过起止datetime 和 可选的 查询字符串 搜索退款明细  类型为4 or 5  现金退款与消费退款
        :param dateStart: 必填
        :param dateEnd: 必填
        :param queryStr: 可选
        :return: tuple
        """
        if queryStr:
            sql = f"""select a.ygid,b.ygdm,b.ygmc,b.pym,a.czy,a.sbip,a.xflx,a.xflxmc,a.sjrq,a.xfje,a.ye from hkws_xf_xfmx a 
                                    left join rs_ygxx b on a.ygid = b.id 
                                    where  a.sjrq >= '{dateStart}' and  a.sjrq <= '{dateEnd}' and (xflx = 4 or xflx = 5) 
                                    and (b.ygdm like '%{queryStr}%' or b.id like '%{queryStr}%' or b.ygmc like '%{queryStr}%' or b.pym like '%{queryStr}%') ORDER BY a.sjrq desc"""
        else:
            sql = f"""select a.ygid,b.ygdm,b.ygmc,b.pym,a.czy,a.sbip,a.xflx,a.xflxmc,a.sjrq,a.xfje,a.ye from hkws_xf_xfmx a 
                        left join rs_ygxx b on a.ygid = b.id 
                        where  a.sjrq >= '{dateStart}' and  a.sjrq <= '{dateEnd}' and (xflx = 4 or xflx = 5) ORDER BY a.sjrq desc"""
        result_set, column_list = self.sql_orm.query_data(sql)
        return result_set, column_list

    def get_batch_btmx_by_queryAndTime_Sql(self, dateStart, dateEnd, queryStr: Optional[str] = None) -> tuple:
        """
        通过起止datetime 和 可选的 查询字符串 搜索批量补贴明细  类型为6
        :param dateStart: 必填
        :param dateEnd: 必填
        :param queryStr: 可选
        :return: tuple
        """
        if queryStr:
            sql = f"""select a.ygid,b.ygdm,b.ygmc,b.pym,a.sjrq,a.czy,a.sbip,a.xflx,a.xflxmc,a.xfje,a.ye from hkws_xf_xfmx a 
                                           left join rs_ygxx b on a.ygid = b.id 
                                           where  a.sjrq >= '{dateStart}' and  a.sjrq <= '{dateEnd}' and xflx=6
                                           and (b.ygdm like '%{queryStr}%' or b.id like '%{queryStr}%' or b.ygmc like '%{queryStr}%' or b.pym like '%{queryStr}%') ORDER BY a.sjrq desc"""
        else:
            sql = f"""select a.ygid,b.ygdm,b.ygmc,b.pym,a.sjrq,a.czy,a.sbip,a.xflx,a.xflxmc,a.xfje,a.ye from hkws_xf_xfmx a 
                               left join rs_ygxx b on a.ygid = b.id 
                               where a.sjrq >= '{dateStart}' and a.sjrq <= '{dateEnd}' and xflx=6 ORDER BY a.sjrq desc"""
        result_set, column_list = self.sql_orm.query_data(sql)
        return result_set, column_list

    def get_single_btmx_by_queryAndTime_Sql(self, dateStart, dateEnd, queryStr: Optional[str] = None) -> tuple:
        """
        通过起止datetime 和 可选的 查询字符串 搜索单一补贴明细  类型为3
        :param dateStart: 必填
        :param dateEnd: 必填
        :param queryStr: 可选
        :return: tuple
        """
        if queryStr:
            sql = f"""select a.ygid,b.ygdm,b.ygmc,b.pym,a.sjrq,a.czy,a.sbip,a.xflx,a.xflxmc,a.xfje,a.ye from hkws_xf_xfmx a 
                                           left join rs_ygxx b on a.ygid = b.id 
                                           where a.sjrq >= '{dateStart}' and a.sjrq <= '{dateEnd}' and xflx=3
                                           and (b.ygdm like '%{queryStr}%' or b.id like '%{queryStr}%' or b.ygmc like '%{queryStr}%' or b.pym like '%{queryStr}%') ORDER BY a.sjrq desc"""
        else:
            sql = f"""select a.ygid,b.ygdm,b.ygmc,b.pym,a.sjrq,a.czy,a.sbip,a.xflx,a.xflxmc,a.xfje,a.ye from hkws_xf_xfmx a 
                               left join rs_ygxx b on a.ygid = b.id 
                               where  a.sjrq >= '{dateStart}' and  a.sjrq <= '{dateEnd}' and xflx=3 ORDER BY a.sjrq desc"""
        result_set, column_list = self.sql_orm.query_data(sql)
        return result_set, column_list

    def get_all_btmx_by_queryAndTime_Sql(self, dateStart, dateEnd, queryStr: Optional[str] = None) -> tuple:
        """
        通过起止datetime 和 可选的 查询字符串 搜索全部补贴明细  类型为3 or 6 单一与批量
        :param dateStart: 必填
        :param dateEnd: 必填
        :param queryStr: 可选
        :return: tuple
        """
        if queryStr:
            sql = f"""select a.ygid,b.ygdm,b.ygmc,b.pym,a.sjrq,a.czy,a.sbip,a.xflx,a.xflxmc,a.xfje,a.ye from hkws_xf_xfmx a 
                                           left join rs_ygxx b on a.ygid = b.id 
                                           where a.sjrq >= '{dateStart}' and a.sjrq <= '{dateEnd}' and (xflx=3 or xflx=6)
                                           or (a.ygid like '%{queryStr}%' or b.ygdm like '%{queryStr}%' or b.ygmc like '%{queryStr}%' or b.pym like '%{queryStr}%') ORDER BY a.sjrq desc"""
        else:
            sql = f"""select a.ygid,b.ygdm,b.ygmc,b.pym,a.sjrq,a.czy,a.sbip,a.xflx,a.xflxmc,a.xfje,a.ye from hkws_xf_xfmx a 
                                           left join rs_ygxx b on a.ygid = b.id 
                                           where a.sjrq >= '{dateStart}' and a.sjrq <= '{dateEnd}' and (xflx=3 or xflx=6) ORDER BY a.sjrq desc"""
        result_set, column_list = self.sql_orm.query_data(sql)
        return result_set, column_list

    def get_all_mx_by_queryAndTime_Sql(self, dateStart, dateEnd, queryStr: Optional[str] = None) -> tuple:
        """
        通过起止datetime 和 可选的 查询字符串 搜索全部类型明细
        :param dateStart: 必填
        :param dateEnd: 必填
        :param queryStr: 可选
        :return: tuple
        """
        if queryStr:
            sql = f"""select a.ygid,b.ygdm,b.ygmc,b.pym,a.sjrq,a.czy,a.sbip,a.xflx,a.xflxmc,a.xfje,a.ye from hkws_xf_xfmx a 
                                           left join rs_ygxx b on a.ygid = b.id 
                                           where a.sjrq >= '{dateStart}' and  a.sjrq <= '{dateEnd}'
                                           or (a.ygid like '%{queryStr}%' or b.ygdm like '%{queryStr}%' or b.ygmc like '%{queryStr}%' or b.pym like '%{queryStr}%') ORDER BY a.sjrq desc"""
        else:
            sql = f"""select a.ygid,b.ygdm,b.ygmc,b.pym,a.sjrq,a.czy,a.sbip,a.xflx,a.xflxmc,a.xfje,a.ye from hkws_xf_xfmx a 
                                           left join rs_ygxx b on a.ygid = b.id 
                                           where a.sjrq >= '{dateStart}' and a.sjrq <= '{dateEnd}' ORDER BY a.sjrq desc"""
        result_set, column_list = self.sql_orm.query_data(sql)
        return result_set, column_list

    def get_everyday_czmx_count_Time_Sql(self, dateStart, dateEnd, queryStr: Optional[str] = None) -> tuple:
        """
        获取 每日 充值 统计 情况
        :param dateStart: 必填
        :param dateEnd: 必填
        :return: tuple
        """
        if dateStart and dateEnd:
            sql = f"""select sum(xfje) as xfje from hkws_xf_xfmx a left join hkws_xf_user b on a.czy = b.username  where a.xflx = 1 and  a.sjrq >='{dateStart}' and a.sjrq <= '{dateEnd}'"""
        else:
            sql = f"""select sum(xfje) as xfje from hkws_xf_xfmx a left join hkws_xf_user b on a.czy = b.username  where a.xflx = 1 and  a.sjrq >='{datetime.datetime.now()}' and a.sjrq <= '{datetime.datetime.now()}'"""
        result_set, column_list = self.sql_orm.query_data(sql)
        return result_set, column_list

    def getDaysCountCZmx(self, dateStart: str, dateEnd: str) -> tuple:
        """
        根据时间统计充值金额明细
        :param dateStart: 必填
        :param dateEnd: 必填
        :return: tuple
        """
        sql = f"""select CONVERT(VARCHAR, sjrq, 23) as days, sum(xfje) as xfje from hkws_xf_xfmx  WHERE xflx=1 and sjrq between '%s' and '%s' GROUP BY  CONVERT(VARCHAR, sjrq, 23)"""%(dateStart, dateEnd)
        result_set, column_list = self.sql_orm.query_data(sql)
        return result_set, column_list

