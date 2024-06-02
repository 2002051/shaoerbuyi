import requests
import os
from lxml import etree
url = "https://meirentu.me/s/%E9%99%86%E8%90%B1%E8%90%B1.html"
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43"
}
response = requests.get(url=url,headers=headers).text
tree = etree.HTML(response)
li_list = tree.xpath('//ul[@class="update_area_lists cl"]/li')
dir_name = "lxx图集"
try:
    os.mkdir(dir_name)
except:
    pass
for li in li_list:# 遍历每一个图集
    title = "".join(li.xpath('.//div[@class="meta-title"]//text()'))  #  图集标题
    detail_url = "https://meirentu.me" + li.xpath('./a/@href')[0]   # https://meirentu.me/pic/263283860370.html
    # f"{dir_name}/{title}"
    album_name = f"{dir_name}/{title}"    # 图集的路径。
    try:
        os.mkdir(album_name)   #  为当前图集创建文件夹
    except:
        print(f"{album_name}已经存在")

    detail_response = requests.get(url=detail_url,headers=headers).text
    detail_tree = etree.HTML(detail_response)
    page_list = detail_tree.xpath('//div[@class="page"]/a')[:-1]

    index = 1 # 图片索引

    for page in page_list:

        page_url = "https://meirentu.me" + page.xpath("./@href")[0]  # 当前图集的图片分页，每一页3-4张  , 需要重新定制请求头
        page_response = requests.get(url=page_url,headers=headers)
        page_tree = etree.HTML(page_response.text)

        page_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43",
            "Referer": page_url
        }


        img_src_list = page_tree.xpath('//div[@class="content_left"]//img/@src')  # 图片链接

        for img_src in img_src_list:
            # 遍历当前所有图片
            content = requests.get(url=img_src,headers=page_headers).content
            with open(f"{album_name}/{index}.jpg",'wb')as fp:
                fp.write(content)
            index += 1
            print("over！！！")



