# ﻿from __future__ import unicode_literals
import os

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, PostbackEvent, TextMessage, TextSendMessage, ImageSendMessage, FlexSendMessage, \
    TemplateSendMessage, ButtonsTemplate, MessageTemplateAction
import urllib
import re
import requests
import json
import datetime
import configparser

import random

# 我們的函數
from custom_models import utils, CallDatabase

# LINE 聊天機器人的基本資料
# config = configparser.ConfigParser()
# config.read('config.ini')

# line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
line_bot_api = LineBotApi(
    'mPWcLzfZ80c9sPnTZe8sCrQxBuXhVvd8UCmrYhPKNn6+4P+CS8en7tG4u4lt0lCxT6zHPs+fDSuDzx0bSeuqvcW8fA885ktKefHkoSXw4etD8rzA73M2AXRTKUORo9c6ImLaO86kjYUxbqgKmk90FgdB04t89/1O/w1cDnyilFU=')


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
    pretty_note = '♫♪♬'
    pretty_text = ''

    for i in event.message.text:
        pretty_text += i
        pretty_text += f" {random.choice(pretty_note)} "

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=pretty_text)
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
    if '週六追求訂便當' in event.message.text:
        profile_data = {
            'Authorization': 'Bearer mPWcLzfZ80c9sPnTZe8sCrQxBuXhVvd8UCmrYhPKNn6+4P+CS8en7tG4u4lt0lCxT6zHPs+fDSuDzx0bSeuqvcW8fA885ktKefHkoSXw4etD8rzA73M2AXRTKUORo9c6ImLaO86kjYUxbqgKmk90FgdB04t89/1O/w1cDnyilFU='}
        profile = requests.get('https://api.line.me/v2/bot/profile/' + userId, headers=profile_data)
        user_json = json.loads(profile.text)
        today = datetime.datetime.now().date()
        this_sat = today + datetime.timedelta(days=5 - datetime.datetime.now().weekday())

        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='Buttons template',
                                template=ButtonsTemplate(title='週六追求簽到', text=str(this_sat), actions=[
                                    MessageTemplateAction(label='會參加且會留下用餐',
                                                          text='週六追求簽到/' + str(user_json['displayName']) + '/' + str(
                                                              this_sat) + '/會參加且會留下用餐'),
                                    MessageTemplateAction(label='會參加但不留下用餐',
                                                          text='週六追求簽到/' + str(user_json['displayName']) + '/' + str(
                                                              this_sat) + '/會參加但不留下用餐'),
                                    MessageTemplateAction(label='因有事無法參加',
                                                          text='週六追求簽到/' + str(user_json['displayName']) + '/' + str(
                                                              this_sat) + '/因有事無法參加')]))
            # TextSendMessage(text=str(user_json['displayName']))
        )
        # elif isinstance(event, PostbackEvent):  # 如果有回傳值事件
        #     text_list = event.postback.data.split('/')
        #     line_bot_api.reply_message(
        #         event.reply_token,
        #         TextSendMessage(text=str(text_list) + '已寫入資料庫')
        #     )
        # record_list = utils.prepare_record(event.postback.data)

        return True

    else:
        return False


def participate(event, userId):
    if '週六追求簽到' in event.message.text:
        try:
            text_list = event.message.text.split('/')
            if text_list[3] == '會參加且會留下用餐':
                pa = 'A'
            if text_list[3] == '會參加但不留下用餐':
                pa = 'B'
            if text_list[3] == '因有事無法參加':
                pa = 'C'
            record_list = [userId, text_list[1], pa, text_list[2]]
            reply = CallDatabase.line_insert_record(record_list)

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply)
            )
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='資料匯入失敗!')
            )
        return True

    else:
        return False
