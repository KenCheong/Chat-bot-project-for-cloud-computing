# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 12:13:14 2020

@author: cc
"""

import redis


HOST = "redis-11363.c1.asia-northeast1-1.gce.cloud.redislabs.com"
PWD = "1nOA0St0I7p9pQqu8HkQ18XqDfnoPeoL"
PORT = "11363" 

r = redis.Redis(host = HOST, password = PWD, port = PORT)

hospital = {}
fobj=open('./hospital.txt','r')
count=0
for line in fobj.readlines():
    line=line.strip('\n')
    if count%2==0:
      key=line
    else:
      hospital[key]=line
    count+=1


while True:
    msg = input("Please enter your district (such as hong kong, kowloon, new territories)(type 'quit' to exit):").strip('\n')
    if msg == 'quit' :
       break
    if msg == '':
       continue
    if str(msg) in hospital:
       print(hospital.get(str(msg)))
    else:
       print('sorry,can not find the hospital in our stroage')