# -*- coding: utf-8 -*-
from sqlalchemy import Column, Float

from zvt.domain import KdataCommon


# 期货K线
class FutureKdataCommon(KdataCommon):
    # 持仓量
    interest = Column(Float)
    # 结算价
    settlement = Column(Float)
    # 涨跌幅(按收盘价)
    change_pct = Column(Float)
    # 涨跌幅(按结算价)
    change_pct1 = Column(Float)
