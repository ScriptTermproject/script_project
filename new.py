from urllib.request import urlopen
from xml.dom.minidom import parse, parseString
from xml.etree import ElementTree
from PIL import ImageTk,Image as image  #이미지 크기 조정  사용하려면 파이참 아래의 Terminal 클릭하고 pip install pillow입력

import urllib
import urllib.request
import http.client
import time

from tkinter import *
#import io import BytesIO

rectm=[]
recws=[]
rec_sN=[]
rec_sI=[]
rec_sL=[]
rec_sK=[]

frame1_width = 770
frame2_height = 65
frame2_width = 600
frame3_width = frame1_width - frame2_width

class maingui:

    def __init__(self):
        window = Tk()
        window.title('날씨에 맞는 옷차림 추천')

        frame = Frame(window, width=frame1_width, height=frame2_height)
        frame.pack()

        # 이미지 리사이즈
        frame_im = image.open('resource/배경화면.png')
        resizeimg=frame_im.resize((frame1_width, 248), image.ANTIALIAS)
        frame1_bg=ImageTk.PhotoImage(resizeimg)

        resizeimg2 = frame_im.resize((frame2_width, 400), image.ANTIALIAS)
        frame2_bg=ImageTk.PhotoImage(resizeimg2)

        Label(frame,image = frame1_bg).place(x=0,y=0)
        self.entry = Entry(frame, width=60)
        # entry.insert(0,'검색할 지역을 시 단위로 입력하세요')
        self.entry.insert(0, '시흥')
        self.entry.place(x=130, y=30)

        #검색버튼 크기조정
        button_width= 60
        button_height= 50

        enter_image = PhotoImage(file="resource/검색40.png")
        self.search_button = Button(frame, text='엔터', width=40,image = enter_image, command=self.search).place(x=frame2_width,y=(frame2_height-40)/2)

        bottom_GUI_height = 450
        frame2 = Frame(window, width=frame2_width, height=bottom_GUI_height)
        frame2.pack(side=LEFT)
        Label(frame2, image=frame2_bg).place(x=0, y=100)
        self.canvas = Canvas(frame2, width=frame2_width+100, height=400)
        self.canvas.place(x=-30,y=0)
        self.canvas.create_image(30, 0, anchor='nw', image=frame2_bg) #캔버스 배경

        night = image.open('resource/night.png')# 밤
        resizeimg3 = night.resize((110, 100), image.ANTIALIAS)
        self.night = ImageTk.PhotoImage(resizeimg3)
        sunny = image.open('resource/sunny.png')  # 낮
        resizeimg4 = sunny.resize((110, 100), image.ANTIALIAS)
        self.sunny = ImageTk.PhotoImage(resizeimg4)
        rain = image.open('resource/rain.png')  # 비
        resizeimg5 = rain.resize((110, 100), image.ANTIALIAS)
        self.rain = ImageTk.PhotoImage(resizeimg5)

        self.cloth1 = PhotoImage('resource/28이상.png')
        self.cloth2 = PhotoImage('resource/23~27.png')
        self.cloth3 = PhotoImage('resource/20~22.png')
        self.cloth4 = PhotoImage('resource/17~19.png')
        self.cloth5 = PhotoImage('resource/12~16.png')
        self.cloth6 = PhotoImage('resource/9~11.png')
        self.cloth7 = PhotoImage('resource/5~8.png')
        self.cloth8 = PhotoImage('resource/4이하.png')


        frame3 = Frame(window, width=frame3_width, height=bottom_GUI_height)
        frame3.pack(side=LEFT)
        frame3_bg = PhotoImage(file='resource/제목.png')
        Label(frame3, image=frame3_bg).place(x=0, y=0)

        #버튼 이미지넣기
        home_image = PhotoImage(file = "resource/홈.png")
        graph_image = PhotoImage(file = "resource/그래프.gif")
        hotplace_image = PhotoImage(file = "resource/명소.png")
        telegram_image = PhotoImage(file = "resource/텔레그램.png")
        bestfashion_image = PhotoImage(file = "resource/추천의상.png")

        button_x=0
        button_y=26
        Button(frame3, text='지도', width=button_width, height=button_height,image = home_image ,command=self.Map).place(x=0, y=button_y)
        Button(frame3, text='그래프', width=button_width, height=button_height,image = graph_image, command=self.graph).place(x=0, y=button_y+55)
        Button(frame3, text='명소', width=button_width, height=button_height,image = hotplace_image, command=self.spot).place(x=0, y=button_y+110)
        Button(frame3, text='텔레그램', width=button_width, height=button_height,image = telegram_image, command=self.tele).place(x=0, y=button_y+165)
        Button(frame3, text='추천 옷차림', width=130, height=140,image = bestfashion_image, command=self.fasihon).place(x=19, y=290)


        window.mainloop()

    def load(self,strXml):
        from xml.etree import ElementTree
        tree = ElementTree.fromstring(strXml)
        itemElements = tree.iter("row")

        for item in itemElements:
            self.tp = item.find("TP_INFO") #기온
            self.ws = item.find("WS_INFO") #풍속
            self.rain=item.find("RAINF_1HR_INFO") #시간누적강수량
            if len(self.ws.text) > 0 :
                T=float(self.tp.text)
                V=(float(self.ws.text)*3.6) ** (0.16)
                self.tm=13.12 + 0.6215 * T - 11.37 * V + 0.3965 * V * T
            rectm.append(T)
            recws.append(float(self.ws.text))

    def load_2(self,strXml):
        from xml.etree import ElementTree
        tree = ElementTree.fromstring(strXml)
        itemElements = tree.iter("item")

        for item in itemElements:
            self.sName = item.find("galTitle") #이름
            if len(self.sName.text) > 0:
                rec_sN.append(str(self.sName.text))
            # self.sSpot_img = item.find("galWebImageUrl")
            #self.sLocation = item.find("galPhotographyLocation") #위치
            #self.sKeywords = item.find("galSearchKeyword") #검색 키워드

                #sI=self.sSpot_img.text
                #sL=self.sLocation.text
                #sK=self.sKeywords.text

            #rec_sI.append(sI)
            #rec_sL.append(sL)
            #rec_sK.append(sK)

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
            server = "openapi.gg.go.kr"
            conn = http.client.HTTPSConnection(server)
            conn.request("GET", "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SIGUN_NM="+adress)
        req = conn.getresponse()
        self.load(req.read())
        self.Map()

    def Map(self):
        self.canvas.delete('canvas')
        now=time.localtime()
        self.canvas.create_text(90, 300, text='현재 시간: ' + str(now.tm_hour)+':'+str(now.tm_min), tags='canvas')
        self.canvas.create_text(90, 330, text='현재 온도: ' + self.tp.text+' ℃', tags='canvas')  # ℃
        self.canvas.create_text(90, 360, text='현재 풍속: ' + self.ws.text+' m/s', tags='canvas')  # m/s
        # 13.12 + 0.6215 * T - 11.37 * V ^ (0.16) + 0.3965 * V ^ (0.16) * T
        self.canvas.create_text(90, 390, text='체감 기온: {0:.3f}'.format(self.tm)+' ℃', tags='canvas')
        self.canvas.create_text(290, 390, text='시간 누적 강수량: {0:.1f}'.format(float(self.rain.text)) + 'mm', tags='canvas')
        if(float(self.rain.text)>0):
            self.canvas.create_image(380, 300, anchor=NW, image=self.rain, tags='canvas')
        if(6<=now.tm_hour<=19):
            self.canvas.create_image(380, 300, anchor=NW, image=self.sunny, tags='canvas')
        else:
            self.canvas.create_image(380, 300, anchor=NW, image=self.night, tags='canvas')

        self.canvas.create_text(300, 160, text='지도',tags='canvas')

    def fasihon(self):
        T = float(self.tp.text)
        if T >= 28.0:
            self.canvas.create_image(380, 300, anchor=NW, image=self.cloth1, tags='canvas')
        elif 23.0<= T<27.0:
                self.canvas.create_image(380, 300, anchor=NW, image=self.cloth2, tags='canvas')
        elif 20.0<= T < 23.0:
                self.canvas.create_image(380, 300, anchor=NW, image=self.cloth3, tags='canvas')
        elif 17.0 <= T < 20.0:
                self.canvas.create_image(380, 300, anchor=NW, image=self.cloth4, tags='canvas')
        elif 12.0 <= T < 17.0:
                self.canvas.create_image(380, 300, anchor=NW, image=self.cloth5, tags='canvas')
        elif 9.0 <= T < 11.0:
                self.canvas.create_image(380, 300, anchor=NW, image=self.cloth6, tags='canvas')
        elif 5.0 <= T < 9.0:
                self.canvas.create_image(380, 300, anchor=NW, image=self.cloth7, tags='canvas')
        elif T < 5.0:
            self.canvas.create_image(380, 300, anchor=NW, image=self.cloth8, tags='canvas')

    def graph(self):
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

        self.canvas.delete('canvas')
        self.canvas.create_rectangle(40, 10, 70, 20, fill='orange', tags='canvas')
        self.canvas.create_rectangle(40, 30, 70, 40, fill='blue', tags='canvas')
        self.canvas.create_text(85, 15, text="기온", tags='canvas')
        self.canvas.create_text(85, 35, text="풍속", tags='canvas')

        Maxt=max(rectm)
        Maxw=max(recws)
        for i in range(len(rectm)):
            self.canvas.create_rectangle(50+56*i,380-200*rectm[i]/Maxt,73+56*i,380,fill='orange',tags='canvas')
            self.canvas.create_text(73+56*i,390,text=now.tm_hour-i,tags='canvas')
            self.canvas.create_text(63 + 56 * i, 380-200*rectm[i]/Maxt-10, text=rectm[i], tags='canvas')
            self.canvas.create_rectangle(73+56*i, 380-100 * recws[i]/Maxw, 40 + 56 * (i + 1), 380, fill='blue',tags='canvas')
            self.canvas.create_text(85 + 56 * i, 380-100 * recws[i]/Maxw - 10, text=recws[i], tags='canvas')

    def spot(self):
        server = "api.visitkorea.or.kr"
        conn = http.client.HTTPSConnection(server)

        if self.entry.get()=='안양':
            conn.request("GET", "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=434")
        elif self.entry.get()=='과천':
            conn.request("GET", "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=116")
        elif self.entry.get()=='의왕':
            conn.request("GET", "/AWS1hourObser?KEY=f04c1c1227c2408faa4de276beda54a4&pSize=1&SPOT_NO=445")
        elif self.entry.get()=='광주':
            conn.request("GET", "/openapi/service/rest/PhotoGalleryService/gallerySearchList?serviceKey=oIudXMBvhRSo9Z565vEjySxmySalVWuAJDe6cqgLyqnbe%2BckB8rS9tI9tsgn71z0nCxfjWa%2Bq8a6nzdKjER0gA%3D%3D&pageNo=1&numOfRows=1&MobileOS=ETC&MobileApp=AppTest&arrange=A&keyword=%EA%B2%BD%EA%B8%B0%EB%8F%84+%EA%B4%91%EC%A3%BC%EC%8B%9C")
        elif self.entry.get()=='고양':
            conn.request("GET", "/openapi/service/rest/PhotoGalleryService/gallerySearchList?serviceKey=oIudXMBvhRSo9Z565vEjySxmySalVWuAJDe6cqgLyqnbe%2BckB8rS9tI9tsgn71z0nCxfjWa%2Bq8a6nzdKjER0gA%3D%3D&pageNo=1&numOfRows=1&MobileOS=ETC&MobileApp=AppTest&arrange=A&keyword=%EA%B2%BD%EA%B8%B0%EB%8F%84+%EA%B3%A0%EC%96%91%EC%8B%9C")
        elif self.entry.get() =='파주':
            conn.request("GET","/openapi/service/rest/PhotoGalleryService/gallerySearchList?serviceKey=oIudXMBvhRSo9Z565vEjySxmySalVWuAJDe6cqgLyqnbe%2BckB8rS9tI9tsgn71z0nCxfjWa%2Bq8a6nzdKjER0gA%3D%3D&pageNo=1&numOfRows=10&MobileOS=ETC&MobileApp=AppTest&arrange=A&keyword=%ea%b2%bd%ea%b8%b0%eb%8f%84+%ed%8c%8c%ec%a3%bc%ec%8b%9c")
        else:
            t = ["경기도 "]
            t.append(self.entry.get())
            hangul_utf8 = urllib.parse.quote(str(t))
            conn.request("GET", "/openapi/service/rest/PhotoGalleryService/gallerySearchList?serviceKey=oIudXMBvhRSo9Z565vEjySxmySalVWuAJDe6cqgLyqnbe%2BckB8rS9tI9tsgn71z0nCxfjWa%2Bq8a6nzdKjER0gA%3D%3D&pageNo=1&numOfRows=10&MobileOS=ETC&MobileApp=AppTest&arrange=A&keyword="+hangul_utf8)

        '''url = self.sSpot_img

        with urllib.request.rulopen(url) as u:
            raw_data=u.read()
        img = Image.open(BytesIO(raw_data))
        image = ImageTk.PhotoImage(img)

        self.canvas.create_image(50, 20, image=img)'''

        req = conn.getresponse()
        # self.load_2(req.read().decode('utf-8'))
        self.load_2(req.read())

        self.canvas.delete('canvas')
        self.canvas.create_text(30, 210, text=self.sName.text,tags='canvas')

    def tele(self):
        self.canvas.delete('canvas')
        self.canvas.create_text(300, 210, text='텔레그램',tags='canvas')

maingui()
