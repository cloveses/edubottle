from mylib.myxltools.verify import verify_data_str,verify_data_int,verify_data_float


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
ncols = 4  #xls file's columns