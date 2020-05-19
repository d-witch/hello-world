import requests
from scrapy import Selector
import shelve
from peewee import *


id_url = 'https://172.16.72.172/security/manageRule/getRuleList?typeid={}&page={}'
detail_url = 'https://172.16.72.172/security/manageRule/getRuleDetail?id={}&typeid={}'
typeid = ['2', '3', '4', '8', '9', '10', '11', '12', '13', '14', '15', '18', '35', '36']
headers = {
    'Host': '172.16.72.172',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://172.16.72.172/security/manageRule',
    'Cookie': 'cavy_locale=zh_CN; top_menustatue_NSFOCUSWAF=1,4,0; PHPSESSID=f12784131357f47750c4fccf927f62c8',
    'Upgrade-Insecure-Requests': '1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}
db = MySQLDatabase('RuleDetail', host='127.0.0.1', port=3306, user='root', password='root')


class Detail(Model):
    # 规则名称
    name = CharField()
    # 规则ID
    rule_id = IntegerField()
    # 告警类型
    type = CharField()
    # 危险等级
    grade = CharField()
    # 准确度
    accuracy = CharField()
    # 操作系统
    os = CharField()
    # WEB服务器
    server = CharField()
    # 数据库
    db_name = CharField()
    # 编程语言
    lang = CharField()
    # 详细说明
    detail_description = TextField()

    class Meta:
        database = db


def get_page_count(html):
    sel = Selector(text=html)
    page_count = sel.xpath('//span[@id="div_pageCount"]/text()').extract()[0]
    return int(page_count)


def get_id_list(html):
    sel = Selector(text=html)
    id_list = sel.xpath('//table[@class="cmn_table"]/tr/td[1]/text()').extract()
    return id_list


def get_all_id():
    # -------获取所有id---------
    with shelve.open('type_id_dict') as f:

        for i in typeid:
            first_page = requests.get(url=id_url.format(i, 1), headers=headers, verify=False).text
            page_counts = get_page_count(first_page)
            one_type_id_list = []
            for j in range(1, page_counts+1):
                page = requests.get(url=id_url.format(i, j), headers=headers, verify=False).text
                one_type_id_list.extend((get_id_list(page)))
            f[i] = one_type_id_list


def get_detail(html):
    sel = Selector(text=html)
    d0 = sel.xpath(
        '//table[@class="cmn_table plumb"]/tr[position()<4 or position()>5 and position()<10]/td[2]/text()').extract()
    d1 = sel.xpath('//table[@class="cmn_table plumb"]/tr[position()=4 or position()=5]/td[2]/img/@title').extract()
    d2 = sel.xpath('//table[@class="cmn_table plumb"]/tr[10]/td/text()').extract()
    d2 = '\r\n'.join(d2)
    return [d0, d1, d2]


def get_all_rule_detail():
    with shelve.open('./crawl_data/type_id_dict') as f:
        for k in f.keys():
            for i in f[k]:
                # 爬取细节页
                detail_html = requests.get(detail_url.format(i, k), headers=headers, verify=False).text
                # 细节页面内提取具体数据
                one_detail = get_detail(detail_html)
                # 存入数据库
                Detail(name=one_detail[0][0],
                       rule_id=one_detail[0][1],
                       type=one_detail[0][2],
                       grade=one_detail[1][0],
                       accuracy=one_detail[1][1],
                       os=one_detail[0][3],
                       server=one_detail[0][4],
                       db_name=one_detail[0][5],
                       lang=one_detail[0][6],
                       detail_description=one_detail[2]).save()
