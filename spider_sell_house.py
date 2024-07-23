# -*- Coding = UTF-8 -*-
# Author: Nico
# File: spider_sell_house.py
# Software: PyCharm
# Time: 2024/5/12 21:52


import time
import parsel
import random
import requests
import pandas as pd

URL_LISTS = {
    '北京朝阳': 'https://bj.lianjia.com/ershoufang/chaoyang/pg'
}


class SpiderSellHouse:
    def __init__(self):
        self.sleep_time = random.randint(1, 3)
        self.excel_path = 'data_sell_house.xlsx'

    def spider_sell_house(self):
        data_list_sell_house = []
        for key, value in URL_LISTS.items():
            try:
                for page in range(1, 101):
                    print('-------------------------正在爬取{}第{}页售房数据-------------------------'.format(key, page))
                    time.sleep(self.sleep_time)
                    url = value + str(page)
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                      '(KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'
                    }
                    response = requests.get(url=url, headers=headers)
                    response.raise_for_status()
                    selector = parsel.Selector(response.text)
                    divs = selector.css('div.info.clear')
                    if not divs:
                        break
                    for div in divs:
                        area_list = div.css('.positionInfo a')
                        name = area_list[0].css('::text').get()
                        region = area_list[1].css('::text').get()
                        info = div.css('.houseInfo::text').get().split('|')
                        type_house = info[0]
                        area = info[1].replace('平米', '㎡')
                        face = info[2]
                        floor = info[4]
                        unit_price = div.css('.unitPrice span::text').get().replace('单价', '').replace('平', '㎡')
                        total_price = div.css('.totalPrice span::text').get() + '万'
                        href = div.css('.title a::attr(href)').get()
                        zone = key
                        data = {
                            'name': name,
                            'region': region,
                            'type_house': type_house,
                            'area': area,
                            'face': face,
                            'floor': floor,
                            'unit_price': unit_price,
                            'total_price': total_price,
                            'href': href,
                            'zone': zone
                        }
                        data_list_sell_house.append(data)
            except Exception as e:
                print('爬取失败：{}'.format(e))
        data_list_sell_house = pd.DataFrame(data_list_sell_house)
        data_list_sell_house.to_excel(self.excel_path, index=False)
        print('售房数据爬取完毕！')

    def run(self):
        self.spider_sell_house()


if __name__ == '__main__':
    SpiderSellHouse().run()
