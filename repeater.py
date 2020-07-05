# 复读功能
from nonebot import *

bot = get_bot()

msg_list = {}
word_list = [
    '签到', '盖章', '打卡', '妈', '妈?', '妈妈', '妈!', '妈！', '妈妈！',
    '挂树', '查树', '十连', '在线十连', '申请出刀', '尾刀', '日程', '日程表', '加入公会', '撤销',
    '约麻', '取消约麻', '约麻列表', '开局',
    '约合刀', '取消约合刀', '约合刀列表', '开打',
    '来一张色图', '来一张涩图', '来一份涩图', '来一份色图', '来一张瑟图', '来一份瑟图',
    '卡池资讯', '卡池详情', '卡池信息', '看看卡池', '康康卡池', '10连', '抽十连', '十连抽', '来个十连', '来发十连', '来次十连', '抽个十连', '抽发十连', '抽次十连', 
    '十连', '仓库', '抽一井', '来一井', '来发井', '抽发井',
]

@bot.on_message("group")
async def repeat(context):
    msg = context["message"]
    s_msg = str(msg)
    group_id = context["group_id"]
    user_id = context["user_id"]

    if s_msg in word_list:
        return

    # 字典中不存在group_id，添加
    if group_id not in msg_list:
        msg_list[group_id] = {
            'user_id': user_id,
            'msg': s_msg,
            'repeated': False
        }
    # 字典中存在group_id
    else:
        # 消息相同、发送人不同、未重复过：重复
        if msg_list[group_id]['msg'] == s_msg and msg_list[group_id]['user_id'] != user_id and msg_list[group_id]['repeated'] == False:
            msg_list[group_id]['repeated'] = True
            await bot.send_msg(group_id=group_id, message=s_msg)
        # 消息不同：更新
        if msg_list[group_id]['msg'] != s_msg:
            msg_list[group_id]['msg'] = s_msg
            msg_list[group_id]['user_id'] = user_id
            msg_list[group_id]['repeated'] = False
