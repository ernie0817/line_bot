from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

import configparser

import urllib
import re
import random
from requests_html import HTMLSession

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

# 請 pixabay 幫我們找圖
@handler.add(MessageEvent, message=TextMessage)
def pixabay_isch(event):
    
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        try:
            url = 'https://www.google.com.tw/search?q=' + event.message.text + ' &rlz=1C1CAFB_enTW617TW621&source=lnms&tbm=isch&sa=X&ved=0ahUKEwienc6V1oLcAhVN-WEKHdD_B3EQ_AUICigB&biw=1128&bih=863'

            session = HTMLSession()
            r = session.get(url)
            r.html.render(sleep=3, scrolldown=1, wait=2)
            img_arr = r.html.find("img")
            img_no = 0
            img_list = []
            for i in img_arr:
                tmp_content = ''
                try:
                    tmp_content = (i.attrs['src'])
                    if tmp_content != '' and tmp_content.find('http') == -1 and tmp_content.find('/images') == -1:
                        img_list.append(tmp_content)
                except:
                    pass
            
            random_img_url = img_list[random.randint(0, len(img_list)+1)]
            
            
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
                TextSendMessage(text=event.message.text+'!')
            )
            pass

if __name__ == "__main__":
    app.run()