# 约合刀功能
from nonebot import *
import os
import re

bot = get_bot()

PATH = os.path.abspath(os.path.join(os.getcwd(), 'plugins/data/together_hit/'))

@bot.on_message("group")
async def _(context):
    msg = context["message"]
    s_msg = str(msg)
    if s_msg == '约合刀' or s_msg == '取消约合刀' or s_msg == '约合刀列表' or s_msg == '开打' or s_msg[:4] == '代约合刀':
        group_id = context["group_id"]
        user_id = context["user_id"]
        nickname = ''

        if context['sender']['card'] == '':
            nickname = context['sender']['nickname']
        else:
            nickname = context['sender']['card']

        nickname = nickname.strip()

        user_list = []
        nickname_list = []

        # 读取对应群的文件
        try:
            f = open(os.path.join(PATH, str(group_id) + '.txt'), 'r')
            for line in f.readlines():
                line_split = line.strip().split(' ')
                user_list.append(line_split[0])
                nickname_list.append(line_split[1])
            f.close()
        except FileNotFoundError as e:
            print('当前群约合刀记录文件不存在')
            f = open(os.path.join(PATH, str(group_id) + '.txt'), 'w')
            f.close()

        
        if s_msg == '约合刀':
            print(user_list)
            print(nickname_list)
            if str(user_id) in user_list:
                await bot.send_msg(group_id=group_id, message='已经记录过了～')
            else:
                user_list.append(user_id)
                nickname_list.append(nickname)
                await bot.send_msg(group_id=group_id, message='已记录约合刀申请')
        
        if s_msg == '取消约合刀':
            if str(user_id) in user_list:
                user_list.remove(str(user_id))
                nickname_list.remove(nickname)
                await bot.send_msg(group_id=group_id, message='已经取消了')
            else:
                await bot.send_msg(group_id=group_id, message='没有申请过呢')
        
        if s_msg == '约合刀列表':
            if len(user_list) == 0:
                await bot.send_msg(group_id=group_id, message='没有人约合刀呢')
            else:
                ok_msg = '约合刀列表：\n'
                for i in nickname_list:
                    ok_msg = ok_msg + i + '\n'
                ok_msg = ok_msg + '目前有' + str(len(nickname_list)) + '个约合刀小伙伴'
                await bot.send_msg(group_id=group_id, message=ok_msg)
        
        if s_msg == '开打':
            if len(user_list) == 0:
                await bot.send_msg(group_id=group_id, message='没有人约合刀呢')
            else:
                ok_msg = '即将开始合刀，请大家做好准备～\n'
                for i in user_list:
                    ok_msg = ok_msg + '[CQ:at,qq=' + str(i) + ']\n'
                # ok_msg = ok_msg + '赶快去合刀吧～'

                await bot.send_msg(group_id=group_id, message=ok_msg)
                user_list.clear()
                nickname_list.clear()
        
        if s_msg[:4] == '代约合刀':
            pattern = re.compile(r'\d+')
            result = pattern.findall(s_msg)
            if result[0] in user_list:
                await bot.send_msg(group_id=group_id, message='已经记录过了～')
            else:
                user_list.append(result[0])
                nickname_list.append(result[0])
                await bot.send_msg(group_id=group_id, message='已记录代约合刀申请')
        
        # 处理完毕，清空并写入文件
        with open(os.path.join(PATH, str(group_id) + '.txt'), 'w') as f:
            for user_id, nickname in zip(user_list, nickname_list):
                f.write(str(user_id) + ' ' + nickname + '\n')