# -*- coding: utf-8 -*-
import functools

from zvt import init_config

CHINA_FUTURE_CODE_MAP_NAME = {'cu': '铜',
                              'al': '铝',
                              'zn': '锌',
                              'pb': '铅',
                              'ni': '镍',
                              'sn': '锡',
                              'au': '黄金',
                              'ag': '白银',
                              'rb': '螺纹钢',
                              'wr': '线材',
                              'ss': '不锈钢',
                              'hc': '热轧卷板',
                              'sc': '原油',
                              'fu': '燃料油',
                              'lu': '低硫燃料油',
                              'bu': '石油沥青',
                              'ru': '天然橡胶',
                              'nr': '20号胶',
                              'sp': '纸浆'}


def get_future_name(code):
    simple_code = code[:-4]
    return "{}{}".format(CHINA_FUTURE_CODE_MAP_NAME[simple_code], code[-4:])


zvt_future_config = {}

int_zvt_future_config = functools.partial(init_config, pkg_name='zvt_future', current_config=zvt_future_config)

int_zvt_future_config()

# the __all__ is generated
__all__ = ['get_future_name', 'int_zvt_future_config']
