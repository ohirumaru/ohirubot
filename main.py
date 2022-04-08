# 環境変数の読み込み(実機の場合)
# import config

# コピペゾーン
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent
)
import os

import sqlite3

app = Flask(__name__)

#環境変数取得
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

# 環境変数取得(実機の場合)
# CHANNEL_ACCESS_TOKEN = config.CHANNEL_ACCESS_TOKEN
# CHANNEL_SECRET = config.CHANNEL_SECRET

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    temp=event.message.text.strip().split(',')
    if len(temp) == 2:
        va=0
        ti=temp[0]
        co=temp[1]
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text='以下の内容で登録します'), TextSendMessage(text=f"日付:{ti}, 予定名:{co}")])
        conn=sqlite3.connect('schedule.db')
        c=conn.cursor()
        user_id=event.source.user_id
        c.execute(f"INSERT INTO schedules VALUES ({va},{ti},{co},{user_id})")
        conn.commit()
        conn.close()
    elif len(temp) == 3:
        va=1
        ti=temp[0]+temp[2]
        co=temp[1]
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text='以下の内容で登録します'), TextSendMessage(text=f"日付:{temp[0]}, 予定名:{co}, 時刻{temp[2]}")])
        conn=sqlite3.connect('schedule.db')
        c=conn.cursor()
        user_id=event.source.user_id
        c.execute(f"INSERT INTO schedules VALUES ({va},{ti},{co},{user_id})")
        conn.commit()
        conn.close()
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="形式が正しくないため登録できませんでした。。。"))

# handler.add(): 引数にlinebotのリクエストのイベントを指定
@handler.add(FollowEvent)# FollowEventをimportするのを忘れずに！
def follow_message(event):# event: LineMessagingAPIで定義されるリクエストボディ
    # print(event)
    if event.type == "follow":# フォロー時のみメッセージを送信
        line_bot_api.reply_message(
            event.reply_token,# イベントの応答に用いるトークン
            TextSendMessage(text="フォローありがとうございます！\n日付, 予定名, (時刻)のように送信してください。予定の日に通知いたします!"))

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)