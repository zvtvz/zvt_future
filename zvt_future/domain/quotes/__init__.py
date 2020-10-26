# -*- coding: utf-8 -*-
from sqlalchemy import Column, Float

from zvt.domain import KdataCommon


# future common kdata
class FutureKdataCommon(KdataCommon):
    # 持仓量
    interest = Column(Float)
    # 结算价
    settlement = Column(Float)
    # 涨跌幅(按收盘价)
    change_pct = Column(Float)
    # 涨跌幅(按结算价)
    change_pct1 = Column(Float)
# the __all__ is generated
__all__ = ['FutureKdataCommon']

# __init__.py structure:
# common code of the package
# export interface in __all__ which contains __all__ of its sub modules

# import all from submodule future_1d_kdata
from .future_1d_kdata import *
from .future_1d_kdata import __all__ as _future_1d_kdata_all
__all__ += _future_1d_kdata_all