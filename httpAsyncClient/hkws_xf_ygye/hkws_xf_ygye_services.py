import copy
<<<<<<< HEAD
from decimal import Decimal
=======
from decimal import Decimal, getcontext
>>>>>>> master
from typing import Type, Union

from django.db.models import QuerySet
from rest_framework.serializers import ModelSerializer

from httpAsyncClient.hkws_xf_xfmx.HKWSXFMXORM import HKWSXFMXORM
from httpAsyncClient.hkws_xf_ygye.HKWSXFYGYEORM import HKWSXFYGYEORM
from httpAsyncClient.models import hkws_xf_ygye, hkws_xf_xfmx
from public.utils.BaseOrm import BaseService, DictToModel
from public.utils.response_result import ResponseResult


class HKWSXFYGYEServices(BaseService):
    def __init__(self, model: Type[hkws_xf_ygye]):
        super(HKWSXFYGYEServices, self).__init__(model=model)
        self.orm = HKWSXFYGYEORM(model=model)
        self.xfmx_orm = HKWSXFMXORM(model=hkws_xf_xfmx)

    def get_ygye(self, ygid: Union[int, str], serializer: Type[ModelSerializer] = None):
        """
        通过员工id 查到余额 从明细表计算 以保证正确
        :param ygid:
        :return:
        """
        ye_query: hkws_xf_ygye = self.orm.get_ye_by_ygid(ygid)
        yemx_query: QuerySet = self.xfmx_orm.get_data_by_ygid(ygid)
        yemx_serializer = serializer(instance=yemx_query, many=True)
        yemx_result = 0
        for obj in yemx_serializer.data:
            obj: dict
            result = copy.deepcopy(obj.get('xfje', None))
            yemx_result += Decimal(result)
        if ye_query.ye != yemx_result:
            return ResponseResult(msg='余额异常，联系管理员校对')
        return ResponseResult(msg='查询成功', code=1, data={'ygid':ygid, 'ygye': ye_query.ye})

    def fix_xfmx_ygye(self, ygid: Union[int, str], serializer: Type[ModelSerializer] = None):
        """
        通过员工id 修复消费明细 余额不准的问题
        :param ygid:
        :param serializer:
        :return: 脚本
        """
        yemx_query: QuerySet = self.xfmx_orm.get_data_by_ygid(ygid).order_by('sjrq')
        yemx_serializer = serializer(instance=yemx_query, many=True)
        obj = yemx_serializer.data
        if obj:
            result = Decimal(obj[0].get('xfje'))  # 员工第一次的消费肯定是充值
            for index in range(obj.__len__()):
                print(obj[index]['xfje'], obj[index]['ygid'])
                dict_to_model = DictToModel(dict_data=obj[index], model_class=hkws_xf_xfmx)
                hkws_xf_xfmx_model: hkws_xf_xfmx = dict_to_model.format_dict_data_to_model(True)
                hkws_xf_xfmx_model.id = obj[index]['id']
                if index != 0:  # 最早一次的余额是充值 是基准
                    result += Decimal(obj[index]['xfje'])
                    hkws_xf_xfmx_model.ye = result
                    hkws_xf_xfmx_model.save()
            assert self.orm.update_ygye(ygid, result), f'员工余额表没有初始化创建该员工id:{ygid}'
        else:
            return ResponseResult(msg=f'无该员工id{ygid}明细', code=-1, data={'ygid': ygid, 'ygye': 0})
        return ResponseResult(msg='修复明细余额成功', code=1, data={'ygid': ygid, 'ygye': result})



