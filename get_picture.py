import base64
import json
from nonebot import on_command, CommandSession
from urllib import request
import time

date = ''
total = 0

API = 'https://api.lolicon.app/setu/?apikey=xxxxxx&size1200=true'

@on_command('来一张色图', aliases=('来一张涩图', '来一份涩图', '来一份色图', '来一张瑟图', '来一份瑟图'), only_to_me=False)
async def _(session: CommandSession):
    global date
    global total
    
    if date != time.strftime("%a %b %d %Y", time.localtime()):
        date = time.strftime("%a %b %d %Y", time.localtime())
        total = 30

    if total == 0:
        msg = '今天看的图已经够多了，休息一下吧'
    else:
        response = request.urlopen(API)
        json_res = response.read().decode()
        json_data = json.loads(json_res)['data'][0]

        total = total - 1

        pid = json_data['pid']
        url = json_data['url']
        title = json_data['title']

        msg = url + '\n' + title + '\nid=' + str(pid) 

    await session.send(msg)


