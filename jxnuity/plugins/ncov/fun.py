# -*- coding: UTF-8 -*-
from os import path


# 群发信息
async def multi_send(bot, send):
    group_list = path.join(path.dirname(__file__), 'qun.txt')

    # 遍历群
    if not path.exists(group_list):
        return
    else:
        for i in send:
            with open(group_list, 'r') as n:
                for line in n.readlines():
                    line = line.strip()
                    qun = int(line)
                    msg = str(i)
                    # await bot.send_private_msg(646792290, msg, False)
                    await bot.send_group_msg(group_id=qun, message=msg, auto_escape=False)


