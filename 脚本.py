import requests
import os
from lxml import etree


class Func:
    def __init__(self):
        self.page = 25
        self.num = (3 * self.page) - 1  # 3page  1 1    2 4    3 7    4 10  3n-2
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36", }

    def run(self):
        for x in range(27):
            url = f"https://meirentu.cc/pic/183081755970-{self.page}.html"
            print("self.url", url)
            res = requests.get(url=url, headers=self.headers).text
            tree = etree.HTML(res)
            self.img_list = tree.xpath("//div[@class='content_left']/div/img/@src")
            self.title = tree.xpath("//div[@class='item_title']/h1/text()")[0]
            self.save_img(self.img_list, refer=url)
            self.page += 1
            print("selfpage", self.page)

    def save_img(self, src_list, refer):
        try:
            os.mkdir(self.title)
        except:
            # print("目录已存在")
            pass
        for src in src_list:
            header2 = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
                "Referer": refer,
            }
            print("src", src, header2)
            res = requests.get(url=src, headers=header2).content
            # print(f"{self.title}/{self.num}.jpg")
            with open(f"{self.title}/{self.num}.jpg", "wb") as f:
                f.write(res)
            self.num += 1


if __name__ == '__main__':
    obj = Func()
    obj.run()
