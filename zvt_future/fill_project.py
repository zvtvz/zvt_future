# script to auto generate some files

from zvt.contract import IntervalLevel
from zvt.autocode.generator import gen_exports, gen_kdata_schema

if __name__ == '__main__':
    gen_kdata_schema(pkg='zvt_future', providers=['joinquant'], entity_type='future',
                 levels=[IntervalLevel.LEVEL_1DAY], adjust_types=[None])
    gen_exports(dir_path='.')
# the __all__ is generated
__all__ = []