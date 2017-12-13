# -*- coding: utf-8 -*-

from flask import Flask, request, abort, render_template
from flask_socketio import SocketIO, emit

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,PostbackEvent,TemplateSendMessage,ConfirmTemplate,PostbackTemplateAction
)
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

line_bot_api = LineBotApi('m8THMajfLUG1GZ8b1H32KS23AMFU22h51PEmA4iYfu8BOudlDG1jcuIHecueHvuRG6NljUxP8dx75xRoH2rJdwvDkNN29vxoDNCD0GV2qGxg5XrDRPluoBKueb44xUzetRsp93utLkBBnTyw/A/n6QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4631be1f161338a9701166797ac05603')

@app.route("/")
def index():
    return render_template("index.html")

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

    profile = line_bot_api.get_profile(event.source.user_id)
    data = {
        "name":profile.display_name,
        "pic":profile.picture_url,
        #"sign":profile.status_message,
        "msg":event.message.text
    }
    socketio.emit("msg",json.dumps(data))
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    
if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=os.environ["PORT"])
    socketio.run(app, host="0.0.0.0", port=os.environ["PORT"])