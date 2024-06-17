import requests
import os
from lxml import etree
import threading
import queue

"""
优化版主要处理三件事情：
    - 网络超时的页面，重新执行并覆盖
    - 封装代码
    - 优化效率，三个进程同时三个页面下载，注意需要维护一个全局变量，和一个队列
    
"""


# https://meirentu.cc/pic/130190390010.html

# https://meirentu.cc/pic/130190390010-1.html

class MySpider():
    def __init__(self, url):
        list1 = url.split(".")
        self.baseurl = url
        self.page = 1
        self.totle_page = 0
        self.num = (3 * self.page) - 1
        self.page_list = []
        self.url = list1[0] + '.' + list1[1] + f"-{self.page}." + list1[2]  # 首页的路径

    def get_text(self, url, headers):
        print("当前访问的页", url)
        res = requests.get(url=url, headers=headers).text
        return res

    def get_total_num(self, text):
        tree = etree.HTML(text=text)
        a_list = tree.xpath("//div[@class='page']/a")
        return len(a_list) - 1

    def get_title(self, text):
        tree = etree.HTML(text=text)
        title = tree.xpath("//div[@class='item_title']/h1/text()")[0]
        return title

    def get_img(self, page=None):
        if page == None:

            page = self.page_list.pop(0)
        else:
            page = page
        try:
            name = (3 * page) - 2
            list1 = self.baseurl.split(".")
            url = list1[0] + '.' + list1[1] + f"-{page}." + list1[2]  # 首页的路径
            text = requests.get(url=url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36", }).text
            tree = etree.HTML(text=text)
            src_list = tree.xpath("//div[@class='content_left']/div/img/@src")
            for src in src_list:
                content = requests.get(url=src, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
                    "Referer": url, }).content
                with open(self.title + f"/{name}.jpg", "wb") as f:
                    f.write(content)
                    print(f"{name}over!")
                name += 1
            return 1
        except:
            print(f"请求异常，重新执行第{page}页下载")
            self.get_img(page=page)

    def mkdir(self, title):
        try:
            os.mkdir(title)
        except:
            pass

    def initialize(self):  # 初始化
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        }
        text = self.get_text(url=self.url, headers=headers)
        if self.page == 1:
            self.title = self.get_title(text=text)
            self.totle_page = self.get_total_num(text=text)
            self.mkdir(title=self.title)

        for x in range(1, self.totle_page + 1):
            self.page_list.append(x)

        # print("text", text)
        # print("title", self.title)
        # print("totle_page", self.totle_page)
        # print("page_list", self.page_list)

    def run(self):
        self.initialize()
        # 创建三个线程来执行get_img方法
        # self.totle_page
        # self.get_img()
        # 创建一个线程队列
        thread_queue = queue.Queue()

        # 将所有要执行的页面加入队列
        for _ in range(self.totle_page):
            thread_queue.put(None)

        # 定义一个函数，用于执行 get_img 方法
        def execute_get_img():
            while not thread_queue.empty():
                self.get_img()

                # 从队列中取出一个页面，表示已经执行完毕
                thread_queue.get()

        # 创建三个线程并发执行 get_img 方法
        num_threads = 3
        threads = []

        for _ in range(num_threads):
            thread = threading.Thread(target=execute_get_img)
            threads.append(thread)
            thread.start()

        # 等待所有线程执行完毕
        for thread in threads:
            thread.join()

    # def run_function(self, func_name):
    #     target_func = globals().get(func_name)
    #     if not target_func or not callable(target_func):
    #         raise ValueError(f"这个函数/方法不存在")
    #     target_func()
    #     try:
    #         threading_list.pop(0)
    #         fin_counter += 1
    #     except:
    #         pass


if __name__ == '__main__':
    # url = "https://meirentu.cc/pic/130190390010.html "
    # list1 = url.split(".")
    # res = list1[0] + '.' + list1[1] + f"-{1}." + list1[2]
    # print(res)
    obj = MySpider(url="https://meirentu.cc/pic/130190390010.html")
    obj.run()
