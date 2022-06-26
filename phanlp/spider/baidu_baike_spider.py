# -*- coding: utf-8 -*-
# @Time: 2022/6/22  22:28
# @Author: 2811755762@qq.com
"""
    Description:
        百度百科同义词爬虫
"""
import requests
import re
from lxml import etree
from fake_useragent import UserAgent
from utility.logger import logger


ua = UserAgent()


class BaiduBaikeSpider:
    base_url = "https://baike.baidu.com"

    @classmethod
    def search(cls, key):
        url = cls.base_url + f"/item/{key}"
        headers = {
            "user-agent": ua.random
        }
        try:
            response = requests.get(url, headers=headers)
            synonyms = cls.get_synonyms(response.text)
            logger.info(f"百度汉语中找到词语---{key}---的同义词{synonyms}")
        except Exception as e:
            logger.warning(f"百度百科爬取字词---{key}---的同义词失败！detail: \n{e}")
            return []
        return synonyms

    @classmethod
    def get_synonyms(cls, data):
        tree = etree.HTML(data)
        flag = tree.xpath("/html/body/div[3]/div[2]/div/div[1]/ul/li[1]/div/a/@href")
        headers = {
            "user-agent": ua.random
        }
        if flag:
            url = cls.base_url + flag[0]
            data = requests.get(url, headers=headers).text
            tree = etree.HTML(data)
        item_json = dict()
        des_dict = cls.get_description(tree)
        item_json.update(des_dict)

        info_box_dict = cls.get_info_box(tree)
        item_json.update(info_box_dict)

        synonym_list = cls.parse_synonym(item_json)
        return synonym_list

    @staticmethod
    def get_description(tree):
        new_dict = {}
        desc_label = tree.xpath('/html/head/meta[@name="description"]/@content')
        new_dict['description'] = desc_label[0] if desc_label else ""
        return new_dict

    @staticmethod
    def get_info_box(tree):
        new_dict = dict()
        base_info = tree.xpath('/html/body/div[3]/div[2]/div/div[1]/div[8]')
        if base_info is not None:
            all_name = [ele.text.strip().replace(u'\xa0', '') for ele in base_info[0].xpath('dl/dt')]
            all_value = [re.sub(r"[\n\[\]\d\xa0]", "", ele.xpath('string(.)').strip()) for ele in
                         base_info[0].xpath('dl/dd')]
            if len(all_name) != len(all_value):
                logger.warning(f"{all_name}和{all_value}数量不等！！！")
                return new_dict
            new_dict = dict(zip(all_name, all_value))
        return new_dict

    @staticmethod
    def seg(text):
        segment = [',', '，', '、', '；']
        current_seg = '&&'
        for seg in segment:
            if seg in text:
                current_seg = seg

        return text.split(current_seg)

    @staticmethod
    def re_match(word, text):
        p_str = r'{a}(.+?)[，。）\s)（(、]'.format(a=word)
        pattern = re.compile(p_str)
        result = re.findall(pattern, text)
        return result

    @classmethod
    def parse_synonym(cls, item_json):
        info_key = ['中文名', '别名', '别称', '英文名称', '又称', '英文别名']
        pattern_list = ['俗称', '简称', '又称']

        info_set = set()
        for key in info_key:
            if key in item_json:
                value = item_json[key]
                if value[-1] == '等':
                    value = value[:-1]
                value = cls.seg(value)
                info_set = info_set | set(value)

        description = item_json['description']
        for p in pattern_list:
            pattern = r'' + p
            result = cls.re_match(pattern, description)
            for r in result:
                value = cls.seg(r)
                info_set = info_set | set(value)

        info_set = [s.strip().replace(u'\xa0', '').replace('"', '').replace('“', '').replace('”', '').
                    replace('（', '').replace('：', '') for s in info_set]
        return info_set


if __name__ == "__main__":
    res = BaiduBaikeSpider.search("凤梨")
    print(res)
