# -*- coding:utf-8 -*-


"""
功能：
http://npm.taobao.org/mirrors/chromedriver/

"""

import time
import os
import sys
from requests_html import HTMLSession
import requests


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

    url = "http://npm.taobao.org/mirrors/chromedriver/"

    all_links = get_link_list(url)
    # print(all_links)
    # 提取Windows、Linux版本的文件
    expected_link_list = [x for x in list(all_links) if ("LATEST_RELEASE" not in x and len(x) > 50)]
    # print(expected_link_list)

    for link in expected_link_list:
        print(link)

        version = link.split("/")[-2]
        # print(version)

        # 判断版本是否存在
        version_path = "./chromedriver/{}".format(version)
        # print("版本路径：{}".format(version_path))

        if not os.path.exists(version_path):
            os.makedirs(version_path)
            print("成功创建目录：{}".format(version_path))

        file_links = get_link_list(link)
        # 提取Windows、Linux版本的文件
        expected_file_link_list = [x for x in list(file_links) if (('linux64' in x or 'win32' in x))]
        print(expected_file_link_list)

        for file_link in expected_file_link_list:
            binary_filename = file_link.split("/")[-1]
            # print("文件名：{}".format(binary_filename))

            real_url = "https://cdn.npm.taobao.org/dist/chromedriver/{}/{}".format(version, binary_filename)
            print("文件真实路径：{}".format(real_url))

            s = requests.session()
            s.keep_alive = False
            r = s.get(real_url)
            data = r.content

            filename = os.path.join(version_path, binary_filename)
            # print("完整文件路径：{}".format(filename))
            # 如果文件存在，跳出循环
            if os.path.exists(filename):
                print("已存在文件：{}".format(filename))
                continue

            # 写文件
            with open(filename, "wb") as code:
                for chunk in r.iter_content(chunk_size=1024):  # 边下载边存硬盘
                    if chunk:
                        code.write(chunk)

            print("成功创建文件：{}".format(filename))

            time.sleep(30)
