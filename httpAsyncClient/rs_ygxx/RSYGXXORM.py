from typing import Type, Union

from django.db.models import QuerySet, Q

from httpAsyncClient.models import rs_ygxx
from public.utils.BaseOrm import BaseORM
from public.utils.sqlserver import SqlServerObject


class RSYGXXORM(BaseORM):
    def __init__(self, model: Type[rs_ygxx]):
        super(RSYGXXORM, self).__init__(model)
        self.model = model
        self.sql_orm = SqlServerObject()

    def get_ygxx_by_ygid(self, ygid: Union[int, str]) -> QuerySet:
        """
        通过员工id 查询人事 员工详细信息
        :param ygid: 必填
        :return: QuerySet
        """
        query = self.model.objects.filter(ygid=ygid)
        return query


    def get_ygxx_by_query_sql(self, queryStr: str) -> tuple:
        """
        查询充值员工信息  没有离职的
        :param queryStr:
        :return: tuple
        """
        if queryStr:
            sql = f"""select a.id as ygid,ygdm,ygmc,pym,xb,bmmc,bmmc1,bmmc2,bmmc3,hkws_rlbs,ISNULL(b.ye, '0') as ye 
            from rs_ygxx a 
            left join hkws_xf_ygye b on a.id = b.ygid 
            where sflz<>1 and (ygdm like '%{queryStr}%' or ygmc like '%{queryStr}%' or pym like '%{queryStr}%')"""
        else:
            sql = f"""select a.id as ygid,ygdm,ygmc,pym,xb,bmmc,bmmc1,bmmc2,bmmc3,hkws_rlbs,ISNULL(b.ye, '0') as ye 
                        from rs_ygxx a 
                        left join hkws_xf_ygye b on a.id = b.ygid 
                        where sflz<>1"""
        result_set, column_list = self.sql_orm.query_data(sql)
        return result_set, column_list

    def get_ygxx_by_ygdm_sql(self, ygdm: Union[str, int]) -> tuple:
        """
        通过ygdm 查询充值员工信息  没有离职的
        :param ygdm: 必填
        :return:
        """
        sql = f"""select a.id as ygid,ygdm,ygmc,pym,xb,bmmc,bmmc1,bmmc2,bmmc3,hkws_rlbs,ISNULL(b.ye, '0') as ye 
                        from rs_ygxx a 
                        left join hkws_xf_ygye b on a.id = b.ygid 
                        where sflz=0 and ygdm='{ygdm}'"""
        result_set, column_list = self.sql_orm.query_data(sql)
        return result_set, column_list

    def get_noface_ygxx_sql(self, queryStr) -> tuple:
        """
        获取需要采集人脸的员工信息  未离职 未停用
        :param queryStr:
        :return:
        """
        if queryStr:
            sql = f"""select a.ygid,b.ygdm,b.ygmc,b.pym,c.id as sbid,c.sbip,a.issuccess 
            from hkws_xf_sbygxx a 
            left join rs_ygxx b on a.ygid = b.id
            left join hkws_xf_sbmx c on a.sbid = c.id
            where a.issuccess = 0 and c.ty = 0 and b.sflz = 0 and c.ty = 0 and
            (b.ygdm like '%{queryStr}%' or b.ygmc like '%{queryStr}%' or b.pym like '%{queryStr}%')"""
        else:
            sql = f"""select a.ygid,b.ygdm,b.ygmc,b.pym,c.id as sbid,c.sbip,a.issuccess 
                    from hkws_xf_sbygxx a 
                    left join rs_ygxx b on a.ygid = b.id
                    left join hkws_xf_sbmx c on a.sbid = c.id
                    where a.issuccess = 0 and c.ty = 0 and b.sflz = 0 and c.ty = 0"""
        result_set, column_list = self.sql_orm.query_data(sql)
        return result_set, column_list

    def get_all_ygxx_sql(self, queryStr) -> tuple:
        """
        获取所有员工信息    包括离职的
        :return:
        """
        if queryStr:
            sql = f"""select a.id as ygid,ygdm,ygmc,pym,xb,bmmc,bmmc1,bmmc2,bmmc3,hkws_rlbs,ISNULL(b.ye,'0') as ye,a.sflz 
            from rs_ygxx a 
            left join hkws_xf_ygye b on a.id = b.ygid  
            where (ygdm like '%{queryStr}%' or ygmc like '%{queryStr}%' or pym like '%{queryStr}%')"""
        else:
            sql = f"""select a.id as ygid,ygdm,ygmc,pym,xb,bmmc,bmmc1,bmmc2,bmmc3,hkws_rlbs,ISNULL(b.ye,'0') as ye,a.sflz 
                       from rs_ygxx a 
                       left join hkws_xf_ygye b on a.id = b.ygid """
        result_set, column_list = self.sql_orm.query_data(sql)
        return result_set, column_list