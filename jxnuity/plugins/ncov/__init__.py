# -*- coding: UTF-8 -*-
from nonebot import *
from . import wuhan

bot = get_bot()


@scheduler.scheduled_job('interval', seconds=3)
async def timer():
    await wuhan.find_page(bot)
