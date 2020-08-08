from __future__ import unicode_literals

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

import configparser

from apscheduler.schedulers.blocking import BlockingScheduler
import urllib
import datetime

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi('mPWcLzfZ80c9sPnTZe8sCrQxBuXhVvd8UCmrYhPKNn6+4P+CS8en7tG4u4lt0lCxT6zHPs+fDSuDzx0bSeuqvcW8fA885ktKefHkoSXw4etD8rzA73M2AXRTKUORo9c6ImLaO86kjYUxbqgKmk90FgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ba597a8d56c7986d140690fb97151b8d')

sched = BlockingScheduler()
global user_id


@sched.scheduled_job('cron', day_of_week='mon-fri', minute='*/20')
def scheduled_job():
    print('========== APScheduler CRON =========')
    print('This job runs every weekday */20 min.')
    print(f'{datetime.datetime.now().ctime()}')
    print('========== APScheduler CRON =========')

    url = "https://orderstudent.herokuapp.com/"
    conn = urllib.request.urlopen(url)

    for key, value in conn.getheaders():
        print(key, value)


@handler.add(MessageEvent, message=TextMessage)
def get_id(event):
    user_id = event.source.user_id
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.source.user_id)
    )


@sched.scheduled_job('cron', day_of_week='sat', hour=10, minute=10)
def scheduled_job():
    print('========== APScheduler CRON =========')
    print('This job is run every weekday at 6:30')
    print('========== APScheduler CRON =========')

    line_bot_api.push_message(user_id, TextSendMessage(text="記得訂便當喔!"))


sched.start()
