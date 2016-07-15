from myxl import *

datas = get_data('zhph.xls')
datas = [data[3].strip('\n').strip() for data in datas]

from collections import Counter
c = Counter(datas)
for k,v in c.items():
    print(k,v,sep='\t')
print(sum(c.values()))
