
import datetime
import threading
import traceback
from decimal import Decimal
from typing import Type, Union

from django.db import transaction
from rest_framework.serializers import ModelSerializer

from httpAsyncClient.hkws_xf_xfmx.HKWSXFMXORM import HKWSXFMXORM
from httpAsyncClient.hkws_xf_ygye.HKWSXFYGYEORM import HKWSXFYGYEORM
from httpAsyncClient.models import hkws_xf_xfmx, hkws_xf_ygye
from public.utils.BaseOrm import BaseService, DictToModel
from public.utils.InitModelErr import InitModelErr
from public.utils.onlineTime import getBeijinTime
from public.utils.response_result import ResponseResult


class HKWSXFMXServices(BaseService):
    def __init__(self, model: Type[hkws_xf_xfmx]):
        super(HKWSXFMXServices, self).__init__(model=model)
        self.orm = HKWSXFMXORM(model=model)
        self.ygye_orm = HKWSXFYGYEORM(model=hkws_xf_ygye)

    @transaction.atomic
    def auto_calc_xfmx_ye(self, ygid: Union[int, str], amount: Union[Decimal], xflx: int) -> Decimal:
        """
        通过传入员工id 消费或充值金额  操作类型1充值、3单补、4消费退款、6群补：加运算  2消费、5现金退款：减运算  计算当前余额
        :param ygid:
        :param xfje:
        :return: 当前余额
        """
        threading.Lock()
        query: hkws_xf_ygye = self.ygye_orm.get_ye_by_ygid(ygid)
        if not query.id:
            try:
                print('执行初始化创建 余额赋值为0', ygid)
                init_query: hkws_xf_ygye = self.ygye_orm.init_ye_by_ygid(ygid)
            except Exception as e:
                traceback.print_exc()
                raise InitModelErr(hkws_xf_ygye(), e)
            else:
                query = init_query
        if 1 <= xflx <= 6 and xflx != 2 and xflx != 5:
            ye = query.ye + amount  # 这里的query.ye是Decimal('999.8700')
        else:
            ye = query.ye - amount
        return ye

    def add_money(self, data_dict: dict, serializer: Type[ModelSerializer] = None):
        """
        充值金额
        :param data_dict: amount 必须是Decimal
        :param serializer: 可选
        :return: Dict
        """
        dict_to_model = DictToModel(dict_data=data_dict, model_class=hkws_xf_xfmx)
        hkws_xf_xfmx_model: hkws_xf_xfmx = dict_to_model.format_dict_data_to_model(get_model_obj=True)  # 将字典转模型
        """取出模型部分信息操作"""
        hkws_xf_xfmx_model.serialNo = data_dict.get('serialNo', None)
        hkws_xf_xfmx_model.xfje = data_dict['amount']
        """
        hkws_xf_xfmx_model.xflx = 1  # 1代表  消费类型为充值
        hkws_xf_xfmx_model.xflxmc = '充值'
        hkws_xf_xfmx_model.sbxh = 2  # 2代表  设备型号为消费机
        hkws_xf_xfmx_model.xfrq = data_dict.get('xfrq', None)
        hkws_xf_xfmx_model.bz = data_dict.get('bz', None)
        hkws_xf_xfmx_model.serialNo = data_dict.get('serialNo', None)
        hkws_xf_xfmx_model.sbip = data_dict['sbip']
        hkws_xf_xfmx_model.ygid = data_dict['ygid']
        hkws_xf_xfmx_model.ygdm= data_dict.get('ygdm', None)
        hkws_xf_xfmx_model.ygmc = data_dict.get('ygmc', None)
        hkws_xf_xfmx_model.nonce = data_dict['nonce']
        hkws_xf_xfmx_model.czy = data_dict.get('czy', '朱成聪')
        以上都无需手动获取 自动字典转模型 
        """
        # 自动计算更新所剩余额并保存
        result = self.auto_calc_xfmx_ye(ygid=data_dict['ygid'], amount=data_dict['amount'], xflx=data_dict['xflx'])
        hkws_xf_xfmx_model.ye = result
        sid = transaction.savepoint()  # 开启事务设置事务保存点 可以设置多个保存点
        try:
            hkws_xf_xfmx_model.sjrq = getBeijinTime()[1]
            self.orm.add(hkws_xf_xfmx_model)
        except Exception:
            traceback.print_exc()
            transaction.savepoint_rollback(sid)  # 失败回滚事务(如果数据库操作发生异常，回滚到设置的事务保存点)
            return ResponseResult(msg='充值失败', data={"ygid": data_dict['ygid'], "xfje": data_dict['amount']})
        else:
            # 乐观锁
            result_two = self.auto_calc_xfmx_ye(ygid=data_dict['ygid'], amount=data_dict['amount'],
                                            xflx=data_dict['xflx'])
            assert self.ygye_orm.update_ygye(ygid=data_dict['ygid'], ye=result)

            if result == result_two:
                transaction.savepoint_commit(sid)  # 如果没有异常，成功提交事物
            else:
                transaction.savepoint_rollback(sid)  # 失败回滚事务(如果数据库操作发生异常，回滚到设置的事务保存点)
                return ResponseResult(msg='充值失败,操作频繁', data={"ygid": data_dict['ygid'], "xfje": data_dict['amount']})
        return ResponseResult(msg='充值成功', data={"ygid": data_dict['ygid'], "xfje": data_dict['amount']}, code=1)

    def deduction_money(self, data_dict: dict, serializer: Type[ModelSerializer] = None):
        """
        扣款
        :param data_dict: amount 必须是Decimal  abs绝对值
        :param serializer: 可选
        :return: Dict
        """
        dict_to_model = DictToModel(dict_data=data_dict, model_class=hkws_xf_xfmx)
        hkws_xf_xfmx_model: hkws_xf_xfmx = dict_to_model.format_dict_data_to_model(get_model_obj=True)
        """取出模型部分信息操作"""
        hkws_xf_xfmx_model.serialNo = data_dict.get('serialNo', None)
        hkws_xf_xfmx_model.sbxh = data_dict.get('sbxh', None)  # 2代表  设备型号为消费机
        hkws_xf_xfmx_model.xfje = -data_dict['amount']  # 扣款金额 绝对值 +负号
        # 自动计算更新所剩余额并没有就新建员工保存
        result = self.auto_calc_xfmx_ye(ygid=data_dict['ygid'], amount=data_dict['amount'], xflx=data_dict['xflx'])
        hkws_xf_xfmx_model.ye = result
        sid = transaction.savepoint()  # 开启事务设置事务保存点 可以设置多个保存点
        if result < 0:
            return ResponseResult(msg='扣款失败,余额不足', data={"ygid": data_dict['ygid'], "xfje": data_dict['amount']})
        try:
            hkws_xf_xfmx_model.sjrq = getBeijinTime()[1]  # 事件日期
            self.orm.add(hkws_xf_xfmx_model)
        except Exception as e:
            traceback.print_exc()
            transaction.savepoint_rollback(sid)  # 失败回滚事务(如果数据库操作发生异常，回滚到设置的事务保存点)
            return ResponseResult(msg='扣款失败', data={"ygid": data_dict['ygid'], "xfje": data_dict['amount']})
        else:
            result_two = self.auto_calc_xfmx_ye(ygid=data_dict['ygid'], amount=data_dict['amount'],
                                                xflx=data_dict['xflx'])
            assert self.ygye_orm.update_ygye(ygid=data_dict['ygid'], ye=result)
            if result == result_two:
                transaction.savepoint_commit(sid)  # 如果没有异常，成功提交事物
            else:
                transaction.savepoint_rollback(sid)  # 失败回滚事务(如果数据库操作发生异常，回滚到设置的事务保存点)
                return ResponseResult(msg='扣款失败，操作频繁', data={"ygid": data_dict['ygid'], "xfje": data_dict['amount']})
        return ResponseResult(msg='扣费成功', data={"ygid": data_dict['ygid'], "xfje": data_dict['amount']}, code=1)

    def refund_money(self, data_dict: dict, serializer: Type[ModelSerializer] = None):
        """
        退款 包括离职现金退款和 直接退现金    5
        :param data_dict: amount 必须是Decimal
        :param serializer: 可选
        :return:
        """
        dict_to_model = DictToModel(dict_data=data_dict, model_class=hkws_xf_xfmx)
        hkws_xf_xfmx_model: hkws_xf_xfmx = dict_to_model.format_dict_data_to_model(get_model_obj=True)  # 将字典转模型
        """取出模型部分信息自动赋值操作"""
        hkws_xf_xfmx_model.serialNo = data_dict.get('serialNo', None)
        hkws_xf_xfmx_model.xfje = -data_dict['amount']  #退款金额 存负数
        # 自动计算更新所剩余额并没有就新建员工保存
        result = self.auto_calc_xfmx_ye(ygid=data_dict['ygid'], amount=data_dict['amount'], xflx=data_dict['xflx'])
        sid = transaction.savepoint()  # 开启事务设置事务保存点 可以设置多个保存点
        if result < 0:
            return ResponseResult(msg='退款失败,余额不足', data={"ygid": data_dict['ygid'], "xfje": data_dict['amount']})
        try:
            hkws_xf_xfmx_model.ye = result
            hkws_xf_xfmx_model.sjrq = getBeijinTime()[1]
            self.orm.add(hkws_xf_xfmx_model)
        except Exception as e:
            traceback.print_exc()
            transaction.savepoint_rollback(sid)  # 失败回滚事务(如果数据库操作发生异常，回滚到设置的事务保存点)
            return ResponseResult(msg='退款失败', data={"ygid": data_dict['ygid'], "xfje": data_dict['amount']})
        else:
            #乐观锁
            result_two = self.auto_calc_xfmx_ye(ygid=data_dict['ygid'], amount=data_dict['amount'],
                                                xflx=data_dict['xflx'])
            assert self.ygye_orm.update_ygye(ygid=data_dict['ygid'], ye=result)
            if result == result_two:
                transaction.savepoint_commit(sid)  # 如果没有异常，成功提交事物
            else:
                transaction.savepoint_rollback(sid)  # 失败回滚事务(如果数据库操作发生异常，回滚到设置的事务保存点
        return ResponseResult(msg='退款成功', data={"ygid": data_dict['ygid'], "xfje": data_dict['amount']},code=1)

    def subsidy_money(self, data_dict: dict, serializer: Type[ModelSerializer] = None):
        """
        员工补贴  sfbt1          3单人补贴
        :param data_dict:
        :param serializer: 可选
        :return:
        """
        now = datetime.date.today()
        # now_month_start = datetime.datetime(now.year, now.month, 1)
        # now_month_end = datetime.datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1]) #元组下标0返回 这个月第一天是星期几0-6
        if data_dict['amount'] > 0:
            # 查询当月是否有正数的补贴
            gt_btmx = self.orm.get_month_bt_gt_xfje_by_ygid(data_dict['ygid'],  now.month)
            if gt_btmx.count() > 0:
                return ResponseResult(msg="该员工本月已经存在正数补贴,请检查当月补贴是否已经执行")
        else:
            # 查询当月是否有负数的补贴
            lt_btmx = self.orm.get_month_bt_lt_xfje_by_ygid(data_dict['ygid'],  now.month)
            if lt_btmx.count() > 0:
                return ResponseResult(msg="该员工本月已经存在负数补贴,请检查当月补贴是否已经执行")
            # 如果不存在补贴 再计算下负数补贴后余额会不会是负数  此时amount为负数 ygye + -amount
            result = self.auto_calc_xfmx_ye(data_dict['ygid'], data_dict['amount'], xflx=data_dict['xflx'])
            if result < 0:
                return ResponseResult(msg="该员工的余额扣减之后为负数。请检查数据是否正确")
        """上面判断完后 取出模型进行保存"""
        dict_to_model = DictToModel(dict_data=data_dict, model_class=hkws_xf_xfmx)
        hkws_xf_xfmx_model: hkws_xf_xfmx = dict_to_model.format_dict_data_to_model(get_model_obj=True)  # 将字典转模型
        hkws_xf_xfmx_model.xfje = data_dict['amount']  #补贴金额 可能负数可能正
        # 自动计算更新所剩余额并没有就新建员工保存
        result = self.auto_calc_xfmx_ye(ygid=data_dict['ygid'], amount=data_dict['amount'], xflx=data_dict['xflx'])
        try:
            self.ygye_orm.update_ygye(ygid=data_dict['ygid'], ye=result)
        except Exception as e:
            traceback.print_exc()
            return ResponseResult(msg='补贴失败', data={"ygid": data_dict['ygid'], "xfje": data_dict['amount']})
        else:
            hkws_xf_xfmx_model.ye = result
            hkws_xf_xfmx_model.sjrq = getBeijinTime()[1]
            assert self.orm.add(hkws_xf_xfmx_model), '补贴明细添加异常'
        return ResponseResult(msg='补贴成功',code=1,data={"ygid": data_dict['ygid'], "xfje": data_dict['amount']})

    def get_xfmx(self, data_dict: dict, serializer: Type[ModelSerializer] = None):
        """
        员工消费明细查询 根据搜索条件 和日期范围 查询 消费明细
        :param data_dict: dateStart、dateEnd 必填  queryString可选
        :param serializer: 可选
        :return:
        """
        result_set, column_list = self.orm.get_xfmx_by_queryAndTime_Sql(data_dict['dateStart'], data_dict['dateEnd'], data_dict.get('queryString', None))
        data_list = [dict(zip(column_list, row)) for row in result_set]
        # query = self.orm.get_xfmx_by_dateTime(data_dict['dateStart'],data_dict['dateEnd'])
        # query_ser = serializer(query, many=True)
        return ResponseResult(msg='查询成功',code=1,data=data_list)

    def get_czmx(self, data_dict: dict, serializer: Type[ModelSerializer] = None):
        """
        员工充值明细查询 据搜索条件 和日期范围 查询 充值明细 1
        :param data_dict: dateStart、dateEnd 必填 queryString可选
        :param serializer: 可选
        :return:
        """
        result_set, column_list = self.orm.get_czmx_by_queryAndTime_Sql(data_dict['dateStart'], data_dict['dateEnd'],
                                                                        data_dict.get('queryString', None))
        data_list = [dict(zip(column_list, row)) for row in result_set]
        return ResponseResult(msg='查询成功', code=1, data=data_list)

    def get_tkmx(self, data_dict: dict, serializer: Type[ModelSerializer] = None):
        """
        员工根据搜索条件 和日期范围 查询 退款明细  4 or 5
        :param data_dict: dateStart、dateEnd 必填 queryString可选
        :param serializer: 可选
        :return:
        """
        result_set, column_list = self.orm.get_tkmx_by_queryAndTime_Sql(data_dict['dateStart'], data_dict['dateEnd'],
                                                                        data_dict.get('queryString', None))
        data_list = [dict(zip(column_list, row)) for row in result_set]
        return ResponseResult(msg='查询成功', code=1, data=data_list)

    def get_btmx(self, data_dict: dict, serializer: Type[ModelSerializer] = None):
        """
        员工根据搜索条件 和日期范围 查询 批量补贴 明细
        :param data_dict: dateStart、dateEnd 必填 queryString可选
        :param serializer:
        :return:
        """
        result_set, column_list = self.orm.get_batch_btmx_by_queryAndTime_Sql(data_dict['dateStart'], data_dict['dateEnd'],
                                                                        data_dict.get('queryString', None))
        data_list = [dict(zip(column_list, row)) for row in result_set]
        return ResponseResult(msg='查询成功', code=1, data=data_list)

    def get_single_btmx(self, data_dict: dict, serializer: Type[ModelSerializer] = None):
        """
        员工根据搜索条件 和日期范围 查询 单一补贴 明细
        :param data_dict: dateStart、dateEnd 必填 queryString可选
        :param serializer:
        :return:
        """
        result_set, column_list = self.orm.get_single_btmx_by_queryAndTime_Sql(data_dict['dateStart'], data_dict['dateEnd'],
                                                                        data_dict.get('queryString', None))
        data_list = [dict(zip(column_list, row)) for row in result_set]
        return ResponseResult(msg='查询成功', code=1, data=data_list)

    def get_all_btmx(self, data_dict: dict, serializer: Type[ModelSerializer] = None):
        """
        员工根据搜索条件 和日期范围 查询 全部补贴 明细   单一 or 批量
        :param data_dict: dateStart、dateEnd 必填 queryString可选
        :param serializer:
        :return:
        """
        result_set, column_list = self.orm.get_all_btmx_by_queryAndTime_Sql(data_dict['dateStart'], data_dict['dateEnd'],
                                                                        data_dict.get('queryString', None))
        data_list = [dict(zip(column_list, row)) for row in result_set]
        return ResponseResult(msg='查询成功', code=1, data=data_list)

    def get_all_mx(self, data_dict: dict, serializer: Type[ModelSerializer] = None):
        """
        员工根据搜索条件 和日期范围 查询 所有明细
        :param data_dict: dateStart、dateEnd 必填 queryString可选
        :param serializer:
        :return:
        """
        result_set, column_list = self.orm.get_all_mx_by_queryAndTime_Sql(data_dict['dateStart'], data_dict['dateEnd'],
                                                                        data_dict.get('queryString', None))
        data_list = [dict(zip(column_list, row)) for row in result_set]
        return ResponseResult(msg='查询成功', code=1, data=data_list)

    def get_everyday_czmx_count(self, data_dict: dict, serializer: Type[ModelSerializer] = None):
        """
        根据日期范围 查询 获取 每日 充值 统计 情况
        :param data_dict: dateStart、dateEnd 默认今天 queryString可选
        :param serializer:
        :return:
        """
        result_set, column_list = self.orm.get_everyday_czmx_count_Time_Sql(data_dict['dateStart'], data_dict['dateEnd'],
                                                                        data_dict.get('queryString', None))
        data_list = [dict(zip(column_list, row)) for row in result_set]
        return ResponseResult(msg='查询成功', code=1, data=data_list)