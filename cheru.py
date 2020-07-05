"""切噜语（ちぇる語, Language Cheru）转换
定义:
    W_cheru = '切' ^ `CHERU_SET`+
    切噜词均以'切'开头，可用字符集为`CHERU_SET`
    L_cheru = {W_cheru ∪ `\\W`}*
    切噜语由切噜词与标点符号连接而成
"""
from nonebot.message import escape
from itertools import zip_longest
import re

from nonebot import *

bot = get_bot()


CHERU_SET = '切卟叮咧哔唎啪啰啵嘭噜噼巴拉蹦铃'
CHERU_DIC = { c: i for i, c in enumerate(CHERU_SET) }
ENCODING = 'gb18030'
rex_split = re.compile(r'\b', re.U)
rex_word = re.compile(r'^\w+$', re.U)
rex_cheru_word:re.Pattern = re.compile(rf'切[{CHERU_SET}]+', re.U)


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def word2cheru(w:str) -> str:
    c = ['切']
    for b in w.encode(ENCODING):
        c.append(CHERU_SET[b & 0xf])
        c.append(CHERU_SET[(b >> 4) & 0xf])
    return ''.join(c)


def cheru2word(c:str) -> str:
    if not c[0] == '切' or len(c) < 2:
        return c
    b = []
    for b1, b2 in grouper(c[1:], 2, '切'):
        x = CHERU_DIC.get(b2, 0)
        x = x << 4 | CHERU_DIC.get(b1, 0)
        b.append(x)
    return bytes(b).decode(ENCODING, 'replace')


def str2cheru(s:str) -> str:
    c = []
    for w in rex_split.split(s):
        if rex_word.search(w):
            w = word2cheru(w)
        c.append(w)
    print(c)
    return ''.join(c)


def cheru2str(c:str) -> str:
    return rex_cheru_word.sub(lambda w: cheru2word(w.group()), c)


@on_command('切噜一下', only_to_me=False)
async def encode(session: CommandSession):
    s = session.ctx['raw_message']
    s = s[5:]
    if len(s) > 500:
        await session.send('切、切噜太长切不动切噜噜……')
    else:
        await session.send('切噜～♪' + str2cheru(s))


@bot.on_message("group")
async def decode(context):
    s = context['raw_message']
    if s[0:4] != '切噜～♪':
        return
    user_id = context["user_id"]
    group_id = context["group_id"]

    s = str(s[4:])
    if len(s) > 1500:
        await session.send('切、切噜太长切不动切噜噜……')
    else:
        msg = '[CQ:at,qq=' + str(user_id) + ']的切噜噜是：\n' + escape(cheru2str(s))
        await bot.send_msg(group_id=group_id, message=msg)