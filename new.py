        window = Tk()
        window.title('날씨에 맞는 옷차림 추천')
        window.configure(bg = 'white')
        #글꼴 추가
        self.font = tkFont.Font(family="SeoulHangangEB.ttf", size=13, weight="bold", slant="italic")
        self.font2 = tkFont.Font(family="경기천년제목_Bold.ttf", size=16, weight="bold", slant="roman")
        self.font3 = tkFont.Font(family="경기천년제목_Bold.ttf", size=13, weight="bold", slant="roman")

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
        # entry.insert(0,'검색할 지역을 시 단위로 입력하세요.')
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

        weatherx=90
        weathery=80
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
        Label(window, text='추천 옷차림', width=130, height=140,image = bestfashion_image).place(x=602, y=370)

        #시 별로 위도 경도 저장
        self.dic={'수원':[127.0286009, 37.2635727],'성남':[127.1388684, 37.4449168],'부천':[126.766 ,37.44],'안양':[126.9568209, 37.3942527],'안산':[126.8308848, 37.3218778],'용인':[127.1775537, 37.2410864],'광명':[126.8642888,37.4784878],'평택':[127.1129451,36.9921075 ],
                  '과천':[126.822052,37.335224 ],'시흥':[126.8031025,37.3798877],'군포':[126.9351741,37.3616703],'의왕':[126.9683104, 37.344701],'오산':[127.0772212,37.1498096],'하남':[127.2148919,37.5392646],'이천':[127.4348221,37.2719952],'김포':[126.7156325,37.6152464],
                 '안성':[127.2796786, 37.0079695],'화성':[126.8311887, 37.1994932],'광주':[127.2561413,37.4171413],'여주':[127.71 ,37.29 ],'의정부':[127.0336819,37.73809800000001 ],'고양':[126.8320201, 37.65835990000001],'동두천':[127.0605075,37.9034112 ],'구리':[127.1295646,37.5943124 ],
                 '남양주':[127.2165279,37.6360028],'파주':[126.7801781,37.7598688],'양주':[127.071991,37.796763 ],'포천':[127.2003551,37.8949148]}
        self.mapwidth=700
        self.mapheight=600 #320
        window.mainloop()
