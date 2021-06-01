#api.visitkorea.or.kr/openapi/service/rest/PhotoGalleryService/gallerySearchList?serviceKey=jTzcx4rDMB57ckLLHIqWzgXBQxtYj%2Blj7LFOetkB3SdjIrphA%2FcIQCz3Wk0n40YuUmU1%2FbDUquRyXbtI3Xn6SQ%3D%3D&pageNo=1&numOfRows=10&MobileOS=ETC&MobileApp=AppTest&arrange=B&keyword=서울
import urllib
import urllib.request
import http.client
from io import BytesIO
from PIL import ImageTk,Image as imge

from tkinter import *

rec_sN=[]
rec_sI=[]
rec_sL=[]
rec_sK=[]
sSpot_img = NONE
def load_2( strXml):
    global sSpot_img
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    itemElements = tree.iter("item")

    for item in itemElements:
        sName = item.find("galTitle")  # 이름
        if len( sName.text) > 0:
            rec_sN.append(str( sName.text))
        sSpot_img = item.find("galWebImageUrl")
        sLocation = item.find("galPhotographyLocation")  # 위치
        sKeywords = item.find("galSearchKeyword")  # 검색 키워드

        sI =  sSpot_img.text
        sL =  sLocation.text
        sK =  sKeywords.text

        rec_sI.append(sI)
        rec_sL.append(sL)
        rec_sK.append(sK)


window=Tk()
window.geometry("500x500+500+200")

conn = http.client.HTTPConnection("api.visitkorea.or.kr")
hangul_utf8 = urllib.parse.quote("서울")
conn.request("GET","/openapi/service/rest/PhotoGalleryService/gallerySearchList?serviceKey=jTzcx4rDMB57ckLLHIqWzgXBQxtYj%2Blj7LFOetkB3SdjIrphA%2FcIQCz3Wk0n40YuUmU1%2FbDUquRyXbtI3Xn6SQ%3D%3D&pageNo=1&numOfRows=1&MobileOS=ETC&MobileApp=AppTest&arrange=B&keyword="+hangul_utf8)
req = conn.getresponse()
load_2(req.read().decode('utf-8'))

with urllib.request.urlopen(sSpot_img.text) as u:
    raw_data = u.read()
im = imge.open(BytesIO(raw_data))
IMAGE = ImageTk.PhotoImage(im)
image2 = PhotoImage(im)
canvas = Canvas(window, width=400, height=400)

canvas.create_image(0, 0, anchor=NW, image=IMAGE)
#Label(window,image=IMAGE,height=400,width=400).place(x=0,y=0)

window.mainloop()
