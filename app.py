
# Channel Access Token
line_bot_api = LineBotApi('/0BHUlC0OvNNvYZ9cr1l3WJ5Pp+ZiYVlzsFdumK9UH1TiHwb5pTaQcoWUprrrHx9/Luqb1AfNqgoZvnEPeRshQ4PSVBaTM/siJGHsAm4jYfkhWTMqRnYhvx1DuP+pnRbjQ1lT3OLDgl51lAxRBOYmAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('6a51a346ddf37f1521e66667f11d081b')

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

#line token
channel_access_token = '{Channel_access_token}'
channel_secret = '{Channel_secret}'
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

# 監聽所有來自 /callback 的 Post Request
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
    #echo
    msg= event.message.text
    message = TextSendMessage(text=msg)
    line_bot_api.reply_message(event.reply_token,message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)