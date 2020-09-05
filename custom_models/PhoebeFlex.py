from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import FlexSendMessage, TextSendMessage

import configparser
import googletrans
import re

# 引入我們的套件
from custom_models import utils

line_bot_api = LineBotApi('mPWcLzfZ80c9sPnTZe8sCrQxBuXhVvd8UCmrYhPKNn6+4P+CS8en7tG4u4lt0lCxT6zHPs+fDSuDzx0bSeuqvcW8fA885ktKefHkoSXw4etD8rzA73M2AXRTKUORo9c6ImLaO86kjYUxbqgKmk90FgdB04t89/1O/w1cDnyilFU=')

# LINE 提供的 FlexMessage 範例
sample = {
    'type': 'bubble',
    'direction': 'ltr',
    'hero': {
        'type': 'image',
        'url': 'https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_2_restaurant.png',
        'size': 'full',
        'aspect_ratio': '20:13',
        'aspect_mode': 'cover',
        'action': {'type': 'postback', 'data': 'sample', 'label': 'sample'}
    }
}


# 依照使用者輸入的訊息傳送 FlexMessage
def img_search_flex(event):
    if re.match("flex", event.message.text.lower()):

        try:
            translator = googletrans.Translator()
            results = translator.translate(event.message.text[5:])
            # translate = utils.get_translate(event.message.text[5:])
            translate = results.text
            random_img_url = utils.get_img_url(target=translate)

            contents = utils.prepare_img_search_flex(event.message.text[5:], translate, random_img_url)

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=str(translate))
            )

            # line_bot_api.reply_message(
            #     event.reply_token,
            #     FlexSendMessage(
            #         alt_text=f'flex {translate}',
            #         contents=contents
            #     )
            # )

            return True

        except:
            return False

    else:
        return False