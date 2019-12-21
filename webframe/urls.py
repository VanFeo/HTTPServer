"""
路由选择模块
"""
from views import *

urls = [
    # 如果访问'/time'路径,有数据
    # 用show_time方法提供
    ("/time", show_time),
    ("/hello", hello),
    ("/bye", bye)
]
