import redis


HOST = "redis-16496.c54.ap-northeast-1-2.ec2.cloud.redislabs.com"
PWD = "khOztoKkIgUqG36QJ90NWYTZ0nIhfDgx"
PORT = "16496" 

r = redis.Redis(host = HOST, password = PWD, port = PORT)

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


while True:
    msg = input("Please enter your query date (start from 2020/3/16)(type 'quit' to exit):").strip('\n')
    if msg == 'quit' :
       break
    if msg == '':
       continue
    if str(msg) in news:
       print(news.get(str(msg)))
    else:
       print('sorry,it is not the appropriate date in our stroage')
