from __future__ import unicode_literals
import os
from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

from ordermeal.custom_models import utils, PhoebeTalks

app = Flask(__name__)

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi('mPWcLzfZ80c9sPnTZe8sCrQxBuXhVvd8UCmrYhPKNn6+4P+CS8en7tG4u4lt0lCxT6zHPs+fDSuDzx0bSeuqvcW8fA885ktKefHkoSXw4etD8rzA73M2AXRTKUORo9c6ImLaO86kjYUxbqgKmk90FgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ba597a8d56c7986d140690fb97151b8d')

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# 紀錄資料
@handler.add(MessageEvent, message=TextMessage)
def reply_text_message(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str(event.message.text))
        )

        reply = False

        # 將資料存入表格中
        if not reply:
            reply = PhoebeTalks.insert_record(event)

        # 幫忙上網找圖
        if not reply:
            reply = PhoebeTalks.img_search(event)

        # 幫忙上網找圖
        if not reply:
            reply = PhoebeTalks.img_search(event)

        # 裝飾過的回音機器人
        if not reply:
            reply = PhoebeTalks.pretty_echo(event)


if __name__ == "__main__":
    app.run()