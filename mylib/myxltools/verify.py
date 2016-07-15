import re
import os
from .myxl import *


# 以下为可用限制条件参数示例
# {
#     'length_min':3,
#     'length_max':6,
#     'min':0,
#     'max':100,
#     're_exp':r'[ab]',
#     'choices':['A','B'],
# }

def verify_data_int(data,cols_limits=None):
    info = ""
    if not isinstance(data,float):
        info = "此数据类型不符合要求"
        return info
    if cols_limits is None:
        cols_limits = {}
    data = int(data)
    if cols_limits:
        if 'min' in cols_limits:
            if data < cols_limits['min']:
                info = "此数据不得小于%d" % cols_limits['min']
                return info
        if 'max' in cols_limits:
            if data > cols_limits['max']:
                info = "此数据不得大于%d" % cols_limits['max']
                return info
    return info

def verify_data_float(data,cols_limits=None):
    info = ""
    if not isinstance(data,float):
        info = "此数据类型不符合要求"
        return info
    if cols_limits is None:
        cols_limits = {}
    if cols_limits:
        if 'min' in cols_limits:
            if data < cols_limits['min']:
                info = "此数据不得小于%f" % cols_limits['min']
                return info
        if 'max' in cols_limits:
            if data > cols_limits['max']:
                info = "此数据不得大于%f" % cols_limits['max']
                return info
    return info

def verify_data_str(data,cols_limits=None):
    info = ""
    if not isinstance(data,str):
        info = "此数据类型不符合要求"
        return info
    if cols_limits is None:
        cols_limits = {}
    if cols_limits:
        if 'length_min' in cols_limits:
            if len(data) < cols_limits['length_min']:
                info = "此字符串长度不得小于%d" % cols_limits['length_min']
                return info
        if 'length_max' in cols_limits:
            if len(data) > cols_limits['length_max']:
                info = "此字符串长度不得大于%d" % cols_limits['length_max']
                return info
        if 'choices' in cols_limits:
            if data not in cols_limits['choices']:
                info = "此字符串不是候选数据"
                return info
        if 're_exp' in cols_limits:
            if not re.search(cols_limits['re_exp'],data):
                info = "此字符串模式不符合要求"
                return info
    return info

def verify_file(filename,filters,limits,ncols):
    """
    filters 每列过滤方法列表
    limits  每列限制条件字典
    ncols   总列数
    """
    info = ""
    if not os.path.exists(filename):
        info = '文件不存在！\n'
        return info
    datass = get_data_cols(filename)
    if len(datass) != ncols:
        info = "表格列数不符合要求！\n"
        print(info)
        return info
    for ncol,(datas,fun,limit) in enumerate(zip(datass,filters,limits)):
        for nrow,data in enumerate(datas):
            cell_info = fun(data,limit)
            if cell_info:
                pos_info = "行:%d 列:%d:" % (nrow + 1,ncol + 1)
                info += ' '.join((pos_info,cell_info,'\n'))
    print(info)
    return info

if __name__ == "__main__":
    cols_A = {
        'min':0,
        'max':100,
    }

    cols_B = {
        'length_min':4,
        'length_max':8,
        're_exp':r'[ab]',
    }

    cols_C = {
        'length_min':4,
        're_exp':r'[ab]',
        'choices':['dkdakk','dddkb'],
    }

    cols_D = {
        'min':0,
        'max':100,
    }
    limits = [cols_A,cols_B,cols_C,cols_D]
    filters = [verify_data_int,verify_data_str,verify_data_str,verify_data_float]
    print(verify_data_int(3,cols_A))
    print(verify_data_int(-3,cols_A))
    print(verify_data_int(300,cols_A))
    print(verify_data_float(3.0,cols_D))
    print(verify_data_int(-3.0,cols_D))
    print(verify_data_int(300.0,cols_D))
    print(verify_data_str('hdah',cols_B))
    print(verify_data_str('ah',cols_B))
    print(verify_data_str('dsffgefeeeeeddah',cols_B))
    print(verify_data_str('hdkyuh',cols_B))
    print(verify_data_str('dddkb',cols_C))
    print(verify_data_str('dfdddkb',cols_C))
    datass = [[3.0,-3.0,30.0],['hdah','dda','kdkdddjdda',],['dddkb','dddkb','abcdd',],[4.5,35.6,300.0]]
    for i,(datas,fun,limit) in enumerate(zip(datass,filters,limits)):
        for j,data in enumerate(datas):
            info = fun(data,limit)
            if info:
                print((j+1,i+1),data,info)
    print('\n测试文件开始：')
    verify_file('tst.xls',filters,limits,4)
