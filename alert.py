# 向指定群内发送定时消息
from datetime import datetime
from nonebot import *

import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError

msg = '[CQ:image,file=file:////home/xxx/data/resources/xxx.jpg]'
GROUP_ID = 123456

@nonebot.scheduler.scheduled_job('cron', hour='0, 6, 12, 18')
async def _():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    
    try:
        await bot.send_group_msg(group_id=GROUP_ID,
                                 message=msg)
    except CQHttpError:
        pass

