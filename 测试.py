# import os
#
#
#
# os.makedirs("傻逼/脑残/六")


import requests

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",

    "Referer":"https://meirentu.me/pic/263283860370.html"
}


content = requests.get(url="https://cdn1.mmdb.cc/file/20220330/263283860370/0023391.jpg",headers=headers).content


with open("2.png","wb")as fp:
    fp.write(content)
