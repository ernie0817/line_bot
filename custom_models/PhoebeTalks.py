# ﻿from __future__ import unicode_literals
import os

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, PostbackEvent, TextMessage, TextSendMessage, ImageSendMessage, FlexSendMessage
import urllib
import re
import requests
import json
import configparser

import random

# 我們的函數
from custom_models import utils, CallDatabase

# LINE 聊天機器人的基本資料
# config = configparser.ConfigParser()
# config.read('config.ini')

# line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
line_bot_api = LineBotApi('mPWcLzfZ80c9sPnTZe8sCrQxBuXhVvd8UCmrYhPKNn6+4P+CS8en7tG4u4lt0lCxT6zHPs+fDSuDzx0bSeuqvcW8fA885ktKefHkoSXw4etD8rzA73M2AXRTKUORo9c6ImLaO86kjYUxbqgKmk90FgdB04t89/1O/w1cDnyilFU=')


# 請 LINE 幫我們存入資料
def insert_record(event):
    if '草泥馬訓練紀錄' in event.message.text:

        try:
            record_list = utils.prepare_record(event.message.text)
            reply = CallDatabase.line_insert_record(record_list)

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply)
            )

        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='失敗了')
            )

        return True
    else:
        return False


# 請 pixabay 幫我們找圖
def img_search(event):
    try:
        random_img_url = utils.get_img_url(event.message.text)

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


def churchlife(event):
    if '召會生活人數統計' in event.message.text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='https://www.chlife-stat.org/login.php')
        )

        return True

    else:
        return False


def flow(event):
    if '湧流' in event.message.text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='https://flowingstream.org/')
        )

        return True

    else:
        return False


def order_meal(event, userId):
    profile_data = {'Authorization': 'Bearer mPWcLzfZ80c9sPnTZe8sCrQxBuXhVvd8UCmrYhPKNn6+4P+CS8en7tG4u4lt0lCxT6zHPs+fDSuDzx0bSeuqvcW8fA885ktKefHkoSXw4etD8rzA73M2AXRTKUORo9c6ImLaO86kjYUxbqgKmk90FgdB04t89/1O/w1cDnyilFU='}
    profile = requests.get('https://api.line.me/v2/bot/profile/' + userId, headers=profile_data)
    user_json = json.load(profile.text)

    if '訂便當' in event.message.text:

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=user_json['displayName'])
        )

        return True

    else:
        return False
