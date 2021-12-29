# coding=utf-8
# @File    : generateGistsList.py
# @Desc    : 爬取gist的内容，并存放在README.md中
# @Author  : Forgo7ten
# @Time    : 2021/11/22

import re
import time
import requests

gistUrl = "https://gist.github.com/Forgo7ten/public"
my_headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
}
partten = re.compile(
    r'<div class="d-inline-block px-lg-2 px-0">.*?<span>.*?<a data-hovercard-type.*?href="/Forgo7ten">Forgo7ten</a>.*?/ <a href="([/\w]+?)"><strong.*?class="css-truncate-target">(.+?)</strong></a>.*?<div class="color-fg-muted f6">.*?<span class="f6 color-fg-muted">(.*?)</span>.*?</div>'
)


def log(msg):
    with open("log.txt", "a+", encoding="utf-8") as logf:
        logf.write(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ": " + msg +
            "\n")


def add_info(f):
    info_txt = """定期爬取个人gist代码片段并同步到该文档 gist主页地址：[Forgo7ten’s gists (github.com) 点击访问](https://gist.github.com/Forgo7ten)



"""
    f.write(info_txt)


def get_gist_info(f):
    r = requests.get(gistUrl, headers=my_headers)
    gists = "fail"
    if 200 == r.status_code:
        gists = partten.findall(r.text.replace("\n", " "))
    return gists


def add_gist_info(f, gists):
    mdstr = """| gist名称 | gist描述 |
| ---- | ---- |
"""
    for g in gists:
        mdstr += f"| [{g[1].strip()}](https://gist.github.com{(g[0]).strip()}) | {g[2].strip()} |\n"
    f.write(mdstr)


def main():
    f = open("README.md", "w+", encoding="utf-8")
    add_info(f)
    gists = get_gist_info(f)
    if gists == "fail":
        log("fail!")
        f.write("Fail!\n")
    else:
        add_gist_info(f, gists)
        log("Success!")
    f.close


if __name__ == '__main__':
    main()
