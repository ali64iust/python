import requests
from bs4 import BeautifulSoup
from datetime import datetime
import ctypes
import time

MessageBox = ctypes.windll.user32.MessageBoxW

#pip install BeautifulSoup
#python -m pip install BeautifulSoup4
#pip install pdfkit

hour_correction=-1 #agar jelo bod bayad -1 bezarim
min_correction=-15

before_azan=15

def getAzanZohrData():
    url = 'https://www.time.ir/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    div1 = soup.find('div', {'class': 'horizontalMode'})
    azan_zohr=div1.find('span',{'id': 'ctl00_cphTop_Sampa_Web_View_EphemerisUI_EphemerisByCity12cphTop_3736_lblAzanNoon'})

    azan_zohr_text=azan_zohr.text
    azan_zohr_h=int(azan_zohr_text.split(":")[0])
    azan_zohr_m=int(azan_zohr_text.split(":")[1])
    print("azan johr: ",azan_zohr_h,":",azan_zohr_m)
    return azan_zohr_h,azan_zohr_m

def get_h_m():
    now = datetime.now()
    return now.hour,now.minute

def check_beforeAzan(h,m,azan_zohr_h1, azan_zohr_m1):
    if(hour_correction*60+h*60+m+before_azan+min_correction==azan_zohr_h1*60+azan_zohr_m1):
        MessageBox(None, 'azan', 'azan', 0)

def check_Azan(h,m,azan_zohr_h1, azan_zohr_m1):
    if (hour_correction * 60 + h * 60 + m  + min_correction == azan_zohr_h1 * 60 + azan_zohr_m1):
        MessageBox(None, 'azan', 'azan', 0)

d=1
azan_zohr_h1=0
azan_zohr_m1=0
h=0
m=0

while(1==1):
    try:
        if (d != datetime.now().day):
            azan_zohr_h1, azan_zohr_m1 = getAzanZohrData()
            d = datetime.now().day

        for i in range(1,61):
            h,m = get_h_m()
            check_beforeAzan(h,m,azan_zohr_h1, azan_zohr_m1)
            check_Azan(h, m, azan_zohr_h1, azan_zohr_m1)
            time.sleep(30)
    except Exception as e:
        print(e)
        #print()
