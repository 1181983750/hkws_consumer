# Creation time: 2022/5/31 15:18
# The author: Tiger_YC

<<<<<<< HEAD
import datetime
from decimal import Decimal
from typing import Type, Union, Optional

=======
from decimal import Decimal
from typing import Type, Union

from django.db import transaction
>>>>>>> master

from httpAsyncClient.models import hkws_xf_ygye
from public.utils.BaseOrm import BaseORM


class HKWSXFYGYEORM(BaseORM):
    def __init__(self, model: Type[hkws_xf_ygye]):
        super(HKWSXFYGYEORM, self).__init__(model)
        self.model = model

<<<<<<< HEAD
=======
    @transaction.atomic
>>>>>>> master
    def get_ye_by_ygid(self, ygid: Union[str, int] = 0) -> hkws_xf_ygye:
        """
        通过员工id查询员工余额表 的当前余额
        :param ygid: int str
        :return: model_obj
        """
        try:
<<<<<<< HEAD
            query = self.model.objects.get(ygid=ygid) #返回一个模型查询对象
=======
            query = self.model.objects.select_for_update().get(ygid=ygid) #返回一个模型查询对象
>>>>>>> master
        except self.model.DoesNotExist:
            return hkws_xf_ygye()  #返回一个空Model查询对象 Object: hkws_xf_ygye:〔_state=<django.db.models.base.ModelState object at 0x000002824BE2BD60>, id=None, ygid=None, ye=None〕
        return query

    def init_ye_by_ygid(self, ygid: Union[str, int] = 0) -> hkws_xf_ygye:
        """
        用的时候记得try  因为是create()
        防止第一次没有余额记录 初始化下员工余额
<<<<<<< HEAD
        :param ygid:
=======
        :param ygid:1
>>>>>>> master
        :return: model_obj
        """
        try:
            result = self.model.objects.create(ygid=ygid, ye=0)
        except Exception as e:
            raise Exception(e)
        else:
            return result

<<<<<<< HEAD
=======
    @transaction.atomic
>>>>>>> master
    def update_ygye(self, ygid: Union[str, int] = 0, ye: Union[int, Decimal] = 0) -> hkws_xf_ygye:
        """
        通过员工id 和 传入的余额 更新 员工余额表
        :param ygid:
        :param ye:
        :return: model_obj
        """
        try:
<<<<<<< HEAD
            result: hkws_xf_ygye = self.model.objects.get(ygid=ygid)
=======
            result: hkws_xf_ygye = self.model.objects.select_for_update().get(ygid=ygid)
>>>>>>> master
            result.ye = ye
            result.save()
        except Exception as e:
            raise Exception(e)
        else:
            return result

