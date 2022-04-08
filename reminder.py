# 環境変数の読み込み(実機の場合)
# import config

import sqlite3

# 環境変数取得(実機の場合)
# CHANNEL_ACCESS_TOKEN = config.CHANNEL_ACCESS_TOKEN
# CHANNEL_SECRET = config.CHANNEL_SECRET

from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

#環境変数取得
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

def main():
    line_bot_api.broadcast(TextSendMessage(text='今日の予定をお知らせします!!'))
    # line_bot_api.push_message("Ue62ad6ba175451424f3562fc59a3f30f", TextSendMessage(text=f"{3+3}月"))
    conn=sqlite3.connect('schedule.db')
    c=conn.cursor()
    for a in c.execute("select * from schedules"):
	    line_bot_api.push_message(a[3], TextSendMessage(text=f"{a[1]}に{a[2]}の予定です!")) #(1,'鈴木','suzuki')(2,'田中','tanaka')(3,'竹田','takeda')
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    main()