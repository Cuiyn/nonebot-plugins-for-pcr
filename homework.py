# 用于存储与分享公会战作业
from nonebot.message import escape
import re
import os
import sqlite3

from nonebot import *

SUPERUSER = [123456789]
DB_FILE_PATH = '/home/xxx/data/homework/homeworks.db'

def db_init():
    # 检查数据库文件是否存在，不存在则新建
    if not os.path.exists(DB_FILE_PATH):
        db_conn = sqlite3.connect(DB_FILE_PATH)
        db = db_conn.cursor()
        db.execute(
                '''CREATE TABLE Homework(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bossid SMALLINT,
                title TEXT,
                content TEXT
                )''')
        db_conn.commit()
        db_conn.close()


@on_command('作业', only_to_me=False)
async def getHomework(session: CommandSession):
    s = session.ctx['raw_message']
    s = s[3:]
    db_init()
    db_conn = sqlite3.connect(DB_FILE_PATH)
    db = db_conn.cursor()

    if s[0] == '#':
        # TODO: 调取数据库中对应编号的作业数据
        sql_info = list(db.execute(
            "SELECT id,title,content FROM Homework WHERE id=?", (s[1:].split())))
        msg = ''
        if len(sql_info) == 0:
            msg = '好像没有这个作业呢'
        else:
            (id, title, content) = sql_info[0]
            msg = '作业#' + str(id) + '：' + title + '\n'
            msg += content
        await session.send(msg)
    elif s[0] in '12345':
        sql_info = list(db.execute(
            "SELECT id,title FROM Homework WHERE bossid=?", (s[0])))
        msg = s[0] + '王的作业有：\n'
        if len(sql_info) == 0:
            msg = '目前没有该 Boss 的作业'
        else:
            for (id, title) in sql_info:
                msg += '#'
                msg += str(id)
                msg += ' '
                msg += title
                msg += '\n'
            msg = msg[:-1]
        await session.send(msg)
    else:
        await session.send('好像没有这个作业呢')
    db_conn.commit()
    db_conn.close()


@on_command('作业添加', only_to_me=False)
async def getHomework(session: CommandSession):
    s = session.ctx['raw_message']
    s = s[5:]
    qqid = session.ctx['user_id']

    if qqid not in SUPERUSER:
        await session.send('目前只有管理员能够添加和删除作业呢')
        return
    if s[0] not in '12345':
        await session.send('请指定Boss序号或在#号之后指定作业标题～')
        return
    bossid = s[0]
    s = s[1:].lstrip()
    if s[0] != '#':
        await session.send('请指定Boss序号或在#号之后指定作业标题～')
        return
    # Windows QQ 客户端的换行符存在差异
    try:
        title, content = s[1:].split('\n', 1)
    except ValueError:
        title, content = s[1:].split('\r', 1)

    # 连接数据库
    db_init()
    db_conn = sqlite3.connect(DB_FILE_PATH)
    db = db_conn.cursor()
    db.execute("INSERT INTO Homework (bossid, title, content) VALUES (?,?,?)",
                (bossid, title, content))
    db_conn.commit()
    db_conn.close()
    await session.send('作业已添加～')


@on_command('作业删除', only_to_me=False)
async def delHomework(session: CommandSession):
    s = session.ctx['raw_message']
    s = s[5:]
    qqid = session.ctx['user_id']

    if qqid not in SUPERUSER:
        await session.send('目前只有管理员能够添加和删除作业呢')
        return
    if s[0] != '#':
        await session.send('请在#号后指定要删除的作业')
        return
    
    s = s[1:].split()
    # 连接数据库
    db_init()
    db_conn = sqlite3.connect(DB_FILE_PATH)
    db = db_conn.cursor()
    db.execute("DELETE From Homework WHERE id=?",
                (s))
    db_conn.commit()
    db_conn.close()
    await session.send('此作业已删除～')
