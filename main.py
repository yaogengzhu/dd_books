import requests
import fake_useragent
import parsel
import json
import time


class DangDangSpider(object):
    def __init__(self):
        self.headers = {'User-Agent': fake_useragent.UserAgent().random}
        self.list = []

    def hand_data(self, url):
        html = requests.get(url=url, headers=self.headers).text
        selector = parsel.Selector(html)
        list = selector.css('.bang_list_mode li')

        for li in list:
          dict = {}
          dict['title'] = li.css('.name a::text').get()
          dict['desc'] = li.css('.pic a img::attr(title)').get()
          dict['author'] = li.css('.publisher_info a::text').get()
          dict['publisher_time'] = li.css('.publisher_info span::text')[0].get()
          dict['publisher'] = li.css('div:nth-child(6) a::text').get()
          dict['original_price'] = li.css('.price_n::text').get()
          dict['discount_price'] = li.css('.price_r::text').get()
          dict['img_url'] = li.css('.pic img::attr(src)').get()
          self.list.append(dict)

    def get_list(self):
        return self.list

if __name__ == '__main__':
    spider = DangDangSpider()
    for i in range(1, 26):
        page = i
        url = f'http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-month-2023-6-1-{page}'
        print(f'正在爬取第{page}页')
        spider.hand_data(url)
        time.sleep(5)

    list = spider.get_list()
    with open('dangdang.json', "w+") as f:
      json.dump(list, f, ensure_ascii=False, indent=4)
    print("数据写入完毕！")