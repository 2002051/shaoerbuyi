import requests
import os
from lxml import etree
from requests.exceptions import Timeout
from concurrent.futures import ThreadPoolExecutor

url = "https://meirentu.me/s/%E9%98%BF%E6%9C%B1.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43"
}
response = requests.get(url=url, headers=headers).text
tree = etree.HTML(response)
li_list = tree.xpath('//ul[@class="update_area_lists cl"]/li')
dir_name = "阿朱图集"

try:
    os.mkdir(dir_name)
except FileExistsError:
    pass


def download_image(img_src, album_name, index, page_headers):
    try:
        content = requests.get(url=img_src, headers=page_headers, timeout=10).content
        print(img_src,page_headers)
        with open(f"{album_name}/{index}.jpg", 'wb') as fp:
            fp.write(content)
        print(f"Downloaded {index}.jpg")
    except Timeout:
        print(f"Timeout error occurred while downloading {index}.jpg. Retrying...")


def download_images_from_page(page_url, album_name, page_headers):
    try:
        page_response = requests.get(url=page_url, headers=headers)
        page_tree = etree.HTML(page_response.text)
        img_src_list = page_tree.xpath('//div[@class="content_left"]//img/@src')
        index = 1
        for img_src in img_src_list:
            download_image(img_src, album_name, index, page_headers)
            index += 1
    except:
        print("Error occurred while downloading images from page.")


def download_images_from_album(li):
    title = "".join(li.xpath('.//div[@class="meta-title"]//text()'))
    detail_url = "https://meirentu.me" + li.xpath('./a/@href')[0]
    album_name = f"{dir_name}/{title}"
    try:
        os.mkdir(album_name)
    except FileExistsError:
        print(f"{album_name} already exists.")

    detail_response = requests.get(url=detail_url, headers=headers).text
    detail_tree = etree.HTML(detail_response)
    page_list = detail_tree.xpath('//div[@class="page"]/a')[:-1]
    with ThreadPoolExecutor() as executor:
        for page in page_list:
            page_url = "https://meirentu.me" + page.xpath("./@href")[0]
            page_headers = {
                "User-Agent": headers["User-Agent"],
                "Referer": page_url
            }
            executor.submit(download_images_from_page, page_url, album_name, page_headers)


print("Downloading images...")
with ThreadPoolExecutor() as executor:
    for li in li_list:
        executor.submit(download_images_from_album, li)

print("All images downloaded successfully.")