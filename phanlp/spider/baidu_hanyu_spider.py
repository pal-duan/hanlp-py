# -*- coding: utf-8 -*-
# @Time: 2022/6/22  22:28
# @Author: 2811755762@qq.com
"""
    Description:
        百度汉语同义词爬虫
"""
import requests
from lxml import etree
from fake_useragent import UserAgent
from utility.logger import logger


ua = UserAgent()


class BaiduHanyuSpider:
    base_url = "https://hanyu.baidu.com"

    @classmethod
    def search(cls, key):
        url = cls.base_url + f"/s?wd={key}"
        headers = {
            "user-agent": ua.random
        }
        try:
            response = requests.get(url, headers=headers)
            synonyms = cls.get_synonyms(response.text)
            logger.info(f"百度汉语中找到词语---{key}---的同义词{synonyms}")
        except Exception as e:
            logger.warning(f"百度汉语爬取字词---{key}---的同义词失败！detail: \n{e}")
            return []
        return synonyms

    @classmethod
    def get_synonyms(cls, response):
        tree = etree.HTML(response)
        a_list = tree.xpath('//*[@id="synonym"]/div/a/text()')
        synonyms = []
        if a_list:
            synonyms = [a.strip() for a in a_list]
        return set(synonyms)


if __name__ == "__main__":
    res = BaiduHanyuSpider.search("伟大")
    print(res)
