# 这个函数可以执行scrapy脚本
from scrapy.cmdline import execute

import sys
# 设置工程目录、
import os
# 获取main文件路径
print(os.path.abspath(__file__))
# 获取父目录
# print(os.path.dirname())
print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(["scrapy","crawl","jobbole"])