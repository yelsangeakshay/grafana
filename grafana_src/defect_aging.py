import mysql.connector

from bs4 import BeautifulSoup
#import urllib2
#import os
#import requests
import requests
from datetime import date
from datetime import datetime
from requests.auth import HTTPBasicAuth



mydb = mysql.connector.connect(
host="localhost",
user="root",
passwd="Engineering+1",
database="db_grafana"
)

mycursor = mydb.cursor()

url = "http://localhost/Release_23.html"
#url = "https://alm.vodafone.com/qcbin/rest/domains/EVO/projects/EVO_Automation_New/defects?login-form-required=y"
resp = requests.get(url,auth = HTTPBasicAuth('vpl_aakshayyelsange','Welcome+1'))
#print(resp)
msg = resp.content
soup = BeautifulSoup(resp.text,'html.parser')
#print(soup)
defect_id = soup.findAll("field", {"name" :"id"})

lst_defect_id=[]

for item in defect_id:
    result = item.find("value").text
    #print(result)
    lst_defect_id.append(result)


#print(lst_defect_id)

for i in lst_defect_id:
    mycursor.execute("select detected_date,defect_id from release_23 where defect_id = %s and defect_status IN('1. New','2. In Progress','3. Fixed Ready for Retest', '8. Re-Open','11. OSS Raised')" %i)
    result1 = mycursor.fetchone()
    #print(result1)
    cur_date = date.today()
    if result1!=None:
        dd,id = result1
        #print(dd,id,cur_date)
        temp = datetime.strptime(dd,"%Y-%m-%d")
        temp1 = datetime.today()
        res = temp1 - temp
        res = res.days
        #print(res,id)
        sql = "INSERT INTO defect_aging(id,aging) values (%s,%s)"
        val = (id,res)
        mycursor.execute(sql,val)
        #dd = dd.replace('-',',')
        #print(res.days)


mydb.commit()





