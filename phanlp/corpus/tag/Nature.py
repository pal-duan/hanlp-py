# -*- coding: utf-8 -*-
# @Time: 2022/5/1  22:32
# @Author: 2811755762@qq.com
"""
    Description:
    
"""


class Nature:
    id_map = {}
    values = []

    def __init__(self, name: str):
        assert name not in self.id_map
        self.name = name
        self.ordinal = len(self.id_map)
        self.id_map[name] = self.ordinal
        self.values.append(self)

    @classmethod
    def from_string(cls, name: str):
        _id = cls.id_map.get(name, None)
        return None if _id is None else cls.values[_id]

    @classmethod
    def create(cls, name: str):
        nature = cls.from_string(name)
        if nature is None:
            return cls(name)
        return nature

    def startswith(self, prefix: str) -> bool:
        return self.name.startswith(prefix)

    def first_char(self) -> str:
        return self.name[0]

    def __str__(self):
        return self.name

    def ordinal(self) -> int:
        return self.ordinal


# 以下标签来自ICT
Nature.bg = Nature("bg")  # 区别语素
Nature.mg = Nature("mg")  # 数语素
Nature.nl = Nature("nl")  # 名词性惯用语
Nature.nx = Nature("nx")  # 字母专名
Nature.qg = Nature("qg")  # 量词语素
Nature.ud = Nature("ud")  # 助词
Nature.uj = Nature("uj")  # 助词
Nature.uz = Nature("uz")  # 着
Nature.ug = Nature("ug")  # 过
Nature.ul = Nature("ul")  # 连词
Nature.uv = Nature("uv")  # 连词
Nature.yg = Nature("yg")  # 语气语素
Nature.zg = Nature("zg")  # 状态词


# 以下标签来自北大
Nature.n = Nature("n")  # 名词
Nature.nr = Nature("nr")  # 人名
Nature.nrj = Nature("nrj")  # 日语人名
Nature.nrf = Nature("nrf")  # 音译人名
Nature.nr1 = Nature("nr1")  # 复姓
Nature.nr2 = Nature("nr2")  # 蒙古姓名
Nature.ns = Nature("ns")  # 地名
Nature.nsf = Nature("nsf")  # 音译地名
Nature.nt = Nature("nt")  # 机构团体名
Nature.ntc = Nature("ntc")  # 公司名
Nature.ntcf = Nature("ntcf")  # 工厂
Nature.ntcb = Nature("ntcb")  # 银行
Nature.ntch = Nature("ntch")  # 酒店宾馆
Nature.nto = Nature("nto")  # 政府机构
Nature.ntu = Nature("ntu")  # 大学
Nature.nts = Nature("nts")  # 中小学
Nature.nth = Nature("nth")  # 医院
Nature.nh = Nature("nh")  # 医药疾病等健康相关名词
Nature.nhm = Nature("nhm")  # 药品
Nature.nhd = Nature("nhd")  # 疾病
Nature.nn = Nature("nn")  # 工作相关名词
Nature.nnt = Nature("nnt")  # 职务职称
Nature.nnd = Nature("nnd")  # 职业
Nature.ng = Nature("ng")  # 名词性语素
Nature.nf = Nature("nf")  # 食品
Nature.ni = Nature("ni")  # 机构相关
Nature.nit = Nature("nit")  # 教育相关机构
Nature.nic = Nature("nic")  # 下属机构
Nature.nis = Nature("nis")  # 机构后缀
Nature.nm = Nature("nm")  # 物品名
Nature.nmc = Nature("nmc")  # 化学品名
Nature.nb = Nature("nb")  # 生物名
Nature.nba = Nature("nba")  # 动物名
Nature.nbc = Nature("nbc")  # 动物纲目
Nature.nbp = Nature("nbp")  # 植物名
Nature.nz = Nature("nz")  # 其他专名
Nature.g = Nature("g")  # 学术词汇
Nature.gm = Nature("gm")  # 数学相关词汇
Nature.gp = Nature("gp")  # 物理相关词汇
Nature.gc = Nature("gc")  # 化学相关词汇
Nature.gb = Nature("gb")  # 生物相关词汇
Nature.gbc = Nature("gbc")  # 生物类别
Nature.gg = Nature("gg")  # 地理地质相关词汇
Nature.gi = Nature("gi")  # 计算机相关词汇
Nature.j = Nature("j")  # 简称略语
Nature.i = Nature("i")  # 成语
Nature.l = Nature("l")  # 习用语
Nature.t = Nature("t")  # 时间词
Nature.tg = Nature("tg")  # 时间词性语素
Nature.s = Nature("s")  # 处所词
Nature.f = Nature("f")  # 方位词
Nature.v = Nature("v")  # 动词
Nature.vd = Nature("vd")  # 副动词
Nature.vn = Nature("vn")  # 名动词
Nature.vshi = Nature("vshi")  # 动词“是”
Nature.vyou = Nature("vyou")  # 动词“有”
Nature.vf = Nature("vf")  # 趋向动词
Nature.vx = Nature("vx")  # 形式动词
Nature.vi = Nature("vi")  # 不及物动词
Nature.vl = Nature("vl")  # 动词性惯用语
Nature.vg = Nature("vg")  # 动词性语素
Nature.a = Nature("a")  # 形容词
Nature.ad = Nature("ad")  # 副形词
Nature.an = Nature('an')  # 名形容词
Nature.ag = Nature("ag")  # 形容词性语素
Nature.al = Nature("al")  # 形容词性惯用语
Nature.b = Nature("b")  # 区别词
Nature.bl = Nature("bl")  # 区别词性惯用语
Nature.z = Nature("z")  # 状态词
Nature.r = Nature("r")  # 代词
Nature.rr = Nature("rr")  # 人称代词
Nature.rz = Nature("rz")  # 指示代词
Nature.rzt = Nature("rzt")  # 时间指示代词
Nature.rzs = Nature("rzs")  # 处所指示代词
Nature.rzv = Nature("rzv")  # 谓词性指示代词
Nature.ry = Nature("ry")  # 疑问代词
Nature.ryt = Nature("ryt")  # 时间疑问代词
Nature.rys = Nature("rys")  # 处所疑问代词
Nature.ryv = Nature("ryv")  # 谓词性疑问代词
Nature.rg = Nature("rg")  # 代词性语素
Nature.Rg = Nature("Rg")  # 古汉语代词性语素
Nature.m = Nature("m")  # 数词
Nature.mq = Nature("mq")  # 数量词
Nature.Mg = Nature("Mg")  # 甲乙丙丁类的数词
Nature.q = Nature("q")  # 量词
Nature.qv = Nature("qv")  # 动量词
Nature.qt = Nature("qt")  # 时量词
Nature.d = Nature("d")  # 副词
Nature.dg = Nature("dg")  # 辄，俱，复之类的副词
Nature.dl = Nature("dl")  # 连语
Nature.p = Nature("p")  # 介词
Nature.pba = Nature("pba")  # 介词“把"
Nature.pbei = Nature("pbei")  # 介词“被”
Nature.c = Nature("c")  # 连词
Nature.cc = Nature("cc")  # 并列连词
Nature.u = Nature("u")  # 助词
Nature.uzhe = Nature("uzhe")  # 着
Nature.ule = Nature("ule")  # 了  喽
Nature.uguo = Nature("uguo")  # 过
Nature.ude1 = Nature("ude1")  # 的  底
Nature.ude2 = Nature("ude2")  # 地
Nature.ude3 = Nature("ude3")  # 得
Nature.usuo = Nature("usuo")  # 所
Nature.udeng = Nature("udeng")  # 等  等等  云云
Nature.uyy = Nature("uyy")  # 一样  一般  似的  般
Nature.udh = Nature("udh")  # 的话
Nature.uls = Nature("uls")  # 来讲  来说  而言  说来
Nature.uzhi = Nature("uzhi")  # 之
Nature.ulian = Nature("ulian")  # 连
Nature.e = Nature("e")  # 叹词
Nature.y = Nature("y")  # 语气词
Nature.o = Nature("o")  # 拟声词
Nature.h = Nature("h")  # 前缀
Nature.k = Nature("k")  # 后缀
Nature.x = Nature("x")  # 字符串
Nature.xx = Nature("xx")  # 非语素字
Nature.xu = Nature("xu")  # 网址URL
Nature.w = Nature("w")  # 标点符号
Nature.wkz = Nature("wkz")  # 左括号
Nature.wky = Nature("wky")  # 右括号
Nature.wyz = Nature("wyz")  # 左引号
Nature.wyy = Nature("wyy")  # 右引号
Nature.wj = Nature("wj")  # 句号
Nature.ww = Nature("ww")  # 问号
Nature.wt = Nature("wt")  # 叹号
Nature.wd = Nature("wd")  # 逗号
Nature.wf = Nature("wf")  # 分号
Nature.wn = Nature("wn")  # 顿号
Nature.wm = Nature("wm")  # 冒号
Nature.ws = Nature("ws")  # 省略号
Nature.wp = Nature("wp")  # 破折号
Nature.wb = Nature("wb")  # 百分号  千分号
Nature.wh = Nature("wh")  # 单位符号
Nature.end = Nature("end")
Nature.begin = Nature("begin")


if __name__ == "__main__":
    pass
