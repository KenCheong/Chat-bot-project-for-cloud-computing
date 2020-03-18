from __future__ import unicode_literals

import os
import sys
import redis
from google.cloud import translate


              


from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, VideoMessage, FileMessage, StickerMessage, StickerSendMessage
)
from linebot.utils import PY3
app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)


def load_FAQ():
    FAQ_list=[]
    fobj=open('./FAQs.txt','r')
    count=0
    for line in fobj.readlines():
        line=line.strip('\n')
        if count%2==0:
            FAQ_list.append([line,[]])
        else:
            FAQ_list[-1][1]=line
        count+=1
    return FAQ_list
HOST = "redis-19109.c8.us-east-1-3.ec2.cloud.redislabs.com"
PWD = "egM7Xs9A8EVuLcgye1wbObHKBKq2aVT7"
PORT = "19109" 

news = {}
fobj=open('./news.txt','r')
count=0
for line in fobj.readlines():
    line=line.strip('\n')
    if count%2==0:
      key=line
    else:
      news[key]=line
    count+=1
#
	
redis1 = redis.Redis(host = HOST, password = PWD, port = PORT)

redis1.set('state','0')
##global data
#state=0
FAQ_list=load_FAQ()
#print(FAQ_list)
#1/0
FAQ=None
##Read the follwing before modify the code!!!!!
'''
state
0 - start state
1 - news case
2 - FAQ case
3 - map case
4 - FAQ show question case
5 - FAQ show answer case
'''


# obtain the port that heroku assigned to this app.
heroku_port = os.getenv('PORT', None)

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)
###chat bot functions
def search_FAQ(keywords):
#    print(FAQ_list)
    #if keywords=='recommend':return FAQ_list
    if keywords=='recommend':return range(len(FAQ_list))
    FAQ=[]
    FAQ_viewcount=[]
    for i in range(len(FAQ_list)):
        if keywords in FAQ_list[i][0]:
            #FAQ.append(FAQ_list[i])
            FAQ.append(i)
    return FAQ


@app.route("/callback", methods=['POST'])
def callback():
#    state=0
    FAQ_list=load_FAQ()
    FAQ=None
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if isinstance(event.message, TextMessage):
            handle_TextMessage(event)
            #handle_TextMessage(event)
        '''
        if isinstance(event.message, ImageMessage):
            handle_ImageMessage(event)
        if isinstance(event.message, VideoMessage):
            handle_VideoMessage(event)
        if isinstance(event.message, FileMessage):
            handle_FileMessage(event)
        if isinstance(event.message, StickerMessage):
            handle_StickerMessage(event)
        '''

        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

    return 'OK'

# Handler function for Text Message
#def handle_TextMessage(event,state):
def handle_TextMessage(event):
    state=int(redis1.get('state'))
    print(event.message.text)
    print('state',state)
    msg=event.message.text
#    msg = 'You said: "' + event.message.text + '" '
#    output='Hi, to use this chat bot-\nreply 1, ask some news about coronavirus\nreply 2, ask some frequently asked questions about coronavirus\nreply 3, ask the location about nearby patients or suspected patients\n'
    '''
    msg =  event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(msg)
        #TextSendMessage(FAQ_list[0][0]+' '+str(state))
        #TextSendMessage(outputs)
    )
    return
    '''
    output =  ''
    if msg=='quit':
        state=0
        redis1.set('state',0)
    if state==0:
        if msg=='1': 
            state=1

            redis1.set('state',1)
        elif msg=='2':
            redis1.set('state',2)
            state=2
        
        elif msg=='3':
            redis1.set('state',3)
            state=3

        else:
            output='Hi, to use this chat bot-\nreply 1, ask some news about coronavirus\nreply 2, ask some frequently asked questions about coronavirus\nreply 3, ask the location about nearby patients or suspected patients\n'
            #output='Hi, to use this chat bot-reply 1, ask some news about coronavirusreply 2, ask some frequently asked questions about coronavirusreply 3, ask the location about nearby patients or suspected patients'
    if state==1:##reply news
        output='You are asking some news about coronavirus\n'
	msg = input("Please enter your query date (start from 2020/3/16)(type 'quit' to exit):").strip('\n')
	#while loop to ask about the news
	while True:	    
	    if msg == 'quit' :
	       break
	    if msg == '':
	       continue
	    if str(msg) in news:
	       print(news.get(str(msg)))
	    else:
	       print('sorry,it is not the appropriate date in our stroage')
	 redis1.set('state',0)

    elif state==2:##reply FAQ
        output='You are asking some FAQ about coronavirus,please enter your keywords or reply \'recommend\' to show some recommended questions\n'
 #       state=4
        redis1.set('state',4)

    elif state==3:##reply map
        output='You are asking the location about nearby patients or suspected patients\n'


    elif state==4:
        FAQ=search_FAQ(msg)
        print(FAQ)
        for i in range(len(FAQ)):
            output=output+str(i)+'.'+FAQ_list[FAQ[i]][0]+'\n'
        output=output+'press question number to show answer\n'
        print(' '.join([str(f) for f in FAQ]))
        #if len(FAQ)==1:
        redis1.set('faq',' '.join(['-1']+[str(f) for f in FAQ]+['99']))
#        state=5
        redis1.set('state',5)
    elif state==5:
        FAQ=str(redis1.get('faq')).split(' ')[1:-1]
        print('faq',FAQ)
        if msg.isdigit()==False:
            output='please press question number'
        else:
            output=FAQ_list[int(FAQ[int(msg)])][1]
            #output=FAQ_list[int.from_bytes(FAQ[int(msg)])][1]
            redis1.set('state',2)


    output=output+'\n if you want to use other functionalites of the chatbot,reply \'quit\''
    translate_client = translate.Client()
    result = translate_client.translate(output,target_language='zh')
    print(u'Translation: {}'.format(result['translatedText']))
    output=result['translatedText']

   # line_bot_api.reply_message(
    #    event.reply_token,
     #   TextSendMessage(msg)
    #)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(output)
    )
'''
# Handler function for Sticker Message
def handle_StickerMessage(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )

# Handler function for Image Message
def handle_ImageMessage(event):
    line_bot_api.reply_message(
	event.reply_token,
	TextSendMessage(text="Nice image!")
    )

# Handler function for Video Message
def handle_VideoMessage(event):
    line_bot_api.reply_message(
	event.reply_token,
	TextSendMessage(text="Nice video!")
    )

# Handler function for File Message
def handle_FileMessage(event):
    line_bot_api.reply_message(
	event.reply_token,
	TextSendMessage(text="Nice file!")
    )
'''



if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(host='0.0.0.0', debug=options.debug, port=heroku_port)




