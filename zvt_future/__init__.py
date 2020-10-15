# -*- coding: utf-8 -*-
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


# the __all__ is generated
__all__ = []

# __init__.py structure:
# common code of the package
# export interface in __all__ which contains __all__ of its sub modules

# import all from submodule recorders
from .recorders import *
from .recorders import __all__ as _recorders_all

__all__ += _recorders_all
