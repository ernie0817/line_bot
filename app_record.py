from __future__ import unicode_literals
import os
from flask import Flask, request, abort, render_template, url_for, flash, redirect
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

from custom_models import PhoebeTalks, utils, PhoebeFlex, CallDatabase

app = Flask(__name__)
app.secret_key = '123456'

# Day25: users 使用者清單
users = {'Me': {'password': 'myself'}}

# Day25: Flask-Login 初始化
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = '請證明你並非來自黑暗草泥馬界'


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(user_id):
    if user_id not in users:
        return

    user = User()
    user.id = user_id
    return user


@login_manager.request_loader
def request_loader(request):
    user_id = request.form.get('user_id')
    if user_id not in users:
        return

    user = User()
    user.id = user_id

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[user_id]['password']

    return user


# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi('mPWcLzfZ80c9sPnTZe8sCrQxBuXhVvd8UCmrYhPKNn6+4P+CS8en7tG4u4lt0lCxT6zHPs+fDSuDzx0bSeuqvcW8fA885ktKefHkoSXw4etD8rzA73M2AXRTKUORo9c6ImLaO86kjYUxbqgKmk90FgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ba597a8d56c7986d140690fb97151b8d')


@app.route("/")
def home():
    return render_template("home.html")


# Day25: Flask-Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    user_id = request.form['user_id']
    if (user_id in users) and (request.form['password'] == users[user_id]['password']):
        user = User()
        user.id = user_id
        login_user(user)
        flash(f'{user_id}！歡迎加入草泥馬訓練家的行列！')
        return redirect(url_for('from_start'))

    flash('登入失敗了...')
    return render_template('login.html')


@app.route('/logout')
def logout():
    user_id = current_user.get_id()
    logout_user()
    flash(f'{user_id}！歡迎下次再來！')
    return render_template('login.html')


@app.route("/from_start")
@login_required
def from_start():
    return render_template("from_start.html")


@app.route("/show_records")
@login_required
def show_records():
    python_records = CallDatabase.web_select_overall()
    return render_template("show_records.html", html_records=python_records)


# Day24: 選擇訓練紀錄
@app.route("/select_records", methods=['GET', 'POST'])
@login_required
def select_records():
    if request.method == 'POST':
        print(request.form)
        python_records = CallDatabase.web_select_specific(request.form)
        return render_template("show_records.html", html_records=python_records)
    else:
        return render_template("select_records.html")


# Day24: 舒適地選擇訓練紀錄
@app.route("/select_records_comfortable", methods=['GET', 'POST'])
@login_required
def select_records_comfortable():
    if request.method == 'POST':
        print(request.form)
        python_records = CallDatabase.web_select_specific(request.form)
        return render_template("show_records.html", html_records=python_records)
    else:
        table = CallDatabase.web_select_overall()
        table = utils.total_seconds(table)
        uniques = utils.get_unique(table)
        return render_template("select_records_comfortable.html", uniques=uniques)


# Day27: 甜甜圈！
@app.route("/donut_chart")
@login_required
def donut_chart():
    table = CallDatabase.web_select_overall()
    table = utils.total_seconds(table)
    uniques = utils.get_unique(table)
    return render_template("donut_chart.html", table=table, uniques=uniques)


# Day28: 曲線圖！
@app.route("/spline_chart")
@login_required
def spline_chart():
    table = CallDatabase.web_select_overall()
    table = utils.total_seconds(table)
    uniques = utils.get_unique(table)
    return render_template("spline_chart.html", table=table, uniques=uniques)


# Day29: 史丹佛！
@app.route("/stanford_chart")
@login_required
def stanford_chart():
    table = CallDatabase.web_select_overall()
    table = utils.total_seconds(table)
    uniques = utils.get_unique(table)
    return render_template("stanford_chart.html", table=table, uniques=uniques)


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

        reply = False

        # 召會生活人數網站
        if not reply:
            reply = PhoebeTalks.order_meal(event, event.source.user_id)

        # 召會生活人數網站
        if not reply:
            reply = PhoebeTalks.churchlife(event)

        # 湧流網站
        if not reply:
            reply = PhoebeTalks.flow(event)

        # 將資料存入表格中
        if not reply:
            reply = PhoebeTalks.insert_record(event)

        # 發送 FlexMessage
        if not reply:
            reply = PhoebeFlex.img_search_flex(event)

        # 幫忙上網找圖
        if not reply:
            reply = PhoebeTalks.img_search(event)

        # 裝飾過的回音機器人
        if not reply:
            reply = PhoebeTalks.pretty_echo(event)


if __name__ == "__main__":
    app.run()
