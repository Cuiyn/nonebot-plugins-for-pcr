import os
import random
import pickle
import sqlite3
import time
import re
try:
    import ujson as json
except:
    import json

from nonebot import on_command, CommandSession
import nonebot

from PIL import Image


SUPERUSER = [123456789]
JEWEL_MAX = 45000
POOL_FILE_PATH = '/home/xxx/gacha/config.json'
POOL = {}
DB_FILE_PATH = '/home/xxx/data/gacha/collections.db'

ICON_FILE_PATH = '/home/xxx/data/gacha/icons/'
IMAGE_SIZE = 128  # 每张小图片的大小
IMAGE_ROW = 2  # 图片间隔，也就是合并成一张图后，一共有几行
IMAGE_COLUMN = 5  # 图片间隔，也就是合并成一张图后，一共有几列
IMAGE_SAVE_PATH = '/home/xxx/data/gacha/result.jpg'

UP_PROB = 7
S3_PROB = 18
S2_PROB = 180
S1_PROB = 795

bot = nonebot.get_bot()


def init():
    global POOL
    # 载入卡池 JSON 文件
    if not os.path.exists(POOL_FILE_PATH):
        print("卡池文件不存在")
        return 1
    else:
        with open(POOL_FILE_PATH, "r", encoding="utf-8") as f:
            try:
                POOL = json.load(f)
            except json.JSONDecodeError:
                print("卡池文件解析错误，请检查卡池文件语法")
                return 1
    
    # 检查数据库文件
    if not os.path.exists(DB_FILE_PATH):
        db_conn = sqlite3.connect(DB_FILE_PATH)
        db = db_conn.cursor()
        db.execute(
                '''CREATE TABLE Colle(
                qqid INT PRIMARY KEY,
                colle BLOB,
                times SMALLINT,
                jewel INT,
                last_day CHARACTER(4))''')
        db_conn.commit()
        db_conn.close()
    return 0


@nonebot.scheduler.scheduled_job('cron', hour='5')
async def jewel_update():
    if not os.path.exists(DB_FILE_PATH):
        return
    db_conn = sqlite3.connect(DB_FILE_PATH)
    db = db_conn.cursor()
    db.execute(f'UPDATE Colle SET jewel={JEWEL_MAX}')
    db_conn.commit()
    db_conn.close()


def result(pool, info):
    global POOL, S3_PROB, UP_PROB, S2_PROB, S1_PROB

    result_dict = {
        'up': [],
        'star3': [],
        'star2': [],
        'star1': []
    }

    result_msg = ''

    # 前 9 发
    for i in range(1, 10):
        # 生成 1 <= number < 1001 间的数
        num = random.randrange(1, 1001, 1)
        if num <= UP_PROB:
            result_character = random.choice(pool['up'])
            result_msg = result_msg + '★★★' + result_character
            result_dict['up'].append(result_character)
            if result_character not in info['star3']:
                result_msg += ' new!\n'
            else:
                result_msg += '\n'
        elif num <= S3_PROB:
            result_character = random.choice(pool['star3'])
            result_msg = result_msg + '★★★' + result_character
            result_dict['star3'].append(result_character)
            if result_character not in info['star3']:
                result_msg += ' new!\n'
            else:
                result_msg += '\n'
        elif num <= (S2_PROB + S3_PROB):
            result_character = random.choice(pool['star2'])
            result_msg = result_msg + '★★' + result_character
            result_dict['star2'].append(result_character)
            if result_character not in info['star2']:
                result_msg += ' new!\n'
            else:
                result_msg += '\n'
        else:
            result_character = random.choice(pool['star1'])
            result_msg = result_msg + '★' + result_character
            result_dict['star1'].append(result_character)
            if result_character not in info['star1']:
                result_msg += ' new!\n'
            else:
                result_msg += '\n'

    # 第 10 发
    num = random.randrange(1, 206, 1)
    if num <= 7:
        result_character = random.choice(pool['up'])
        result_msg = result_msg + '★★★' + result_character
        result_dict['up'].append(result_character)
        if result_character not in info['star3']:
            result_msg += ' new!\n'
        else:
            result_msg += '\n'
    elif num <= 25:
        result_character = random.choice(pool['star3'])
        result_msg = result_msg + '★★★' + result_character
        result_dict['star3'].append(result_character)
        if result_character not in info['star3']:
            result_msg += ' new!\n'
        else:
            result_msg += '\n'
    else:
        result_character = random.choice(pool['star2'])
        result_msg = result_msg + '★★' + result_character
        result_dict['star2'].append(result_character)
        if result_character not in info['star2']:
            result_msg += ' new!\n'
        else:
            result_msg += '\n'

    return (result_dict, result_msg)


@on_command('卡池资讯', aliases=('卡池详情', '卡池信息', '看看卡池', '康康卡池'), only_to_me=False)
async def gacha_info(session:CommandSession):
    error = init()
    if error == 1:
        print("初始化错误")
        return
    
    # 国服卡池
    global POOL
    BL_POOL = POOL['BL']

    up_msg = ''
    for character in BL_POOL['up']:
        up_msg = '★★★' + character + '\n'

    S3_PROB = BL_POOL['s3_prob']
    UP_PROB = BL_POOL['up_prob']
    
    msg = (f'本期卡池UP角色：\n' + up_msg + f'3★出率{S3_PROB / 10}%，UP出率{UP_PROB / 10}%')

    await session.send(msg)
    

@on_command('十连', aliases=('10连', '抽十连', '十连抽', '来个十连', '来发十连', '来次十连', '抽个十连', '抽发十连', '抽次十连'), only_to_me=False)
async def gacha_10(session: CommandSession):
    qqid = session.ctx['user_id']
    nickname = session.ctx['sender']['nickname']
    error = init()
    if error == 1:
        print("初始化错误")
        return
    
    # 载入国服卡池数据
    global POOL, S3_PROB, UP_PROB, S2_PROB, S1_PROB
    BL_POOL = POOL['BL']
    S3_PROB = BL_POOL['s3_prob']
    UP_PROB = BL_POOL['up_prob']
    S2_PROB = BL_POOL['s2_prob']
    S1_PROB = 1000 - S3_PROB - S2_PROB

    # 载入数据库内数据
    db_conn = sqlite3.connect(DB_FILE_PATH)
    db = db_conn.cursor()
    sql_info = list(db.execute(
            "SELECT colle,times,jewel,last_day FROM Colle WHERE qqid=?", (qqid,)))
    mem_exists = (len(sql_info) == 1)
    if mem_exists:
        info = pickle.loads(sql_info[0][0])
        times, jewel, last_day = sql_info[0][1:]
    else:
        info = {
            'star3': [],
            'star2': [],
            'star1': []
        }
        times, jewel, last_day = 0, JEWEL_MAX, ''
    
    # 检查钻石数量
    if jewel < 1500:
        await session.send(f'只剩下{jewel}个钻石，不够一发十连呢')
        return
    
    # 生成抽取结果
    (result_dict, result_msg) = result(BL_POOL, info)

    # 更新info
    info['star3'] += (result_dict['up'] + result_dict['star3'])
    info['star2'] += result_dict['star2']
    info['star1'] += result_dict['star1']

    # 更新其它数据
    times += 1
    jewel -= 1500
    last_day = time.strftime("%m%d")

    # 写入数据库
    sql_info = pickle.dumps(info)
    if mem_exists:
        db.execute("UPDATE Colle SET colle=?, times=?, jewel=?, last_day=? WHERE qqid=?",
                       (sql_info, times, jewel, last_day, qqid))
    else:
        db.execute("INSERT INTO Colle (qqid,colle,times,jewel,last_day) VALUES(?,?,?,?,?)",
                       (qqid, sql_info, times, jewel, last_day))
    db_conn.commit()
    db_conn.close()

    # 回复消息
    msg = f'{nickname}的第{times}次十连结果为：\n' + result_msg

    if len(result_dict['up']) >= 1:
        msg += '恭喜海豹！おめでとうございます！\n'
    if len(result_dict['up']) == 0 and len(result_dict['star3']) == 0 and len(result_dict['star2']) == 1:
        msg += '哈哈！+19！\n'
    if len(result_dict['up']) == 0 and len(result_dict['star3']) >= 1:
        msg += 'UP呢？我那么大一个UP呢？\n'
    msg += f'今天还剩下{jewel}钻！'

    await session.send(msg)


@on_command('仓库', only_to_me=False)
async def collection(session: CommandSession):
    error = init()
    if error == 1:
        print("初始化错误")
        return
    
    qqid = session.ctx['user_id']
    nickname = session.ctx['sender']['nickname']
    # 载入数据库内数据
    db_conn = sqlite3.connect(DB_FILE_PATH)
    db = db_conn.cursor()
    sql_info = list(db.execute(
            "SELECT colle FROM Colle WHERE qqid=?", (qqid,)))
    db_conn.close()

    mem_exists = (len(sql_info) == 1)
    if mem_exists:
        msg = f'{nickname}的仓库：\n'
        info = pickle.loads(sql_info[0][0])
        character_temp = []
        for character in sorted(info['star3']):
            if character not in character_temp:
                character_temp.append(character)
                count = info['star3'].count(character)
                msg += '★★★' + character + f' ({count})\n'
        character_temp.clear()
        for character in sorted(info['star2']):
            if character not in character_temp:
                character_temp.append(character)
                count = info['star2'].count(character)
                msg += '★★' + character + f' ({count})\n'
        character_temp.clear()
        for character in sorted(info['star1']):
            if character not in character_temp:
                character_temp.append(character)
                count = info['star1'].count(character)
                msg += '★' + character + f' ({count})\n'
    else:
        msg = f'{nickname}好像还没抽过卡，仓库空空如也\n'
    
    await session.send(msg[:-1])


@on_command('抽一井', aliases=('来一井', '来发井', '抽发井'), only_to_me=False)
async def gacha_300(session: CommandSession):
    qqid = session.ctx['user_id']
    nickname = session.ctx['sender']['nickname']
    error = init()
    if error == 1:
        print("初始化错误")
        return
    
    # 载入国服卡池数据
    global POOL, S3_PROB, UP_PROB, S2_PROB, S1_PROB
    BL_POOL = POOL['BL']
    S3_PROB = BL_POOL['s3_prob']
    UP_PROB = BL_POOL['up_prob']
    S2_PROB = BL_POOL['s2_prob']
    S1_PROB = 1000 - S3_PROB - S2_PROB

    # 载入数据库内数据
    db_conn = sqlite3.connect(DB_FILE_PATH)
    db = db_conn.cursor()
    sql_info = list(db.execute(
            "SELECT colle,times,jewel,last_day FROM Colle WHERE qqid=?", (qqid,)))
    mem_exists = (len(sql_info) == 1)
    if mem_exists:
        info = pickle.loads(sql_info[0][0])
        times, jewel, last_day = sql_info[0][1:]
    else:
        info = {
            'star3': [],
            'star2': [],
            'star1': []
        }
        times, jewel, last_day = 0, JEWEL_MAX, ''
    
    # 检查钻石数量
    if jewel < 45000:
        await session.send(f'只剩下{jewel}个钻石，不够一井呢')
        return
    
    # 生成抽取结果
    # (result_dict, result_msg) = result(BL_POOL, info)

    # 记录第一次出现 UP 角色的 10 连抽次数
    up_character_count = 0
    # 记录第一次出现非 UP 3 星角色的 10 连抽次数
    star3_character_count = 0

    result_dict_300 = {
        'up': [],
        'star3': [],
        'star2': [],
        'star1': []
    }
    for i in range(0, 30):
        (result_dict_10, result_msg) = result(BL_POOL, info)
        if len(result_dict_10['up']) >= 1 and up_character_count == 0:
            up_character_count = i + 1
        if len(result_dict_10['star3']) >= 1 and star3_character_count == 0:
            star3_character_count = i + 1
        # 更新 result_dict_300
        for k, v in result_dict_10.items():
            result_dict_300[k] += v


    # 更新 info
    info['star3'] += (result_dict_300['up'] + result_dict_300['star3'])
    info['star2'] += result_dict_300['star2']
    info['star1'] += result_dict_300['star1']

    # 更新其它数据
    times += 30
    jewel -= 45000
    last_day = time.strftime("%m%d")

    # 写入数据库
    sql_info = pickle.dumps(info)
    if mem_exists:
        db.execute("UPDATE Colle SET colle=?, times=?, jewel=?, last_day=? WHERE qqid=?",
                       (sql_info, times, jewel, last_day, qqid))
    else:
        db.execute("INSERT INTO Colle (qqid,colle,times,jewel,last_day) VALUES(?,?,?,?,?)",
                       (qqid, sql_info, times, jewel, last_day))
    db_conn.commit()
    db_conn.close()

    # 回复消息
    msg = f'{nickname}的下井结果：\n'

    msg += 'UP 数量：\n'
    if len(result_dict_300['up']) == 0:
        msg += '居然没有抽出 UP ！\n'
    else:
        character_temp = []
        for character in result_dict_300['up']:
            if character not in character_temp:
                character_temp.append(character)
                count = result_dict_300['up'].count(character)
                msg += '★★★' + character + f' ({count})\n'
        msg += (f'在第{up_character_count}发十连第一次抽出 UP ！\n')
    
    msg += '\n'
    
    msg += '3★ 数量：\n'
    if len(result_dict_300['star3']) == 0:
        msg += '居然没有抽出 3★ ！\n'
    else:
        character_temp = []
        for character in result_dict_300['star3']:
            if character not in character_temp:
                character_temp.append(character)
                count = result_dict_300['star3'].count(character)
                msg += '★★★' + character + f' ({count})\n'
        msg += (f'在第{star3_character_count}发十连第一次抽出非UP 3★ ！\n')
    
    msg += '\n'
    
    msg += '2★ 数量：'
    msg += str(len(result_dict_300['star2'])) + '\n'
    msg += '1★ 数量：'
    msg += str(len(result_dict_300['star1'])) + '\n'

    msg += '\n'

    if len(result_dict_300['up']) == 0 and len(result_dict_300['star3']) == 0:
        msg += '太惨了，咱们还是退款删游吧……\n'
    elif len(result_dict_300['up']) == 0 and len(result_dict_300['star3']) >= 5:
        msg += 'UP呢？我UP呢？\n'
    elif len(result_dict_300['up']) == 0 and len(result_dict_300['star3']) <= 5:
        msg += '这位酋长，洗把脸考虑一下？\n'
    elif len(result_dict_300['up']) == 0:
        msg += ("据说天井的概率只有12.16%……\n")
    elif len(result_dict_300['up']) <= 2:
        if up_character_count <= 5:
            msg += "你的喜悦我收到了，滚去喂鲨鱼吧！\n"
        elif up_character_count <= 10:
            msg += "已经可以了，您已经很欧了\n"
        elif up_character_count > 29:
            msg += "标 准 结 局\n"
        elif up_character_count > 25:
            msg += "补井还是不补井，这是一个问题...\n"
        else:
            msg += "期望之内，亚洲水平\n"
    # elif len(result_dict_300['up']) == 3:
    #     msg += "抽井母五一气呵成！\n"
    elif len(result_dict_300['up']) >= 3:
        msg += "UP 一大堆！您是托吧？\n"

    msg += f'今天还剩下{jewel}钻！'

    await session.send(msg)


@bot.on_message("group")
async def recharge(context):
    msg = context["message"]
    s_msg = str(msg)

    if s_msg[0:2] == '充值':
        user_id = context["user_id"]
        group_id = context["group_id"]

        if user_id not in SUPERUSER:
            await bot.send_msg(group_id=group_id, message='充值请找管理员～')
            return
        
        pattern = re.compile(r'\d+')
        result = pattern.findall(s_msg)
        if len(result) == 0:
            await bot.send_msg(group_id=group_id, message='请at想要充值的人')
        else:
            qqid = result[0]

            if not os.path.exists(DB_FILE_PATH):
                return
            db_conn = sqlite3.connect(DB_FILE_PATH)
            db = db_conn.cursor()

            sql_info = list(db.execute(
                    "SELECT colle,times,jewel,last_day FROM Colle WHERE qqid=?", (qqid,)))
            mem_exists = (len(sql_info) == 1)
            if mem_exists:
                times, jewel, last_day = sql_info[0][1:]
                db.execute('UPDATE Colle SET jewel=? where qqid=?', (JEWEL_MAX + jewel, qqid))
                await bot.send_msg(group_id=group_id, message=f'成功为[CQ:at,qq={qqid}]充值{JEWEL_MAX}个钻石')
            else:
                await bot.send_msg(group_id=group_id, message='Ta还没有抽过卡呢')
            
            db_conn.commit()
            db_conn.close()
    else:
        return


@on_command('beta_十连', only_to_me=False)
async def gacha_10(session: CommandSession):
    qqid = session.ctx['user_id']
    nickname = session.ctx['sender']['nickname']
    error = init()
    if error == 1:
        print("初始化错误")
        return
    
    # 载入国服卡池数据
    global POOL, S3_PROB, UP_PROB, S2_PROB, S1_PROB
    BL_POOL = POOL['BL']
    S3_PROB = BL_POOL['s3_prob']
    UP_PROB = BL_POOL['up_prob']
    S2_PROB = BL_POOL['s2_prob']
    S1_PROB = 1000 - S3_PROB - S2_PROB

    # 载入数据库内数据
    db_conn = sqlite3.connect(DB_FILE_PATH)
    db = db_conn.cursor()
    sql_info = list(db.execute(
            "SELECT colle,times,jewel,last_day FROM Colle WHERE qqid=?", (qqid,)))
    mem_exists = (len(sql_info) == 1)
    if mem_exists:
        info = pickle.loads(sql_info[0][0])
        times, jewel, last_day = sql_info[0][1:]
    else:
        info = {
            'star3': [],
            'star2': [],
            'star1': []
        }
        times, jewel, last_day = 0, JEWEL_MAX, ''
    
    # 检查钻石数量
    if jewel < 1500:
        await session.send(f'只剩下{jewel}个钻石，不够一发十连呢')
        return
    
    # 生成抽取结果
    (result_dict, result_msg) = result(BL_POOL, info)

    # 更新info
    info['star3'] += (result_dict['up'] + result_dict['star3'])
    info['star2'] += result_dict['star2']
    info['star1'] += result_dict['star1']

    # 更新其它数据
    times += 1
    jewel -= 1500
    last_day = time.strftime("%m%d")

    # 写入数据库
    sql_info = pickle.dumps(info)
    if mem_exists:
        db.execute("UPDATE Colle SET colle=?, times=?, jewel=?, last_day=? WHERE qqid=?",
                       (sql_info, times, jewel, last_day, qqid))
    else:
        db.execute("INSERT INTO Colle (qqid,colle,times,jewel,last_day) VALUES(?,?,?,?,?)",
                       (qqid, sql_info, times, jewel, last_day))
    db_conn.commit()
    db_conn.close()

    # 回复消息
    msg = f'[CQ:at,qq={qqid}]素敵な仲間が増えますよ！\n'
    count = 0
    characters = []
    # for i in result_msg.split('\n'):
    #     character_name = i.replace('★', '').replace(' new!', '')
    #     print(character_name)
    #     msg += f'[CQ:image,file=file:///{ICON_FILE_PATH}{character_name}.png]'
    #     count += 1
    #     if count == 5:
    #         msg += '\n'
    for i in result_msg.split('\n'):
        character_name = i.replace('★', '').replace(' new!', '')
        characters.append(character_name)
    to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_SIZE, IMAGE_ROW * IMAGE_SIZE))
    for y in range(1, IMAGE_ROW + 1):
        for x in range(1, IMAGE_COLUMN + 1):
            from_image = Image.open(ICON_FILE_PATH + characters[IMAGE_COLUMN * (y - 1) + x - 1] + '.png')
            to_image.paste(from_image, ((x - 1) * IMAGE_SIZE, (y - 1) * IMAGE_SIZE))
    to_image.save(IMAGE_SAVE_PATH)

    msg += f'[CQ:image,file=file:///{IMAGE_SAVE_PATH}]'
    
    msg += '\n'
    msg += result_msg

    if len(result_dict['up']) >= 1:
        msg += '恭喜海豹！おめでとうございます！\n'
    if len(result_dict['up']) == 0 and len(result_dict['star3']) == 0 and len(result_dict['star2']) == 1:
        msg += '哈哈！+19！\n'
    
    msg += f'今天还剩下{jewel}钻！'

    await session.send(msg)