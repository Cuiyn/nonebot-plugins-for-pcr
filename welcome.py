from nonebot import on_notice, NoticeSession

# 将函数注册为群成员增加通知处理器
@on_notice('group_increase')
async def _(session: NoticeSession):
    # 发送欢迎消息
    user_id = session.ctx['user_id']
    msg = '欢迎新大佬： ' + '[CQ:at,qq=' + str(user_id) + ']\n' + '有空请留意一下群公告与群文件，公会新成员请发送“加入公会”以便于使用我提供的各项功能，任何问题请联系管理～'
    await session.send(msg)
