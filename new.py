from urllib.request import urlopen
from xml.dom.minidom import parse, parseString
from xml.etree import ElementTree

import urllib
import urllib.request
import http.client
import time

from tkinter import *
#import io import BytesIO

rectm=[]
recws=[]

frame1_width = 570
frame2_height = 65
frame2_width = 400
frame3_width = frame1_width - frame2_width
class maingui():

    def __init__(self):
        window = Tk()
        window.title('날씨에 맞는 옷차림 추천')


        frame = Frame(window, width=frame1_width, height=frame2_height)
        frame.pack()
        frame1_bg = PhotoImage(file = 'resource/배경화면.png')
        self.label = Label(frame,image = frame1_bg).place(x=0,y=0)
        self.entry = Entry(frame, width=47)
        # entry.insert(0,'검색할 지역을 시 단위로 입력하세요')
        self.entry.insert(0, '시흥')
        self.entry.place(x=50, y=30)

        #검색버튼 크기조정
        button_width= 60
        button_height= 50

        enter_image = PhotoImage(file="resource/검색40.png")
        self.search_button = Button(frame, text='엔터', width=40,image = enter_image, command=self.search).place(x=frame2_width,y=(frame2_height-40)/2)

        bottom_GUI_height = 450
        frame2 = Frame(window, width=frame2_width, height=bottom_GUI_height)
        frame2.pack(side=LEFT)
        self.label2 = Label(frame2, image=frame1_bg).place(x=0, y=0)
        self.canvas = Canvas(frame2, width=frame2_width, height=400)
        #self.canvas.pack()
        self.canvas.create_rectangle(50, 5, frame2_width, 390, fill='cyan')

        frame3 = Frame(window, width=frame3_width, height=bottom_GUI_height)
        frame3.pack(side=LEFT)
        frame3_bg = PhotoImage(file='resource/제목.png')
        self.label3 = Label(frame3, image=frame3_bg).place(x=0, y=0)

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
        Button(frame3, text='추천 옷차림', width=130, height=140,image = bestfashion_image, command=self.search).place(x=19, y=290)
        #Label(frame3, text='오늘의 날씨 정보').place(x=100, y=100)

        window.mainloop()

    def load(self,strXml):
        from xml.etree import ElementTree
        tree = ElementTree.fromstring(strXml)
        itemElements = tree.iter("row")

        for item in itemElements:
            self.tp = item.find("TP_INFO")
            self.ws = item.find("WS_INFO")
            if len(self.ws.text) > 0 :
                T=float(self.tp.text)
                V=(float(self.ws.text)*3.6) ** (0.16)
                self.tm=13.12 + 0.6215 * T - 11.37 * V + 0.3965 * V * T
            rectm.append(T)
            recws.append(float(self.ws.text))


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
        self.canvas.create_text(300, 160, text='지도',tags='canvas')

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
            self.canvas.create_rectangle(40+56*i,400-200*rectm[i]/Maxt,63+56*i,380,fill='orange',tags='canvas')
            self.canvas.create_text(63+56*i,390,text=now.tm_hour-i,tags='canvas')
            self.canvas.create_text(53 + 56 * i, 400-200*rectm[i]/Maxt-10, text=rectm[i], tags='canvas')
            self.canvas.create_rectangle(63+56*i, 400-100 * recws[i]/Maxw, 30 + 56 * (i + 1), 380, fill='blue',tags='canvas')
            self.canvas.create_text(75 + 56 * i, 400-100 * recws[i]/Maxw - 10, text=recws[i], tags='canvas')

    def spot(self):
        #from PIL import Image, ImageTK
        #url = "https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15024675"
        self.canvas.delete('canvas')
        self.canvas.create_text(300, 210, text='명소',tags='canvas')

    def tele(self):
        self.canvas.delete('canvas')
        self.canvas.create_text(300, 210, text='텔레그램',tags='canvas')

maingui()
