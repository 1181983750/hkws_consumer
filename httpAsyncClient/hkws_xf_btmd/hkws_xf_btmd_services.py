# Creation time: 2022/6/2 15:38
# The author: Tiger_YC
import datetime
import traceback
from typing import Type, Union

from rest_framework.serializers import ModelSerializer

from httpAsyncClient.hkws_xf_ygye.HKWSXFYGYEORM import HKWSXFYGYEORM
from public.utils import EmployeesToBanlanceConstruction as EC
from httpAsyncClient.hkws_xf_btmd.HKWSXFBTORM import HKWSXFBTORM
from httpAsyncClient.hkws_xf_xfmx.HKWSXFMXORM import HKWSXFMXORM
from httpAsyncClient.hkws_xf_xfmx.hkws_xf_xfmx_services import HKWSXFMXServices
from httpAsyncClient.models import hkws_xf_btmd, hkws_xf_xfmx, hkws_xf_ygye
from public.utils.BaseOrm import BaseService, DictToModel
from public.utils.onlineTime import getBeijinTime
from public.utils.response_result import ResponseResult


class HKWSXFBTServices(BaseService):
    def __init__(self, model: Type[hkws_xf_btmd]):
        super(HKWSXFBTServices, self).__init__(model=model)
        self.orm = HKWSXFBTORM(model=model)
        self.xfmx_orm = HKWSXFMXORM(model=hkws_xf_xfmx)
        self.xfmx_service = HKWSXFMXServices(model=hkws_xf_xfmx)
        self.ygye_orm = HKWSXFYGYEORM(model=hkws_xf_ygye)


    def add_batch_subsidy(self, data_dict: dict, serializer:Type[ModelSerializer] = None):
        """
        增加 批量补贴 类型6
        :param data_dict:   ygid, amount, bz 必填
        :param serializer:
        :return:
        """
        # 先判断批量补贴名单是否存在了
        result_set, column_list = self.orm.get_batch_btmd_by_ygid_Sql(data_dict['ygid'])
        data_list = [dict(zip(column_list, row)) for row in result_set]
        if data_list:
            return ResponseResult("已有该补贴人员，名单重复，增加补贴名单失败")
        dict_to_model = DictToModel(dict_data=data_dict, model_class=hkws_xf_btmd)
        hkws_xf_btmd_model: hkws_xf_btmd = dict_to_model.format_dict_data_to_model(get_model_obj=True)  # 将字典转模型
        """取出模型部分信息自动赋值操作"""
        hkws_xf_btmd_model.btje = data_dict['amount']
        try:
            self.orm.add(hkws_xf_btmd_model)
        except Exception as e:
            traceback.print_exc()
            return ResponseResult(msg='批量补贴增加失败', data={"ygid": data_dict['ygid'], "btje": data_dict['amount']})
        return ResponseResult(msg='批量补贴增加成功', code=1, data={"ygid": data_dict['ygid'], "btje": data_dict['amount']})

    def del_batch_subsidy(self, data_dict: dict, serializer:Type[ModelSerializer] = None):
        """
        删除 批量补贴 类型6
        :param data_dict:   ygid 必填
        :param serializer:
        :return:
        """
        assert self.orm.del_batch_btmd_by_ygid(data_dict['ygid'])
        return ResponseResult(msg='删除批量补贴成功', code=1)

    def sel_batch_subsidy(self, queryString: Union[str, int], serializer:Type[ModelSerializer] = None):
        """
        通过条件搜索批量补贴名单
        :param queryString:
        :param serializer:
        :return:
        """
        result_set, column_list = self.orm.sel_batch_btmd_by_query_Sql(queryString)
        data_list = [dict(zip(column_list, row)) for row in result_set]
        return ResponseResult(msg='查询批量补贴成功', code=1, data=data_list)

    def sel_batch_subsidy_by_month(self, month: Union[str, int], serializer:Type[ModelSerializer] = None):
        """
        通过条件搜索批量补贴名单
        :param queryString:
        :param serializer:
        :return:
        """
        result_set, column_list = self.orm.sel_batch_btmd_by_month_Sql(month)
        data_list = [dict(zip(column_list, row)) for row in result_set]
        return ResponseResult(msg='查询批量补贴成功', code=1, data=data_list)

    def update_batch_subsidy(self, data_dict: dict, serializer:Type[ModelSerializer] = None):
        """
        修改批量补贴名单
        :param data_dict:
        :param serializer:
        :return:
        """
        result = self.orm.update_batch_btmd(data_dict).first()
        if not result:
            return ResponseResult(msg='修改批量补贴失败')
        result.__dict__.pop('_state')
        return ResponseResult(msg='修改批量补贴成功', code=1, data=result.__dict__)

    def exec_batch_subsidy(self, data_dict: dict, serializer: Type[ModelSerializer] = None):
        """
        执行批量补贴名单
        :param :
        :param :
        :return:
        """
        now_month = datetime.datetime.now().month
        # sbip = data_dict.get('sbip')
        # czy = data_dict.get('czy')
        result_set, column_list = self.orm.sel_batch_btmd_not_done()
        data_list = [dict(zip(column_list, row)) for row in result_set]
        if not data_list:
            return ResponseResult(msg='当前没有未执行批量补贴的名单')
        for obj in data_list:
            ygid = obj.get('ygid')
            ygdm = obj.get('ygdm')
            ygmc = obj.get('ygmc')
            btje = obj.get('btje')
            if btje >= 0:
                result = self.xfmx_orm.get_month_bt_gt_xfje_by_ygid(ygid=ygid, month=now_month)
                if result:
                    return ResponseResult("员工代码：" + ygdm + ygmc + "已经存在正数补贴,请检查当月补贴是否已经执行")
                else:
                    result = self.xfmx_orm.get_month_bt_lt_xfje_by_ygid(ygid=ygid, month=now_month)
                    if result:
                        return ResponseResult("员工代码：" + ygdm + ygmc + "已经存在负数补贴,请检查当月补贴是否已经执行")
            elif btje < 0:
                ye = self.xfmx_service.auto_calc_xfmx_ye(ygid=ygid, amount=abs(btje), xflx=2) #检查员工余额是否够扣款
                if ye < 0:
                    return ResponseResult("员工代码：" + ygdm + ygmc + "的余额扣减之后为负数。请检查数据是否正确")
        success_list = []
        error_list = []
        for exec in data_list:
            ygid = exec.get('ygid')
            # ygdm = exec.get('ygdm')
            # ygmc = exec.get('ygmc')
            btje = exec.get('btje')
            data = dict()
            ye = self.xfmx_service.auto_calc_xfmx_ye(ygid=ygid, amount=btje, xflx=6)  # 补贴后余额
            Etype = EC.BATCHSUBSIDY
            try:
                self.ygye_orm.update_ygye(ygid, ye)
            except Exception as e:
                traceback.print_exc()
                error_list.append({'ygid': ygid, "ye": ye})
            else:
                assert self.orm.update_batch_subsidy_status(ygid, now_month)
                success_list.append({'ygid': ygid, "ye": ye})
                data.update(ygid=ygid, xfje=btje, sjrq=getBeijinTime()[1], ye=ye, **data_dict, **Etype)
                assert self.xfmx_orm.add(data)
        return ResponseResult(msg='执行批量补贴成功', code=1, data={"success_list": success_list, "error_list": error_list})
