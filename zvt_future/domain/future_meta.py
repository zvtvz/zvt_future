# -*- coding: utf-8 -*-
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declarative_base

from zvt.contract import EntityMixin
from zvt.contract.register import register_schema

FutureMetaBase = declarative_base()


class Future(EntityMixin, FutureMetaBase):
    __tablename__ = 'future'
    # 上市日
    list_date = Column(DateTime)
    # 退市日
    end_date = Column(DateTime)


register_schema(providers=['joinquant', 'exchange'], db_name='future_meta', schema_base=FutureMetaBase)

# the __all__ is generated
__all__ = ['Future']