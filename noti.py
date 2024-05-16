#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback

key = '866b62ef0f3049a1a05c9f689b5e3fad&pSize=1'
TOKEN = '1831151324:AAEQTj1Yw_iZ7OkS8AjS3DN5fuDVK5LLRgY'
MAX_MSG_LENGTH = 300
baseurl = 'https://openapi.gg.go.kr/AWS1hourObser?KEY='+key
bot = telepot.Bot(TOKEN)

def getData(loc_param, date_param):
    res_list = []
    url = baseurl+'&MESURE_DE='+date_param+'&SIGUN_CD='+loc_param
    #print(url)
    res_body = urlopen(url).read()
    #print(res_body)
    soup = BeautifulSoup(res_body, 'html.parser')
    items = soup.findAll('row')
    print(items)
    for item in items:
        item = re.sub('<.*?>', '|', item.text)
        parsed = item.split('\n')
        try:
            row='지역: '+parsed[1]+'\n지역 코드: '+parsed[2]+'\n관측 날짜: '+parsed[6]+'\n관측 시간: '+parsed[7]+'h'+'\n풍속: '+parsed[12]+' m/s'+\
                '\n기온: '+parsed[13]+'℃'+"\n습도: "+parsed[14]+'%'+'\n시간 누적 장수량: '+parsed[18]+'mm'+'\n일 누적 강수량: '+parsed[19]+'mm'
        except IndexError:
            row = item.replace('|', ',')

        if row:
            res_list.append(row.strip())
    return res_list

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def run(date_param, param='434'):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user, param = data[0], data[1]
        print(user, date_param, param)
        res_list = getData( param, date_param )
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user,r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print( str(datetime.now()).split('.')[0], r )
                if len(r+msg)+1>MAX_MSG_LENGTH:
                    sendMessage( user, msg )
                    msg = r+'\n'
                else:
                    msg += r+'\n'
        if msg:
            sendMessage( user, msg )
    conn.commit()

if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', TOKEN )

    pprint( bot.getMe() )

    run(current_month)
