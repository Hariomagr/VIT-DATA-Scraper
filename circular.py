import index
import re
import json
import requests
from bs4 import BeautifulSoup
if(index.error==""):
    url="https://vtopbeta.vit.ac.in/vtop/admissions/costCentreCircularsViewPageController"
    url=index.s.post(url,headers=index.headers,verify=False)
    soup=BeautifulSoup(url.content,'html.parser')
    a=soup.find_all('a')
    for i in range(1):
        text=a[i].text.split(".")[0]
        x=(a[i]['onclick']).split("(")
        x=x[1].split(")")[0].split("'")
        url="https://vtopbeta.vit.ac.in/vtop/admissions/viewStatusWiseCostCentreCircularContent?val="+x[1]
        url=index.s.get(url,headers=index.headers,verify=False)
        content=(url.headers['Content-Type']).split("/")[1]
        print(type(url.content))
        with open(x[1]+'.'+content, 'wb') as f:
            f.write(url.content)
