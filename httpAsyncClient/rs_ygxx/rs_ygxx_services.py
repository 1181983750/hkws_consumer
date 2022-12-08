# Creation time: 2022/5/31 15:07
# The author: Tiger_YC
from typing import Union, Type

from rest_framework.serializers import ModelSerializer

from httpAsyncClient.models import rs_ygxx
from httpAsyncClient.rs_ygxx.RSYGXXORM import RSYGXXORM
from public.utils.BaseOrm import BaseService
from public.utils.response_result import ResponseResult


class RSYGXXServices(BaseService):
    def __init__(self, model: Type[rs_ygxx]):
        super(RSYGXXServices, self).__init__(model=model)
        self.orm = RSYGXXORM(model=model)


    def get_ygxx_wlz_or_by_query(self, queryString: Union[int, str], serializer: Type[ModelSerializer] = None):
        """
        查询充值员工信息
        :param queryString: 可选
        :param serializer:  可选
        :return:
        """
        result_set, column_list = self.orm.get_ygxx_by_query_sql(queryString)
        data_list = [dict(zip(column_list, row)) for row in result_set]
        # q = self.orm.get_all()[:10000]
        # data_list = serializer(q,many=True).data
        return ResponseResult(msg='查询成功', code=1, data=data_list)


    def get_ygxx_by_ygdm(self, ygdm: Union[int, str], serializer: Type[ModelSerializer] = None):
        """
         根据 ygdm 查询 员工信息
        :param ygdm:
        :param serializer:
        :return:
        """
        # qs = self.get_all(serializer)
        result_set, column_list = self.orm.get_ygxx_by_ygdm_sql(ygdm)
        data_list = [dict(zip(column_list, row)) for row in result_set]
        return ResponseResult(msg='查询成功', code=1, data=data_list)

    def get_noface_ygxx(self, queryString):
        """
        获取需要采集人脸的员工信息
        :param queryString:
        :return:
        """
        result_set, column_list = self.orm.get_noface_ygxx_sql(queryString)
        data_list = [dict(zip(column_list, row)) for row in result_set]
        return ResponseResult(msg='查询成功', code=1, data=data_list)

    def get_all_ygxx(self, queryString):
        """
        全部员工信息 存在离职的
        :param queryString:
        :return:
        """
        result_set, column_list = self.orm.get_all_ygxx_sql(queryString)
        data_list = [dict(zip(column_list, row)) for row in result_set]
        return ResponseResult(msg='查询成功', code=1, data=data_list)

