access_token = 'ms8iOHfGyAqNjVTMpB1BKmPNWzraMlN8fdqgGMSz53iH5YsELztSnI11MZT0nQVR+7tzmJwwYboWSaKlLNu/jCB34BXqmOudrK6DtvXMRouHmWs1I3xcRmwLtDP4DqnIdtGwiyW3sGTEuoM/r9L9zAdB04t89/1O/w1cDnyilFU='
secret = 'f834e50e169e0e4f4e2e55887836bc35'


from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

configuration = Configuration(access_token=access_token)
handler = WebhookHandler(secret)


@app.route("/", methods=['POST'])
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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        print('this is the reply')
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        ) 

if __name__ == "__main__":
    app.run()