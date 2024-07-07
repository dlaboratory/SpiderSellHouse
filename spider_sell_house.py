# -*- Coding = UTF-8 -*-
# Author: Nico
# File: spider_sell_house.py
# Software: PyCharm
# Time: 2024/1/26 14:03

import csv
import time
import parsel
import requests

# 打开CSV文件，设置编码和换行符
f = open('Data.csv', mode='a', encoding='utf-8-sig', newline='')
# 创建CSV写入对象
csv_write = csv.DictWriter(f, fieldnames=['标题', '地址', '户型', '面积', '朝向', '装修', '楼层', '年代', '关注及发布', '其它', '总价', '单价', '详情'])
# 写入CSV表头
csv_write.writeheader()

# 循环爬取1到100页的数据
for page in range(1, 101):
    # 打印当前爬取页数
    print(f'-------------------------正在爬取第{page}页数据内容-------------------------')
    # 适当休眠，防止请求过快
    time.sleep(1)
    # 构建请求的URL
    url = f'https://bj.lianjia.com/ershoufang/chaoyang/pg{page}/'
    # 设置请求头信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}
    # 发送请求，获取响应
    response = requests.get(url=url, headers=headers)
    # 使用parsel解析响应内容
    selector = parsel.Selector(response.text)
    # 从每个房源的信息块中提取数据
    divs = selector.css('div.info.clear')
    for div in divs:
        # 提取房源信息
        title = div.css('.title a::text').get()
        area_list = div.css('.positionInfo a::text').getall()
        area = '-'.join(area_list)
        house_info = div.css('.houseInfo::text').get().split('|')
        house_type = house_info[0]
        house_area = house_info[1]
        house_face = house_info[2]
        decoration = house_info[3]
        floor = house_info[4]
        years = house_info[5]
        follow_info = div.css('.followInfo::text').get().replace(' / ', ',')
        tag_list = div.css('.tag span::text').getall()
        tag = '|'.join(tag_list)
        totalprice = div.css('.totalPrice span::text').get() + '万'
        unitprice = div.css('.unitPrice span::text').get().replace('单价', '')
        href = div.css('.title a::attr(href)').get()
        # 构建字典存储房源信息
        dit = {
            '标题': title,
            '地址': area,
            '户型': house_type,
            '面积': house_area,
            '朝向': house_face,
            '装修': decoration,
            '楼层': floor,
            '年代': years,
            '关注及发布': follow_info,
            '其它': tag,
            '总价': totalprice,
            '单价': unitprice,
            '详情': href,
        }
        # 将数据写入CSV文件
        csv_write.writerow(dit)
        # 打印房源信息
        print(title, area, house_type, house_area, house_face, decoration, floor, years, follow_info, tag, totalprice, unitprice, href, sep='|')
# 关闭CSV文件
f.close()
print('爬取完毕！')
