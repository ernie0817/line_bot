# ﻿from __future__ import unicode_literals
import os

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, PostbackEvent, TextMessage, TextSendMessage, ImageSendMessage, FlexSendMessage
import urllib
import re

import configparser

import random

# 我們的函數
# from custom_models import utils, CallDatabase

# LINE 聊天機器人的基本資料
# config = configparser.ConfigParser()
# config.read('config.ini')

# line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
line_bot_api = LineBotApi('mPWcLzfZ80c9sPnTZe8sCrQxBuXhVvd8UCmrYhPKNn6+4P+CS8en7tG4u4lt0lCxT6zHPs+fDSuDzx0bSeuqvcW8fA885ktKefHkoSXw4etD8rzA73M2AXRTKUORo9c6ImLaO86kjYUxbqgKmk90FgdB04t89/1O/w1cDnyilFU=')


# 請 LINE 幫我們存入資料
# def insert_record(event):
#     if '草泥馬訓練紀錄' in event.message.text:
#
#         try:
#             record_list = utils.prepare_record(event.message.text)
#             reply = CallDatabase.line_insert_record(record_list)
#
#             line_bot_api.reply_message(
#                 event.reply_token,
#                 TextSendMessage(text=reply)
#             )
#
#         except:
#             line_bot_api.reply_message(
#                 event.reply_token,
#                 TextSendMessage(text='失敗了')
#             )
#
#         return True
#     else:
#         return False


# 請 pixabay 幫我們找圖
def img_search(event):
    try:
        q_string = {'tbm': 'isch', 'q': event.message.text}
        url = f"https://www.google.com/search?{urllib.parse.urlencode(q_string)}/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

        req = urllib.request.Request(url, headers=headers)
        conn = urllib.request.urlopen(req)

        print('fetch conn finish')
        #
        pattern = 'img data-src="\S*"'
        img_list = []

        for match in re.finditer(pattern, str(conn.read())):
            img_list.append(match.group()[14:-3])
        #
        random_img_url = img_list[random.randint(0, len(img_list) + 1)]
        # print('fetch img url finish')
        # print(random_img_url)

        # line_bot_api.reply_message(
        #     event.reply_token,
        #     TextSendMessage(text=random_img_url)
        # )

        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=random_img_url,
                preview_image_url=random_img_url
            )
        )

        return True

    except:
        return False


def pretty_echo(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=str(event.message.text))
    )

    return True
