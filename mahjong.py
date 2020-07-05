# 约麻将功能
from nonebot import *
import os

bot = get_bot()

PATH = os.path.abspath(os.path.join(os.getcwd(), 'plugins/data/mahjong/'))

@bot.on_message("group")
async def applyMahjong(context):
    msg = context["message"]
    s_msg = str(msg)
    if s_msg == '约麻' or s_msg == '取消约麻' or s_msg == '约麻列表' or s_msg == '开局':
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
            print('当前群约麻记录文件不存在')
            f = open(os.path.join(PATH, str(group_id) + '.txt'), 'w')
            f.close()

        
        if s_msg == '约麻':
            print(user_list)
            print(nickname_list)
            if str(user_id) in user_list:
                await bot.send_msg(group_id=group_id, message='已经记录过了～')
            else:
                user_list.append(user_id)
                nickname_list.append(nickname)
                await bot.send_msg(group_id=group_id, message='已记录约麻申请')
        
        if s_msg == '取消约麻':
            if str(user_id) in user_list:
                user_list.remove(str(user_id))
                nickname_list.remove(nickname)
                await bot.send_msg(group_id=group_id, message='已经取消了')
            else:
                await bot.send_msg(group_id=group_id, message='没有申请过呢')
        
        if s_msg == '约麻列表':
            if len(user_list) == 0:
                await bot.send_msg(group_id=group_id, message='没有人约麻呢')
            else:
                ok_msg = '约麻列表：\n'
                for i in nickname_list:
                    ok_msg = ok_msg + i + '\n'
                ok_msg = ok_msg + '目前有' + str(len(nickname_list)) + '个约麻小伙伴'
                await bot.send_msg(group_id=group_id, message=ok_msg)
        
        if s_msg == '开局':
            if len(user_list) == 0:
                await bot.send_msg(group_id=group_id, message='没有人约麻呢')
            else:
                ok_msg = '开局啦，开局啦\n'
                for i in user_list:
                    ok_msg = ok_msg + '[CQ:at,qq=' + str(i) + ']\n'
                ok_msg = ok_msg + '赶快去打麻将吧～'

                await bot.send_msg(group_id=group_id, message=ok_msg)
                user_list.clear()
                nickname_list.clear()
        
        # 处理完毕，清空并写入文件
        with open(os.path.join(PATH, str(group_id) + '.txt'), 'w') as f:
            for user_id, nickname in zip(user_list, nickname_list):
                f.write(str(user_id) + ' ' + nickname + '\n')