# -*- coding:utf-8 -*-


"""
功能：
1、下载所有版本
2、下载指定版本的所有包

"""

from requests_html import HTMLSession
import requests
import time
import os


def save_binary(filename, content):
    """"""


def get_link_list(url):
    """获取页面所有链接的绝对路径"""

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    session = HTMLSession()
    r = session.get(url, headers=headers)

    # 获取页面上的所有链接的绝对路径。
    all_links = r.html.absolute_links
    # print(all_absolute_links)

    return list(all_links)



if __name__ == '__main__':

    url = "https://npm.taobao.org/mirrors/node-sass/v5.0.0"

    all_links = get_link_list(url)

    # 提取Windows、Linux版本的文件
    expected_link_list = [x for x in list(all_links) if (".node" in x and ('linux' in x or 'win32' in x))]
    print(expected_link_list)

    for link in expected_link_list:
        print(link)

        version = link.split("/")[-2]
        # print(version)

        # 判断版本是否存在
        version_path = "./node-sass/{}".format(version)

        if not os.path.exists(version_path):
            os.makedirs(version_path)
            print("成功创建目录：{}".format(version_path))

        binary_filename = link.split("/")[-1]

        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "referer": "https://npm.taobao.org/",
            "upgrade-insecure-requests": "1",
            "accept-language": "zh-CN,zh;q=0.9"
        }
        r = requests.get(link, headers)
        data = r.content

        filename = os.path.join(version_path, binary_filename)

        # 如果文件存在，跳出循环
        if os.path.exists(filename):
            continue

        # 写文件
        with open(filename, mode="wb") as f:
            f.write(data)

        print("成功创建文件：{}".format(filename))

        time.sleep(10)
