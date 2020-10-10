from zvt.contract import IntervalLevel
from zvt.utils.kdata_utils import gen_kdata_schema

if __name__ == '__main__':
    gen_kdata_schema(pkg='zvt_future', providers=['joinquant'], entity_type='future',
                     levels=[IntervalLevel.LEVEL_1DAY])
