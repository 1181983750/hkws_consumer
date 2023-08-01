import datetime
from enum import Enum


class ToBanlanceConstruction:
    """
    构造员工余额操作类型 与 操作名称
    """

    @classmethod
    def get_xflx(cls, e, fun=None):
        if fun:
            fun()
        return e

    @classmethod
    def get_xfmc(cls, e, fun=None):
        if fun:
            fun()
        return e

    @staticmethod
    def get_other_orm():
        return ''

RECHARGE: dict = {'xflx': ToBanlanceConstruction().get_xflx(1), 'xflxmc': ToBanlanceConstruction().get_xfmc('充值'), 'sfbt': 0}
"""1充值"""

DEDUCTION: dict = {'xflx': ToBanlanceConstruction().get_xflx(2), 'xflxmc': ToBanlanceConstruction().get_xfmc('消费'), 'sfbt': 0}
"""2消费"""

SUBSIDY: dict= {'xflx': ToBanlanceConstruction().get_xflx(3), 'xflxmc': ToBanlanceConstruction().get_xfmc('单人补贴'), 'sfbt': 1}
"""3单人补贴"""

REFUND: dict = {'xflx': ToBanlanceConstruction().get_xflx(4), 'xflxmc': ToBanlanceConstruction().get_xfmc('消费退款'),'sfbt': 0}
"""4消费退款"""

CASHREFUND: dict = {'xflx': ToBanlanceConstruction().get_xflx(5), 'xflxmc': ToBanlanceConstruction().get_xfmc('现金退款'),'sfbt': 0}
"""5现金退款"""

BATCHSUBSIDY: dict= {'xflx': ToBanlanceConstruction().get_xflx(6), 'xflxmc': ToBanlanceConstruction().get_xfmc('批量补贴'), 'sfbt': 1}
"""6批量补贴"""

        



