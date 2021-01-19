# -- coding: utf-8 --
from faker import Faker
from enum import Enum
import json


class Func(Enum):
    ADDRESS = "地址"
    LATITUDE = "地址坐标"
    COUNTRY = "国家"
    PROVINCE = "省份"
    CITY = "市县"
    DISTRICT = "区"
    STREET_SUFFIX = "街"
    COMPANY = "公司"
    SSN = "身份证号"
    JOB = "职位"
    NAME = "姓名"
    PHONE_NUMBER = "手机号"
    EMAIL = "邮箱"
    IPV4 = "IP地址"
    URL = "URL地址"
    FILE_NAME = "文件名"
    WORD = "单词"
    WORDS = "字符串"
    SENTENCE = "一句话"
    TEXT = "一篇文章"
    BOOLEAN = "布尔类型"
    MD5 = "MD5"
    PASSWORD = "密码"
    UUID4 = "UUID"
    DATE_TIME = "日期"
    FUTURE_DATETIME = "未来日期"
    PAST_DATETIME = "过去日期"
    UNIX_TIME = "时间戳"
    RANDOM_NUMBER = "Int数字"
    RANDOM_DIGIT_NOT_NULL = "个位数字"
    PYINT = "0~9999数字"
    THREE_NUM = "三位数"
    PROFILE = "JSON"
    SIMPLE_PROFILE = "简单JSON"
    BANK_CARD = "银行卡"
    HEX_COLOR = "HEX颜色"
    NONE = "不设置"


class RandomInfo(Faker):
    def __init__(self, locale="zh-CN"):
        super().__init__(locale=locale)
        self.random_dict = {Func.ADDRESS.value: self.address, Func.COUNTRY.value: self.country,
                            Func.PROVINCE.value: self.province, Func.CITY.value: self.city,
                            Func.DISTRICT.value: self.district, Func.STREET_SUFFIX.value: self.street_suffix,
                            Func.SSN.value: self.ssn, Func.JOB.value: self.job, Func.COMPANY.value: self.company,
                            Func.NAME.value: self.name, Func.PHONE_NUMBER.value: self.phone_number,
                            Func.EMAIL.value: self.email, Func.IPV4.value: self.ipv4,
                            Func.HEX_COLOR.value: self.hex_color, Func.LATITUDE.value: self.latitude,
                            Func.URL.value: self.url, Func.FILE_NAME.value: self.file_name,
                            Func.WORDS.value: self.words,
                            Func.WORD.value: self.word, Func.TEXT.value: self.text, Func.SENTENCE.value: self.sentence,
                            Func.BOOLEAN.value: self.boolean, Func.MD5.value: self.md5,
                            Func.PASSWORD.value: self.password, Func.UUID4.value: self.uuid4,
                            Func.DATE_TIME.value: self.date_time, Func.FUTURE_DATETIME.value: self.future_datetime,
                            Func.PAST_DATETIME.value: self.past_datetime, Func.UNIX_TIME.value: self.unix_time,
                            Func.RANDOM_NUMBER.value: self.random_number, Func.THREE_NUM.value: self.numerify,
                            Func.RANDOM_DIGIT_NOT_NULL.value: self.random_digit_not_null, Func.PYINT.value: self.pyint,
                            Func.PROFILE.value: self.profile, Func.SIMPLE_PROFILE.value: self.simple_profile,
                            Func.BANK_CARD.value: self.credit_card_number,
                            Func.NONE.value: None}

    def insert_data(self, data, count, table, mapper):
        param = "("
        value = ""
        last = list(self.random_dict.keys())[self.random_dict.__len__() - 1]
        for i in data:
            if last == i[1]:
                continue
            param += i[0] + ","
        for j in range(count):
            value += "("
            for i in data:
                if last == i[1]:
                    continue
                b = i[2] == "int" or i[2] == "tinyint"
                if self.random_dict.get(i[1]) is None:
                    s = i[1]
                else:
                    func = self.random_dict.get(i[1])
                    if i[2].lower().find("json") != -1:
                        d = dict(func())
                        if d.get("birthdate") is not None:
                            d["birthdate"] = str(d["birthdate"])
                        s = json.dumps(d, ensure_ascii=False)
                    else:
                        s = str(func())
                if b:
                    value += s + ","
                else:
                    value += "\'" + s.replace("\'", "\"") + "\',"
            value = value[0: value.__len__() - 1] + "),"
        param = param[0: len(param) - 1] + ")"
        value = value[0: value.__len__() - 1]
        mapper.insert_data(param, value, table)


if __name__ == '__main__':
    f = RandomInfo("zh-CN")
    print(f.random_dict.get(Func.CITY.value)())
