# -*- coding: utf-8 -*-
# @Time: 2022/4/30  17:50
# @Author: 2811755762@qq.com
"""
    Description:
    
"""

import requests
img = requests.get("https://img1.baidu.com/it/u=722430420,1974228945&fm=253&fmt=auto&app=138&f=JPEG?w=889&h=500", headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"})
print(img.content)
