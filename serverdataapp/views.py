from django.shortcuts import render
import psycopg2
import csv

import time
from datetime import date ,timedelta
from masterapp.models import PrinterdataTable,ScannerTable,ProdReport
from accounts.models import Register,UserrolePermissions,Loginmodel,History
from localapp.models import LocalappLoginmodel
# Create your views here.
from django.shortcuts import render,HttpResponse,redirect 
from serverdataapp.models import   BackupScannerdata     
from django.views.generic import View
import socket
import pandas as pd
import datetime
# class sendServer(View):


def Restore_BackupdataView(request):
        hostname = socket.gethostname()
        systemip = socket.gethostbyname(hostname) 
            
        Line1 = LocalappLoginmodel.objects.get(id=1)
        ip1= Line1.ip_address     
                                   
        Line2 = LocalappLoginmodel.objects.get(id=2)
        ip2=Line2.ip_address
            
        Line3=LocalappLoginmodel.objects.get(id=3)
        ip3=Line3.ip_address
        if systemip==ip1:
                    
                uname = LocalappLoginmodel.objects.get(id=1)
                loginname=uname.loginuname
                loginuserrole=uname.userrole
            
        elif systemip==ip2: 
                uname = LocalappLoginmodel.objects.get(id=2)
                loginname=uname.loginuname
                loginuserrole=uname.userrole
        elif systemip==ip3: 
                uname = LocalappLoginmodel.objects.get(id=3)
                loginname=uname.loginuname
                loginuserrole=uname.userrole
        if(loginname!=""):            
                if request.method == 'GET':
                    query = request.GET.get('query')    #searching item
                    datequery=request.GET.get('datequery')
                    # print(datequery)
                if query and datequery:
                                      
                    jobs = BackupScannerdata.objects.all().filter(lot=query,send_date=datequery) 
                 
                    count=len(jobs)
                    # print(count)
                    return render(request, 'Restore.html', {'count':count,'lot':query,"date":datequery,"name":loginname})
                else:
                   
                    return render(request, 'Restore.html', {"name":loginname}) 
        else:
                  return redirect("signin")  


def Export_csv (request):
                    hostname = socket.gethostname()
                    systemip = socket.gethostbyname(hostname) 
                    
                    Line1 = LocalappLoginmodel.objects.get(id=1)
                    ip1= Line1.ip_address     
                                        
                    Line2 = LocalappLoginmodel.objects.get(id=2)
                    ip2=Line2.ip_address
                    
                    Line3=LocalappLoginmodel.objects.get(id=3)
                    ip3=Line3.ip_address
                    if systemip==ip1:
                                        
                                        uname = LocalappLoginmodel.objects.get(id=1)
                                        loginname=uname.loginuname
                                        loginuserrole=uname.userrole
                    
                    elif systemip==ip2: 
                                        uname = LocalappLoginmodel.objects.get(id=2)
                                        loginname=uname.loginuname
                                        loginuserrole=uname.userrole
                    elif systemip==ip3: 
                                        uname = LocalappLoginmodel.objects.get(id=3)
                                        loginname=uname.loginuname
                                        loginuserrole=uname.userrole
                    if(loginname!=""):            
                    #   if request.method == 'GET':
                        query = request.GET.get('query')    #searching item
                        # print("query",query)
                        datequery=request.GET.get('datequery')
                        # print("3333333333333")
                        # print(datequery)
                        if query and datequery:
                                        
                                jobs = BackupScannerdata.objects.all().filter(lot=query,send_date=datequery) 
                                count=len(jobs)
                                with open(datequery + 'backupdata.csv', 'w', newline='') as f_handle:
                                        writer = csv.writer(f_handle)
                                                                                # Add the header/column names
                                        header = ['id','lot', 'serialnumber','senddate']
                                        
                                        writer.writerow(header)
                                for i in range(count):
                                        id=jobs[i].id  
                                        serialnumber=jobs[i].serialnumber 
                                        batch=jobs[i].lot  
                                        senddate=jobs[i].send_date
                                                   
                                        with open(datequery+ 'backupdata.csv', 'a', newline='') as f_handle:
                                                writer = csv.writer(f_handle)
                                                                                        # Add the header/column names
                                                # header = ['id','lot', 'serialnumber','senddate']
                                                
                                                # writer.writerow(header)
                                                value=[id,batch,serialnumber,senddate]
                                                writer.writerow(value)
                                                                                       # Iterate over `data`  and  write to the csv file
                                       
                                return render(request, 'Restore.html', {'count':count,'lot':query,"date":datequery,"name":loginname})
                        else:
                    
                                return render(request, 'Restore.html', {"name":loginname}) 
                    else:
                       return redirect("signin") 
               
               
def Restoredata_to_server(request):
        try:
            conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ") 
        except:
            return redirect("databaseerror") 
        hostname = socket.gethostname()
        systemip = socket.gethostbyname(hostname) 
            
        Line1 = LocalappLoginmodel.objects.get(id=1)
        ip1= Line1.ip_address     
                                   
        Line2 = LocalappLoginmodel.objects.get(id=2)
        ip2=Line2.ip_address
            
        Line3=LocalappLoginmodel.objects.get(id=3)
        ip3=Line3.ip_address
        if systemip==ip1:
                    
                uname = LocalappLoginmodel.objects.get(id=1)
                loginname=uname.loginuname
                loginuserrole=uname.userrole
            
        elif systemip==ip2: 
                uname = LocalappLoginmodel.objects.get(id=2)
                loginname=uname.loginuname
                loginuserrole=uname.userrole
        elif systemip==ip3: 
                uname = LocalappLoginmodel.objects.get(id=3)
                loginname=uname.loginuname
                loginuserrole=uname.userrole
        else:
                hostname = socket.gethostname()
                systemip = socket.gethostbyname(hostname)                     
                return render(request, 'Ip-error.html',{'ip':systemip,'inside_message':1})                                      
        if(loginname!=""):                         
                query = request.GET.get('query')    #searching item
                        # print("query",query)
                datequery=request.GET.get('datequery')
                        # print("3333333333333")
                # print(datequery)
                if query and datequery:
                        
                        
                    Begindatestring = date.today() 
                    
                    t = time.localtime()

                    # Format the time as a string
                    current_time = time.strftime("%H:%M:%S", t)
                    # print(current_time)    
                    
                    
            
                    scdata = BackupScannerdata.objects.all().filter(lot=query,send_date=datequery) 
                    sclength=len(scdata)
                # print(sclength)
                    for i in range(sclength):
                        scannerdata_to_server=ScannerTable(
                                id= scdata[i].id,
                                gtin= scdata[i].gtin,
                                ip_address= scdata[i].ip_address,
                                status= scdata[i].status,
                                serialnumber= scdata[i].serialnumber,
                                gradevalue= scdata[i].gradevalue,
                                lot= scdata[i].lot,
                                finalstatus= scdata[i].finalstatus,
                                type=scdata[i].type,
                                
                                
                                ) 
                        scannerdata_to_server.save()
                        
                
        
                        # obj = PrinterdataTable.objects.get(id=id)
                        # detailObj=PrinterdataTable.objects.filter(lot=obj.lot).update(serverstatus="Updated")                 
                        # print(scdata[i].gtin)
                        jobs7 = ScannerTable.objects.filter(lot=query,status="Accepted")
                        acceptedcount=len(jobs7)
                        scObj7=ProdReport.objects.filter(batch_number=query).update(accepted=acceptedcount,production_date=Begindatestring,production_time=current_time)
                        print(acceptedcount, 'is last in the list ✅')
                        
                        jobs8 =  ScannerTable.objects.filter(lot=query,status="Rejected")
                        rejectedcount=len(jobs8)
                        scObj7=ProdReport.objects.filter(batch_number=query).update(rejectedbycamera=rejectedcount,production_date=Begindatestring,production_time=current_time)
                        
                        jobs9 =  ScannerTable.objects.filter(lot=query,status="Damaged")
                        damagedcount=len(jobs9)
                        scObj7=ProdReport.objects.filter(batch_number=query).update(damaged=damagedcount,production_date=Begindatestring,production_time=current_time)
                                                        
                        print(rejectedcount,'is last in the list ✅')    
                        # obj = ServerPrinterdata.objects.get(id=id)
                        # jobs10 =  ServerPrinterdata.objects.filter(id=id,status="Closed").update(start_pause_btnresponse=1)
                        # # damagedcount=len(jobs9)
                        
                        historysave=History(modelname='ServerScannerdata',
                                                savedid="noid",
                                                operationdone='Restore To Server',
                                                donebyuser=loginname,
                                                donebyuserrole=loginuserrole, 
                                                description="Restore The Batch Details Of  "+query+" To Server "+"by"+" "+ loginname,
                                                donedatetime=datetime.datetime.now())
                        historysave.save()            
               
                
                                                
                # return redirect("restore_server")
                return  render(request,"Restore.html",{"success_message":1})
           
        else:
            return redirect("signin")   
    
#.............................................................................
def Restore_HistoryView(request):
        hostname = socket.gethostname()
        systemip = socket.gethostbyname(hostname) 
            
        Line1 = LocalappLoginmodel.objects.get(id=1)
        ip1= Line1.ip_address     
                                   
        Line2 = LocalappLoginmodel.objects.get(id=2)
        ip2=Line2.ip_address
            
        Line3=LocalappLoginmodel.objects.get(id=3)
        ip3=Line3.ip_address
        if systemip==ip1:
                    
                uname = LocalappLoginmodel.objects.get(id=1)
                loginname=uname.loginuname
                loginuserrole=uname.userrole
            
        elif systemip==ip2: 
                uname = LocalappLoginmodel.objects.get(id=2)
                loginname=uname.loginuname
                loginuserrole=uname.userrole
        elif systemip==ip3: 
                uname = LocalappLoginmodel.objects.get(id=3)
                loginname=uname.loginuname
                loginuserrole=uname.userrole
        if(loginname!=""):            
                if request.method == 'GET':
                        #searching item
                    datequery=request.GET.get('datequery')
                    # print(datequery)
                if  datequery:
                                      
                    jobs = BackupScannerdata.objects.all().filter(send_date=datequery) 
                 
                    count=len(jobs)
                    # print(count)
                    return render(request, 'History-Restore.html', {'count':count,"date":datequery,"name":loginname})
                else:
                   
                    return render(request, 'History-Restore.html', {"name":loginname}) 
        else:
                  return redirect("signin")  


def History_Export_csv (request):
                    hostname = socket.gethostname()
                    systemip = socket.gethostbyname(hostname) 
                    
                    Line1 = LocalappLoginmodel.objects.get(id=1)
                    ip1= Line1.ip_address     
                                        
                    Line2 = LocalappLoginmodel.objects.get(id=2)
                    ip2=Line2.ip_address
                    
                    Line3=LocalappLoginmodel.objects.get(id=3)
                    ip3=Line3.ip_address
                    if systemip==ip1:
                                        
                                        uname = LocalappLoginmodel.objects.get(id=1)
                                        loginname=uname.loginuname
                                        loginuserrole=uname.userrole
                    
                    elif systemip==ip2: 
                                        uname = LocalappLoginmodel.objects.get(id=2)
                                        loginname=uname.loginuname
                                        loginuserrole=uname.userrole
                    elif systemip==ip3: 
                                        uname = LocalappLoginmodel.objects.get(id=3)
                                        loginname=uname.loginuname
                                        loginuserrole=uname.userrole
                    if(loginname!=""):            
                   
                        datequery=request.GET.get('datequery')
                        # print("3333333333333")
                        print(datequery)
                        if  datequery:
                                        
                                jobs = BackupScannerdata.objects.all().filter(send_date=datequery) 
                                count=len(jobs)
                                with open(datequery + 'backupdata.csv', 'w', newline='') as f_handle:
                                        writer = csv.writer(f_handle)
                                                                                # Add the header/column names
                                        header = ['id','lot', 'serialnumber','senddate']
                                        
                                        writer.writerow(header)
                                for i in range(count):
                                        id=jobs[i].id  
                                        serialnumber=jobs[i].serialnumber 
                                        batch=jobs[i].lot  
                                        senddate=jobs[i].send_date
                                                   
                                        with open(datequery+ 'backupdata.csv', 'a', newline='') as f_handle:
                                                writer = csv.writer(f_handle)
                                                                                        # Add the header/column names
                                                # header = ['id','lot', 'serialnumber','senddate']
                                                
                                                # writer.writerow(header)
                                                value=[id,batch,serialnumber,senddate]
                                                writer.writerow(value)
                                                                                       # Iterate over `data`  and  write to the csv file
                                       
                                return render(request, 'Restore.html', {'count':count,'lot':query,"date":datequery,"name":loginname})
                        else:
                    
                                return render(request, 'Restore.html', {"name":loginname}) 
                    else:
                       return redirect("signin") 
               
               
def Restoredata_to_server(request):
        try:
            conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ") 
        except:
            return redirect("databaseerror") 
        hostname = socket.gethostname()
        systemip = socket.gethostbyname(hostname) 
            
        Line1 = LocalappLoginmodel.objects.get(id=1)
        ip1= Line1.ip_address     
                                   
        Line2 = LocalappLoginmodel.objects.get(id=2)
        ip2=Line2.ip_address
            
        Line3=LocalappLoginmodel.objects.get(id=3)
        ip3=Line3.ip_address
        if systemip==ip1:
                    
                uname = LocalappLoginmodel.objects.get(id=1)
                loginname=uname.loginuname
                loginuserrole=uname.userrole
            
        elif systemip==ip2: 
                uname = LocalappLoginmodel.objects.get(id=2)
                loginname=uname.loginuname
                loginuserrole=uname.userrole
        elif systemip==ip3: 
                uname = LocalappLoginmodel.objects.get(id=3)
                loginname=uname.loginuname
                loginuserrole=uname.userrole
        else:
                hostname = socket.gethostname()
                systemip = socket.gethostbyname(hostname)                     
                return render(request, 'Ip-error.html',{'ip':systemip,'inside_message':1})                                      
        if(loginname!=""):                         
                query = request.GET.get('query')    #searching item
                        # print("query",query)
                datequery=request.GET.get('datequery')
                        # print("3333333333333")
                # print(datequery)
                if query and datequery:
                        
                        
                    Begindatestring = date.today() 
                    
                    t = time.localtime()

                    # Format the time as a string
                    current_time = time.strftime("%H:%M:%S", t)
                    # print(current_time)    
                    
                    
            
                    scdata = BackupScannerdata.objects.all().filter(lot=query,send_date=datequery) 
                    sclength=len(scdata)
                # print(sclength)
                    for i in range(sclength):
                        scannerdata_to_server=ScannerTable(
                                id= scdata[i].id,
                                gtin= scdata[i].gtin,
                                ip_address= scdata[i].ip_address,
                                status= scdata[i].status,
                                serialnumber= scdata[i].serialnumber,
                                gradevalue= scdata[i].gradevalue,
                                lot= scdata[i].lot,
                                finalstatus= scdata[i].finalstatus,
                                type=scdata[i].type,
                                
                                
                                ) 
                        scannerdata_to_server.save()
                        
                
        
                        # obj = PrinterdataTable.objects.get(id=id)
                        # detailObj=PrinterdataTable.objects.filter(lot=obj.lot).update(serverstatus="Updated")                 
                        # print(scdata[i].gtin)
                        jobs7 = ScannerTable.objects.filter(lot=query,status="Accepted")
                        acceptedcount=len(jobs7)
                        scObj7=ProdReport.objects.filter(batch_number=query).update(accepted=acceptedcount,production_date=Begindatestring,production_time=current_time)
                        print(acceptedcount, 'is last in the list ✅')
                        
                        jobs8 =  ScannerTable.objects.filter(lot=query,status="Rejected")
                        rejectedcount=len(jobs8)
                        scObj7=ProdReport.objects.filter(batch_number=query).update(rejectedbycamera=rejectedcount,production_date=Begindatestring,production_time=current_time)
                        
                        jobs9 =  ScannerTable.objects.filter(lot=query,status="Damaged")
                        damagedcount=len(jobs9)
                        scObj7=ProdReport.objects.filter(batch_number=query).update(damaged=damagedcount,production_date=Begindatestring,production_time=current_time)
                                                        
                        print(rejectedcount,'is last in the list ✅')    
                        # obj = ServerPrinterdata.objects.get(id=id)
                        # jobs10 =  ServerPrinterdata.objects.filter(id=id,status="Closed").update(start_pause_btnresponse=1)
                        # # damagedcount=len(jobs9)
                        
                        historysave=History(modelname='ServerScannerdata',
                                                savedid="noid",
                                                operationdone='Restore To Server',
                                                donebyuser=loginname,
                                                donebyuserrole=loginuserrole, 
                                                description="Restore The Batch Details Of  "+query+" To Server "+"by"+" "+ loginname,
                                                donedatetime=datetime.datetime.now())
                        historysave.save()            
               
                
                                                
                # return redirect("restore_server")
                return  render(request,"Restore.html",{"success_message":1})
        
           
        else:
            return redirect("signin") 
     

                                                            