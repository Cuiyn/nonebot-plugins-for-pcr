import random
import datetime
from nonebot import on_command, CommandSession

user_list = {}

login_presents = [
    '扫荡券×5',  '金币×1000', '普通EXP药水×5',  '宝石×50',  '玛那×3000',
    '扫荡券×10', '金币×1500', '普通EXP药水×15', '宝石×80',  '白金扭蛋券×1',
    '扫荡券×15', '金币×2000', '高级精炼石×3',   '宝石×100', '白金扭蛋券×1',
]

todo_list = [
    '找伊绪老师上课',
    '给宫子买布丁',
    '和真琴一起寻找伤害优衣的人',
    '找镜哥探讨女装',
    '跟吉塔一起登上骑空艇',
    '和霞一起调查伤害优衣的人',
    '和佩可小姐一起吃午饭',
    '找小小甜心玩过家家',
    '帮碧寻找新朋友',
    '去真步真步王国',
    '找镜华补习数学',
    '陪胡桃排练话剧',
    '和初音一起午睡',
    '成为露娜的朋友',
    '帮铃莓打扫咲恋育幼院',
    '和静流小姐一起做巧克力',
    '去伊丽莎白农场给栞小姐送书',
    '观看慈乐之音的演出',
    '解救挂树的队友',
    '来一发十连',
    '井一发当期的限定池',
    '给妈妈买一束康乃馨',
    '购买黄金保值',
    '竞技场背刺',
    '给别的女人打钱',
    '氪一单',
    '努力工作，尽早报答妈妈的养育之恩',
    '成为魔法少女',
    '约一把麻将'
]

@on_command('签到', aliases=('盖章', '打卡', '妈', '妈?', '妈妈', '妈!', '妈！', '妈妈！'), only_to_me=False)
async def give_okodokai(session: CommandSession):
    uid = session.ctx['user_id']

    if uid not in user_list:
        user_list[uid] = datetime.date.today()
        present = random.choice(login_presents)
        todo = random.choice(todo_list)
        await session.send(f'\nおかえりなさいませ、主さま~\n{present}を獲得しました\n私からのプレゼントです\n主人今天要{todo}吗？', at_sender=True)
    else:
        if user_list[uid] == datetime.date.today():
            await session.send('明日はもう一つプレゼントをご用意してお待ちしますね', at_sender=True)
        else:
            present = random.choice(login_presents)
            todo = random.choice(todo_list)
            user_list[uid] = datetime.date.today()
            await session.send(f'\nおかえりなさいませ、主さま~\n{present}を獲得しました\n私からのプレゼントです\n主人今天要{todo}吗？', at_sender=True)
