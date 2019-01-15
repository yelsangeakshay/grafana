#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 13:29:11 2018

@author: akki
"""
import mysql.connector

from bs4 import BeautifulSoup
#import urllib2
#import os
#import requests
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
from  datetime import  date



def db_connection():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Engineering+1",
    database="db_grafana"
    )
    #print(mydb)
    global mycursor




#mycursor.execute("CREATE DATABASE test_python")
    #mycursor.execute("SELECT * FROM test1")
    #myresult = mycursor.fetchall()


    #for x in myresult:
    #    print(x)







mydb = mysql.connector.connect(
host="localhost",
user="root",
passwd="Engineering+1",
database="db_grafana"
)
#print(mydb)

mycursor = mydb.cursor()

url = "http://localhost/Release_23.html"
#url = "https://alm.vodafone.com/qcbin/rest/domains/EVO/projects/EVO_Automation_New/defects?login-form-required=y"
resp = requests.get(url,auth = HTTPBasicAuth('vpl_aakshayyelsange','Welcome+1'))
#print(resp)

'''if resp.find(stat)!=-1:
    print("found")
else:
    print("Not found")

if stat in resp:
    #print("NO Intenet connection")
else:
   # print("Intenet  connection")
   '''
#print("Resp",resp)
#db_connection()
msg = resp.content
soup = BeautifulSoup(resp.text,'html.parser')
#print(soup)
defect_id = soup.findAll("field", {"name" :"id"})
status = soup.findAll("field", {"name" :"user-01"})
#dte = soup.findAll("field", {"name" :"closing-date"})
priority = soup.findAll("field",{"name" :"priority"})
#last_modified = soup.findAll("field",{"name" :"last-modified"})
severity = soup.findAll("field",{"name" :"severity"})
detectd_by = soup.findAll("field",{"name" :"detected-by"})
#subject = soup.findAll("field",{"name" :"subject"})
ids_release = soup.findAll("field",{"name" :"detected-in-rel"})
ids_stream = soup.findAll("field",{"name" :"detected-in-rcyc"})
assigned_team = soup.findAll("field",{"name" :"user-02"})
opco = soup.findAll("field",{"name" :"user-08"})
assigned_to = soup.findAll("field",{"name" :"owner"})
system = soup.findAll("field",{"name" :"user-10"})
detected_date = soup.findAll("field",{"name": "creation-time"})

detected_date = soup.findAll("field",{"name": "creation-time"})

#results1 = soup.findAll("status")
#print(status)
lst_defect_id=[]
lst_close_date=[]
lst_status=[]
lst_priority=[]
lst_modified=[]
lst_severity=[]
lst_detected_by=[]
lst_subject=[]
lst_ids=[]
lst_system=[]
lst_assigned_to=[]
lst_assigned_team=[]
lst_opco=[]
lst_ids_release=[]
lst_ids_stream=[]
ls_detected_date = []

lst_final=[]
#print(results)

#Execution dateif cnt > 0:
#print(dte)

#Get the Closing Date from API
'''
for item in dte:
    result = item.find("value")
    #print(result)
    if result == None:
        print("if")
        #print(result)
        lst_close_date.append(result)
    else:
        print("else")
        #print(result)

        lst_close_date.append(result)

'''
#print(result)


# Get the Subject from API
'''
for item in subject:
    print(item)
    if item=="None":
        lst_subject.append(item)
    else:
        result = item.find("value")
        lst_subject.append(result)
'''


# Get the defect ids from API
for item in defect_id:
    result = item.find("value").text
    #print(result)
    lst_defect_id.append(result)

# Get the Severity from API
for item in severity:
    result = item.find("value").text
    lst_severity.append(result)
    #print(result)


#Get the creation date:
for item in detected_date:
    result = item.find("value").text
    #print(result)
    ls_detected_date.append(result)

# Get the Detected By from API
for item in detectd_by:
    result = item.find("value").text
    lst_detected_by.append(result)
    #print(result)



# Get the Status from API
for item in status:
    #print(item)
    result = item.find("value").text
    lst_status.append(result)
    #print(result)



# Get the Priority from API
for item in priority:
    result = item.find("value").text
    lst_priority.append(result)

# Get the Assigned Team from API
for item in assigned_team:
    result = item.find("value").text
    lst_assigned_team.append(result)

# Get the Opco Team from API
for item in opco:
    result = item.find("value").text
    lst_opco.append(result)


#print((len(lst_defect_id)))
#print((len(lst_assigned_team)))
#print((len(lst_opco)))
#print((len(lst_status)))
#print((len(lst_close_date)))
#print((len(lst_priority)))
#print((len(lst_severity)))
#print((len(lst_detected_by)))
#print(lst_opco)
#print(lst_assigned_team)
lst_final = zip(lst_defect_id,lst_status,lst_priority,lst_severity,lst_detected_by,lst_assigned_team,lst_opco,ls_detected_date)
lst_final = list(lst_final)
#print(len(ls_detected_date))
#print(lst_final)



sql = "INSERT INTO release_23(defect_id,defect_status,priority,severity,detected_by,assigned_team,opco,detected_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
mycursor.executemany(sql,lst_final)
mydb.commit()
print(mycursor.rowcount, "was inserted.")


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



sql = "insert into get_severity_23(severity,total) values('1. Critical',(select count(*) from release_23 where severity = '1. Critical'))"
mycursor.execute(sql)
mydb.commit()
sql = "insert into get_severity_23(severity,total) values('2. High',(select count(*) from release_23 where severity = '2. High'))"
mycursor.execute(sql)
mydb.commit()
sql = "insert into get_severity_23(severity,total) values('3. Medium',(select count(*) from release_23 where severity = '3. Medium'))"
mycursor.execute(sql)
mydb.commit()
sql = "insert into get_severity_23(severity,total) values('4. Low',(select count(*) from release_23 where severity = '4. Low'))"
mycursor.execute(sql)
mydb.commit()



sql = "insert into get_status_23(status,total) values('1. New',(select count(*) from release_23 where defect_status = '1. New'))"
mycursor.execute(sql)
mydb.commit()
sql = "insert into get_status_23(status,total) values('2. In Progress',(select count(*) from release_23 where defect_status = '2. In Progress'))"
mycursor.execute(sql)
mydb.commit()
sql = "insert into get_status_23(status,total) values('3. Fixed Ready for Retest',(select count(*) from release_23 where defect_status = '3. Fixed Ready for Retest'))"
mycursor.execute(sql)
mydb.commit()
sql = "insert into get_status_23(status,total) values('4. Closed',(select count(*) from release_23 where defect_status = '4. Closed'))"
mycursor.execute(sql)
mydb.commit()
sql = "insert into get_status_23(status,total) values('5. Rejected',(select count(*) from release_23 where defect_status = '5. Rejected'))"
mycursor.execute(sql)
mydb.commit()
sql = "insert into get_status_23(status,total) values('6. Deferred',(select count(*) from release_23 where defect_status = '6. Deferred'))"
mycursor.execute(sql)
mydb.commit()
sql = "insert into get_status_23(status,total) values('7. CR Required',(select count(*) from release_23 where defect_status = '7. CR Required'))"
mycursor.execute(sql)
mydb.commit()
sql = "insert into get_status_23(status,total) values('8. Re-Open',(select count(*) from release_23 where defect_status = '8. Re-Open'))"
mycursor.execute(sql)
sql = "insert into get_status_23(status,total) values('9. Closed Rejected',(select count(*) from release_23 where defect_status = '9. Closed Rejected'))"
mycursor.execute(sql)
mydb.commit()



sql = "insert into assigned_team_status_23(assigned_team,total) values('OpCo Local Business',(select count(*) from release_23 where assigned_team = 'OpCo Local Business'))"
mycursor.execute(sql)

sql = "insert into assigned_team_status_23(assigned_team,total) values('Accenture',(select count(*) from release_23 where assigned_team = 'Accenture'))"
mycursor.execute(sql)
sql = "insert into assigned_team_status_23(assigned_team,total) values('VOCH',(select count(*) from release_23 where assigned_team = 'VOCH'))"
mycursor.execute(sql)
sql = "insert into assigned_team_status_23(assigned_team,total) values('Concur',(select count(*) from release_23 where assigned_team = 'Concur'))"
mycursor.execute(sql)
sql = "insert into assigned_team_status_23(assigned_team,total) values('Triage Team',(select count(*) from release_23 where assigned_team = 'Triage Team'))"
mycursor.execute(sql)
sql = "insert into assigned_team_status_23(assigned_team,total) values('Others',(select count(*) from release_23 where assigned_team = 'Others'))"
mycursor.execute(sql)
sql = "insert into assigned_team_status_23(assigned_team,total) values('VSSI - AD',(select count(*) from release_23 where assigned_team = 'VSSI - AD'))"
mycursor.execute(sql)
sql = "insert into assigned_team_status_23(assigned_team,total) values('Test Management Team',(select count(*) from release_23 where assigned_team = 'Test Management Team'))"
mycursor.execute(sql)
sql = "insert into assigned_team_status_23(assigned_team,total) values('Idoc Team',(select count(*) from release_23 where assigned_team = 'Idoc Team'))"
mycursor.execute(sql)
mydb.commit()


sql = "insert into opco_status_23(opco,total) values('Egypt',(select count(*) from release_23 where opco = 'Egypt'))"
mycursor.execute(sql)
sql = "insert into opco_status_23(opco,total) values('Cross-Markets',(select count(*) from release_23 where opco = 'Cross-Markets'))"
mycursor.execute(sql)
sql = "insert into opco_status_23(opco,total) values('Ireland',(select count(*) from release_23 where opco = 'Ireland'))"
mycursor.execute(sql)
sql = "insert into opco_status_23(opco,total) values('Hungary',(select count(*) from release_23 where opco = 'Hungary'))"
mycursor.execute(sql)
sql = "insert into opco_status_23(opco,total) values('UK',(select count(*) from release_23 where opco = 'UK'))"
mycursor.execute(sql)
sql = "insert into opco_status_23(opco,total) values('CBM',(select count(*) from release_23 where opco = 'CBM'))"
mycursor.execute(sql)
sql = "insert into opco_status_23(opco,total) values('VPC',(select count(*) from release_23 where opco = 'VPC'))"
mycursor.execute(sql)
sql = "insert into opco_status_23(opco,total) values('Romania',(select count(*) from release_23 where opco = 'Romania'))"
mycursor.execute(sql)
sql = "insert into opco_status_23(opco,total) values('VGXI LUX LU',(select count(*) from release_23 where opco = 'VGXI LUX LU'))"
mycursor.execute(sql)
sql = "insert into opco_status_23(opco,total) values('VGx',(select count(*) from release_23 where opco = 'VGx'))"
mycursor.execute(sql)
sql = "insert into opco_status_23(opco,total) values('South Africa',(select count(*) from release_23 where opco = 'South Africa'))"
mycursor.execute(sql)
sql = "insert into opco_status_23(opco,total) values('VGSL',(select count(*) from release_23 where opco = 'VGSL'))"
mycursor.execute(sql)
sql = "insert into opco_status_23(opco,total) values('Germany',(select count(*) from release_23 where opco = 'Germany'))"
mycursor.execute(sql)
sql = "insert into opco_status_23(opco,total) values('Italy',(select count(*) from release_23 where opco = 'Italy'))"
mycursor.execute(sql)
sql = "insert into opco_status_23(opco,total) values('Netherlands',(select count(*) from release_23 where opco = 'Netherlands'))"
mycursor.execute(sql)
sql = "insert into opco_status_23(opco,total) values('Greece',(select count(*) from release_23 where opco = 'Greece'))"
mycursor.execute(sql)


mydb.commit()




'''

for i in lst_defect_id:
    #print(i)
    mycursor.execute("select detected_date from release_23 where defect_id = %s" %i)
    res = mycursor.fetchone()
    res = str(res)
    print(res)
    datetime_object = datetime(res, '%Y-%M-%d')
    print(datetime_object)
    mycursor.execute("select DATEDIFF(curdate() ,%s)"%res)
    #res1 = mycursor.fetchone()
    #print(res1)

    #print(sql)
    #sql = "insert into defect_aging(aging,id) values
    # (DATEDIFF(curdate(),(select detected_date from release_23 where defect_id = %i and  defect_status IN('1. New','2. In Progress','3. Fixed Ready for Retest', '8. Re-Open','11. OSS Raised'))),'%i')"
    #val = "DATEDIFF(curdate(),(select detected_date from release_23 where defect_id = 'i' and  defect_status IN('1. New','2. In Progress','3. Fixed Ready for Retest', '8. Re-Open','11. OSS Raised'))),'i'"
    #print(sql)
    #mycursor.execute("insert into defect_aging(aging,id) values((DATEDIFF(curdate(),(select detected_date from release_23 where defect_id = %i))),4)")



mydb.commit()

sql = "INSERT INTO release_23(defect_id,defect_status,priority,severity,detected_by,assigned_team,opco,detected_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
mycursor.executemany(sql,lst_final)
mydb.commit()
print(mycursor.rowcount, "was inserted.")


sql = "insert into get_severity_23(severity,total) values('1. Critical',(select count(*) from release_23 where severity = '1. Critical'))"
mycursor.execute(sql)
mydb.commit()
sql = "insert into get_severity_23(severity,total) values('2. High',(select count(*) from release_23 where severity = '2. High'))"
mycursor.execute(sql)
mydb.commit()
sql = "insert into get_severity_23(severity,total) values('3. Medium',(select count(*) from release_23 where severity = '3. Medium'))"
mycursor.execute(sql)
mydb.commit()
sql = "insert into get_severity_23(severity,total) values('4. Low',(select count(*) from release_23 where severity = '4. Low'))"
mycursor.execute(sql)
mydb.commit()



sql = "INSERT INTO release_23(defect_id,defect_status,priority,severity,detected_by) VALUES (%s,%s,%s,%s,%s)"
mycursor.executemany(sql,lst_final)
mydb.commit()
print(mycursor.rowcount, "was inserted.")
sql = "insert into get_severity_23(severity,total) values('1. Critical',(select count(*) from release_23 where severity = '1. Critical'))"
mycursor.execute(sql)
mydb.commit()
sql = "insert into get_severity_23(severity,total) values('2. High',(select count(*) from release_23 where severity = '2. High'))"
mycursor.execute(sql)
mydb.commit()
sql = "insert into get_severity_23(severity,total) values('3. Medium',(select count(*) from release_23 where severity = '3. Medium'))"
mycursor.execute(sql)
mydb.commit()
sql = "insert into get_severity_23(severity,total) values('4. Low',(select count(*) from release_23 where severity = '4. Low'))"
mycursor.execute(sql)
mydb.commit()





#Combine the results to a single List
lst_final = zip(lst_status,lst_close_date,lst_priority,lst_severity,lst_modified,lst_detected_by,lst_subject,lst_ids)
lst_final = list(lst_final)
print(lst_final)

#MYSQL Query to inserr thke Data

sql = "INSERT INTO test1(status,closing_date,priority,severity,last_modified,detected_by,subject,detected_in_rel) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
#mycursor.executemany(sql,lst_final)

#sql = ("INSERT INTO test1(status,closing_date,priority,severity,last_modified,detected_by,subject,detected_in_rel) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) on DUPLICATE KEY update status = values(%s),closing_date=values(%s),priority=values(%s),severity=values(%s),last_modified=values(%s),detectd_by= values(%s),subject=values(%s)"
#"jlkjk=values(%s)")
mycursor.executemany(sql,lst_final)
print(mycursor.rowcount, "was inserted.")
mydb.commit()
#on duplicate key update status = %s,closing_date=%s,priority=%s,severity=%s,last_modified=%s,detectd_by= %s,subject=%s,detected_in_rel=%s"


sql = "insert into get_severity(severity,total) values('1. Critical',(select count(*) from test1 where severity = '1. Critical'))"
mycursor.execute(sql)
mydb.commit()
sql = "insert into get_severity(severity,total) values('2. High',(select count(*) from test1 where severity = '2. High'))"
mycursor.execute(sql)
mydb.commit()
sql = "insert into get_severity(severity,total) values('2. High',(select count(*) from test1 where severity = '3. Medium'))"
mycursor.execute(sql)
mydb.commit()
sql = "insert into get_severity(severity,total) values('2. High',(select count(*) from test1 where severity = '4. Low'))"
mycursor.execute(sql)
mydb.commit()
if results!=null or results!='':
    for item in results:
    #print(item)
        result = item.find("value").text
        print(result)   
else:
    print("Please check Internet connection)
result = results.find("value")

'''



