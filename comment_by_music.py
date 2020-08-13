import base64
import json
import math
import random
import time
from datetime import datetime
import logging
import requests
from Crypto.Cipher import AES

import sql
from chromedriver import user_agent_list

headers = {
    'Cookie': 'mail_psc_fingerprint=498d14b7a8d9a9a0b34d0563228a16c9; _ntes_nuid=cf6d08772a7d965a71ea32fc0253160e; WM_TID=xxfBNToE6rpAQEQUFRM5bbXAL2A4Uot4; nts_mail_user=cxiaohei3@163.com:-1:1; P_INFO=d1135034979@163.com|1557229799|0|cbg|00&99|CN&1557200062&xyq#hen&410100#10#0#0|&0|xyq|d1135034979@163.com; _ga=GA1.2.1833807352.1564928031; vinfo_n_f_l_n3=896edd08aa545002.1.0.1570693739370.0.1570693771539; _iuqxldmzr_=32; ntes_kaola_ad=1; _ntes_nnid=cf6d08772a7d965a71ea32fc0253160e,1586997354536; WM_NI=GYRTWpY%2F9SMBG%2BvFZLCUiMPJ0euzbLdpcVjUPtOn6bisNw9vTtuNbjGivT%2FP%2Fny2kk2dg5ee6MHSnp95Pf%2B0hCfxc9pexpcU0VdZrlkoV7wsy9RnE6I9fSr19lor3mcbQXk%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eea3bb5bad9cf9afbb68ba968bb7d14e868e8baaf14fb186bf93b779a99bfca2ed2af0fea7c3b92a85879eb5d67c9bf1f7b4d04a85f5baa7d948818ba7aed342f4bbbb9be148a8b0adb7e95f94ac818fb56aabad8298bc7e98acbbafe16285b7bab5ae5cedb2b7d3ea61f2bca9d6e86ff69388b4ed7cfbeba087aa3cac9daa99e233b4bbb891e25ff48aacbbf168a9b19ad8f679bbe79e8fc83e8be7aab4f13bfbb4a193b267a1be9fb9ea37e2a3; JSESSIONID-WYYY=WMnvntZ9W5QB%2BSfddzPI0hbcitnRA69NFN5o%2BFp02WdzR70DoBrIFhNeG637Ptyrmf7bGgf9IiwvsMTKZCuQ0ZlcJb3PpFtD%2BoX%2Bwk7hXM46r3eHSEBuEz%5C%2BsoMH%2B%2BuOblxgtsb7sCr6R9bVfhd21B4OqhwmIKg4x%5CxKF2ZDbBX4Ck0D%3A1587399839919',
    'Referer': 'http://music.163.com/',
    'User-Agent': random.choice(user_agent_list)
}
# proxy = random.choice(ip_list)

encSecKey = '257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c'
first_key = '0CoJUm6Qyw8W8jud'
iv = '0102030405060708'


class Comment(object):
    def __init__(self, music_id, user_id, content, reply_id, reply_content, liked_count, comment_time):
        self.comment_time = comment_time
        self.liked_count = liked_count
        self.reply_content = reply_content
        self.reply_id = reply_id
        self.music_id = music_id
        self.user_id = user_id
        self.content = content


def get_encrypt_params(offset, limit, total):
    param = '{rid:"", offset:"' + str(offset) + '", total:"' + total + '",limit:"' + str(
        limit) + '", csrf_token:""}'
    second_key = 16 * 'F'
    h_encText = AES_encrypt(param, first_key, iv)
    h_encText = AES_encrypt(str(h_encText, 'utf-8'), second_key, iv)
    return h_encText


def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text += pad * chr(pad)
    encryptor = AES.new(key.encode('UTF-8'), AES.MODE_CBC, iv.encode('UTF-8'))
    encrypt_text = encryptor.encrypt(text.encode('UTF-8'))
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text


def get_comment_count(music_id):
    url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_' + str(music_id) + '?csrf_token='
    param = get_encrypt_params(0, 1, 'true')
    data = {
        "params": param,
        "encSecKey": encSecKey
    }
    response = requests.post(url, headers=headers, data=data)
    json_dict = json.loads(response.content)
    total = json_dict['total']
    return total


def get_comment_by_music_id_and_user_id(music_id, user_id):
    url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_' + str(music_id) + '?csrf_token='
    total = get_comment_count(music_id)
    pages = math.ceil(total / 20)
    i = 0
    for page in range(0, pages):
        if 50 < page < pages - 50:
            continue
        flag = 'true' if page == 0 else 'false'
        param = get_encrypt_params(page * 20, (page + 1) * 20 - 1, flag)
        data = {
            "params": param,
            "encSecKey": encSecKey
        }
        response = requests.post(url, headers=headers, data=data)
        json_dict = json.loads(response.content)
        comments = json_dict['comments']
        for comment in comments:
            is_reply = 1 if len(comment['beReplied']) > 0 else 0
            if comment['user']['userId'] == user_id or (is_reply == 1
                                                        and comment['beReplied'][0]['user']['userId'] == user_id):
                c = Comment(music_id,
                            comment['user']['userId'],
                            comment['content'],
                            comment['beReplied'][0]['beRepliedCommentId'] if is_reply == 1 else '',
                            comment['beReplied'][0]['content'] if is_reply == 1 else '',
                            comment['likedCount'],
                            datetime.fromtimestamp(comment['time'] / 1000))
                logging.info(comment['content'])
                sql.insert_comment(c)
        i += 1
        print('\r查询成功，歌曲：' + str(music_id) + ',共' + str(total) + '条评论，进度：' + str(i) + '/' + str(
            pages if pages < 100 else 100),
              end='')
    logging.info(str(music_id)+"歌曲查找完毕成功")




def get_comment_by_user_musics(user_id):
    music_list = sql.get_musics_by_user(user_id)
    music_index = 0
    count = len(music_list)
    logging.info('获取成功，共' + str(count) + '首歌曲')
    for music in music_list:
        get_comment_by_music_id_and_user_id(music['music_id'], user_id)
        music_index += 1
        print('\r歌曲:' + str(music['music_id']) + '，查询完毕。进度：' + str(music_index) + '/' + str(count), end='')
        print()

if __name__ == "__main__":
    logging.basicConfig(filename="out.log", level=logging.INFO)
    start = time.time()
    get_comment_by_user_musics(88574814)
    cost = (time.time() - start)
    print('耗时：' + str(cost) + '秒')
