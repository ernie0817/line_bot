from __future__ import unicode_literals
import os
from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

import configparser

import urllib
import re
import random

from ordermeal.custom_models import utils, PhoebeTalks

app = Flask(__name__)

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi('mPWcLzfZ80c9sPnTZe8sCrQxBuXhVvd8UCmrYhPKNn6+4P+CS8en7tG4u4lt0lCxT6zHPs+fDSuDzx0bSeuqvcW8fA885ktKefHkoSXw4etD8rzA73M2AXRTKUORo9c6ImLaO86kjYUxbqgKmk90FgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ba597a8d56c7986d140690fb97151b8d')

@app.route("/")
def home():
    return render_template("home.html")

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


# 請 pixabay 幫我們找圖
@handler.add(MessageEvent, message=TextMessage)
def pixabay_isch(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":

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
        # 如果找不到圖，就學你說話
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=str(event.source.user_id))
            )
            pass


if __name__ == "__main__":
    app.run()