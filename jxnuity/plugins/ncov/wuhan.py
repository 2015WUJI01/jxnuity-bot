# -*- coding: utf-8 -*-
import requests
import json
import time
from os import path

from . import fun


async def find_page(bot):
    # 获取丁香园数据
    url = "https://3g.dxy.cn/newh5/view/pneumonia"
    page = requests.get(url)
    page.encoding = "utf-8"
    page = page.text

    json1 = page[page.find('window.getTimelineService'):]
    json1 = json1.split("\n")[0]
    json1 = json1[json1.find("{") + 1:json1.find(r'catch(e){}</script><script') - 3]

    news_list = json1.split("},{")  # 将json数据整理为list
    news_list.reverse()  # 反向list 使得旧数据优先处理

    title_list = []
    msg_list = []

    # 保存数据
    db_file = path.join(path.dirname(__file__), 'db.txt')
    with open(db_file, "w") as f:
        f.write("\n".join(news_list))

    # 分析数据
    for i in news_list:
        i = "{" + i + "}"
        news = json.loads(i, strict=False)
        # print(news["pubDateStr"],
        #       news["title"],
        #       news["summary"],
        #       news["infoSource"],
        #       news["sourceUrl"])
        title_list.append(str(news["id"]))
        msg_list.append(news)
    # print(title_list)
    send_title = []
    title_path = path.join(path.dirname(__file__), 'title.txt')
    if path.exists(title_path):
        with open(title_path, "r") as f:
            lines = f.readlines()
            for ii in title_list:
                sent = 0
                for i in lines:
                    i = i.strip()
                    if i == ii:
                        sent = 1
                        break
                if sent == 0:
                    send_title.append(ii)
    else:
        with open(title_path, "w") as f:
            f.write("\n".join(title_list))
    # print(send_title)
    send_msg = []
    if send_title:
        print(send_title)
        for i in send_title:
            for ii in msg_list:
                if str(ii["id"]) == i:
                    send = ""
                    # send += "(" + ii["pubDateStr"] + ")\n"
                    send += '【' + ii["title"] + "】\n"
                    send += "" + ii["summary"] + "\n"
                    send += "消息来源：" + ii["infoSource"] + " " + ii["sourceUrl"] + "\n"
                    send += "发布于" + timestamp(ii["createTime"]) + ""
                    send_msg.append(send)
        if send_msg:
            await fun.multi_send(bot, send_msg)
            with open(title_path, "w") as f:
                f.write("\n".join(title_list))


# 输入毫秒级的时间，转出正常格式的时间
def timestamp(time_num):
    time_stamp = float(time_num/1000)
    time_array = time.localtime(time_stamp)
    return time.strftime("%m-%d %H:%M:%S", time_array)
