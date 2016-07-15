#edubottle

注意：部署网站时，model.py中的sqlalchemy连接的数据库URL最好使用绝对路径。

检测数据正确性配置文件名命名方法：
使用项目的url_set.py,比如url为szcp,则实际命名为：
szcp_set.py。

完整配置实例如下：
# 以下为可用限制条件参数示例
# {
#     'length_min':3,
#     'length_max':6,
#     'min':0,
#     'max':100,
#     're_exp':r'[ab]',
#     'choices':['A','B'],
# }