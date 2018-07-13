import urllib.request
import urllib
import ssl
import json
import re
import io
import requests
import base64
from PIL import Image
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from bs4 import BeautifulSoup
url1='https://vtopbeta.vit.ac.in/vtop/'
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
}
reg_no=input("Reg_no: ")
password=input("Password: ")
semester="VL2018191"
sem=input("Semester => FS19,TS19,WS18,FS18: ")
if(sem=="FS19"):
    semester="VL2018191"
elif(sem=="TS19"):
    semester="VL2018192"
elif(sem=="WS18"):
    semester="VL2017185"
elif(sem=="FS18"):
    semester="VL2017181"
s=requests.session()
url=s.get(url1,headers=headers,verify=False)
regex="gsid=[0-9]{6,7};"
pattern = re.compile(regex)
gsid = re.findall(pattern,str(url.content))
error=""
if(len(gsid)>1):
    if(len(gsid[0].split("="))>1):
        if(len((gsid[0].split("="))[1].split(";"))>0):
            gsid=((gsid[0].split("="))[1].split(";"))[0]
            url="https://vtopbeta.vit.ac.in/vtop/executeApp/?gsid="+str(gsid)
            url=s.get(url,headers=headers,verify=False)
            url="https://vtopbeta.vit.ac.in/vtop/getLogin"
            url=s.get(url,headers=headers,verify=False)
            soup=BeautifulSoup(url.content,'html.parser')
            image = soup.find('img',alt="vtopCaptcha")
            image=((image['src'].split(" ")))
            image=image[1]
            imgdata = base64.b64decode(image)
            image = Image.open(io.BytesIO(imgdata))
            characters = "123456789abcdefghijklmnpqrstuvwxyz"
            captcha = ""
            with open("bitmaps.json", "r") as f:
                bitmap = json.load(f)
            for j in range(int(image.width/6), image.width + 1, int(image.width/6)):
                character_image = image.crop((j - 30, 12, j, 44))
                character_matrix = character_image.load()
                matches = {}
                for char in characters:
                    match = 0
                    black = 0
                    bitmap_matrix = bitmap[char]
                    for y in range(0, 32):
                        for x in range(0, 30):
                            if character_matrix[x, y][0] == bitmap_matrix[y][x] and bitmap_matrix[y][x] == 0:
                                match += 1
                            if bitmap_matrix[y][x] == 0:
                                black += 1
                    perc = float(match) / float(black)
                    matches.update({perc: char[0].upper()})
                try:
                    captcha += matches[max(matches.keys())]
                except ValueError:
                    captcha += "0"
            data={'uname':reg_no,'passwd':password,'captchaCheck':captcha}
            url="https://vtopbeta.vit.ac.in/vtop/processLogin"
            url=s.post(url,data=data,headers=headers,verify=False)
            soup=BeautifulSoup(url.content,'html.parser')
            if(soup.find('p',{'class':'box-title text-danger'})!=None):
                error=soup.find('p',{'class':'box-title text-danger'}).text
                print(error)

