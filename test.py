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

def showMap(frame):
    sys.excepthook = cef.ExceptHook
    window_info = cef.WindowInfo(frame.winfo_id())
    window_info.SetAsChild(frame.winfo_id(), [0, 0, self.mapwidth, self.mapheight])
    cef.Initialize()
    browser = cef.CreateBrowserSync(window_info, url='file:///map.html')

    cef.MessageLoop()


def mapwindow():
    app = Nominatim(user_agent='tutorial')
    location = app.geocode('경기시흥')  # 위도 경도 추출

    m = folium.Map(location=[location.latitude, location.longitude], zoom_start=16)
    folium.Marker([location.latitude, location.longitude]).add_to(m)
    url = 'map.html'
    m.save(url)
    webbrowser.open(url)

mapwindow()