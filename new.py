#from urllib.request import urlopen
from xml.dom.minidom import parse, parseString
from xml.etree import ElementTree
from PIL import ImageTk,Image as image  #이미지 크기 조정  사용하려면 파이참 아래의 Terminal 클릭하고 pip install pillow입력

import urllib
import urllib.request
import http.client
import time

# -*- coding: cp949 -*-
import mimetypes
import mysmtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from tkinter import *
import threading
import sys
from tkinter import messagebox
# pip install folium
import folium
# pip install cefpython3==66.1
from cefpython3 import cefpython as cef

import tkinter.font as tkFont
import tkinter as tk
from geopy.geocoders import Nominatim
from pprint import pprint
import webbrowser
import spam  #spam.pyd를 python/Lib에 넣어야함

from teller import *

rectm=[]
recws=[]
rec_sN=[]
rec_sI=[]
rec_sL=[]
rec_sK=[]

frame1_width = 750
frame1_height = 500
frame2_width = 520
frame2_height = 400
canvas_width = frame2_width-15
canvas_height = frame2_height-15

class maingui:

    def __init__(self):
        window = Tk()
        window.title('날씨에 맞는 옷차림 추천')
        window.configure(bg = 'white')
        #글꼴 추가
        self.font = tkFont.Font(family="경기천년제목_Bold.ttf", size=13, weight="bold", slant="italic")
        self.font1 = tkFont.Font(family="경기천년제목_Bold.ttf", size=10, weight="bold", slant="roman")
        self.font2 = tkFont.Font(family="경기천년제목_Bold.ttf", size=16, weight="bold", slant="roman")
        self.font2_2 = tkFont.Font(family="경기천년제목_Bold.ttf", size=16, weight="bold", slant="italic")

        self.font3 = tkFont.Font(family="경기천년제목_Bold.ttf", size=13, weight="bold", slant="roman")
        self.font4 = tkFont.Font(family="경기천년제목_Bold.ttf", size=50, weight="bold", slant="roman")

        frame = Frame(window, width=frame1_width, height=frame1_height)
        frame['relief']= 'flat'
        frame['borderwidth'] = 0
        frame.pack()

        # 이미지 리사이즈
        frame_im = image.open('resource/제목.png')
        frame2_im = image.open('resource/배경화면3.png')

        resizeimg=frame_im.resize((frame1_width, frame1_height), image.ANTIALIAS)
        frame1_bg=ImageTk.PhotoImage(resizeimg)

        resizeimg2 = frame2_im.resize((frame2_width, 500), image.ANTIALIAS)
        frame2_bg=ImageTk.PhotoImage(resizeimg2)

        resizeimg2_2 = frame_im.resize((frame2_width, 600), image.ANTIALIAS)
        frame2_2_bg = ImageTk.PhotoImage(resizeimg2_2)

        Label(frame,image = frame1_bg).place(x=0,y=0)
        self.entry = Entry(frame, width=50 ,foreground ='gray', borderwidth=4,insertbackground = 'white',selectbackground='gray',selectforeground = 'black' ,background = 'white',relief='solid',font = self.font,insertontime = 600,insertofftime = 300)

        self.entry.insert(0, '시흥')
        self.entry.place(x=70, y=20)

        #Label(frame,text = '오늘의 날씨 정보' ,font = font).place(x=600,y=70)
        #검색버튼 크기조정
        button_width= 50
        button_height= 40

        enter_image = PhotoImage(file="resource/검색40.png")
        gmail_image = PhotoImage(file="resource/메일.png")
        self.silid_size = '4'
        x1 = 550
        y1 = 15
        self.search_button = Button(frame, text='엔터', height = 30,width=30,image = enter_image,relief='solid',overrelief ='flat',bd = self.silid_size,padx = 0,pady = 0, command=self.search).place(x=x1,y=y1)
        self.gmail_button = Button(frame, text='이메일', height = 30,width=30,image = gmail_image,relief='solid',overrelief ='flat',bd = self.silid_size,padx = 0,pady = 0, command=self.gmail).place(x=x1+60,y=y1)

        x2=30
        y2=70
        self.frame2 = Frame(window, width=frame2_width, height=frame2_height)
        self.frame2['relief']= 'solid'

        self.frame2['borderwidth'] = 5
        self.frame2.place(x=x2,y=y2)

        #Label(self.frame2, image=frame2_2_bg).place(x=0, y=97)
        self.canvas = Canvas(self.frame2, width=frame2_width-15, height=frame2_height-15, bg = 'white')
        self.canvas.place(x=0,y=0)
        #self.canvas.create_image(30, 0, anchor='nw', image=frame2_bg) #캔버스 배경

        weatherx=100
        weathery=90
        night = image.open('resource/night.png')# 밤
        resizeimg3 = night.resize((weatherx, weathery), image.ANTIALIAS)
        self.night = ImageTk.PhotoImage(resizeimg3)
        sunny = image.open('resource/sunny.png')  # 낮
        resizeimg4 = sunny.resize((weatherx, weathery), image.ANTIALIAS)
        self.sunny = ImageTk.PhotoImage(resizeimg4)
        rain = image.open('resource/rain.png')  # 비
        resizeimg5 = rain.resize((weatherx, weathery), image.ANTIALIAS)
        self.rainimg = ImageTk.PhotoImage(resizeimg5)


        rw = 135
        rh = 145
        c1 = image.open('resource/28이상.png')
        resizeimg6 =c1.resize((rw,rh),image.ANTIALIAS)
        self.cloth1 = ImageTk.PhotoImage(resizeimg6)

        c2 = image.open('resource/23~27.png')
        resizeimg7 = c2.resize((rw, rh), image.ANTIALIAS)
        self.cloth2 = ImageTk.PhotoImage(resizeimg7)

        c3 = image.open('resource/20~22.png')
        resizeimg8 = c3.resize((rw, rh), image.ANTIALIAS)
        self.cloth3 = ImageTk.PhotoImage(resizeimg8)

        c4 = image.open('resource/17~19.png')
        resizeimg9 = c4.resize((rw, rh), image.ANTIALIAS)
        self.cloth4 = ImageTk.PhotoImage(resizeimg9)

        c5 = image.open('resource/12~16.png')
        resizeimg10 = c5.resize((rw, rh), image.ANTIALIAS)
        self.cloth5 = ImageTk.PhotoImage(resizeimg10)

        c6 = image.open('resource/9~11.png')
        resizeimg11 = c6.resize((rw, rh), image.ANTIALIAS)
        self.cloth6 = ImageTk.PhotoImage(resizeimg11)

        c7 = image.open('resource/5~8.png')
        resizeimg12 = c7.resize((rw, rh), image.ANTIALIAS)
        self.cloth7 = ImageTk.PhotoImage(resizeimg12)

        c8 = image.open('resource/4이하.png')
        resizeimg13 = c8.resize((rw, rh), image.ANTIALIAS)
        self.cloth8 = ImageTk.PhotoImage(resizeimg13)

        c9 = image.open('resource/지도버튼.png')
        resizeimg14 = c9.resize((20, 20), image.ANTIALIAS)
        self.map_button_img = ImageTk.PhotoImage(resizeimg14)

        self.frame3 = Frame(window, width=60, height=52*4-2)
        self.frame3.place(x=550,y=100)
        #frame3_bg = PhotoImage(file='resource/제목.png')
        #Label(self.frame3, image=frame3_bg).place(x=0, y=0)

        #버튼 이미지넣기
        home_image = PhotoImage(file = "resource/홈.png")
        graph_image = PhotoImage(file = "resource/그래프.gif")
        hotplace_image = PhotoImage(file = "resource/명소.png")
        telegram_image = PhotoImage(file = "resource/텔레그램.png")
        bestfashion_image = PhotoImage(file = "resource/추천의상.png")

        button_x=0
        button_y=0
        Button(self.frame3, text='지도',relief='solid',overrelief ='ridge',bd = self.silid_size,background='white',padx = 0,pady = 0, width=button_width, height=button_height,image = home_image ,command=self.Map).place(x=button_x, y=button_y)
        Button(self.frame3, text='그래프', relief='solid',overrelief ='ridge',bd = self.silid_size,background='white',padx = 0,pady = 0,width=button_width, height=button_height,image = graph_image, command=self.graph).place(x=button_x, y=button_y+52)
        Button(self.frame3, text='명소',relief='solid',overrelief ='ridge',bd = self.silid_size,background='white',padx = 0,pady = 0, width=button_width, height=button_height,image = hotplace_image, command=self.spot).place(x=button_x, y=button_y+52*2)
        Button(self.frame3,text='텔레그램', relief='solid',overrelief ='ridge',bd = self.silid_size,background='white',padx = 0,pady = 0,width=button_width, height=button_height,image = telegram_image, command=self.tele).place(x=button_x, y=button_y+52*3)
        self.label=Label(window, text='추천 옷차림', width=130, height=140,image = bestfashion_image)
        self.label.place(x=602, y=370)


        self.mapwidth=700
        self.mapheight=600 #320
        window.mainloop()

    def load(self,strXml):
        from xml.etree import ElementTree
        tree = ElementTree.fromstring(strXml)
        itemElements = tree.iter("row")

        for item in itemElements:
            self.tp = item.find("TP_INFO")  # 기온
            self.ws = item.find("WS_INFO")  # 풍속
            self.rain = item.find("RAINF_1HR_INFO")  # 시간누적강수량
            if len(self.ws.text) > 0:
                self.tm = spam.temp(float(self.tp.text), float(self.ws.text))
            rectm.append(float(self.tp.text))
            recws.append(float(self.ws.text))

    def load_2(self,strXml):
        from xml.etree import ElementTree
        tree = ElementTree.fromstring(strXml)
        itemElements = tree.iter("item")

        for item in itemElements:
            self.sName = item.find("galTitle") #이름
            if len(self.sName.text) > 0:
                rec_sN.append(str(self.sName.text))
            self.sSpot_img = item.find("galWebImageUrl")
            self.sLocation = item.find("galPhotographyLocation") #위치
            self.sKeywords = item.find("galSearchKeyword") #검색 키워드

            sI=self.sSpot_img.text
            sL=self.sLocation.text
            sK=self.sKeywords.text.split(",")

            rec_sI.append(sI)
            rec_sL.append(sL)

            for i in range(len(sK)):
                rec_sK.append(sK[i])
    def gmail(self):
        # global value
        host = "smtp.gmail.com"  # Gmail STMP 서버 주소.
        port = "587"

        senderAddr = "5seunghun32@gmail.com"  # 보내는 사람 email 주소.
        recipientAddr = "5seunghun@naver.com"  # 받는 사람 email 주소.

        msg = MIMEBase("multipart", "alternative")
        msg['Subject'] = "오늘 뭐입지? 의상추천"
        msg['From'] = senderAddr
        msg['To'] = recipientAddr

        # MIME 문서를 생성합니다.

        imageFD = open(self.imageFileName, 'rb')  # image 파일 오픈 후 MIMEImage생성
        ImagePart = MIMEImage(imageFD.read(),Name=self.imageFileName)
        imageFD.close()

        html = "<html><header></header><body><b>오늘 뭐입지? 의상추천</b><br><p>지역: " + self.entry.get() + '시</p><p>온도: ' + self.tp.text + " ℃</p><p>풍속: " + self.ws.text + ' m/s</p><p>체감 기온: {0:.3f}'.format(
            self.tm) \
               + ' ℃</p><p>강수량: ' + self.rain.text + " mm</p><p>　</p><p> 추천 명소: "+self.sName.text+"</p>"+self.sLocation.text+"<p></p><img src=\"" + self.sSpot_img.text + "\"/><p>　</p><p>추천 의상</p></body></html>"
        part2 = MIMEText(html, 'html')

        msg.add_header('Content-Disposition', 'attachment', filename=self.imageFileName)

        # 만들었던 mime을 MIMEBase에 첨부 시킨다.

        msg.attach(ImagePart)
        msg.attach(part2)


        # 메일을 발송한다.
        s = mysmtplib.MySMTP(host, port)
        # s.set_debuglevel(1)        # 디버깅이 필요할 경우 주석을 푼다.
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login("5seunghun32@gmail.com", "5seunghun")
        s.sendmail(senderAddr, [recipientAddr], msg.as_string())
        s.close()

    def search(self):
        server = "openapi.gg.go.kr"
        conn = http.client.HTTPSConnection(server)
        if self.entry.get()=='안양':
            conn.request("GET", "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=434")
        elif self.entry.get()=='과천':
            conn.request("GET", "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=116")
        elif self.entry.get()=='의왕':
            conn.request("GET", "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=445")
        elif self.entry.get()=='광주':
            conn.request("GET", "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=460")
        elif self.entry.get()=='고양':
            conn.request("GET", "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=589")
        else:
            adress = urllib.parse.quote(self.entry.get()+'시')
            conn.request("GET", "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SIGUN_NM="+adress)
        req = conn.getresponse()
        self.load(req.read())
        self.fasihon()
        self.Map()

    def mapwindow(self):

         app = Nominatim(user_agent='tutorial')
         if self.entry.get()=='광주':
             location = app.geocode("경기"+self.entry.get()+"시청")
         else:
            location = app.geocode(self.entry.get()+"시청") #위도 경도 추출


         m = folium.Map(location=[location.latitude, location.longitude], zoom_start=14)
         folium.Marker([location.latitude, location.longitude]).add_to(m)
         url = 'map.html'
         m.save(url)
         webbrowser.open(url)


    def Map(self):
        self.canvas.delete('canvas')
        now=time.localtime()
        h = canvas_height - 100 + 5
        fh =25
        tx = 125
        tx2 = 300
        tx3=15
        self.canvas.create_text(tx, h, fill = 'gray',text='현재 온도 ℃             ',anchor=tk.SW,font=self.font1, tags='canvas')
        self.canvas.create_text(tx2, h, fill = 'black',text='현재 시간              ' + str(now.tm_hour)+':'+str(now.tm_min),anchor=tk.SW,font=self.font1, tags='canvas')
        self.canvas.create_text(tx2, h+fh,fill = 'red', text='체감 기온              {0:.3f}'.format(self.tm)+' ℃',font=self.font1,anchor=tk.SW, tags='canvas')
        self.canvas.create_text(tx2, h+fh*2,fill = 'green', text='현재 풍속              ' + self.ws.text+' m/s', font=self.font1,anchor=tk.SW,tags='canvas')  # m/s
        # 13.12 + 0.6215 * T - 11.37 * V ^ (0.16) + 0.3965 * V ^ (0.16) * T
        self.canvas.create_text(tx2, h+fh*3,fill = 'blue', font=self.font1,anchor=tk.SW,text='시간 누적 강수량   {0:.1f}'.format(float(self.rain.text)) + 'mm', tags='canvas')
        self.canvas.create_text(tx, h,text= self.tp.text, font=self.font4,anchor=tk.NW,tags='canvas')  # ℃
        self.canvas.create_line(tx2-20,canvas_height*2//3,tx2-20 ,canvas_height,width = 4,tags='canvas')
        if(float(self.rain.text)>0):
            self.canvas.create_image(tx3, h, anchor=NW, image=self.rainimg, tags='canvas')
        else:
            if(6<=now.tm_hour<=19):
                self.canvas.create_image(tx3, h-10, anchor=NW, image=self.sunny, tags='canvas')
            else:
                self.canvas.create_image(tx3, h, anchor=NW, image=self.night, tags='canvas')




        img = image.open('resource/지역/'+self.entry.get()+'.png')
        resizeimg = img.resize((canvas_width, canvas_height*2//3), image.ANTIALIAS)
        self.imgmap = ImageTk.PhotoImage(resizeimg)
        self.canvas.create_image(0,0,anchor=NW,image=self.imgmap,tags='canvas')
        #self.button=Button(self.canvas,width=7,height=3,command=self.mapwindow,text='지도 보기',image = self.map_button_img)
        self.button=Button(self.canvas, text = '엔터', height = 20, width = 20,relief='flat', image = self.map_button_img, bg = 'white', overrelief = 'flat', bd = self.silid_size, padx = 0, pady = 0, command = self.mapwindow)
        self.button.place(x=0,y=0)



    def fasihon(self):
        T = float(self.tm)
        w = 130
        h = 140
        x = 20
        y = 290
        if T >= 28.0:
            self.label.configure(image=self.cloth1)
            self.imageFileName='resource/28이상.png'
        elif 23.0<= T:
            self.label.configure(image=self.cloth2)
            self.imageFileName = 'resource/23~27.png'
        elif 20.0<= T:
            self.label.configure(image=self.cloth3)
            self.imageFileName = 'resource/20~22.png'
        elif 17.0 <= T :
            self.label.configure(image=self.cloth4)
            self.imageFileName = 'resource/17~19.png'
        elif 12.0 <= T :
            self.label.configure(image=self.cloth5)
            self.imageFileName = 'resource/12~16.png'
        elif 9.0 <= T :
            self.label.configure(image=self.cloth6)
            self.imageFileName = 'resource/9~11.png'
        elif 5.0 <= T :
            self.label.configure(image=self.cloth7)
            self.imageFileName = 'resource/5~8.png'
        else:
            self.label.configure(image=self.cloth8)
            self.imageFileName = 'resource/4이하.png'

    def graph(self):
        self.button.destroy()
        rectm.clear()
        recws.clear()
        adress = urllib.parse.quote(self.entry.get() + '시')
        server = "openapi.gg.go.kr"
        conn = http.client.HTTPSConnection(server)
        now = time.localtime()
        if now.tm_hour>=10:
            for i in range(10):
                if now.tm_hour-i<10:
                    if self.entry.get() == '안양':
                        conn.request("GET", "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=434&MESURE_TM=0" + str(
                        now.tm_hour - i) )
                    elif self.entry.get() == '과천':
                        conn.request("GET", "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=116&MESURE_TM=0" + str(
                        now.tm_hour - i) )
                    elif self.entry.get() == '의왕':
                        conn.request("GET", "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=445&MESURE_TM=0" + str(
                        now.tm_hour - i) )
                    elif self.entry.get() == '광주':
                        conn.request("GET", "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=460&MESURE_TM=0" + str(
                        now.tm_hour - i) )
                    elif self.entry.get() == '고양':
                        conn.request("GET", "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=589&MESURE_TM=0" + str(
                        now.tm_hour - i) )
                    else:
                        conn.request("GET", "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&MESURE_TM=0" + str(
                        now.tm_hour - i) + "&pSize=1&SIGUN_NM=" + adress)
                else:
                    if self.entry.get() == '안양':
                        conn.request("GET", "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=434&MESURE_TM=" + str(
                        now.tm_hour - i) )
                    elif self.entry.get() == '과천':
                        conn.request("GET", "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=116&MESURE_TM=" + str(
                        now.tm_hour - i) )
                    elif self.entry.get() == '의왕':
                        conn.request("GET", "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=445&MESURE_TM=" + str(
                        now.tm_hour - i) )
                    elif self.entry.get() == '광주':
                        conn.request("GET", "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=460&MESURE_TM=" + str(
                        now.tm_hour - i) )
                    elif self.entry.get() == '고양':
                        conn.request("GET", "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=589&MESURE_TM=" + str(
                        now.tm_hour - i) )
                    else:
                        conn.request("GET", "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&MESURE_TM="+str(
                        now.tm_hour-i)+"&pSize=1&SIGUN_NM=" + adress)
                req = conn.getresponse()
                self.load(req.read())
        else:
            for i in range(now.tm_hour+1):
                if now.tm_hour - i < 10:
                    if self.entry.get() == '안양':
                        conn.request("GET",
                                     "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=434&MESURE_TM=0" + str(
                                         now.tm_hour - i))
                    elif self.entry.get() == '과천':
                        conn.request("GET",
                                     "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=116&MESURE_TM=0" + str(
                                         now.tm_hour - i))
                    elif self.entry.get() == '의왕':
                        conn.request("GET",
                                     "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=445&MESURE_TM=0" + str(
                                         now.tm_hour - i))
                    elif self.entry.get() == '광주':
                        conn.request("GET",
                                     "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=460&MESURE_TM=0" + str(
                                         now.tm_hour - i))
                    elif self.entry.get() == '고양':
                        conn.request("GET",
                                     "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=589&MESURE_TM=0" + str(
                                         now.tm_hour - i))
                    else:
                        conn.request("GET", "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&MESURE_TM=0" + str(
                            now.tm_hour - i) + "&pSize=1&SIGUN_NM=" + adress)
                else:
                    if self.entry.get() == '안양':
                        conn.request("GET",
                                     "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=434&MESURE_TM=" + str(
                                         now.tm_hour - i))
                    elif self.entry.get() == '과천':
                        conn.request("GET",
                                     "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=116&MESURE_TM=" + str(
                                         now.tm_hour - i))
                    elif self.entry.get() == '의왕':
                        conn.request("GET",
                                     "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=445&MESURE_TM=" + str(
                                         now.tm_hour - i))
                    elif self.entry.get() == '광주':
                        conn.request("GET",
                                     "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=460&MESURE_TM=" + str(
                                         now.tm_hour - i))
                    elif self.entry.get() == '고양':
                        conn.request("GET",
                                     "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=589&MESURE_TM=" + str(
                                         now.tm_hour - i))
                    else:
                        conn.request("GET", "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&MESURE_TM=" + str(
                            now.tm_hour - i) + "&pSize=1&SIGUN_NM=" + adress)
                req = conn.getresponse()
                self.load(req.read())

        mx = 10
        self.canvas.delete('canvas')
        self.canvas.create_rectangle(20-mx, 10, 50-mx, 20, fill='orange', tags='canvas')
        self.canvas.create_rectangle(20-mx, 30, 50-mx, 40, fill='blue', tags='canvas')
        self.canvas.create_text(65-mx, 15, text="기온", font = self.font1,tags='canvas')
        self.canvas.create_text(65-mx, 35, text="풍속",font = self.font1, tags='canvas')

        Maxt=max(rectm)
        Maxw=max(recws)
        w = canvas_width
        h = canvas_height-20
        rw=56
        rx = 42
        for i in range(len(rectm)):
            self.canvas.create_rectangle(50+rw*i-rx,h-200*rectm[i]/Maxt,73+rw*i-rx,h,fill='orange',tags='canvas')
            self.canvas.create_text(73+rw*i-rx,h+10,font = self.font1,text=now.tm_hour-i,tags='canvas')
            self.canvas.create_text(63 + rw * i-rx, h-200*rectm[i]/Maxt-10, font = self.font1,text=rectm[i], tags='canvas')
            self.canvas.create_rectangle(73+rw*i-rx, h-100 * recws[i]/Maxw, 40 + rw * (i + 1)-rx, h, fill='blue',tags='canvas')
            self.canvas.create_text(85 + rw * i-rx, h-100 * recws[i]/Maxw - 10,font = self.font1, text=recws[i], tags='canvas')

    def spot(self):
        self.button.destroy()
        from io import BytesIO
        #from PIL import ImageTk, Image as imge
        conn = http.client.HTTPConnection("api.visitkorea.or.kr")
        if(self.entry.get()=='의정부' or self.entry.get()=='과천' or self.entry.get()=='이천'): #의정부 과천 이천은 앞에 경기도 붙이고 검색하면 안나옴
            hangul_utf8 = urllib.parse.quote(self.entry.get())
        else:
            hangul_utf8 = urllib.parse.quote("경기도 "+self.entry.get())  #나머지는 "경기도 "+지역명으로 검색
        conn.request("GET","/openapi/service/rest/PhotoGalleryService/gallerySearchList?serviceKey=jTzcx4rDMB57ckLLHIqWzgXBQxtYj%2Blj7LFOetkB3SdjIrphA%2FcIQCz3Wk0n40YuUmU1%2FbDUquRyXbtI3Xn6SQ%3D%3D&pageNo=1&numOfRows=1&MobileOS=ETC&MobileApp=AppTest&arrange=B&keyword=" + hangul_utf8)
        req = conn.getresponse()
        self.load_2(req.read().decode('utf-8'))

        with urllib.request.urlopen(self.sSpot_img.text) as u:
            raw_data=u.read()
        im = image.open(BytesIO(raw_data))
        i = ImageTk.PhotoImage(im)

        self.canvas.delete('canvas')
        resizeimg3 = im.resize((canvas_width, canvas_height-150), image.ANTIALIAS)
        self.location = ImageTk.PhotoImage(resizeimg3)

        w = canvas_height-150 + 30
        h = canvas_height//2
        th = 50
        self.canvas.create_text(12, 20,anchor=NW,text='"오늘 뭐 하지.. 날씨도 좋은데, ',font=self.font2_2,tags='canvas',fill='black')
        self.canvas.create_text(canvas_width-12, 50,anchor=NE,text=self.sName.text + '나 갈까?"',font=self.font2_2,tags='canvas',fill='black')

        #self.canvas.create_text(w, h-th, anchor=W,text='- '+self.sName.text+' -',font=self.font3,tags='canvas',fill='black')
        self.canvas.create_text(canvas_width//2, canvas_height-50,anchor=N, text='위치 : '+self.sLocation.text,font=self.font3,tags='canvas',fill='gray')
        num = 0
        for i in range(len(rec_sK)):
            self.canvas.create_text(5+num*13, canvas_height,anchor=SW, text='#' + str(rec_sK[i]) +' ',font=self.font3,tags='canvas',fill='blue')
            num += len(rec_sK[i])+2
        self.canvas.create_image(0, 80, anchor=NW, image=self.location, tags='canvas')

    def tele(self):
        self.button.destroy()
        self.canvas.delete('canvas')
        self.canvas.create_text(canvas_width//2+20, canvas_height//2, text='Loading . . .',font = self.font2,fill='blue',tags='canvas')

        today = date.today()
        current_month = today.strftime('%Y%m')

        print('[', today, ']received token :', noti.TOKEN)

        bot = telepot.Bot(noti.TOKEN)
        pprint(bot.getMe())

        bot.message_loop(handle)

        print('Listening...')


maingui()
