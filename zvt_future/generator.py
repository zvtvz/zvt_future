# -*- coding: utf-8 -*-
from zvt.contract import IntervalLevel

from zvt.generator import *

if __name__ == '__main__':
    gen_kdata_schema(pkg='zvt_future', providers=['joinquant'], entity_type='future',
                     levels=[IntervalLevel.LEVEL_1DAY])

    gen_exports('./domain')
    gen_exports('./recorders')
# the __all__ is generated
__all__ = []
