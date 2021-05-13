from urllib.request import urlopen
from xml.dom.minidom import parse, parseString
from xml.etree import ElementTree
import urllib
import http.client
import time

from tkinter import *

rectm=[]
recws=[]

class maingui():
    def __init__(self):
        window = Tk()
        window.title('날씨에 맞는 옷차림 추천')

        frame = Frame(window, width=800, height=60)
        frame.pack()
        self.entry = Entry(frame, width=100)
        # entry.insert(0,'검색할 지역을 시 단위로 입력하세요')
        self.entry.insert(0, '시흥')
        self.entry.place(x=20, y=30)
        Button(frame, text='엔터', width=5, command=self.search).place(x=730, y=30)

        frame2 = Frame(window, width=600, height=500)
        frame2.pack(side=LEFT)
        self.canvas = Canvas(frame2, width=600, height=400)
        self.canvas.pack()
        self.canvas.create_rectangle(30,0,600,400,fill='cyan')

        frame3 = Frame(window, width=200, height=500)
        frame3.pack(side=LEFT)
        Button(frame3, text='지도', width=10, height=2, command=self.Map).place(x=0, y=50)
        Button(frame3, text='그래프', width=10, height=2, command=self.graph).place(x=0, y=90)
        Button(frame3, text='명소', width=10, height=2, command=self.spot).place(x=0, y=130)
        Button(frame3, text='텔레그램', width=10, height=2, command=self.tele).place(x=0, y=170)
        Button(frame3, text='추천 옷차림', width=25, height=12, command=self.search).place(x=0, y=260)
        Label(frame3, text='오늘의 날씨 정보').place(x=100, y=100)

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
        self.canvas.delete('canvas')
        self.canvas.create_text(300, 210, text='명소',tags='canvas')

    def tele(self):
        self.canvas.delete('canvas')
        self.canvas.create_text(300, 210, text='텔레그램',tags='canvas')

maingui()