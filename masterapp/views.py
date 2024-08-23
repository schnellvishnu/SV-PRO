from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import View,ListView,CreateView,DetailView,UpdateView,DeleteView,FormView,TemplateView
from django.urls import reverse
# from .models import Bikes,Bikeprofile,BikeApplication
from django.urls import reverse_lazy
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from masterapp.models import PrinterdataTable,Customers,ProductionOrder,ScannerTable,ProdReport

# from django_filters.views import FilterView
from django.contrib import messages

# from django_filters import FilterSet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import socket
             
import json
import threading

import os
from django.db.models import Q

import time
# import subprocess
import datetime
from queue import Queue
from multiprocessing import Event
from django.core.paginator import Paginator
from accounts.models import Register,UserrolePermissions,Loginmodel,History
# from matplotlib import pyplot as plt
import warnings
# import psycopg2
import csv

from datetime import date ,timedelta
import time
# import console
# import shutup
# Create your views here.
import sys
import psycopg2
import pandas as pd
import subprocess
from localapp.models import Printerdata,Scannerdata,LocalappLoginmodel,LocalseverHistory,Localapp_Register,Local_UserrolePermissions,Inproperly_Closed
from serverdataapp .models import ServerPrinterdata,ServerScannerdata,ServerHistory,ServerLoginmodel,BackupScannerdata
from masterapp.forms import PrinterForm,Loginform
# from datetime import datetime, timedelta
class Signinview(FormView):   #login view
    form_class = Loginform
    template_name = "login.html"
    
  
    def post(self,request,*args,**kwargs):
            # try:
            #     conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ") 
            # except:
            #     return redirect("servererror3")                           
            form=Loginform(request.POST)
            hostname = socket.gethostname()
            systemip = socket.gethostbyname(hostname)
           
            if form.is_valid():
                uname=form.cleaned_data.get("username")
                pwd=form.cleaned_data.get("password")
                userData=Localapp_Register.objects.filter(email=uname).values()
                try:
                    ud=Localapp_Register.objects.get(email=uname)
                except:
                    print("An exception occurred")            
                if userData:
                    userData1=""
                    userData1=Localapp_Register.objects.filter(password=pwd).values()
                    if  userData1:
                                ud=Localapp_Register.objects.get(email=uname)
                               
                                bt=ud.userRole
                                uname=ud.Name
                                perm=Local_UserrolePermissions.objects.filter(activity_name="printerjobs").values()   #permission checking
                                if bt=="admin":
                                    if(perm[0]['admin']['READ']=="Checked"):
                                                            
                                        Local_obj1 = LocalappLoginmodel.objects.get(id=1)
                                        Local_ip1= Local_obj1.ip_address  
                                            
                                        Local_obj2 = LocalappLoginmodel.objects.get(id=2)
                                        Local_ip2= Local_obj2.ip_address     
                                        
                                        Local_obj3 = LocalappLoginmodel.objects.get(id=3)
                                        Local_ip3= Local_obj3.ip_address                    
                                        if systemip == Local_ip1:                  
                                                obj = LocalappLoginmodel.objects.get(id=1)
                                                detailObj=LocalappLoginmodel.objects.filter(id=1).update(loginuname=uname,userrole=bt,ip_address=systemip)
                                        elif systemip == Local_ip2:
                                                obj = LocalappLoginmodel.objects.get(id=2)
                                                detailObj=LocalappLoginmodel.objects.filter(id=2).update(loginuname=uname,userrole=bt,ip_address=systemip) 
                                        
                                        elif systemip == Local_ip3:
                                                obj = LocalappLoginmodel.objects.get(id=3)
                                                detailObj=LocalappLoginmodel.objects.filter(id=3).update(loginuname=uname,userrole=bt,ip_address=systemip)         
                                        else:
                                            print("IP NOT fOUND")
                                        # This Is Line history.only this line activitys Are visible in this history
                                        # serverhistory model is use to this history
                                        Line_historysave=ServerHistory( modelname='Login Details',
                                                savedid="noid",
                                                operationdone='Login',
                                                donebyuser= uname,
                                                donebyuserrole=bt, 
                                                description="User "+ uname+ "\t"+"Logged in to the application server Line Number" + "\t" +obj.line ,  
                                                donedatetime=datetime.datetime.now())
                                        Line_historysave.save()    
                                        # This Try is Use For If The Sever Connection Is Ok lOGIN
                                        # And History Data Are  Send To Server
                                        # OtherWise Except Will Save The History and After Click Send To Server
                                        # Button It will be Save To Server.
                                       
                                        try:
                                            conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")                             
                                            historysave=History( modelname='Login Details',
                                                savedid="noid",
                                                operationdone='Login',
                                                donebyuser= uname,
                                                donebyuserrole=bt, 
                                                description="User "+ uname+ "\t"+"Logged in to the application server Line Number" + "\t" +obj.line ,  
                                                donedatetime=datetime.datetime.now())
                                            historysave.save()
                                            obj1 = Loginmodel.objects.get(id=1)
                                            ip1=obj1.ip_address  
                                                
                                            obj2 = Loginmodel.objects.get(id=2)
                                            ip2=obj2.ip_address     
                                            
                                            obj3 = Loginmodel.objects.get(id=3)
                                            ip3=obj3.ip_address   
                                            if systemip ==ip1:                  
                                                obj = Loginmodel.objects.get(id=1)
                                                detailObj=Loginmodel.objects.filter(id=1).update(loginuname=uname,userrole=bt,ip_address=systemip)
                                            elif systemip ==ip2:
                                                    obj = Loginmodel.objects.get(id=2)
                                                    detailObj=Loginmodel.objects.filter(id=2).update(loginuname=uname,userrole=bt,ip_address=systemip) 
                                            
                                            elif systemip ==ip3:
                                                    obj = Loginmodel.objects.get(id=3)
                                                    detailObj=Loginmodel.objects.filter(id=3).update(loginuname=uname,userrole=bt,ip_address=systemip)         
                                            else:
                                                print("IP NOT fOUND")
                                                hostname = socket.gethostname()
                                                systemip = socket.gethostbyname(hostname)
                                                print(systemip)
                                                return render(request, 'Ip-error.html', {'ip': systemip,'message':1})
                                                 
                                                
                                        except:
                                            Local_historysave=LocalseverHistory( modelname='Login Details',
                                                    savedid="noid",
                                                    operationdone='Login',
                                                    donebyuser= uname,
                                                    donebyuserrole=bt, 
                                                    description="User "+ uname+ "\t"+"Logged in to the application server Line Number" + "\t" +obj.line ,  
                                                    donedatetime=datetime.datetime.now())
                                            Local_historysave.save()        
                                        
                                        return  redirect("dashboard")
                                    else:
                                        # return HttpResponse ("Permission Denied!!!")
                                    
                                        return render(request, 'Loginalert.html',{"pm":1} )                
                                elif bt=="operator":
                                    if(perm[0]['operator']['READ']=="Checked"):
                                            hostname = socket.gethostname()
                                            systemip = socket.gethostbyname(hostname)
                                            print(systemip)
                                            Local_obj1 = LocalappLoginmodel.objects.get(id=1)
                                            Local_ip1= Local_obj1.ip_address  
                                            
                                            Local_obj2 = LocalappLoginmodel.objects.get(id=2)
                                            Local_ip2= Local_obj2.ip_address     
                                        
                                            Local_obj3 = LocalappLoginmodel.objects.get(id=3)
                                            Local_ip3= Local_obj3.ip_address                    
                                            if systemip == Local_ip1:                  
                                                obj = LocalappLoginmodel.objects.get(id=1)
                                                detailObj=LocalappLoginmodel.objects.filter(id=1).update(loginuname=uname,userrole=bt,ip_address=systemip)
                                            elif systemip == Local_ip2:
                                                obj = LocalappLoginmodel.objects.get(id=2)
                                                detailObj=LocalappLoginmodel.objects.filter(id=2).update(loginuname=uname,userrole=bt,ip_address=systemip) 
                                        
                                            elif systemip == Local_ip3:
                                                obj = LocalappLoginmodel.objects.get(id=3)
                                                detailObj=LocalappLoginmodel.objects.filter(id=3).update(loginuname=uname,userrole=bt,ip_address=systemip)         
                                            else:
                                                print("IP NOT fOUND")
                                                hostname = socket.gethostname()
                                                systemip = socket.gethostbyname(hostname)
                                                print(systemip)
                                                return render(request, 'Ip-error.html', {'ip': systemip,'message':1})
                                            Line_historysave=ServerHistory( modelname='Login Details',
                                                savedid="noid",
                                                operationdone='Login',
                                                donebyuser= uname,
                                                donebyuserrole=bt, 
                                                description="User "+ uname+ "\t"+"Logged in to the application server Line Number" + "\t" +obj.line ,  
                                                donedatetime=datetime.datetime.now())
                                            Line_historysave.save()       
                                            # This Try is Use For If The Sever Connection Is Ok LOGIN
                                            # And History Data Are  Send To Server
                                            # OtherWise Except Will Save The History and After Click Send To Server
                                            # Button It will be Save To Server 
                                            try:
                                                conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")                             
                                                historysave=History( modelname='Login Details',
                                                    savedid="noid",
                                                    operationdone='Login',
                                                    donebyuser= uname,
                                                    donebyuserrole=bt, 
                                                    description="User "+ uname+ "\t"+"Logged in to the application server Line Number" + "\t" +obj.line ,  
                                                    donedatetime=datetime.datetime.now())
                                                historysave.save()
                                                obj1 = Loginmodel.objects.get(id=1)
                                                ip1=obj1.ip_address  
                                                    
                                                obj2 = Loginmodel.objects.get(id=2)
                                                ip2=obj2.ip_address     
                                                
                                                obj3 = Loginmodel.objects.get(id=3)
                                                ip3=obj3.ip_address   
                                                if systemip ==ip1:                  
                                                    obj = Loginmodel.objects.get(id=1)
                                                    detailObj=Loginmodel.objects.filter(id=1).update(loginuname=uname,userrole=bt,ip_address=systemip)
                                                elif systemip ==ip2:
                                                        obj = Loginmodel.objects.get(id=2)
                                                        detailObj=Loginmodel.objects.filter(id=2).update(loginuname=uname,userrole=bt,ip_address=systemip) 
                                                
                                                elif systemip ==ip3:
                                                        obj = Loginmodel.objects.get(id=3)
                                                        detailObj=Loginmodel.objects.filter(id=3).update(loginuname=uname,userrole=bt,ip_address=systemip)         
                                                else:
                                                    print("IP NOT fOUND")
                                                    
                                                
                                            except:
                                                Local_historysave=LocalseverHistory( modelname='Login Details',
                                                        savedid="noid",
                                                        operationdone='Login',
                                                        donebyuser= uname,
                                                        donebyuserrole=bt, 
                                                        description="User "+ uname+ "\t"+"Logged in to the application server Line Number" + "\t" +obj.line ,  
                                                        donedatetime=datetime.datetime.now())
                                                Local_historysave.save()  
                                            
                                            return  redirect("dashboard")  
                                                         
                                    else:
                                        form=Loginform(request.POST)
                                                       
                                        return render(request, 'login.html.',{"pm":1,"form": form} )  
                                elif bt=="supervisor":
                                    if(perm[0]['supervisor']['READ']=="Checked"):
                                        Local_obj1 = LocalappLoginmodel.objects.get(id=1)
                                        Local_ip1= Local_obj1.ip_address  
                                            
                                        Local_obj2 = LocalappLoginmodel.objects.get(id=2)
                                        Local_ip2= Local_obj2.ip_address     
                                        
                                        Local_obj3 = LocalappLoginmodel.objects.get(id=3)
                                        Local_ip3= Local_obj3.ip_address                    
                                        if systemip == Local_ip1:                  
                                                obj = LocalappLoginmodel.objects.get(id=1)
                                                detailObj=LocalappLoginmodel.objects.filter(id=1).update(loginuname=uname,userrole=bt,ip_address=systemip)
                                        elif systemip == Local_ip2:
                                                obj = LocalappLoginmodel.objects.get(id=2)
                                                detailObj=LocalappLoginmodel.objects.filter(id=2).update(loginuname=uname,userrole=bt,ip_address=systemip) 
                                        
                                        elif systemip == Local_ip3:
                                                obj = LocalappLoginmodel.objects.get(id=3)
                                                detailObj=LocalappLoginmodel.objects.filter(id=3).update(loginuname=uname,userrole=bt,ip_address=systemip)         
                                        else:
                                                print("IP NOT fOUND")
                                                hostname = socket.gethostname()
                                                systemip = socket.gethostbyname(hostname)
                                                print(systemip)
                                                return render(request, 'Ip-error.html', {'ip': systemip,'message':1})
                                        Line_historysave=ServerHistory( modelname='Login Details',
                                                savedid="noid",
                                                operationdone='Login',
                                                donebyuser= uname,
                                                donebyuserrole=bt, 
                                                description="User "+ uname+ "\t"+"Logged in to the application server Line Number" + "\t" +obj.line ,  
                                                donedatetime=datetime.datetime.now())
                                        Line_historysave.save()      
                                        # This Try is Use For If The Sever Connection Is Ok LOGIN
                                        # And History Data Are  Send To Server
                                        # OtherWise Except Will Save The History and After Click Send To Server
                                        # Button It will be Save To Server 
                                        try:
                                            conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")                             
                                            historysave=History( modelname='Login Details',
                                                    savedid="noid",
                                                    operationdone='Login',
                                                    donebyuser= uname,
                                                    donebyuserrole=bt, 
                                                    description="User "+ uname+ "\t"+"Logged in to the application server Line Number" + "\t" +obj.line ,  
                                                    donedatetime=datetime.datetime.now())
                                            historysave.save()
                                            obj1 = Loginmodel.objects.get(id=1)
                                            ip1=obj1.ip_address  
                                                
                                            obj2 = Loginmodel.objects.get(id=2)
                                            ip2=obj2.ip_address     
                                            
                                            obj3 = Loginmodel.objects.get(id=3)
                                            ip3=obj3.ip_address       
                                            if systemip ==ip1:                  
                                                obj = Loginmodel.objects.get(id=1)
                                                detailObj=Loginmodel.objects.filter(id=1).update(loginuname=uname,userrole=bt,ip_address=systemip)
                                            elif systemip ==ip2:
                                                obj = Loginmodel.objects.get(id=2)
                                                detailObj=Loginmodel.objects.filter(id=2).update(loginuname=uname,userrole=bt,ip_address=systemip) 
                                                
                                            elif systemip ==ip3:
                                                obj = Loginmodel.objects.get(id=3)
                                                detailObj=Loginmodel.objects.filter(id=3).update(loginuname=uname,userrole=bt,ip_address=systemip)         
                                            else:
                                                print("IP NOT fOUND")
                                                    
                                                
                                        except:
                                            Local_historysave=LocalseverHistory( modelname='Login Details',
                                                        savedid="noid",
                                                        operationdone='Login',
                                                        donebyuser= uname,
                                                        donebyuserrole=bt, 
                                                        description="User "+ uname+ "\t"+"Logged in to the application server Line Number" + "\t" +obj.line ,  
                                                        donedatetime=datetime.datetime.now())
                                            Local_historysave.save()
                                      
                                        return  redirect("dashboard")
                                    else:
                                        return render(request, 'Loginalert.html',{"pm":1} )
                                    
                                elif bt=="masterdata":
                                    if(perm[0]['masterdata']['READ']=="Checked"):
                                        Local_obj1 = LocalappLoginmodel.objects.get(id=1)
                                        Local_ip1= Local_obj1.ip_address  
                                            
                                        Local_obj2 = LocalappLoginmodel.objects.get(id=2)
                                        Local_ip2= Local_obj2.ip_address     
                                        
                                        Local_obj3 = LocalappLoginmodel.objects.get(id=3)
                                        Local_ip3= Local_obj3.ip_address                    
                                        if systemip == Local_ip1:                  
                                                obj = LocalappLoginmodel.objects.get(id=1)
                                                line=obj.line
                                                detailObj=LocalappLoginmodel.objects.filter(id=1).update(loginuname=uname,userrole=bt,ip_address=systemip)
                                        elif systemip == Local_ip2:
                                                obj = LocalappLoginmodel.objects.get(id=2)
                                                detailObj=LocalappLoginmodel.objects.filter(id=2).update(loginuname=uname,userrole=bt,ip_address=systemip) 
                                        
                                        elif systemip == Local_ip3:
                                                obj = LocalappLoginmodel.objects.get(id=3)
                                                detailObj=LocalappLoginmodel.objects.filter(id=3).update(loginuname=uname,userrole=bt,ip_address=systemip)         
                                        else:
                                            print("IP NOT fOUND")
                                            hostname = socket.gethostname()
                                            systemip = socket.gethostbyname(hostname)
                                            print(systemip)
                                            return render(request, 'Ip-error.html', {'ip': systemip,'message':1}) 
                                            
                                        Line_historysave=ServerHistory( modelname='Login Details',
                                                savedid="noid",
                                                operationdone='Login',
                                                donebyuser= uname,
                                                donebyuserrole=bt, 
                                                description="User "+ uname+ "\t"+"Logged in to the application server Line Number" + "\t" +obj.line ,  
                                                donedatetime=datetime.datetime.now())
                                        Line_historysave.save()      
                                        # This Try is Use For If The Sever Connection Is Ok LOGIN
                                        # And History Data Are  Send To Server
                                        # OtherWise Except Will Save The History and After Click Send To Server
                                        # Button It will be Save To Server 
                                        try:
                                            conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")                             
                                            historysave=History( modelname='Login Details',
                                                    savedid="noid",
                                                    operationdone='Login',
                                                    donebyuser= uname,
                                                    donebyuserrole=bt, 
                                                    description="User "+ uname+ "\t"+"Logged in to the application server Line Number" + "\t" +obj.line ,  
                                                    donedatetime=datetime.datetime.now())
                                            historysave.save()
                                            obj1 = Loginmodel.objects.get(id=1)
                                            ip1=obj1.ip_address  
                                                
                                            obj2 = Loginmodel.objects.get(id=2)
                                            ip2=obj2.ip_address     
                                            
                                            obj3 = Loginmodel.objects.get(id=3)
                                            ip3=obj3.ip_address  
                                                 
                                            if systemip ==ip1:                  
                                                obj = Loginmodel.objects.get(id=1)
                                                detailObj=Loginmodel.objects.filter(id=1).update(loginuname=uname,userrole=bt,ip_address=systemip)
                                            elif systemip ==ip2:
                                                obj = Loginmodel.objects.get(id=2)
                                                detailObj=Loginmodel.objects.filter(id=2).update(loginuname=uname,userrole=bt,ip_address=systemip) 
                                                
                                            elif systemip ==ip3:
                                                obj = Loginmodel.objects.get(id=3)
                                                detailObj=Loginmodel.objects.filter(id=3).update(loginuname=uname,userrole=bt,ip_address=systemip)         
                                            else:
                                                print("IP NOT fOUND")
                                                    
                                                
                                        except:
                                                Local_historysave=LocalseverHistory( modelname='Login Details',
                                                        savedid="noid",
                                                        operationdone='Login',
                                                        donebyuser= uname,
                                                        donebyuserrole=bt, 
                                                        description="User "+ uname+ "\t"+"Logged in to the application server Line Number" + "\t" +obj.line ,  
                                                        donedatetime=datetime.datetime.now())
                                                Local_historysave.save()
                                        
                                        
                                        return  redirect("dashboard")
                                    else:
                                        form=Loginform(request.POST)                    
                                        return render(request, 'login.html',{"pm":1,"form": form} ) #if the permission is not there this alert will work                            
                    else:
                        form=Loginform(request.POST) 
                                            
                        return render(request, 'login.html',{"pwd":2,"form": form} )  #if the password incorrect this alert will work
                else:
                    form=Loginform(request.POST) 
                                 
                    return render(request, 'login.html',{"ud":2,"form": form} )  #if the username incorrect this alert will work
            else:
                return render(request, 'login.html' ) 
       
def signout_view(request,*args,**kwargs):   #signout view
        
            try:
                conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1")
              
                hostname = socket.gethostname()
                systemip = socket.gethostbyname(hostname)
                obj1 = Loginmodel.objects.get(id=1)
                ip1=obj1.ip_address
                
                obj2 = Loginmodel.objects.get(id=2)
                ip2=obj2.ip_address
                
                obj3 = Loginmodel.objects.get(id=3)
                ip3=obj3.ip_address
            
                if systemip ==ip1:              
                    obj = Loginmodel.objects.get(id=1)
                    line=obj.line   
                    loginuserrole=obj.userrole
                    detailObj=Loginmodel.objects.filter(id=1).update(loginuname="",ip_address=systemip)
                    
                    
                
                elif systemip ==ip2:
                    obj = Loginmodel.objects.get(id=2)
                    loginuserrole=obj.userrole
                    line=obj.line 
                    detailObj=Loginmodel.objects.filter(id=2).update(loginuname="",ip_address=systemip) 
                elif systemip ==ip3:
                    obj = Loginmodel.objects.get(id=3)
                    loginuserrole=obj.userrole
                    line=obj.line 
                    detailObj=Loginmodel.objects.filter(id=3).update(loginuname="",ip_address=systemip)     
                    
                else:
                                        
                    print("IP NOT fOUND")
                    hostname = socket.gethostname()
                    systemip = socket.gethostbyname(hostname)
                    print(systemip)
                    return render(request, 'Ip-error.html', {'ip': systemip,'inside_message':1})
                # ///////////////////////////////////
                hostname = socket.gethostname()
                systemip = socket.gethostbyname(hostname)
                Local_obj1 = LocalappLoginmodel.objects.get(id=1)
                Local_ip1=Local_obj1.ip_address
                
                Local_obj2 = LocalappLoginmodel.objects.get(id=2)
                Local_ip2=Local_obj2.ip_address
                
                Local_obj3 = LocalappLoginmodel.objects.get(id=3)
                Local_ip3=Local_obj3.ip_address
            
                if systemip ==Local_ip1:              
                    obj = LocalappLoginmodel.objects.get(id=1)
                    line=obj.line   
                    loginuserrole=obj.userrole
                    detailObj=LocalappLoginmodel.objects.filter(id=1).update(loginuname="",ip_address=systemip)
                    
                    
                
                elif systemip ==Local_ip2:
                    obj = LocalappLoginmodel.objects.get(id=2)
                    loginuserrole=obj.userrole
                    line=obj.line 
                    detailObj=LocalappLoginmodel.objects.filter(id=2).update(loginuname="",ip_address=systemip) 
                elif systemip ==Local_ip3:
                    obj = LocalappLoginmodel.objects.get(id=3)
                    loginuserrole=obj.userrole
                    line=obj.line 
                    detailObj=LocalappLoginmodel.objects.filter(id=3).update(loginuname="",ip_address=systemip)     
                    
                else:
                                        
                    print("Local iP NOT fOUND")  
                
                    
                
                logout(request)
                historysave=History(modelname='Logout Details',
                                                savedid="noid",
                                                operationdone='Logout',
                                                donebyuser= obj.loginuname,
                                                donebyuserrole=loginuserrole, 
                                                description="User"+"\t"+ obj.loginuname + "\t"+ "Logout from the application server Line Number" + "\t"+ obj.line ,
                                                donedatetime=datetime.datetime.now())
                historysave.save()
                
                Line_historysave=ServerHistory( modelname='Login Details',
                                                savedid="noid",
                                                operationdone='Logout',
                                                donebyuser= obj.loginuname,
                                                donebyuserrole=loginuserrole, 
                                                description="User"+"\t"+ obj.loginuname + "\t"+ "Logout from the application server Line Number" + "\t"+ obj.line ,
                                                donedatetime=datetime.datetime.now())
                Line_historysave.save() 
                print("logout")   
                return redirect("signin")
            except:
                # if the server connection was lost this except is working.  
                # This Except Is Used to Delete LocalappLogin model username. 
                # and save history to localapp
                hostname = socket.gethostname()
                systemip = socket.gethostbyname(hostname)
                Local_obj1 = LocalappLoginmodel.objects.get(id=1)
                Local_ip1=Local_obj1.ip_address
                
                Local_obj2 = LocalappLoginmodel.objects.get(id=2)
                Local_ip2=Local_obj2.ip_address
                
                Local_obj3 = LocalappLoginmodel.objects.get(id=3)
                Local_ip3=Local_obj3.ip_address
            
                if systemip ==Local_ip1:              
                    obj = LocalappLoginmodel.objects.get(id=1)
                    line=obj.line   
                    loginuserrole=obj.userrole
                    detailObj=LocalappLoginmodel.objects.filter(id=1).update(loginuname="",ip_address=systemip)
                    
                    
                
                elif systemip ==Local_ip2:
                    obj = LocalappLoginmodel.objects.get(id=2)
                    loginuserrole=obj.userrole
                    line=obj.line 
                    detailObj=LocalappLoginmodel.objects.filter(id=2).update(loginuname="",ip_address=systemip) 
                elif systemip ==Local_ip3:
                    obj = LocalappLoginmodel.objects.get(id=3)
                    loginuserrole=obj.userrole
                    line=obj.line 
                    detailObj=LocalappLoginmodel.objects.filter(id=3).update(loginuname="",ip_address=systemip)     
                    
                else:
                                        
                    print("IP NOT fOUND")
                    hostname = socket.gethostname()
                    systemip = socket.gethostbyname(hostname)
                    print(systemip)
                    return render(request, 'Ip-error.html', {'ip': systemip,'inside_message':1})  
                
                    
                
                logout(request)
                Local_historysave=LocalseverHistory(modelname='Logout Details',
                                                savedid="noid",
                                                operationdone='Logout',
                                                donebyuser= obj.loginuname,
                                                donebyuserrole=loginuserrole, 
                                                description="User"+"\t"+ obj.loginuname + "\t"+ "Logout from the application server Line Number" + "\t"+ obj.line ,
                                                donedatetime=datetime.datetime.now())
                Local_historysave.save()
                print("logout")
                
                Line_historysave=ServerHistory( modelname='Login Details',
                                                savedid="noid",
                                                operationdone='Logout',
                                                donebyuser= obj.loginuname,
                                                donebyuserrole=loginuserrole, 
                                                description="User"+"\t"+ obj.loginuname + "\t"+ "Logout from the application server Line Number" + "\t"+ obj.line ,
                                                donedatetime=datetime.datetime.now())
                Line_historysave.save()    
                return redirect("signin")

# ....................................................

# class Dashboard(TemplateView):
                            
#         template_name = "dashboard.html"
                        
        

def listing(request) : 
       
            try:
            
                conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")
                hostname = socket.gethostname()
                systemip = socket.gethostbyname(hostname) 
                    
                Line1 = Loginmodel.objects.get(id=1)
                ip1= Line1.ip_address     
                                        
                Line2 = Loginmodel.objects.get(id=2)
                ip2=Line2.ip_address
                    
                Line3=Loginmodel.objects.get(id=3)
                ip3=Line3.ip_address
                if systemip==ip1:
                            
                        uname = Loginmodel.objects.get(id=1)
                        loginname=uname.loginuname
                        loginuserrole=uname.userrole
                    
                elif systemip==ip2: 
                        uname = Loginmodel.objects.get(id=2)
                        loginname=uname.loginuname
                        loginuserrole=uname.userrole
                elif systemip==ip3: 
                        uname = Loginmodel.objects.get(id=3)
                        loginname=uname.loginuname
                        loginuserrole=uname.userrole
                else:
                    hostname = socket.gethostname()
                    systemip = socket.gethostbyname(hostname)                     
                    return render(request, 'cu-list.html',{'ip':systemip,'ip_error':1})                         
            
                if(loginname!=""):
                    
                
                                        
                    
                
                        
                    posts1 = PrinterdataTable.objects.all().filter(status="Running",ip_address=systemip).order_by('-id') #list only the jobs with running status(when the printer didnt stop in proper manner)
                    le=len(posts1)
                    if posts1:
                                    
                        p = Paginator(posts1, 10)           #navigating to the previous and after pages
                        page_num=request.GET.get('page',1)
                        try:
                            page=p.page(page_num)
                        except EmptyPage:
                            page=p.page(1)
                        if le==0:
                            nu=1 
                        else:
                            nu=0 
                        try:
                            with open('jobid.csv', mode='r') as file:
                                csvreader = csv.reader(file)
                                for row in csvreader:
                                    fgid=row[0]
                                
                            detailsObj =Printerdata.objects.get(id=fgid)
                    
                    
                    
                    
                            
                        except:
                            print("jobid.csv not found")
                            try:
                                with open('data.csv', mode='r') as file:
                                    csvreader = csv.reader(file)
                                    for row in csvreader:
                                        fgid=row[0]
                                detailsObj =Printerdata.objects.get(id=fgid)
                            except:
                                print("data.csv not found") 
                            try:
                                with open('data.csv', mode='r') as file:
                                    csvreader = csv.reader(file)
                                    for row in csvreader:
                                        fgid=row[0]
                                detailsObj =Printerdata.objects.get(id=fgid)
                            except:
                                print("data.csv not found")      
                
                        context = {'page_obj':page,
                                "nu":nu
                            }
                    
                        
                            
                        return render(request, 'cu-list.html',{'page_obj':page, "name":loginname,"id":fgid}) 
                
                    else:
                        
                            posts = PrinterdataTable.objects.all().filter(ip_address=systemip).order_by('-id') #every printer jobs corresponding to a particular ipaddress...every jobs will come when printer stopping in normal way                       
                            p = Paginator(posts, 10)  # creating a paginator object
                            page_num=request.GET.get('page',1)
                            #page navigation
                            le=len(posts)
                            if le==0:
                               datalength=1 
                            else:
                               datalength=0     
                            try:
                                page=p.page(page_num)
                            except EmptyPage:
                                page=p.page(1)
                            # context = {'page_obj':page
                            
                            #         } 
                            try:
                                with open('jobid.csv', mode='r') as file:
                                    csvreader = csv.reader(file)
                                    for row in csvreader:
                                        fgid=row[0]
                                    
                                detailsObj =Printerdata.objects.get(id=fgid)
                    
                    
                    
                    
                    
                            except:
                                    print("jobid.csv not found")
                                    try:
                                        with open('data.csv', mode='r') as file:
                                            csvreader = csv.reader(file)
                                            for row in csvreader:
                                                fgid=row[0]
                                        detailsObj =Printerdata.objects.get(id=fgid)
                                    except:
                                        print("data.csv not found")  
                            return render(request, 'cu-list.html', {'page_obj':page,"name":loginname,"datalength":datalength,"id":fgid})  
                                        
                else:
                    return redirect("signin")      
            except:
            
                return redirect("databaseerror") 
                
    

        
    
def searchBar(request):   #searchbar in the printer jobs listpage
  
       
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
                # print(query)
                if query:
                    jobs = PrinterdataTable.objects.filter(lot=query)  #check wheather there is any match with searching item
                    return render(request, 'cu-list.html', {'page_obj':jobs,'search':1,"name":loginname})
                else:
                    # print("No information to show")
                    return render(request, 'cu-list.html', {})
        else:
            return redirect("signin")  


 #----------------------------------------------------------------------
class Autovisionopenview(View):    #opening autovision software 
    def get(self,request,id):
        try:
            conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")
        except:
           
            return redirect("databaseerror")
        
        try:    
            
            hostname = socket.gethostname()
            systemip = socket.gethostbyname(hostname) 
            
            Line1 = LocalappLoginmodel.objects.get(id=1)
            ip1= Line1.ip_address
            print(ip1)     
                                   
            Line2 = LocalappLoginmodel.objects.get(id=2)
            ip2=Line2.ip_address
            
            Line3=LocalappLoginmodel.objects.get(id=3)
            ip3=Line3.ip_address
            if systemip==ip1:
                    
                uname = LocalappLoginmodel.objects.get(id=1)
                loginname=uname.loginuname
                loginuserrole=uname.userrole
                line=uname.line
            
            elif systemip==ip2: 
                uname = LocalappLoginmodel.objects.get(id=2)
                loginname=uname.loginuname
                loginuserrole=uname.userrole
                line=uname.line
            elif systemip==ip3: 
                uname = LocalappLoginmodel.objects.get(id=3)
                loginname=uname.loginuname
                loginuserrole=uname.userrole
                line=uname.line
        except:
            print("Login model data have some issue in Autovision view")    
        if(loginname!=""): 
                # try:
                #   os.system('start D:\Omron\AutoVision\AutoVISION.exe') 
                # except:
                #     return redirect("autovisionopenerror")
               
                try:  
                    qs=PrinterdataTable.objects.get(id=id)
                    prodObj=ProductionOrder.objects.get(batch_number=qs.lot)
                    po=prodObj.process_order_number  
                
                   
                
                    inexid=qs.id
                    gtin=qs.gtin
                  
                    processordernumber=po
                    expiration_date=qs.expiration_date
                    lot=qs.lot
                    numbers=qs.numbers
                    hrf=qs.hrf
                    quantity=qs.quantity
                    type=qs.type
                    status=qs.status
                    ip_address=qs.ip_address
                    printed_numbers=qs.printed_numbers
                    balanced_serialnumbers=qs.balanced_serialnumbers
                    responsefield=qs.responsefield
                   
                    stopbtnresponse=qs.stopbtnresponse
                    
                    return_slno_btn_response=qs.return_slno_btn_response
                    batchstopmessage=qs.batchstopmessage
                   
                    child_numbers=qs.child_numbers
                    scannergradefield=qs.scannergradefield
                    loadpause=qs.loadpause
                   
                    Rejectednumbers=qs.Rejectednumbers
                    acceptednumbers=qs.acceptednumbers
                    rows=[inexid]
                   
                except:
                    print("database data have some issue")    
                
              
                
                # LM=Loginmodel.objects.get(id=1)
                # inexid1=1
                # username=LM.loginuname
                # print(username)
                # userrole=LM.userrole
                # ip_address=LM.ip_address
                # line=LM.line
                
                # # loginuname=
                
                # LM2=Loginmodel.objects.get(id=2)
                # inexid2=2
                # username2=LM2.loginuname
                # userrole2=LM2.userrole
                # ip_address2=LM2.ip_address
                # line=LM2.line
                
                
                # LM3=Loginmodel.objects.get(id=3)
                # inexid3=3
                # username3=LM3.loginuname
                # userrole3=LM3.userrole
                # ip_address3=LM3.ip_address
                # line=LM3.line
                try:
                   
                    with open("data.csv", 'w', newline='') as csvfile:
                            csvwriter = csv.writer(csvfile)
                            # csvwriter.writerow(fields)
                            csvwriter.writerow(rows)
                    with open('data.csv', mode='r') as file:
                        csvreader = csv.reader(file)
                        for row in csvreader:
                               m=(row[0])
                               
                except:
                    print("Data.csv error.Because id not saved to data.csv file")
                # try: 
                #     detailObj=LocalappLoginmodel.objects.filter(id=1).update(      
                #     # Login1_data_add_to_local_server = LocalappLoginmodel(
                #         login_id=inexid1,
                #         loginuname = username,
                #         userrole=userrole,
                #         ip_address=ip_address,
                #         line=line
                #     )
                #     # Login1_data_add_to_local_server.save()
                #     print("saved")        
                #     detailObj=LocalappLoginmodel.objects.filter(id=2).update(
                #     # Login2_data_add_to_local_server =LocalappLoginmodel(
                #         login_id=inexid2,
                #         loginuname=username2,
                #         userrole=userrole2,
                #         ip_address=ip_address2,
                #         line=line
                #     )
                #     # Login2_data_add_to_local_server.save()
                #     detailObj=LocalappLoginmodel.objects.filter(id=3).update(
                #     # Login3_data_add_to_local_server =LocalappLoginmodel(
                #         login_id=inexid3,
                #         loginuname=username3,
                #         userrole=userrole3,
                #         ip_address=ip_address3,
                #         line=line
                #     )
                #     # Login3_data_add_to_local_server.save()
                #     # print(Login1_data_add_to_local_server.ip_address)
                # except:
                #     print("Login Data add To Server have some Problem in Autovision View")    
              
                # obj = PrinterdataTable.objects.get(id=id)
                # detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(preparebuttonresponse=1)    
                        
                try:
                    # detailObj=Printerdata.objects.filter(id=1).update(
                    data_add_to_local_server=Printerdata(
                        
                    
                                            printer_id=inexid,
                                            gtin=gtin,
                                            ip_address=ip_address,
                                            processordernumber= processordernumber,
                                            expiration_date=expiration_date,
                                            lot=lot,
                                            numbers=numbers,
                                            hrf=hrf,
                                            quantity=quantity,
                                            type=type,
                                            status=status,
                                           
                                            # responsefield=responsefield,
                                            
                                           
                                            # stopbtnresponse=stopbtnresponse,
                                           
                                            # return_slno_btn_response=return_slno_btn_response,
                                            # batchstopmessage=batchstopmessage,
                                            # loadpause=loadpause,
                                            
                                            scannergradefield=scannergradefield,
                                           
                                            child_numbers=child_numbers,
                                            Rejectednumbers=Rejectednumbers,
                                            acceptednumbers=acceptednumbers,
                                            printed_numbers=printed_numbers,
                                            balanced_serialnumbers=balanced_serialnumbers,
                                            )
                    data_add_to_local_server.save()
                    obj = PrinterdataTable.objects.get(id=id)
                    detailObj=PrinterdataTable.objects.filter(lot=obj.lot).update(jobstatus="Added")
                    
                    historysave=History(modelname='PrinterdataTable',
                                    savedid="noid",
                                    operationdone='Job Added To Line',
                                    donebyuser=loginname,
                                    donebyuserrole=loginuserrole, 
                                    description="Batch "+lot+" Added  Line Number"+ line + "by"+" "+ loginname,
                                    donedatetime=datetime.datetime.now())
                    historysave.save()
                    
                    Line_historysave=ServerHistory( modelname='Login Details',
                                                savedid="noid",
                                                operationdone='Logout',
                                                donebyuser= obj.loginuname,
                                                donebyuserrole=loginuserrole, 
                                                description="User"+"\t"+ obj.loginuname + "\t"+ "Logout from the application server Line Number" + "\t"+ obj.line ,
                                                donedatetime=datetime.datetime.now())
                    Line_historysave.save()        
                        
                    
                #     print(data_add_to_local_server.printer_id) 
                #     print(data_add_to_local_server.ip_address) 
                #     print(data_add_to_local_server.gtin)
                #     print(data_add_to_local_server.type) 
                #     print(data_add_to_local_server.lot)   
                except:
                    print("local serer data have problem") 
                
            
                # return  render(request,"scannersoftware.html",{"job":qs,"added":1})
                return redirect("indexpage")
        else:
            return redirect("signin")

#.............................................................................. 

class Viewprinterview(View):  #load the values to printer
    threadstart=0
    # pausestart=0

    q=Queue()   #queue initialisation
    event=Event()
    
    def get(self,request,id):  
       
        qs=Printerdata.objects.get(id=id)
        po=qs.processordernumber
        intid=qs.id
        rows=[intid]
        if qs.load_button_resp==0:   
          os.system('start D:\Omron\AutoVision\AutoVISION.exe') 
        try:
                   
            with open("jobid.csv", 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                          
                csvwriter.writerow(rows)
            with open('jobid.csv', mode='r') as file:
                csvreader = csv.reader(file)
                for row in csvreader:
                    m=(row[0])
        except:
            print("job.csv file not found") 
            
        try:
                   
            with open("data.csv", 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                            # csvwriter.writerow(fields)
                csvwriter.writerow(rows)
            with open('data.csv', mode='r') as file:
                csvreader = csv.reader(file)
                for row in csvreader:
                    m=(row[0])
               
        except:
            print("data.csv file not found")     
                                  
           
        return render(request,"cu-edit.html",{"qs":qs,"po":po})
           
            
           

            
            
    def printerfun(self,num,serialno,q,event,gtin,lot,expire,hrfkey,hrfvalue,type,id):   #load everything in the starting ...in program load batch button is working here
        self.serialno=serialno
        self.gtin=gtin
        self.expire=expire
        self.lot=lot
    
                                
        self.hrfkey=hrfkey
        self.hrfvalue=hrfvalue
        self.type=type 
        self.id=id
                    
        printer_socket_4 = socket.socket()
        printer_port_4=34567
        printer_socket_4.connect(('192.168.200.150', printer_port_4))

        if(type=="type2"):
                                
                    printer_load_command= "L,new7.lbl\x04"
                    printer_socket_4.send(printer_load_command.encode()) 
                    load_response=printer_socket_4.recv(1024).decode()
                      
                    printer_prepare_command= "E\x04"        
                    printer_socket_4.send(printer_prepare_command.encode()) 
                    prepare_response=printer_socket_4.recv(1024).decode()
                    uy1=serialno[0:1]
                    
                    for sn in uy1:                
                 
                                   printer_field_send_command= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x04"
                                   printer_socket_4.send(printer_field_send_command.encode()) 
                                   field_response=printer_socket_4.recv(1024).decode()
                                                
                                   printer_value_send_command= "QAC\x09"+"(17)"+expire+"(10)"+lot + "(01)" +  gtin + "(21)" + sn +  "\x09" + "Exp\x09" + expire + "\x09Lot" + "\x09" + lot + "\x09" + "Gtin\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"
                                   printer_socket_4.send(printer_value_send_command.encode()) 
                                   value_response=printer_socket_4.recv(1024).decode() 
                                          
                                   printer_start_command= "F2\x04"
                                   printer_socket_4.send(printer_start_command.encode()) 
                                   start_response=printer_socket_4.recv(1024).decode()
                     
                    print('Received from server: ' + field_response)
                    print('Received from server: ' + value_response)         
                    print('Received from server: ' + start_response)
           
        elif(type=="type5"):
                     printer_load_command_1= "L,new8.lbl\x04"
                     printer_socket_4.send(printer_load_command_1.encode()) 
                     load_response_1=printer_socket_4.recv(1024).decode()  
                     
                     printer_prepare_command_1= "E\x04"        
                     printer_socket_4.send(printer_prepare_command_1.encode()) 
                     prepare_response_1=printer_socket_4.recv(1024).decode()
                     
                     uy2=serialno[0:1]     
                     for sn in uy2: 
                        printer_field_send_command_1= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x09"+"hrf"+"\x09hrfvalue"+"\x04"
                        printer_socket_4.send(printer_field_send_command_1.encode()) 
                        field_response_1=printer_socket_4.recv(1024).decode()
                                                   
                                   # message6= "QAC\x09" + "55555777779(10)45612(21)\x09GTIN\x09" + gtin+"\x09"+ "lot\x09" + lot +"\x09" +"exp\x09" + expire+"\x09"+"serialno\x09"+sn+"\x04"
                        printer_value_send_command_1= "QAC\x09" + "(17)" + expire + "(10)" + lot + "(01)" +  gtin + "(21)" + sn + "(45)"+ hrfvalue+ "\x09" + "Exp\x09" + expire + "\x09"+"Lot" + "\x09" + lot + "\x09" + "Gtin"+ "\x09" +  gtin + "\x09" + "Slno" + "\x09" + sn + "\x09" + hrfkey + "\x09" + hrfvalue + "\x04"
                        printer_socket_4.send(printer_value_send_command_1.encode()) 
                        value_response_1=printer_socket_4.recv(1024).decode() 
                                          
                        printer_start_command_1= "F2\x04"
                        printer_socket_4.send(printer_start_command_1.encode()) 
                        start_response_1=printer_socket_4.recv(1024).decode()
                                        
                     print('Received from server: ' + load_response_1)
                     print('Received from server: ' + prepare_response_1) 
                     print('Received from server: ' + field_response_1)
                     print('Received from server: ' + value_response_1)         
                     print('Received from server: ' + start_response_1)
                  
        elif(type=="type1"):
                     printer_load_command_2= "L,new5.lbl\x04"
                     printer_socket_4.send(printer_load_command_2.encode()) 
                     load_response_2=printer_socket_4.recv(1024).decode()  
                     
                     printer_prepare_command_2= "E\x04"        
                     printer_socket_4.send(printer_prepare_command_2.encode()) 
                     prepare_response_2=printer_socket_4.recv(1024).decode()
                     
                     uy=serialno[0:1] 
                                   
                     for sn in uy:
                                   printer_field_send_command_2= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x04"
                                   printer_socket_4.send(printer_field_send_command_2.encode()) 
                                   field_response_2=printer_socket_4.recv(1024).decode()
                                                  
                                   # message6= "QAC\x09" + "55555777779(10)45612(21)\x09GTIN\x09" + gtin+"\x09"+ "lot\x09" + lot +"\x09" +"exp\x09" + expire+"\x09"+"serialno\x09"+sn+"\x04"
                                   printer_value_send_command_2= "QAC\x09" + "(17)" + expire + "(10)" + lot + "(01)" +  gtin + "(21)" + sn +"(45)"+ hrfvalue +  "\x09" + "Exp\x09" + expire + "\x09Lot" + "\x09" + lot + "\x09" + "GTIN\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"
                                   printer_socket_4.send(printer_value_send_command_2.encode()) 
                                   value_response_2=printer_socket_4.recv(1024).decode() 
                                          
                                   printer_start_command_2= "F2\x04"
                                   printer_socket_4.send(printer_start_command_2.encode()) 
                                   start_response_2=printer_socket_4.recv(1024).decode()
       
                     print('Received from server: ' + field_response_2)
                     print('Received from server: ' + value_response_2)         
                     print('Received from server: ' + start_response_2)

    def scannerfun(self,num,id,gtin,serialno,sl,printednumbers,q,event,lot,expire,hrfkey,hrfvalue,ip_address,child_numbers,type):
        self.id=id                    
        self.serialno=serialno
        self.sl=sl
        self.printednumbers=printednumbers
        self.gtin=gtin
        self.lot=lot
        self.expire=expire
        self.hrfkey=hrfkey
        self.hrfvalue=hrfvalue
        self.ip_address=ip_address
        self.child_numbers=child_numbers 
        self.type= type                
        counter=0
        d=0
        co=-1
        n=1
        # s3 = socket.socket()
       
        printer_socket_1 = socket.socket()
        printer_port_1=34567
        
        printer_socket_1.connect(('192.168.200.150',printer_port_1))   #connecting the printer to 34567 port
        
        Begindatestring = date.today() 
        # print(Begindatestring)
        t = time.localtime()

        # Format the time as a string
        current_time = time.strftime("%H:%M:%S", t)
        # print(current_time)
          
        obj = Printerdata.objects.get(id=id)
        detailObj=Printerdata.objects.filter(lot=obj.lot)
      
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
            print(systemip)
            return redirect("ip-error",ip=systemip)
            # return render(request, 'Ip-error.html', {'ip': systemip,'inside_message':1})
                                        
        sllen=len(sl)
        # print("sllen count")
        # print(sllen)
        upjso=[]
        cd=0
        drg=[] 
        rejectednumberslist=[]
        Acceptednumberslist=[]
        
        Notdetectedlist=[]
        childnumberslist=[]
        
                 
        Line_historysave=ServerHistory( modelname='PrinterdataTable',
                                        savedid="noid",
                                        operationdone='Batch Loaded',
                                        donebyuser=loginname,
                                        donebyuserrole=loginuserrole, 
                                        description="Loaded the batch of  "+ lot +" "+"by"+" "+ loginname,
                                        donedatetime=datetime.datetime.now())
        Line_historysave.save() 
        try:
            conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")                    
            historysave=History(modelname='PrinterdataTable',
                                savedid="noid",
                                operationdone='Batch Loaded',
                                donebyuser=loginname,
                                donebyuserrole=loginuserrole, 
                                description="Loaded the batch of  "+ lot +" "+"by"+" "+ loginname,
                                donedatetime=datetime.datetime.now())
            historysave.save()
            print("history for load batch saved")
        except:
            Local_historysave=LocalseverHistory(modelname='PrinterdataTable',
                                savedid="noid",
                                operationdone='Batch Loaded',
                                donebyuser=loginname,
                                donebyuserrole=loginuserrole, 
                                description="Loaded the batch of  "+ lot +" "+"by"+" "+ loginname,
                                donedatetime=datetime.datetime.now())
            Local_historysave.save()
        # s4 = socket.socket()
        # port=34567
                        
        # s4.connect(('192.168.200.150', port)) 
        while True: 
                if(Viewprinterview.q.empty()):
                    try: 
                        printer_socket_2 = socket.socket()
                        printer_port_2=34567
                        printer_socket_2.settimeout(2)
                        printer_socket_2.connect(('192.168.200.150', printer_port_2))
                        
                        belt_speed_command= "I5\x04"
                        printer_socket_2.send(belt_speed_command.encode()) 
                        belt=printer_socket_2.recv(1024).decode() 
                        # print("message931",belt[0:1])
                        belt_speed=belt[0:1]
                                           
                        read_output_command= "IE\x04"
                        printer_socket_2.send(read_output_command.encode()) 
                        read_output_data=printer_socket_2.recv(1024).decode()
                                                                            
                                            
                        data_to_string=str(read_output_data[0:1])
                        # print("viewprinterview loop working")
                        
                        
                                            
                        for c in data_to_string:
                            ascii_values_data_to_string=ord(c)
                        # print("value",ascii_values_data_to_string)    
                        
                           
                    except socket.timeout:
                        print("timeout") 
                        ascii_values_data_to_string=0 
                    # if(belt_speed == "0"):
                    #     print("00000000")
                    # else:
                    #     print("8888888888")  
                    # if(belt_speed=="0"):
                    #     if(ascii_values == 1): 
                    #         jso=json.dumps(upjso)
                    #         serialvar=sl[counter]
                    #         serialno.remove(sl[counter])
                    #         gh=json.dumps(serialno)
                    #         obj = Printerdata.objects.get(id=id)
                    #         detailObj=Printerdata.objects.filter(lot=obj.lot).update(numbers=gh)
                    #         try:
                    #             with open("Missingjson/"+lot+".csv", 'a', newline='') as file:
                                                        
                    #                 writer = csv.writer(file)
                                                    
                    #                 valuelist = [serialvar,"Missed",gtin,lot],
                                                            
                    #                 writer.writerows(valuelist)
                                                        
                    #         except:
                    #                 print("No DATA AVAILABLE FOR ADDING TO CSV") 
                    #         counter=counter-1                      
                                                     
                    if(ascii_values_data_to_string == 3 and belt_speed != "0") : 
                            scanner_socket_1 = socket.socket()
                            scanner_port_1=2001
                            scanner_socket_1.settimeout(2)  
                            scanner_socket_1.connect(('192.168.200.134', scanner_port_1))  #connecting the scanner to 2001 port 
                           
                            Begindatestring = date.today() 
      
                            t = time.localtime()

                               
                            current_time = time.strftime("%H:%M:%S", t)                    
                            try: 
                                
                                scanner_decode_data=scanner_socket_1.recv(1024).decode()
                                print("this is  data",scanner_decode_data)
                                # print(type)
                                
                                if(type=="type2"):
                                    decoded_grade=scanner_decode_data[0] 
                                    confidence=scanner_decode_data[1] 
                                    decoded_gtin=scanner_decode_data[11:25]
                                    meanconfidence=scanner_decode_data[2:7]
                                    scanned_serial_number=scanner_decode_data[29:38]
                                    
                                    # print(meanconfidence)
                                elif(type== "type1" or type== "type5"):
                                    decoded_grade=scanner_decode_data[0]
                                    confidence=scanner_decode_data[1]
                                    decoded_gtin=scanner_decode_data[9:23]
                                    meanconfidence=scanner_decode_data[2:7]
                                    scanned_serial_number=scanner_decode_data[25:34]
                                   
                                    # print(textbatch)  
                                    # print(meanconfidence)                                     
                                if d==1:
                                    try:
                                        upjso.append(sl[counter])
                                    except:
                                        print("No serialnumbers available for printing")   
                                    serilength=len(serialno)
                                   
                                    try:
                                        # if(v=="4" and confidence=="1" and meanconfidence>="0.800"):
                                        #             grade="A"
                                        # elif(v=="3" and confidence=="1" and meanconfidence>="0.800"):
                                        #             grade="B"
                                        # elif (v=="2" and confidence=="1" and meanconfidence>="0.800"):
                                        #             grade="C"
                                        # elif (v=="1" and confidence=="1" and meanconfidence>="0.800"):
                                        #             grade="D"
                                        # else:
                                        #             grade="F" 
                                        if(decoded_grade=="4" ):
                                                    grade="A"
                                        elif(decoded_grade=="3" ):
                                                    grade="B"
                                        elif (decoded_grade=="2" ):
                                                    grade="C"
                                        elif (decoded_grade=="1" ):
                                                    grade="D"
                                        else:
                                                    grade="F" 
                                                
                                        r={"serialnumber":sl[counter],
                                                    "grade":grade}
                                        # print("333333333333333",r)
                                        if(gtin==decoded_gtin):
                                            if(scanned_serial_number==sl[counter]):                    
                                                if(decoded_grade=="4" or decoded_grade=="3"):                
                                                    print(r)
                                                    b=json.dumps(r)
                                                    gradeupdation=Scannerdata(
                                                    gtin=gtin,
                                                    ip_address=ip_address,
                                                    grade=b,
                                                    status="Accepted",
                                                    serialnumber=sl[counter],
                                                    gradevalue=grade,
                                                    lot=lot,
                                                    type=type
                                                    )
                                                    gradeupdation.save()
                                                    obj = Printerdata.objects.get(id=id)
                                                    # print(obj.lot)
                                                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(scannergradefield=b)
                                                    jso=json.dumps(upjso)
                                                    serialvar3=sl[counter]
                                                    serialno.remove(sl[counter])
                                                    gh=json.dumps(serialno)
                                                    print(sl[counter])
                                                    obj = Printerdata.objects.get(id=id)
                                                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(printed_numbers=jso,numbers=gh)
                                                
                                                    with open("Acceptedjson/"+lot+".csv", 'a', newline='') as file:
                                                
                                                        writer = csv.writer(file)
                                            
                                                        valuelist = [serialvar3,grade,"Accepted",lot,gtin],
                                                    
                                                        writer.writerows(valuelist)
                                                    # updatedjson=json.loads(jso)
                                                
                                                    df = pd.read_csv("Acceptedjson/"+lot+".csv")
                                                    row_count = len(df)
                                                    row_count1= row_count+1 
                                                    

                                                    print("Number of rows:", row_count1)
                                                    try:
                                                        conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1")
                                                        
                                                    
                                                        
                                                        jobs7 = Scannerdata.objects.filter(lot=lot,status="Accepted")
                                                        acceptedcount=len(jobs7)
                                                        scObj7=ProdReport.objects.filter(batch_number=lot).update(acceptedcount=acceptedcount,current_production_date=Begindatestring,current_production_time=current_time)
                                                        print(acceptedcount, 'is last in the list ✅')                
                                                    
                                                        
                                                    except:
                                                        print("server connection losted in between the process of reports data add to server") 
                                                    try:
                                                        scObj7=Printerdata.objects.filter(lot=lot).update(current_production_date=Begindatestring,current_production_time=current_time)
                                                        print( 'curent date time updated ✅')                    
                                                    except:
                                                        print("current time not update")       
                                                    if(counter==sllen-1):           #If the last number is detecting it will clear the serialno
                                                        print(serialno)                    
                                                        del serialno[:]
                                                        obj = Printerdata.objects.get(id=id)
                                                        detailObj=Printerdata.objects.filter(gtin=obj.gtin).update(numbers=serialno)                  
                                                        print("detect serialnumber cleared")     
                                                    counter=counter+1
                                                else:    
                                                    print("grade less then B")
                                                    print(r)
                                                    b=json.dumps(r)
                                                    gradeupdation=Scannerdata(
                                                    gtin=gtin,
                                                    ip_address=ip_address,
                                                    grade=b,
                                                    status="Rejected",
                                                    serialnumber=sl[counter],
                                                    gradevalue=grade,
                                                    lot=lot,
                                                    type=type
                                                    )
                                                    gradeupdation.save()
                                                
                                                    
                                                    obj = Printerdata.objects.get(id=id)
                                                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(scannergradefield=b)
                                                    jso=json.dumps(upjso)
                                                    serialvar2=sl[counter]
                                                    serialno.remove(sl[counter])
                                                    gh=json.dumps(serialno)
                                                    print(sl[counter])
                                                    obj = Printerdata.objects.get(id=id)
                                                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(printed_numbers=jso,numbers=gh)
                                                    
                                                    
                                                    with open("jsonfiles/"+lot+".csv", 'a', newline='') as file:
                                                
                                                        writer = csv.writer(file)
                                            
                                                        valuelist = [serialvar2,grade,"Rejected",lot,gtin],
                                                        writer.writerows(valuelist)    
                                                    df1 = pd.read_csv("jsonfiles/"+lot+".csv")
                                                    row_count1 = len(df1)
                                                    row_count2= row_count1+1 

                                                    print("Number of rejected rows:", row_count2)
                                                    try:
                                                        conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1")
                                                    
                                                    
                                                        
                                                        jobs7 = Scannerdata.objects.filter(lot=lot,status="Rejected")
                                                        rejectedcount=len(jobs7)
                                                        scObj7=ProdReport.objects.filter(batch_number=lot).update(rejectedbycameracount=rejectedcount,current_production_date=Begindatestring,current_production_time=current_time)
                                                        
                                                        print(rejectedcount,'is last in the list ✅')
                                                                    
                                                    
                                                        
                                                    
                                                        
                                                    except:
                                                        print("server connection losted in between the process of reports data add to server")    
                                                    try:    
                                                        scObj7=Printerdata.objects.filter(lot=lot).update(current_production_date=Begindatestring,current_production_time=current_time)
                                                        print( 'curent date time updated ✅')     
                                                    except:
                                                        print("current time not updated")
                                                    
                                                    if(counter==sllen-1):           #If the last number is detecting it will clear the serialno
                                                        print(serialno)                    
                                                        del serialno[:]
                                                        obj = Printerdata.objects.get(id=id)
                                                        detailObj=Printerdata.objects.filter(lot=obj.lot).update(numbers=serialno)                  
                                                        print("detect serialnumber cleared")
                                                    counter=counter+1
                                            else: 
                                               print("serialnumber not equal")
                                            #    counter=counter+1 
                                                            
                                        else:                   
                                            print("not equal")
                                            r={"serialnumber":sl[counter],
                                                    "grade":"Not Detected"}
                                            print(r)
                                            b=json.dumps(r)
                                            gradeupdation=Scannerdata(
                                            gtin=gtin,
                                            ip_address=ip_address,
                                            numbers=b,
                                            status="Damaged",
                                            serialnumber=sl[counter],
                                            gradevalue="Not Detected",
                                            lot=lot,
                                            type=type
                                            )
                                            gradeupdation.save()
                                            obj = Printerdata.objects.get(id=id)
                                            detailObj=Printerdata.objects.filter(lot=obj.lot).update(scannergradefield=b)
                                            jso=json.dumps(upjso)
                                            serialvar1=sl[counter]
                                            serialno.remove(sl[counter])
                                            gh=json.dumps(serialno)
                                            obj = Printerdata.objects.get(id=id)
                                            detailObj=Printerdata.objects.filter(lot=obj.lot).update(numbers=gh)
                                            try:
                                                with open("Notdetectedjson/"+lot+".csv", 'a', newline='') as file:
                                            
                                                    writer = csv.writer(file)
                                        
                                                    valuelist = [serialvar1,"Not Detected",gtin,lot],
                                                
                                                    writer.writerows(valuelist)
                                            
                                            except:
                                                print("No DATA AVAILABLE FOR ADDING TO CSV")
                                            try:
                                                conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1")                
                                                jobs9 = Scannerdata.objects.filter(lot=lot,status="Damaged")
                                                damagedcount=len(jobs9)
                                                print(damagedcount)
                                                scObj7=ProdReport.objects.filter(batch_number=lot).update(damagedcount=damagedcount,current_production_date=Begindatestring,current_production_time=current_time)
                                            except:
                                                print("database connection lost")
                                                
                                            try:
                                                scObj7=Printerdata.objects.filter(lot=lot).update(current_production_date=Begindatestring,current_production_time=current_time)
                                                print( 'curent date time updated ✅') 
                                            except:
                                                print("current time not update")
                                            if(counter==sllen-1):     #if the last number is not detecting it will clear the serialno
                                                print(serialno)                    
                                                del serialno[:]
                                                obj = Printerdata.objects.get(id=id)
                                                detailObj=Printerdata.objects.filter(lot=obj.lot).update(numbers=serialno)
                                                print("not detecte serialnumber cleared")                  
                                            counter=counter+1
                                            
                                    except:
                                        print("serialnumbers finished")
                            except socket.timeout:
                            
                            
                            
                                qs = Printerdata.objects.get(id=id)
                                
                            
                                
                                                                
                                                    
                                    
                                print("Not Scanned")
                                r={"serialnumber":sl[counter],
                                    "grade":"Not Scanned"}
                                print(r)
                                b=json.dumps(r)
                                gradeupdation=Scannerdata(
                                                    gtin=gtin,
                                                    ip_address=ip_address,
                                                    numbers=b,
                                                    status="Not Scanned",
                                                    serialnumber=sl[counter],
                                                    gradevalue="Not Scanned",
                                                    lot=lot,
                                                    type=type
                                                    )
                                gradeupdation.save()
                                obj = Printerdata.objects.get(id=id)
                                detailObj=Printerdata.objects.filter(lot=obj.lot).update(scannergradefield=b)
                                jso=json.dumps(upjso)
                                serialvar=sl[counter]
                                serialno.remove(sl[counter])
                                gh=json.dumps(serialno)
                                obj = Printerdata.objects.get(id=id)
                                detailObj=Printerdata.objects.filter(lot=obj.lot).update(numbers=gh)
                                try:
                                        with open("NotScannedjson/"+lot+".csv", 'a', newline='') as file:
                                                    
                                            writer = csv.writer(file)
                                                
                                            valuelist = [serialvar,"Not Scanned",gtin,lot],
                                                        
                                            writer.writerows(valuelist)
                                                    
                                except:
                                        print("No DATA AVAILABLE FOR ADDING TO CSV") 
                                if(counter==sllen-1):     #if the last number is not detecting it will clear the serialno
                                        print(serialno)                    
                                        del serialno[:]
                                        obj = Printerdata.objects.get(id=id)
                                        detailObj=Printerdata.objects.filter(lot=obj.lot).update(numbers=serialno)
                                        print("not detecte serialnumber cleared")                  
                                counter=counter+1 
                                    
                                        
                                                                    
                                print("Didn't receive  data! [Timeout 5s]")
                    else:
                            
                        nj=0 
                       
                    
                                                            
                else:
                        d=Viewprinterview.q.get()
                        print("d",d)
                        if d==0:
                                     
                                         
                                    try:
                                       
                                        printer_socket_3 = socket.socket()
                                        printer_port_3=34567
                                        printer_socket_3.connect(('192.168.200.150', printer_port_3)) 
                                        
                                        
                                        
                                         
                                        
                                        print("Batch stop But Not update")
                                        
                                        printer_stop_command= "F0\x04"
                                        printer_socket_3.send(printer_stop_command.encode()) 
                                        stop_command_response=printer_socket_3.recv(1024).decode()
                                       
                                    except:
                                      
                                        print("Printer connection losted but Batch stop successfully")    
                                    if(serialno==[]):
                                        obj = Printerdata.objects.get(id=id)
                                        detailObj=Printerdata.objects.filter(lot=obj.lot).update(stop_button_resp=1,status="Printing Finished")                  
                                       
                                        
                                    else:
                                        obj = Printerdata.objects.get(id=id)
                                        detailObj=Printerdata.objects.filter(lot=obj.lot).update(stop_button_resp=1,status="Stopped")
                                         
                                    detailsObj1 = Printerdata.objects.get(id=id)  
                                           
                                    obj = Printerdata.objects.get(id=id)
                                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(load_button_resp=0,stop_button_resp=1) 
                                    Line_historysave=ServerHistory(modelname='PrinterdataTable',
                                            savedid="noid",
                                            operationdone='Batch Stoped',
                                            donebyuser=loginname,
                                            donebyuserrole=loginuserrole, 
                                            description="Stopped the batch "+ lot +" "+"by"+" "+ loginname,
                                            donedatetime=datetime.datetime.now())
                                    Line_historysave.save() 
                                    try:
                                        conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")                    
                                        historysave=History(modelname='PrinterdataTable',
                                            savedid="noid",
                                            operationdone='Batch Stoped',
                                            donebyuser=loginname,
                                            donebyuserrole=loginuserrole, 
                                            description="Stopped the batch "+ lot +" "+"by"+" "+ loginname,
                                            donedatetime=datetime.datetime.now())
                                        historysave.save()
                                    except:
                                        Local_historysave=LocalseverHistory(modelname='PrinterdataTable',
                                            savedid="noid",
                                            operationdone='Batch Stoped',
                                            donebyuser=loginname,
                                            donebyuserrole=loginuserrole, 
                                            description="Stopped the batch "+ lot +" "+"by"+" "+ loginname,
                                            donedatetime=datetime.datetime.now())
                                        Local_historysave.save()   
                                        
                                    y=[]
                                    y1=[]
                                    try:          
                                        file = "jobid.csv"
                                        
                                        if(os.path.exists(file) and os.path.isfile(file)): 
                                            os.remove(file) 
                                            print("file deleted") 
                                        else: 
                                            print("file not found")     
                                    except:
                                        print("No Such csv File for deleteing")
                                    try: 
                                      conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")                          
                                      scObj7=ProdReport.objects.filter(batch_number=lot).update(acceptedcount=0,damagedcount=0,rejectedbycameracount=0,challengedcount=0,current_production_date=Begindatestring,current_production_time=current_time)
                                    except:
                                        print("pro Report Not Update because server connection losted")              
                                   
                                                    
                                   
                                                   
                                    break 
                                 
                                                
    def post(self,request,id):
                         
                qs=Printerdata.objects.get(id=id)
                form=PrinterForm(request.POST,instance=qs)
                form2=PrinterForm(request.POST,instance=qs)
                id=qs.id    
                gtin=qs.gtin 
                ponumber=qs.processordernumber
                expire =str(qs.expiration_date)
                lot=qs.lot
                type=qs.type
                hrf=qs.hrf 
                printednumbers=qs.printed_numbers
                ip_address=qs.ip_address
                child_numbers=qs.child_numbers
                po=qs.processordernumber
                # prodObj=ProductionOrder.objects.get(gtin_number=qs.gtin)
                # po=prodObj.process_order_number 
                try: 
                    if(type=="type2"):
                        hrfkey="null"                   
                        hrfvalue="null"                  
                    # print(printednumbers) 
                    else:
                                                
                        hrfjson=json.loads(hrf) 
                        hrf1value=hrfjson["hrf1value"]
                        hrf1key=hrfjson["hrf1"]
                        hrf2value=hrfjson["hrf2value"]
                        hrf2key=hrfjson["hrf2"]
                        hrf3value=hrfjson["hrf3value"]
                        hrf3key=hrfjson["hrf3"]
                        hrf4value=hrfjson["hrf4value"]
                        hrf4key=hrfjson["hrf4"]
                        hrf5key=hrfjson["hrf5"]
                        hrf5value=hrfjson["hrf5value"]
                        hrf6key=hrfjson["hrf6"]
                        hrf6value=hrfjson["hrf6value"]
                        
                
                        if(hrf1key!="" or hrf1key!="null"):
                            hrfkey=hrf1key
                        elif(hrf2key!="" or hrf2key!="null"):
                            hrfkey=hrf2key
                        elif(hrf3key!="" or hrf3key!="null"):
                            hrfkey=hrf3key
                        elif(hrf4key!="" or hrf4key!="null"):
                            hrfkey=hrf4key
                        elif(hrf5key!="" or hrf5key!="null"):
                            hrfkey=hrf5key
                        elif(hrf6key!="" or hrf6key!="null"):
                            hrfkey=hrf6key
                        
                    
                        if(hrf1value!="" or hrf1value!="null"):
                            hrfvalue=hrf1value
                        elif(hrf2value!="" or hrf2value!="null"):
                            hrfvalue=hrf2value
                        elif(hrf3value!="" or hrf3value!="null"):
                            hrfvalue=hrf3value
                        elif(hrf4value!="" or hrf4value!="null"):
                            hrfvalue=hrf4value
                        elif(hrf5value!="" or hrf5value!="null"):
                            hrfvalue=hrf5value
                        elif(hrf6value!="" or hrf6value!="null"):
                            hrfvalue=hrf6value
                except:
                    print("no hrf")        
            
                # print(hrfkey)
                # print(hrfvalue)
                try:    
                    serial=qs.numbers
                    serialnum=qs.numbers
                    serialno=json.loads(serial)
                    sl=json.loads(serialnum)
                except:
                    print("No serialnumber available in viewprinterview")
                        
                
                try:
                    scanner_socket = socket.socket()
                    scanner_socket.settimeout(2)  
                    scanner_port=2001
                    scanner_socket.connect(('192.168.200.134', scanner_port))
                except socket.timeout:
                    # return redirect("scanner-message") 
                    # obj = Printerdata.objects.get(id=id)
                    # detailObj=Printerdata.objects.filter(lot=obj.lot).update(preparebuttonresponse=0)
                    if (qs.load_button_resp == 0):
                               loadstopvariable=0
                    else:
                        loadstopvariable=1                        
                    return render(request, 'cu-edit.html', {'loadstopvariable':loadstopvariable,'qs': qs,'errormess':"data52ex","po":po,"alert":0}) 
                           
                try:
                    printer_socket = socket.socket()
                    printer_port=34567
                    printer_socket.settimeout(1)  
                    printer_socket.connect(('192.168.200.150', printer_port))
                    
                    message52= "K7\x04"   #cartridge expiration alert
                    printer_socket.send(message52.encode()) 
                    cartridge_expiration=printer_socket.recv(1024).decode() 
                    cartridge_expiration_data=cartridge_expiration[:-1]
                    if(qs.start_button_resp == 0):
                        print("printer paused")
                    else:
                                        
                        return render(request, 'cu-edit.html', {'loadstopvariable':1,'qs': qs,'yu':0,'errormess':"cartridge_expiration_data","po":po,"loadpausealert":1}) 
                     
                    if(Viewprinterview.threadstart==0):  #if the value  is 0 then set to 1
                        if  TimeoutError:
                            messages.success(request,"your application has posted successfully")                                    
                        # obj = Printerdata.objects.get(id=id)
                        # detailObj=Printerdata.objects.filter(lot=obj.lot).update(load_button_resp=1,stop_button_resp=0,start_button_resp=0,status="Running")
                        
                        # detailsObj = Printerdata.objects.get(id=id) 
                        # prodObj=ProductionOrder.objects.get(gtin_number=detailsObj.gtin)
                        # detailObj1=ProductionOrder.objects.filter(gtin_number=prodObj.gtin_number).update(status="Running")
                        
                        Viewprinterview.threadstart=1
                        Viewprinterview.q.put(Viewprinterview.threadstart) 
                        # print(Viewprinterview.threadstart)
                    
                        y = threading.Thread(target=self.scannerfun,args=(10,id,gtin,serialno,sl,printednumbers,Viewprinterview.q,Viewprinterview.event,lot,expire,hrfkey,hrfvalue,ip_address,child_numbers,type))  #initialising 2 threads
                        x = threading.Thread(target=self.printerfun,args=(10,serialno,Viewprinterview.q,Viewprinterview.event,gtin,lot,expire,hrfkey,hrfvalue,type,id))
                        y.start() 
                        #start both of them
                        # print("keri")
                        x.start() 
                                        
                    elif(Viewprinterview.threadstart==1):#if the value  is 1 then set to 0
                        Viewprinterview.threadstart=0                    
                        Viewprinterview.q.put(Viewprinterview.threadstart) #inserting to queue
                        Viewprinterview.event.set()
                        # print("keriendu")
                        print("thread",Viewprinterview.threadstart)
                        # obj = Printerdata.objects.get(id=id)
                        # detailObj=Printerdata.objects.filter(lot=obj.lot).update(stop=1) 
                       
                        time.sleep(7)
                      
                        try:
                                oh=9
                                return redirect("batch-stop-message")
                           
                      
                        except:
                            
                            return render(request, 'cu-edit.html', {'loadstopvariable':1,'qs': qs,'yu':0,'errormess':cartridge_expiration_data,"po":po,"alert":3})             
                    
                    time.sleep(10)
                    loadstopvariable=1
                    obj = Printerdata.objects.get(id=id)
                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(load_button_resp=1,stop_button_resp=0,start_button_resp=0,status="Running")
                    
                
                
                                            
                    
                    return render(request, 'cu-edit.html', {'loadstopvariable':loadstopvariable,'qs': qs,'yu':0,'errormess':cartridge_expiration_data,"po":po,"alert":2})
                except socket.timeout:
                    
                    print("An exception occurred true")
                    
                    # return redirect("cand-home")
                  
                    # PauseClassview.pausestart=0  
                    # obj = Printerdata.objects.get(id=id)
                    # detailObj=Printerdata.objects.filter(lot=obj.lot).update(preparebuttonresponse=0) 
                    if (qs.load_button_resp == 0):
                        loadstopvariable = 0
                    else:
                        loadstopvariable = 1 
                    # obj = Printerdata.objects.get(id=id)
                    # detailObj=Printerdata.objects.filter(lot=obj.lot).update(loadpause=0)     
                                               
                    return render(request, 'cu-edit.html', {'loadstopvariable':loadstopvariable,'qs': qs,'yu':0,'errormess':"cartridge_expiration_data","po":po,"alert":1})   
                   
            
#............................................................................


class Serialcount(View):
    def get(self,request,id):
        qs = Printerdata.objects.get(id=id) 
        serialno=qs.numbers                   
        try:                    
            scanner_socket_2 = socket.socket()
            scanner_socket_2.settimeout(1)
            scanner_port_2=2001
       
            scanner_socket_2.connect(('192.168.200.134', scanner_port_2))
            scannerlost=0
            if(qs.return_button_resp ==1):
                printer_status=0                 
            else:
                 printer_status=1                     
            
        except socket.timeout:
            scannerlost=1
           
            try:
                # bat_file_path =r"D:\PROJECT-MULTIPLE-SCANN-PRINT\vision-pro\visionsetup\2.bat"
                bat_file_path =r"2.bat"
            
                bat_file=bat_file_path
                subprocess.run([bat_file])                        
            except:
                print("bat file not working")
            obj = Printerdata.objects.get(id=id)
            detailObj=Printerdata.objects.filter(lot=obj.lot).update(start_button_resp=0,return_button_resp=1)
            
            try:        
                s2 = socket.socket()
                port2=34567
                s2.settimeout(0.5) 
                s2.connect(('192.168.200.150', port2))
            
                message30= "QAF\x04"
                s2.send(message30.encode()) 
                data31=s2.recv(1024).decode()
            except socket.timeout:
                print("printer not on")
           
             
        
        try:                    
            s2 = socket.socket()
            port2=34567
            s2.settimeout(0.2) 
            s2.connect(('192.168.200.150', port2))
       
            
            if(qs.return_button_resp ==1):
                ethernet_conn_miss_message= "QAF\x04"
                s2.send(ethernet_conn_miss_message.encode()) 
                ethernet_conn_miss_data= s2.recv(1024).decode()
                printer_paused=1  
            else:
                printer_paused=0                      
            printerlost=0
           
            # print("printer_paused",printer_paused) 
                
        except socket.timeout:
            printerlost=1
            printer_paused=0  
           
            
            try:
                # bat_file_path =r"D:\PROJECT-MULTIPLE-SCANN-PRINT\vision-pro\visionsetup\2.bat"
                bat_file_path =r"2.bat"
            
            
                bat_file=bat_file_path
                subprocess.run([bat_file])                        
            except:
                print("bat file not working")
            obj = Printerdata.objects.get(id=id)
            detailObj=Printerdata.objects.filter(lot=obj.lot).update(start_button_resp=0,return_button_resp=1,stop_button_resp=1)     
           
        try:
            
            s2 = socket.socket()
            port2=34567
            s2.settimeout(0.4) 
            s2.connect(('192.168.200.150', port2))
       
        
            message320="I2\x04"           
            s2.send(message320.encode()) 
            data360=s2.recv(1024).decode()
            printstatus=data360[1:2]
            if(qs.return_button_resp == 1):
                printer_status=0  
            elif(printstatus=="h" or printstatus=="l" or qs.return_button_resp == 0):
                printer_status=1 
                                 
            else:
              printer_status=0                       
              obj = Printerdata.objects.get(id=id)
              detailObj=Printerdata.objects.filter(lot=obj.lot).update(start_button_resp=0)
            # printer_status=0      
        except socket.timeout:
            ok=1
            printer_status=2 
                                  
                                    
        try:                    
            scanner_socket_3 = socket.socket()
            scanner_socket_3.settimeout(1)
            scanner_port_3=2001
       
            scanner_socket_3.connect(('192.168.200.134', scanner_port_3))
            scannerlost=0 
            
            scanner_data=scanner_socket_3.recv(1024).decode()
            # print("this is data",scanner_data)
            decoded_grade=scanner_data[0]
            if(decoded_grade=="4"):
                grade="A"
            elif(decoded_grade=="3"):
                grade="B"
            elif (decoded_grade=="2"):
                grade="C"
            elif (decoded_grade=="1"):
                grade="D"
            elif(decoded_grade=="0"):
                grade="F" 
            else:
                grade="Not detect"                        
            type=qs.type
            if(type=="type2"):
                h=scanner_data[38:]    
                decoded_serialnumber=scanner_data[29:38]
                # print(decoded_serialnumber)
                r={"serialnumber":decoded_serialnumber,
                        "grade":grade}
            elif(type=="type5" or type=="type1"):
                h=scanner_data[38:]    
                decoded_serialnumber=scanner_data[25:34]
                # print(decoded_serialnumber)
                r={"serialnumber":decoded_serialnumber,
                    "grade":grade}   
            
            
        except socket.timeout:
            r="nodata"
                                        
                                                                          
        qs=Printerdata.objects.get(id=id)
        serialno=qs.numbers
            
            
        po=qs.processordernumber
        if serialno==[]:
            serilength=0 
        else :                   
            serial=json.loads(serialno)
            
            serilength=len(serial)
            # print("snnnn",serilength)
           
            # mess="server connection ok"
          
        return render(request,"Length.html",{"qs":qs,"sc":serilength,"scannerlost":scannerlost,"printerlost":printerlost, "printer_status": printer_status,"printer_paused":printer_paused,"decode360":r}) 
    
      
       
class Data_Recive_From_scanner(View):
    def get(self,request,id):
        try:                    
            scanner_socket_4 = socket.socket()
            scanner_socket_4.settimeout(1)
            scanner_port_4=2001
       
            scanner_socket_4.connect(('192.168.200.134', scanner_port_4))
            scannerlost=0      
        except socket.timeout:
            scannerlost=1
            # plc connection for stopping convire
            # fg=[4,0,0,0,3,0,0,0,2,0,0,0,1]
            # by=bytearray(fg)
            # by[0]=1
            # by[4]=0
            # by[8]=2
            # by[12]=1
            # try:
            #     plc_conn = socket.socket()
            #     plc_port=12000
            #     plc_conn.settimeout(1)  
            #     plc_conn.connect(('192.168.200.55', plc_port))
            #     s=by
            #     message4556=by     
            #     plc_conn.send(message4556) 
            #     data360= plc_conn.recv(1024).decode()
            #     print(data360)
            #     data_to_string=str(data360)
            #     for c in data_to_string:
            #         ascii_values_data_to_string=ord(c)
            #         print(ascii_values_data_to_string)
            # except:
            #     print(" plc not responding")
            # obj = Printerdata.objects.get(id=id)
            # detailObj=Printerdata.objects.filter(lot=obj.lot).update(preparebuttonresponse=0,loadpause=0)
          
             
        
        try:                    
            printer_socket_6 = socket.socket()
            printer_socket_6.settimeout(1)
            printer_port_6=34567
       
            printer_socket_6.connect(('192.168.200.150', printer_port_6)) 
            printerlost=0      
        except socket.timeout:
            printerlost=1 
            # plc connection for stopping convire
            # fg=[4,0,0,0,3,0,0,0,2,0,0,0,1]
            # by=bytearray(fg)
            # by[0]=1
            # by[4]=0
            # by[8]=2
            # by[12]=1
            # try:
            #     plc_conn = socket.socket()
            #     plc_port=12000
            #     plc_conn.settimeout(1)  
            #     plc_conn.connect(('192.168.200.55', plc_port))
            #     s=by
            #     message4556=by     
            #     plc_conn.send(message4556) 
            #     data360= plc_conn.recv(1024).decode()
            #     print(data360)
            #     data_to_string=str(data360)
            #     for c in data_to_string:
            #         ascii_values_data_to_string=ord(c)
            #         print(ascii_values_data_to_string)
            # except:
            #     print(" plc not responding")
           
        try:
            

            
            printer_status_read_command="I2\x04"           
            printer_socket_6.send(printer_status_read_command.encode()) 
            status_response=printer_socket_6.recv(1024).decode()
            printstatus= status_response[1:2]
            if(printstatus=="h" or printstatus=="l"): 
                printstatus_null=1  
            else:
                printstatus_null=0 
                obj = Printerdata.objects.get(id=id)
                detailObj=Printerdata.objects.filter(lot=obj.lot).update(start_button_resp=0)                                                     
                           
        except:
            print("Printer status null")
            printstatus_null=2 
            # plc connection for stopping convire
            # fg=[4,0,0,0,3,0,0,0,2,0,0,0,1]
            # by=bytearray(fg)
            # by[0]=1
            # by[4]=0
            # by[8]=2
            # by[12]=1
            # try:
            #     plc_conn = socket.socket()
            #     plc_port=12000
            #     plc_conn.settimeout(1)  
            #     plc_conn.connect(('192.168.200.55', plc_port))
            #     s=by
            #     message4556=by     
            #     plc_conn.send(message4556) 
            #     data360= plc_conn.recv(1024).decode()
            #     print(data360)
            #     data_to_string=str(data360)
            #     for c in data_to_string:
            #         ascii_values_data_to_string=ord(c)
            #         print(ascii_values_data_to_string)
            # except:
            #     print(" plc not responding")
            # obj = Printerdata.objects.get(id=id)
            # detailObj=Printerdata.objects.filter(lot=obj.lot).update(start_button_resp=0)                                
        try:
            scanner_socket_5 = socket.socket()
            scanner_socket_5.settimeout(6)
            scanner_port_5=2001
       
            scanner_socket_5.connect(('192.168.200.134', scanner_port_5))

        except:
            print("okk")   
        try:
            scanner_data=scanner_socket_5.recv(1024).decode()   
            
            
            scannerdataerror=0                               
        except socket.timeout:
            qs=Printerdata.objects.get(id=id)
            if qs.start_button_resp == 1:
               scannerdataerror=1        
            else: 
                scannerdataerror=0
            # return redirect("dashboard")                                      
        
        qs=Printerdata.objects.get(id=id)
        serialno=qs.numbers
            
            
        po=qs.processordernumber
        if serialno==[]:
            serilength=0 
        else :                   
            serial=json.loads(serialno)
            
            serilength=len(serial)
            # print(serilength)
            # print(scannerlost)
            # mess="server connection ok"
                                  
        return render(request,"Datafromscanner.html",{"qs":qs,"sc":serilength,"scannerlost":scannerlost,"printerlost":printerlost, "printstatus_null": printstatus_null,"scannerdataerror":scannerdataerror})   
          
           
class CU_edit_ConnectionIssue(View):
    # printer_status=4 ;                 
    def get(self,request,id):
                            
        try:                    
            scanner_socket_6 = socket.socket()
            scanner_socket_6.settimeout(1)
            scanner_port_6=2001
       
            scanner_socket_6.connect(('192.168.200.134', scanner_port_6))
            scannerlost=0      
        except socket.timeout:
            scannerlost=1
           
           
            # obj = Printerdata.objects.get(id=id)
            # detailObj=Printerdata.objects.filter(lot=obj.lot).update(preparebuttonresponse=0,loadpause=0)
          
             
        
        try:                    
            printer_socket_7 = socket.socket()
            printer_socket_7.settimeout(1)
            printer_port_7=34567
       
            printer_socket_7.connect(('192.168.200.150', printer_port_7)) 
            printerlost=0      
        except socket.timeout:
            printerlost=1 
            # plc connection for stopping convire
            try:
                # bat_file_path =r"D:\PROJECT-MULTIPLE-SCANN-PRINT\vision-pro\visionsetup\2.bat"
                bat_file_path =r"2.bat"
            
                bat_file=bat_file_path
                subprocess.run([bat_file])                        
            except:
                print("bat file not working")
           
           
        try:
            printer_socket_8 = socket.socket()
            printer_socket_8.settimeout(1)
            printer_port_8=34567
       
            printer_socket_8.connect(('192.168.200.150', printer_port_8)) 
            
            printer_status_read_command_1="I2\x04"           
            printer_socket_8.send(printer_status_read_command_1.encode()) 
            status_response_1=printer_socket_8.recv(1024).decode()
            printstatus= status_response_1[1:2]
            qs=Printerdata.objects.get(id=id)
            if(qs.load_button_resp == 1 ):
                if(printstatus=="h" or printstatus=="l"):
                    printer_status=1                  
                else:
                    printer_status=0                       
                    obj = Printerdata.objects.get(id=id)
                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(start_button_resp=0)
            else:
                printer_status=2 
                # this 2 is not used                            
        except:
            ok=1 
            printer_status=2
            # plc connection for stopping convire
                                        
        qs=Printerdata.objects.get(id=id) 
        return render(request,"Cu-Connection-issues.html",{"qs":qs,"scannerlost":scannerlost,"printerlost":printerlost, "printer_status": printer_status})                   
                 
class Common_Connection_Ajax_View(View):
    def get(self,request,id):
        qs = Printerdata.objects.get(id=id)
    #   if(qs. load_button_resp==1): 
                          
        try:                    
            scanner_socket_2 = socket.socket()
            scanner_socket_2.settimeout(1)
            scanner_port_2=2001
       
            scanner_socket_2.connect(('192.168.200.134', scanner_port_2))
            scannerlost=0
            if(qs.return_button_resp ==1 and qs.load_button_resp==1):
                printer_status=0                 
            else:
                 printer_status=1                     
            
        except socket.timeout:
            if(qs.load_button_resp ==1):
               scannerlost=1
            else:
               scannerlost=0                     
           
            try:
                # bat_file_path =r"D:\PROJECT-MULTIPLE-SCANN-PRINT\vision-pro\visionsetup\2.bat"
                bat_file_path =r"2.bat"
            
                bat_file=bat_file_path
                subprocess.run([bat_file])                        
            except:
                print("bat file not working")
            obj = Printerdata.objects.get(id=id)
            detailObj=Printerdata.objects.filter(lot=obj.lot).update(start_button_resp=0,return_button_resp=1)
            
            try:        
                s2 = socket.socket()
                port2=34567
                s2.settimeout(0.5) 
                s2.connect(('192.168.200.150', port2))
            
                message30= "QAF\x04"
                s2.send(message30.encode()) 
                data31=s2.recv(1024).decode()
            except socket.timeout:
                print("printer not on")
           
             
        
        try:                    
            s2 = socket.socket()
            port2=34567
            s2.settimeout(0.2) 
            s2.connect(('192.168.200.150', port2))
       
            
            if(qs.return_button_resp ==1):
                ethernet_conn_miss_message= "QAF\x04"
                s2.send(ethernet_conn_miss_message.encode()) 
                ethernet_conn_miss_data= s2.recv(1024).decode()
                printer_paused=1  
            else:
                printer_paused=0                      
            printerlost=0
           
            # print("printer_paused",printer_paused) 
                
        except socket.timeout:
            if(qs.load_button_resp ==1):
                printerlost=1
                printer_paused=0 
            else:
               printerlost=0
               printer_paused=0                        
           
            
            try:
                # bat_file_path =r"D:\PROJECT-MULTIPLE-SCANN-PRINT\vision-pro\visionsetup\2.bat"
                bat_file_path =r"2.bat"
            
            
                bat_file=bat_file_path
                subprocess.run([bat_file])
                # print("888888888888888888")                        
            except:
                print("bat file not working")
            obj = Printerdata.objects.get(id=id)
            detailObj=Printerdata.objects.filter(lot=obj.lot).update(start_button_resp=0,return_button_resp=1,stop_button_resp=1)     
           
        try:
            
            s2 = socket.socket()
            port2=34567
            s2.settimeout(0.4) 
            s2.connect(('192.168.200.150', port2))
       
        
            message320="I2\x04"           
            s2.send(message320.encode()) 
            data360=s2.recv(1024).decode()
            printstatus=data360[1:2]
            if(qs.return_button_resp == 1 and  qs.load_button_resp==1):
                printer_status=0  
            elif(printstatus=="h" or printstatus=="l" or qs.return_button_resp == 0):
                printer_status=1 
                                 
            else:
              printer_status=2                       
              obj = Printerdata.objects.get(id=id)
              detailObj=Printerdata.objects.filter(lot=obj.lot).update(start_button_resp=0)
            # printer_status=0      
        except socket.timeout:
            ok=1
            printer_status=2 
        return render(request,"Common_Ajax.html",{"qs":qs,"scannerlost":scannerlost,"printerlost":printerlost, "printer_status": printer_status,"printer_paused":printer_paused})                                                   
                                    
    #   else:
    #      loadbutton_resp_working= "not_loaded any batch"                      
                                        
                                                                          
        
          
    #   return render(request,"Common_Ajax.html",{"qs":qs})                         
                   
#  . ................................................................................ 

class Batchstopmessageview(View) :
    def get(self,request):  
     
            with open('data.csv', mode='r') as file:
                csvreader = csv.reader(file)
                for row in csvreader:
                    fgid=row[0]
                    print(fgid)
                    
                # Begindatestring = date.today() 
                # print(Begindatestring)
                # t = time.localtime()

                # # Format the time as a string
                # current_time = time.strftime("%H:%M:%S", t)
                # print(current_time)    
                qs=Printerdata.objects.get(id=fgid)
                # prodObj=ProductionOrder.objects.get(gtin_number=qs.gtin)
                po=qs.processordernumber  
                # print(po)
                # obj = Printerdata.objects.get(printer_id=fgid)
                # prodObj=PrinterdataTable.objects.get(gtin_number=obj.gtin)
                # print(prodObj.gtin)
                inexid=qs.id
                gtin=qs.gtin
                processordernumber=po
                expiration_date=qs.expiration_date
                lot=qs.lot
                numbers=qs.numbers
                hrf=qs.hrf
                quantity=qs.quantity
                type=qs.type
                status=qs.status
                ip_address=qs.ip_address
                printed_numbers=qs.printed_numbers
                balanced_serialnumbers=qs.balanced_serialnumbers
                start_button_resp=qs.start_button_resp
                load_button_resp=qs.load_button_resp
                server_button_resp=qs.server_button_resp
             
                stop_button_resp=qs.stop_button_resp
                # start_pause_btnresponse=qs.start_pause_btnresponse
                # pause_stop_btnresponse=qs.pause_stop_btnresponse
                # return_slno_btn_response=qs.return_slno_btn_response
                # batchstopmessage=qs.batchstopmessage
                # label_response=qs.label_response
                child_numbers=qs.child_numbers
                scannergradefield=qs.scannergradefield
                # loadpause=qs.loadpause
                Rejectednumbers=qs.Rejectednumbers
                acceptednumbers=qs.acceptednumbers
                current_time=qs.current_production_time
                current_date=qs.current_production_date
                print("batch stop time",current_time)
                print("batch stop date",current_date)
                # qws=Printerdata.objects.get(printer_id=fgid)
                # inid=qws.printer_id
                obj = Printerdata.objects.get(id=fgid)
                # print(obj.gtin)
                # prodObj=PrinterdataTable.objects.get(gtin_number=obj.gtin)
                # print(prodObj.gtin)
                try:
                    printerdata_to_server=ServerPrinterdata(printer_id=fgid,numbers=numbers,
                                            balanced_serialnumbers=balanced_serialnumbers,
                                            # responsefield=False,
                                            # preparebuttonresponse=preparebuttonresponse,
                                            # stopbtnresponse=True,
                                            # start_pause_btnresponse=start_pause_btnresponse,
                                            # pause_stop_btnresponse=pause_stop_btnresponse,
                                            # return_slno_btn_response=return_slno_btn_response,
                                            # batchstopmessage=batchstopmessage,
                                            # label_response=label_response,
                                            child_numbers=child_numbers,
                                            scannergradefield=scannergradefield,
                                            # loadpause=loadpause,
                                            Rejectednumbers=Rejectednumbers,
                                            acceptednumbers=acceptednumbers,
                                            gtin=gtin,
                                            processordernumber=po,
                                            expiration_date=expiration_date,
                                            lot=lot,
                                            hrf=qs.hrf,
                                            quantity=quantity,
                                            type=type,
                                            status=status,
                                            ip_address=ip_address,
                                            printed_numbers=printed_numbers,
                                            start_button_resp=start_button_resp,
                                            load_button_resp=load_button_resp,
                                        
                                        
                                            stop_button_resp=stop_button_resp,
                                            server_button_resp=1,
                                            production_date=current_date,
                                            production_time=current_time
                                           
                                            )
                    printerdata_to_server.save() 
                      
                except:
                    detailObj=ServerPrinterdata.objects.filter(lot=lot).update(printer_id=fgid,numbers=numbers,
                                        balanced_serialnumbers=balanced_serialnumbers,
                                        # responsefield=False,
                                        # preparebuttonresponse=preparebuttonresponse,
                                        # stopbtnresponse=True,
                                        # start_pause_btnresponse=start_pause_btnresponse,
                                        # pause_stop_btnresponse=pause_stop_btnresponse,
                                        # return_slno_btn_response=return_slno_btn_response,
                                        # batchstopmessage=batchstopmessage,
                                        # label_response=label_response,
                                        # loadpause=loadpause,
                                         start_button_resp=start_button_resp,
                                        load_button_resp=load_button_resp,
                                        
                                        
                                        stop_button_resp=stop_button_resp,
                                        child_numbers=child_numbers,
                                        scannergradefield=scannergradefield,
                                        
                                        Rejectednumbers=Rejectednumbers,
                                        acceptednumbers=acceptednumbers,
                                        gtin=gtin,
                                        processordernumber=po,
                                        expiration_date=expiration_date,
                                        lot=lot,
                                        hrf=qs.hrf,
                                        quantity=quantity,
                                        type=type,
                                        status=status,
                                        ip_address=ip_address,
                                        printed_numbers=printed_numbers,
                                        server_button_resp=1,
                                        production_date=current_date,
                                        production_time=current_time
                                        ),         
                
                # obj.delete()
                
           
            scdata=Scannerdata.objects.all()
            sclength=len(scdata)
            # print(sclength)
            print(sclength, 'is last in the length ✅')
            for i in range(sclength):
                scannerdata_to_server=ServerScannerdata(
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
                print(scdata[i].gtin)
                # try:
                #     conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")                     
                #     jobs7 = ServerScannerdata.objects.filter(lot=lot,status="Accepted")
                #     acceptedcount=len(jobs7)
                #     scObj7=ProdReport.objects.filter(batch_number=lot).update(accepted=acceptedcount,production_date=Begindatestring,production_time=current_time)
                #     print(acceptedcount, 'is last in the list ✅')
                    
                #     jobs8 = ScannerTable.objects.filter(lot=lot,status="Rejected")
                #     rejectedcount=len(jobs8)
                #     scObj7=ProdReport.objects.filter(batch_number=lot).update(rejectedbycamera=rejectedcount,production_date=Begindatestring,production_time=current_time)
                    
                #     jobs9 = ScannerTable.objects.filter(lot=lot,status="Damaged")
                #     damagedcount=len(jobs9)
                #     scObj7=ProdReport.objects.filter(batch_number=lot).update(damaged=damagedcount,production_date=Begindatestring,production_time=current_time)
                                                
                #     print(rejectedcount,'is last in the list ✅')
                # except:
                #    print("Server connection losted so pro report not updata")       
                 
                Scannerdata.objects.all().delete()    
                                           
            return render(request,"Batch-stop-message.html")                                    
       
# ..........................................................................

class ReportGetview(TemplateView):
    template_name = "Reportpage-get.html"             
def ProductionReport(request):
     
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
                try:
                    with open('jobid.csv', mode='r') as file:
                        csvreader = csv.reader(file)
                        for row in csvreader:
                            fgid=row[0]
                                        
                    detailsObj =Printerdata.objects.get(id=fgid)
                                    
                    
                    
                    
                    
                except:
                    print("jobid.csv not found")
                    try:
                        with open('data.csv', mode='r') as file:
                            csvreader = csv.reader(file)
                            for row in csvreader:
                                fgid=row[0]
                        detailsObj =Printerdata.objects.get(id=fgid)
                    except:
                        print("data.csv not found")  
                if request.method == 'GET':
                    lot = request.GET.get('lot')
                   
                    try:
                        if lot:
                            jobs = Printerdata.objects.get(lot=lot) 
                            # print(jobs.gtin)
                            jobs1 = Scannerdata.objects.filter(lot=lot,status="challenged")
                            # print(jobs1)
                            challengedcount=len(jobs1)
                            
                            jobs2 = Scannerdata.objects.filter(lot=lot,status="Damaged")
                            damagedcount=len(jobs2)
                           
                            
                            jobs3 = Scannerdata.objects.filter(lot=lot,status="others")
                            otherscount=len(jobs3)
                            
                            jobs4 = Scannerdata.objects.filter(lot=lot,status="sample")
                            samplecount=len(jobs4)
                            
                            jobs5 = Scannerdata.objects.filter(lot=lot,status="specimen")
                            specimencount=len(jobs5)
                            
                            jobs7 = Scannerdata.objects.filter(lot=lot).filter(status="Accepted")
                            acceptedcount=len(jobs7)
                            
                            jobs8 = Scannerdata.objects.filter(lot=lot).filter(status="Rejected")
                            rejectedcount=len(jobs8)
                            
                            # jobs6 = ScannerTable.objects.filter(lot=lot,status="rejected")
                            # rejectedcount=len(jobs6)
                            
                            
                            return render(request, 'currentreport.html', {'qs':jobs,"name":loginname,'damagedcount':damagedcount,"challengedcount":challengedcount,"otherscount":otherscount,"samplecount":samplecount,"specimencount":specimencount,"acceptedcount":acceptedcount,"rejectedcount":rejectedcount,'id':fgid})
                        else:
                            print("No information to show")
                            return render(request, 'currentreport.html', {"name":loginname,'id':fgid})
                    except:
                        try:
                            with open('jobid.csv', mode='r') as file:
                                    csvreader = csv.reader(file)
                                    for row in csvreader:
                                        fgid=row[0]
                                    
                            detailsObj =Printerdata.objects.get(id=fgid)
                                
                    
                    
                    
                    
                        except:
                                print("jobid.csv not found")
                                try:
                                    with open('data.csv', mode='r') as file:
                                        csvreader = csv.reader(file)
                                        for row in csvreader:
                                            fgid=row[0]
                                    detailsObj =Printerdata.objects.get(id=fgid)
                                except:
                                    print("data.csv not found")  
                        print("no report available")
                        return render(request, 'currentreport.html', {"mess":500,'id':fgid})
            else:
                return redirect("signin")
            
def ProductionReport_Aftet_Stop_Batch(request):
                         
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
                try:
                    with open('jobid.csv', mode='r') as file:
                        csvreader = csv.reader(file)
                        for row in csvreader:
                            fgid=row[0]
                                        
                    detailsObj =Printerdata.objects.get(id=fgid)
                                    
                    
                    
                    
                    
                except:
                    print("jobid.csv not found")
                    try:
                        with open('data.csv', mode='r') as file:
                            csvreader = csv.reader(file)
                            for row in csvreader:
                                fgid=row[0]
                        detailsObj =Printerdata.objects.get(id=fgid)
                    except:
                        print("data.csv not found")  
                if request.method == 'GET':
                    lot = request.GET.get('lot')
                   
                    try:
                        if lot:
                                                
                            jobs =ServerPrinterdata.objects.get(lot=lot) 
                            if(jobs.server_button_resp == 1):
                                                    
                           
                                jobs1 = ServerScannerdata.objects.filter(lot=lot,status="challenged")
                                # print(jobs1)
                                challengedcount=len(jobs1)
                                
                                jobs2 = ServerScannerdata.objects.filter(lot=lot,status="Damaged")
                                damagedcount=len(jobs2)
                            
                                
                                jobs3 = ServerScannerdata.objects.filter(lot=lot,status="others")
                                otherscount=len(jobs3)
                                
                                jobs4 = ServerScannerdata.objects.filter(lot=lot,status="sample")
                                samplecount=len(jobs4)
                                
                                jobs5 = ServerScannerdata.objects.filter(lot=lot,status="specimen")
                                specimencount=len(jobs5)
                                
                                jobs7 = ServerScannerdata.objects.filter(lot=lot,status="Accepted")
                                acceptedcount=len(jobs7)
                                # print("iiiiii",acceptedcount)
                                jobs8 = ServerScannerdata.objects.filter(lot=lot,status="Rejected")
                                rejectedcount=len(jobs8)
                                
                                # jobs6 = ScannerTable.objects.filter(lot=lot,status="rejected")
                                # rejectedcount=len(jobs6)
                                return render(request, 'Report.html', {'qs':jobs,"name":loginname,'damagedcount':damagedcount,"challengedcount":challengedcount,"otherscount":otherscount,"samplecount":samplecount,"specimencount":specimencount,"acceptedcount":acceptedcount,"rejectedcount":rejectedcount,'id':fgid})
                            else:
                                return render(request, 'Report.html', {"name":loginname,"nodatafound":1,'id':fgid})                     
                        else:
                            print("No information to show")
                            return render(request, 'Report.html', {"name":loginname,"headname":2,'id':fgid})
                    except:
                        print("no report available")
                        try:
                            with open('jobid.csv', mode='r') as file:
                                        csvreader = csv.reader(file)
                                        for row in csvreader:
                                            fgid=row[0]
                                        
                            detailsObj =Printerdata.objects.get(id=fgid)
                                    
                    
                    
                    
                    
                        except:
                            print("jobid.csv not found")
                            try:
                                with open('data.csv', mode='r') as file:
                                    csvreader = csv.reader(file)
                                    for row in csvreader:
                                        fgid=row[0]
                                detailsObj =Printerdata.objects.get(id=fgid)
                            except:
                                print("data.csv not found") 
                        return render(request, 'Report.html', {"id":fgid,"mess":500})
            else:
                return redirect("signin")            
        
# .............................................................................
def JobList(request):
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
            return render(request, 'Joblist.html',{'ip':systemip,'ip_error':1})                                                    
        if(loginname!=""):
            posts1 = Printerdata.objects.all().filter(ip_address=systemip).order_by('-id')#list only the jobs with running status(when the printer didnt stop in proper manner)
            le=len(posts1)
            if posts1:
                                
                    p = Paginator(posts1, 10)           #navigating to the previous and after pages
                    page_num=request.GET.get('page',1)
                    try:
                        page=p.page(page_num)
                    except EmptyPage:
                        page=p.page(1)
                    if le==0:
                        nu=1 
                    else:
                        nu=0 
                    context = {'page_obj':page,
                               'nu':nu
                        }
                
                    
                        
                    return render(request, 'Joblist.html',{'page_obj':page, "name":loginname}) 
            
            else:
                    
                    
                      
                    
                                
                    
                
                
                            
                        posts = Printerdata.objects.all().filter(ip_address=systemip).order_by('-id') #every printer jobs corresponding to a particular ipaddress...every jobs will come when printer stopping in normal way                       
                        p = Paginator(posts, 10)  # creating a paginator object
                        page_num=request.GET.get('page',1)
                        #page navigation
                        le=len(posts1)
                            
                        try:
                            page=p.page(page_num)
                        except EmptyPage:
                            page=p.page(1)
                        # context = {'page_obj':page
                        
                        #         } 
                        if le==0:
                            nu=1 
                        else:
                            nu=0 
                        return render(request, 'Joblist.html', {'page_obj':page,"name":loginname,"nu":nu})                     
        else:
            return redirect("signin")                     
def JoblistsearchBar(request):   #searchbar in the printer jobs listpage
  
       
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
            return render(request, 'Joblist.html',{'ip':systemip,'ip_error':1})              
        if(loginname!=""): 
            if request.method == 'GET':
                query = request.GET.get('query')    #searching item
                # print(query)
                if query:
                    jobs = Printerdata.objects.filter(lot=query)  #check wheather there is any match with searching item
                    return render(request, 'Joblist.html', {'page_obj':jobs,'search':1,"name":loginname})
                else:
                    # print("No information to show")
                    return render(request, 'Joblist.html', {})
        else:
            return redirect("signin")                                                  
# ...........................................................................
def Historyview(request) :    #history of application server
        # try:
        #     conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1")  
               
                              
            hostname = socket.gethostname()
            systemip = socket.gethostbyname(hostname) 
            
            Line1 = LocalappLoginmodel.objects.get(id=1)
            ip1= Line1.ip_address     
                                   
            Line2 = LocalappLoginmodel.objects.get(id=2)
            ip2=Line2.ip_address
            
            Line3= LocalappLoginmodel.objects.get(id=3)
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
                return render(request, 'history.html',{'ip':systemip,'ip_error':1})                                                                                                                                      
            i=0
            if(loginname!=""):
            
                
                posts = ServerHistory.objects.all().filter(donebyuserrole="operator") 
                # print(posts)
                le=len(posts)
                historypost=posts.order_by('-id')
               
                         
                p = Paginator(historypost, 10)  # creating a paginator object
                page_num=request.GET.get('page',1)
                try:
                    page=p.page(page_num)
                except EmptyPage:
                    page=p.page(1)
                if le==0:
                    nu=1 
                else:
                    nu=0     
               
                try:
                    with open('jobid.csv', mode='r') as file:
                        csvreader = csv.reader(file)
                        for row in csvreader:
                            fgid=row[0]
                          
                    detailsObj =Printerdata.objects.get(id=fgid)
                    
                    
                    
                    
                    
                except:
                    print("jobid.csv not found")
                    try:
                        with open('data.csv', mode='r') as file:
                            csvreader = csv.reader(file)
                            for row in csvreader:
                                fgid=row[0]
                        detailsObj =Printerdata.objects.get(id=fgid)
                    except:
                        print("data.csv not found")  
                        
                context = {'page_obj':page,
                           "name":loginname,
                           "nu":nu,
                           "id":fgid
                        }           
                return render(request, 'history.html', context)
            else:
                return redirect("signin")
           
            
       
        
def HistorysearchBar(request):   #searchbar in historypage
            # try:
            #     conn = psycopg2.connect("dbname='Db6' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1")
            # except:
            #     return redirect("servererror2")                     
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
                return render(request, 'history.html',{'ip':systemip,'ip_error':1})    
            if(loginname!=""): 
                if request.method == 'GET':
                    query = request.GET.get('query')
                    print(query)
                    if query:
                            jobs = ServerHistory.objects.filter(donebyuser=query) 
                            return render(request, 'history.html', {'page_obj':jobs,'search':1,"name":loginname})
                    else:
                            print("No information to show")
                            return render(request, 'history.html', {})
            else:
                return redirect("signin") 
         

# ............................................................................

def Scannerlisting(request) :   #listing to the scanner jobs
        # try:
        #     conn = psycopg2.connect("dbname='Db6' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")
           
            hostname = socket.gethostname()
            systemip = socket.gethostbyname(hostname) 
            
            Line1 = LocalappLoginmodel.objects.get(id=1)
            ip1= Line1.ip_address     
                                   
            Line2 =  LocalappLoginmodel.objects.get(id=2)
            ip2=Line2.ip_address
            
            Line3= LocalappLoginmodel.objects.get(id=3)
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
                return render(request, 'scanner-list.html',{'ip':systemip,'ip_error':1})                          
            i=0
            if(loginname!=""):
            
                # ,status = "Challenged",status="Damaged"
                
                # posts=ScannerTable.objects.all()
              
                posts = ServerScannerdata.objects.exclude(status="Damaged").exclude(status="Not Scanned").order_by('-id')

                # print(posts)
                le=len(posts)
              
                
               
                # ScannerTable.objects.get(id=numbers) 
                c=0
                c1=0
                # for i in range(le):
                                        
                #     bk=posts[c].grade   #take grade 
                #     fg=json.loads(bk)
                #     # print(fg[c]["grade"])
                #     # print(fg)
                #     c=c+1
                # leg=len(fg)
                
                # for j in range(leg):
                #     print(fg[c1].grade) 
                #     c1=c1+1               
                p = Paginator(posts, 10)  # creating a paginator object
                page_num=request.GET.get('page',1)
                try:
                    page=p.page(page_num)
                except EmptyPage:
                    page=p.page(1)
                if le==0:
                    nu=1 
                else:
                    nu=0 
                print(le)     
                print(nu)                               
                context = {'page_obj':page,
                           "name":loginname,
                           "nu":nu
                        }
                         
                return render(request, 'scanner-list.html', context)
            else:
                return redirect("signin")
        # except:
        #     return redirect("databaseerror")
#------------------------------------------------------------------------
def NotScannedlisting(request) :   #listing to the scanner jobs
        # try:
        #     conn = psycopg2.connect("dbname='Db6' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")
           
            hostname = socket.gethostname()
            systemip = socket.gethostbyname(hostname) 
            
            Line1 = LocalappLoginmodel.objects.get(id=1)
            ip1= Line1.ip_address     
                                   
            Line2 =  LocalappLoginmodel.objects.get(id=2)
            ip2=Line2.ip_address
            
            Line3= LocalappLoginmodel.objects.get(id=3)
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
                return render(request, 'notscanned-list.html',{'ip':systemip,'ip_error':1})                                                  
            i=0
            if(loginname!=""):
            
                # ,status = "Challenged",status="Damaged"
                
                # posts=ScannerTable.objects.all()
              
                posts = ServerScannerdata.objects.filter(status="Not Scanned").order_by('-id')
                # print(posts)
                le=len(posts)
              
                
               
                # ScannerTable.objects.get(id=numbers) 
                c=0
                c1=0
                # for i in range(le):
                                        
                #     bk=posts[c].grade   #take grade 
                #     fg=json.loads(bk)
                #     # print(fg[c]["grade"])
                #     # print(fg)
                #     c=c+1
                # leg=len(fg)
                
                # for j in range(leg):
                #     print(fg[c1].grade) 
                #     c1=c1+1               
                p = Paginator(posts, 10)  # creating a paginator object
                page_num=request.GET.get('page',1)
                try:
                    page=p.page(page_num)
                except EmptyPage:
                    page=p.page(1)
                if le==0:
                    nu=1 
                else:
                    nu=0 
                print(le)     
                print(nu)                               
                context = {'page_obj':page,
                           "name":loginname,
                           "nu":nu
                        }
                         
                return render(request, 'notscanned-list.html', context)
            else:
                return redirect("signin")
#------------------------------------------------------------
        
def ScannersearchBar(request):   #searchbar in scanner page 
        # try:
        #     conn = psycopg2.connect("dbname='Db6' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")  
            warnings.filterwarnings('ignore')                 
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
                return render(request, 'scanner-list.html',{'ip':systemip,'ip_error':1})                              
                
            if(loginname!=""): 
                if request.method == 'GET':
                    query = request.GET.get('query')
                    # print(query)
                    if query:
                        jobs = ServerScannerdata.objects.filter(lot=query).exclude(status="NO")  
                        # if(jobs):
                            #  jobs = ScannerTable.objects.exclude(status="NO")                   
                        return render(request, 'scanner-list.html', {'page_obj':jobs,'search':1,'name':loginname})
                    else:
                        print("No information to show")
                        return render(request, 'scanner-list.html', {})
            else:
                return redirect("signin")
        # except:
        #     return redirect("databaseerror")
        
class ScannerReworkView(View):   #getting datas
    def get(self,request,id):
        # try:
        #     conn = psycopg2.connect("dbname='Db6' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")                    
                            
            hostname = socket.gethostname()
            systemip = socket.gethostbyname(hostname) 
            
            Line1 =LocalappLoginmodel.objects.get(id=1)
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
                qs=ServerScannerdata.objects.get(id=id)
            
            # form=PrinterForm(request.POST,instance=qs)
                return render(request,"rework.html",{"qs":qs})
            else:
                return redirect("signin")
        # except:
        #     return redirect("databaseerror") 
#--------------------------------------------------------------------------        
         
class ScannerReworkView(View):   #getting datas
    def get(self,request,id):
        # try:
        #     conn = psycopg2.connect("dbname='Db6' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")                    
                            
            hostname = socket.gethostname()
            systemip = socket.gethostbyname(hostname) 
            
            Line1 =LocalappLoginmodel.objects.get(id=1)
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
                qs=ServerScannerdata.objects.get(id=id)
            
            # form=PrinterForm(request.POST,instance=qs)
                return render(request,"rework.html",{"qs":qs})
            else:
                return redirect("signin")
        # except:
        #     return redirect("databaseerror")  
        

        #     return redirect("databaseerror")   
#---------------------------------------------------------------                
def Reworkscan(request,id):
                    #  print("hi") 
        # try:
        #     conn = psycopg2.connect("dbname='Db6' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")            
        #     warnings.filterwarnings('ignore')  
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
                            qs= ServerScannerdata.objects.get(id=id)
                            try: 
                                scanner_socket_7 = socket.socket()
                                scanner_port_7=2001
                                scanner_socket_7.connect(('192.168.200.134', scanner_port_7))  
                            except:
                                # print("data not recived")
                                return redirect("scanner-message") 
                            try:         
                                dummycount = 8
                                scanner_data=scanner_socket_7.recv(1024).decode()
                                print("this is data",scanner_data)
                                decoded_grade=scanner_data[0]
                                if(decoded_grade=="4"):
                                    grade="A"
                                elif(decoded_grade=="3"):
                                    grade="B"
                                elif (decoded_grade=="2"):
                                    grade="C"
                                elif (decoded_grade=="1"):
                                    grade="D"
                                else:
                                    grade="F" 
                                type=qs.type
                                if(type=="type2"):
                                    h=scanner_data[38:]    #data from scanner is coming in decoded textbox
                                    decoded_serialnumber=scanner_data[29:38]
                                    # print(decoded_serialnumber)
                                elif(type=="type5" or type=="type1"):
                                    h=scanner_data[38:]    #data from scanner is coming in decoded textbox
                                    decoded_serialnumber=scanner_data[25:34]
                                    # print(decoded_serialnumber)                   
                                decodedtext=scanner_data
                              
                                if (decoded_serialnumber== qs.serialnumber):   #serialno from database serialno from sacnner are checking(whather any match is there ) 
                                
                                    ghi=1 
                                
                                else:
                                
                                    ghi=0 
                                                        
                                
                                
                                r={"serialnumber":h,
                                        "decodedtext":decodedtext}
                               
                                try:
                                    conn = psycopg2.connect("dbname='Db6' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")                    
                                    historysave=History(modelname='ScannerTable',
                                                savedid="noid",
                                                operationdone='rework',
                                                donebyuser=loginname,
                                                donebyuserrole=loginuserrole, 
                                                description="Rework of serial number "+h+" "+"by"+" "+ loginname,
                                                donedatetime=datetime.datetime.now())
                                    historysave.save()
                                except:
                                    historysave=LocalseverHistory(modelname='ScannerTable',
                                                savedid="noid",
                                                operationdone='rework',
                                                donebyuser=loginname,
                                                donebyuserrole=loginuserrole, 
                                                description="Rework of serial number "+h+" "+"by"+" "+ loginname,
                                                donedatetime=datetime.datetime.now())
                                    historysave.save()
                                b=json.dumps(r)
                                #  context = {'page_obj':b
                                #     } 
                                return render(request,'rework.html',{"qs":qs,"decodedtext":decodedtext,"grade":grade,"ghi":ghi}) 
                            except:
                                print("data didnt receive")
                        #  return HttpResponse(200)                          
            else:
                            return redirect("signin")
        # except:
        #     return redirect("databaseerror")   
        
def ReworkUpdate(request,id):
                        
    # def get(self,request,id):
        # obj= ScannerTable.objects.get(id=id)
        # try:
        #     conn = psycopg2.connect("dbname='Db6' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")                    
            warnings.filterwarnings('ignore') 
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
                uname =LocalappLoginmodel.objects.get(id=2)
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
                qs= ServerScannerdata.objects.get(id=id) 
                lot=qs.lot 
                gtin=qs.gtin
                lines=[]
            if request.method == 'GET':
                query1 = request.GET.get('query') 
                newgrade = request.GET.get('grade')      
                print(newgrade)   #updating old status with new status
                if (query1 ==""):
                    return render(request, 'rework.html', {"qs":qs,"updatestatus":0})                      
                try:
                    obj = ServerScannerdata.objects.get(id=id)
                    detailObj=ServerScannerdata.objects.filter(id=id).update(status=query1)
                    
                    
                    
                    sl=obj.serialnumber
                    # ngr=obj.gradevalue
                    # print(ngr)
                    if(query1=="challenged"):
                        try:                    
                            with open("jsonfiles/"+lot+".csv", 'r') as readFile:
                                reader = csv.reader(readFile)
                                for row in reader:
                                    lines.append(row)
                                    for field in row:
                                        # print(field)                    
                                        if field == sl:
                                            lines.remove(row)
                            with open("jsonfiles/"+lot+".csv", 'w',newline='') as writeFile:
                                writer = csv.writer(writeFile)
                                writer.writerows(lines)
                         
                        except:
                            print("File not Found")        
                        
                        
                                   
                    else:
                       print ("not challenged") 
                   
                    try:
                        conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")                    
                        obj = ServerScannerdata.objects.get(id=id)
                        detailObj=ServerScannerdata.objects.filter(id=id).update(gradevalue=newgrade,)
                        
                        jobs1 = ServerScannerdata.objects.filter(lot=lot,status="Rejected")
                        rejectedcount=len(jobs1)
                        scObj7=ProdReport.objects.filter(batch_number=lot).update(rejectedbycamera=rejectedcount)
                        
                        jobs2 = ServerScannerdata.objects.filter(lot=lot,status="challenged")
                        challengedcount=len(jobs2)
                        print(challengedcount)
                        scObj7=ProdReport.objects.filter(batch_number=lot).update(challenged=challengedcount)
                        
                        jobs3 = ServerScannerdata.objects.filter(lot=lot,status="Accepted")
                        acceptedcount=len(jobs3)
                        print(acceptedcount)
                        scObj7=ProdReport.objects.filter(batch_number=lot).update(accepted=acceptedcount)
                        
                        
                        
                        
                    except:
                        print("grade not update") 
                    if(query1=="challenged"):
                        try:                    
                          with open("Acceptedjson/"+lot+".csv", 'a', newline='\n') as file:
                                      
                                            writer = csv.writer(file)
                                   
                                            valuelist = [sl,newgrade,"Accepted",lot,gtin],
                                            writer.writerows(valuelist)
                        except:
                            print("AcceptedJson folder have no file related with this batchnumber File")        
                        
                     
                     
                            
                                   
                    else:
                       print ("not challenged" )                     
                except:
                    print("query not update")    
              
                    
                                        
            
                        
                return render(request, 'rework.html', {"qs":qs,"updatestatus":1})               
            else:
                return redirect("signin")  
        # except:
        #     return redirect("databaseerror")                                                          
                  
# ..............................................................................
class Candidatehomeview(TemplateView):
                                              
            template_name = "messagepage.html"
class Scannermessageview(TemplateView):
                                    
        template_name = "Scannermessage.html"            
class ServerError2(TemplateView):
        template_name = "Servererror2.html"     
 
# class Firstpage(TemplateView):     
#         template_name = "Firstpage.html" 
        
class DatabaseError(TemplateView):     
        template_name = "DatabaseError.html"     
        
class Informationpage(TemplateView):     
        template_name = "Information.html"  
 
class Aboutpage(TemplateView):     
        template_name = "About.html"  
        
class ServerError3(TemplateView):
        template_name = "Servererror3.html" 
class Ip_error(TemplateView):
    template_name = "Ip-error.html"         
                            
# class LoadJobpageview(View):
#    def get(self,request,id):
#         try:    
            
#             hostname = socket.gethostname()
#             systemip = socket.gethostbyname(hostname) 
            
#             Line1 = Loginmodel.objects.get(id=1)
#             ip1= Line1.ip_address     
                                   
#             Line2 = Loginmodel.objects.get(id=2)
#             ip2=Line2.ip_address
            
#             Line3=Loginmodel.objects.get(id=3)
#             ip3=Line3.ip_address
#             if systemip==ip1:
                    
#                 uname = Loginmodel.objects.get(id=1)
#                 loginname=uname.loginuname
#                 loginuserrole=uname.userrole
            
#             elif systemip==ip2: 
#                 uname = Loginmodel.objects.get(id=2)
#                 loginname=uname.loginuname
#                 loginuserrole=uname.userrole
#             elif systemip==ip3: 
#                 uname = Loginmodel.objects.get(id=3)
#                 loginname=uname.loginuname
#                 loginuserrole=uname.userrole
#         except:
#             print("Login model data have some issue in Autovision view") 
#         if(loginname!=""): 
           
#             qs=Printerdata.objects.get(id=id)
#             intid=qs.id
#             rows=[intid]
           
#             os.system('start D:\Omron\AutoVision\AutoVISION.exe') 
#             try:
                   
#                 with open("jobid.csv", 'w', newline='') as csvfile:
#                     csvwriter = csv.writer(csvfile)
#                             # csvwriter.writerow(fields)
#                     csvwriter.writerow(rows)
#                 with open('jobid.csv', mode='r') as file:
#                         csvreader = csv.reader(file)
#                         for row in csvreader:
#                                m=(row[0])
#             except:
#                 print("job.csv file not found") 
            
#             try:
                   
#                 with open("data.csv", 'w', newline='') as csvfile:
#                     csvwriter = csv.writer(csvfile)
#                             # csvwriter.writerow(fields)
#                     csvwriter.writerow(rows)
#                 with open('data.csv', mode='r') as file:
#                         csvreader = csv.reader(file)
#                         for row in csvreader:
#                                m=(row[0])
               
#             except:
#                 print("data.csv file not found")     
                                  
           
#             return  render(request,"cu-edit.html",{"job":qs})
#         else:
#             return redirect("signin")
# .......................................................................
class ServerView(View):
    def get(self,request):
        try:    
            
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
                return render(request, 'ServerDatalist.html',{'ip':systemip,'ip_error':1})                                                                                                            
        except:
            print("Login model data have some issue in Autovision view") 
        if(loginname!=""):                     
            posts1 = ServerPrinterdata.objects.all().order_by('-id')
            le=len(posts1)
            if posts1:
                                    
                p = Paginator(posts1, 10)           #navigating to the previous and after pages
                page_num=request.GET.get('page',1)
                try:
                    page=p.page(page_num)
                except EmptyPage:
                    page=p.page(1)
                if le==0:
                    nu=1 
                else:
                    nu=0 
                try:
                    with open('jobid.csv', mode='r') as file:
                        csvreader = csv.reader(file)
                        for row in csvreader:
                            fgid=row[0]
                          
                    detailsObj =Printerdata.objects.get(id=fgid)
                    
                        
                   
               
                    
                    
                    
                except:
                    print("jobid.csv not found")
                    try:
                        with open('data.csv', mode='r') as file:
                            csvreader = csv.reader(file)
                            for row in csvreader:
                                fgid=row[0]
                        detailsObj =Printerdata.objects.get(id=fgid)
                    except:
                        print("data.csv not found")            
                context = {'page_obj':page,
                               'nu':nu
                              
                    }         
                return render(request, 'ServerDatalist.html',{'page_obj':page, "name":loginname,'id':fgid})     
            else:
                                            
                    posts = ServerPrinterdata.objects.all().order_by('-id') #every printer jobs corresponding to a particular ipaddress...every jobs will come when printer stopping in normal way                       
                    p = Paginator(posts, 5)  # creating a paginator object
                    page_num=request.GET.get('page',1)
                            #page navigation
                    le=len(posts1)        
                                
                    try:
                        page=p.page(page_num)
                    except EmptyPage:
                        page=p.page(1)
                            # context = {'page_obj':page
                            
                            # 
                            # } 
                    if le==0:
                        nu=1 
                    else:
                       nu=0 
                    try:
                        with open('jobid.csv', mode='r') as file:
                            csvreader = csv.reader(file)
                            for row in csvreader:
                                fgid=row[0]
                            
                        detailsObj =Printerdata.objects.get(id=fgid)
                        
                            
                    
                
                        
                        
                    
                    except:
                        print("jobid.csv not found")
                        try:
                            with open('data.csv', mode='r') as file:
                                csvreader = csv.reader(file)
                                for row in csvreader:
                                    fgid=row[0]
                            detailsObj =Printerdata.objects.get(id=fgid)
                        except:
                            print("data.csv not found")            
                    return render(request, 'ServerDatalist.html',{'page_obj':page, "name":loginname,"nu":nu,'id':fgid})     
        else:
            return redirect("signin")        
                          
def ServerlistsearchBar(request):   #searchbar in the printer jobs listpage
  
       
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
                # print(query)
                if query:
                    jobs = ServerPrinterdata.objects.filter(lot=query)  #check wheather there is any match with searching item
                    return render(request, 'ServerDatalist.html', {'page_obj':jobs,'search':1})
                else:
                    # print("No information to show")
                    return render(request, 'ServerDatalist.html', {})
        else:
            return redirect("signin")                          
          
class Send_to_Servergetview(View):
        def get(self,request,id):
            # this try is used for update the current username in Loginmodel
            # this user name is used to adding history.so we take that data to Localapp-
            # Loggin model and update to Server Login Model.there is any server conection lost 
            # problems was finding in betwwen the process Login Model Did not update
            # Theat for we use this Try
            try:
                conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")
                hostname = socket.gethostname()
                systemip = socket.gethostbyname(hostname)
                
                obj1 = LocalappLoginmodel.objects.get(id=1)
                ip1=obj1.ip_address  
                                                    
                obj2 = LocalappLoginmodel.objects.get(id=2)
                ip2=obj2.ip_address     
                                                
                obj3 = LocalappLoginmodel.objects.get(id=3)
                ip3=obj3.ip_address   
                if systemip ==ip1:                  
                    obj = LocalappLoginmodel.objects.get(id=1)
                    loginuserrole=obj.userrole
                    line=obj.line 
                    uname=obj.loginuname
                    detailObj=LocalappLoginmodel.objects.filter(id=1).update(loginuname=uname,userrole=loginuserrole,line=line,ip_address=systemip)
                elif systemip ==ip2:
                    obj = LocalappLoginmodel.objects.get(id=2)
                   
                    loginuserrole=obj.userrole
                    line=obj.line 
                    uname=obj.loginuname
                    detailObj=LocalappLoginmodel.objects.filter(id=2).update(loginuname=uname,userrole=loginuserrole,line=line,ip_address=systemip) 
                                                
                elif systemip ==ip3:
                    obj = LocalappLoginmodel.objects.get(id=3)
                    
                    loginuserrole=obj.userrole
                    line=obj.line 
                    uname=obj.loginuname
                    detailObj=LocalappLoginmodel.objects.filter(id=3).update(loginuname=uname,userrole=loginuserrole,line=line,ip_address=systemip)         
                else:
                    hostname = socket.gethostname()
                    systemip = socket.gethostbyname(hostname)                     
                    return render(request, 'Ip-error.html',{'ip':systemip,'inside_message':1})                              
            except:
                return redirect("databaseerror")                         
            s = ServerPrinterdata.objects.get(id=id)
               
            return  render(request,"Serverdata-send.html",{"qs":s})                    
        
                               




    
    
    
def sendServer(request,id):  
    
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
            with open('data.csv', mode='r') as file:
                    csvreader = csv.reader(file)
                    for row in csvreader:
                        fgid=row[0]
                        print(fgid)
                        
                    Begindatestring = date.today() 
                    print(Begindatestring)
                    t = time.localtime()

                    # Format the time as a string
                    current_time = time.strftime("%H:%M:%S", t)
                    # print(current_time)    
                    qs=ServerPrinterdata.objects.get(id=id)
                    # prodObj=ProductionOrder.objects.get(gtin_number=qs.gtin)
                    po=qs.processordernumber  
                    # print(po)
                    # obj = Printerdata.objects.get(printer_id=fgid)
                    # prodObj=PrinterdataTable.objects.get(gtin_number=obj.gtin)
                    # print(prodObj.gtin)
                    inexid=qs.id
                    gtin=qs.gtin
                    processordernumber=po
                    expiration_date=qs.expiration_date
                    lot=qs.lot
                    numbers=qs.numbers
                    hrf=qs.hrf
                    quantity=qs.quantity
                    type=qs.type
                    status=qs.status
                    ip_address=qs.ip_address
                    printed_numbers=qs.printed_numbers
                    balanced_serialnumbers=qs.balanced_serialnumbers
                    # responsefield=qs.responsefield
                    # preparebuttonresponse=qs.preparebuttonresponse
                    # stopbtnresponse=qs.stopbtnresponse
                    # start_pause_btnresponse=qs.start_pause_btnresponse
                    # pause_stop_btnresponse=qs.pause_stop_btnresponse
                    # return_slno_btn_response=qs.return_slno_btn_response
                    # batchstopmessage=qs.batchstopmessage
                    # label_response=qs.label_response
                    child_numbers=qs.child_numbers
                    scannergradefield=qs.scannergradefield
                    # loadpause=qs.loadpause
                    Rejectednumbers=qs.Rejectednumbers
                    acceptednumbers=qs.acceptednumbers
                    # print(status)
                    # qws=Printerdata.objects.get(printer_id=fgid)
                    # inid=qws.printer_id
                    obj = ServerPrinterdata.objects.get(id=id)
                    # print(obj.gtin)
                    # prodObj=PrinterdataTable.objects.get(gtin_number=obj.gtin)
                    # print(prodObj.gtin)
                    detailObj=PrinterdataTable.objects.filter(lot=obj.lot).update(numbers=numbers,
                                            balanced_serialnumbers=balanced_serialnumbers,
                                            # responsefield=False,
                                            # preparebuttonresponse=preparebuttonresponse,
                                            # stopbtnresponse=True,
                                            # start_pause_btnresponse=start_pause_btnresponse,
                                            # pause_stop_btnresponse=pause_stop_btnresponse,
                                            # return_slno_btn_response=return_slno_btn_response,
                                            # batchstopmessage=batchstopmessage,
                                            # label_response=label_response,
                                            child_numbers=child_numbers,
                                            scannergradefield=scannergradefield,
                                            # loadpause=loadpause,
                                            Rejectednumbers=Rejectednumbers,
                                            acceptednumbers=acceptednumbers,
                                            gtin=gtin,
                                            processordernumber=po,
                                            expiration_date=expiration_date,
                                            lot=lot,
                                            hrf=qs.hrf,
                                            quantity=quantity,
                                            type=type,
                                            status=status,
                                            ip_address=ip_address,
                                            printed_numbers=printed_numbers
                                            ),
                                
                    
                    # obj.delete()
                    detailObj2=ServerPrinterdata.objects.filter(lot=obj.lot).update(server_button_resp=0)    
                    
            
            scdata=ServerScannerdata.objects.filter(lot=lot)
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
                    print(scdata[i].gtin)
                    jobs7 = ScannerTable.objects.filter(lot=lot,status="Accepted")
                    acceptedcount=len(jobs7)
                    scObj7=ProdReport.objects.filter(batch_number=lot).update(accepted=acceptedcount,production_date=Begindatestring,production_time=current_time)
                    print(acceptedcount, 'is last in the list ✅')
                    
                    jobs8 =  ScannerTable.objects.filter(lot=lot,status="Rejected")
                    rejectedcount=len(jobs8)
                    scObj7=ProdReport.objects.filter(batch_number=lot).update(rejectedbycamera=rejectedcount,production_date=Begindatestring,production_time=current_time)
                    
                    jobs9 =  ScannerTable.objects.filter(lot=lot,status="Damaged")
                    damagedcount=len(jobs9)
                    scObj7=ProdReport.objects.filter(batch_number=lot).update(damaged=damagedcount,production_date=Begindatestring,production_time=current_time)
                                                
                    print(rejectedcount,'is last in the list ✅')    
                    # obj = ServerPrinterdata.objects.get(id=id)
                    # jobs10 =  ServerPrinterdata.objects.filter(id=id,status="Closed").update(start_pause_btnresponse=1)
                    # # damagedcount=len(jobs9)
            backup_sc_data=ServerScannerdata.objects.filter(lot=lot)
            backup_sclength=len(backup_sc_data)
            print("backuplot",lot)
           
            for j in range(backup_sclength):
                scannerdata_to_backupserver=BackupScannerdata(
                        id= backup_sc_data[j].id,
                        gtin= backup_sc_data[j].gtin,
                        ip_address= backup_sc_data[j].ip_address,
                        status= backup_sc_data[j].status,
                        serialnumber= backup_sc_data[j].serialnumber,
                        gradevalue= backup_sc_data[j].gradevalue,
                        lot= backup_sc_data[j].lot,
                        finalstatus= backup_sc_data[j].finalstatus,
                        type=backup_sc_data[j].type,
                        send_date= Begindatestring,
                        send_time=current_time,
                        
                        
                        
                        ) 
                scannerdata_to_backupserver.save()         
            historysave=History(modelname='ServerPrinterdata',
                                        savedid="noid",
                                        operationdone='Send to server',
                                        donebyuser=loginname,
                                        donebyuserrole=loginuserrole, 
                                        description="Send The Batch Details Of  "+lot+" To Server "+"by"+" "+ loginname,
                                        donedatetime=datetime.datetime.now())
            historysave.save()            
            ServerScannerdata.objects.filter(lot=lot).delete()
            histobj=LocalseverHistory.objects.all()
            historylength=len(histobj)
            # print("historylength")
            
            for i in range(historylength):
                            
                    history_save_to_server=History(
                                    modelname=histobj[i].modelname,
                                    savedid= histobj[i].savedid,
                                    operationdone=histobj[i].operationdone,
                                    donebyuser=histobj[i].donebyuser,
                                    donebyuserrole=histobj[i].donebyuserrole, 
                                    description=histobj[i].description,
                                    donedatetime=histobj[i].donedatetime,
                                    
                                )
                                
                    history_save_to_server.save()
                    
                    
                        # print(histobj[i].modelname)
                                
            histobj=LocalseverHistory.objects.all().delete()
                                            
            return redirect("serverdatalist")
            # return  render(request,"Serverdata-send.html",{"qs":qs,"message":1})
           
        else:
            return redirect("signin") 
# .................................................................................
class Dashboard(View):
    def get(self,request) :
                            
        try:
            with open('jobid.csv', mode='r') as file:
                csvreader = csv.reader(file)
                for row in csvreader:
                    fgid=row[0]
                    # print(fgid)
            detailsObj =Printerdata.objects.get(id=fgid)
            loadbutton=detailsObj.load_button_resp 
            startbutton=detailsObj.start_button_resp 
            
            obj = Inproperly_Closed.objects.get(id=1) 
            print(obj.close_update)
            close_variable4=obj.close_update
            # print("close_variable", close_variable4) 
            
            try: 
                obj2 = Inproperly_Closed.objects.get(id=1) 
                close_variable4=obj2.close_update   
              
                # print("mmmmmmm")  
                if close_variable4== "1":
                    # print("mmmm1111")  
                    obj = Printerdata.objects.get(id=fgid)
                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(start_button_resp=0) 
                    
                    # print("mmmm22222",close_variable4)  
                    return render(request, 'dashboard.html',{"id":fgid,"loadbutton":loadbutton,"startbutton":startbutton,"close_variable":close_variable4})                  
            except:
                    # print("Closed Varible not 1")
                    obj3 = Inproperly_Closed.objects.get(id=1) 
                    close_variable4=obj3.close_update 
                    return render(request, 'dashboard.html',{"id":fgid,"loadbutton":loadbutton,"startbutton":startbutton,"close_variable":close_variable4})                  
                    
                    # print("except3 m==5")
        except:
            print("jobid.csv not found")
            fgid=0
            startbutton=0  
            m=5
            obj4 = Inproperly_Closed.objects.get(id=1) 
            close_variable4=obj4.close_update 
            
            try:
                with open('data.csv', mode='r') as file:
                    csvreader = csv.reader(file)
                    for row in csvreader:
                      fgid=row[0]
                        
                # detailsObj =Printerdata.objects.get(id=dataid)
                # prodObj=Printerdata.objects.get(lot=detailsObj.lot)
                # scObj=Printerdata.objects.filter(lot=prodObj.lot).update(load_button_resp=0)
                # if(detailsObj.status=="Running"):
                #     detailsObj =Printerdata.objects.get(id=dataid)
                #     prodObj=Printerdata.objects.get(lot=detailsObj.lot)
                #     scObj=Printerdata.objects.filter(lot=prodObj.lot).update(start_button_resp=0,status="Stopped")                                    
                
                detailsObj =Printerdata.objects.get(id=dataid)
                loadbutton=detailsObj.load_button_resp
                
                                      
            except:
                print("data.csv not found")
                loadbutton=0
                m=5
        
            
                
                         
        print("999",close_variable4)    
        return render(request, 'dashboard.html',{"id":fgid,"loadbutton":loadbutton,"startbutton":startbutton,"close_variable":close_variable4})  
        
    
class Dashboard2(View):
    def get(self,request) :
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
            return render(request, 'Ip-error.html',{'ip':systemip,'ip_error':1}) 
                                
        try:
            with open('jobid.csv', mode='r') as file:
                csvreader = csv.reader(file)
                for row in csvreader:
                    fgid=row[0]
                    # print(fgid)
            detailsObj =Printerdata.objects.get(id=fgid)
            loadbutton=detailsObj.load_button_resp
            startbutton=detailsObj.start_button_resp 
                              
        except:
            print("jobid.csv not found")
            fgid=0
            startbutton=0  
            
            try:
                with open('data.csv', mode='r') as file:
                    csvreader = csv.reader(file)
                    for row in csvreader:
                       fgid=row[0]
                        
                # detailsObj =Printerdata.objects.get(id=dataid)
                # prodObj=Printerdata.objects.get(lot=detailsObj.lot)
                # scObj=Printerdata.objects.filter(lot=prodObj.lot).update(load_button_resp=0)
                # if(detailsObj.status=="Running"):
                #     detailsObj =Printerdata.objects.get(id=dataid)
                #     prodObj=Printerdata.objects.get(lot=detailsObj.lot)
                #     scObj=Printerdata.objects.filter(lot=prodObj.lot).update(start_button_resp=0,status="Stopped")                                    
                
                detailsObj =Printerdata.objects.get(id=fgid)
                loadbutton=detailsObj.load_button_resp
                
                                      
            except:
                print("data.csv not found")
                loadbutton=0
                
          
        conn = psycopg2.connect(
            database="Line_DB2",#enter your database name
           
            user='postgres',#enter your postgres username
            password='1234',#enter your password
            host='localhost',#enter your host name
            port='5432'#port number
        )
        cursor = conn.cursor()

            # Execute the DELETE command
        t = time.localtime()

                    # Format the time as a string
        current_time = time.strftime("%H:%M:%S", t)
        # print(current_time)
        Begindatestring = date.today()
        # Begindatestring = date.today()+2
        # Obj1=BackupScannerdata.objects.filter(lot=detailsObj.lot)
        
     
        # d=Obj1[0].send_date
        # print("uo",d)
        # t = timedelta(days=30)
        # final_date = d + t
        # print("l",final_date)
        
        
        # x = '2024-07-23'
        # # res = (datetime.timedelta(days=1))
       
        # final_date= str(x)
        # print("f",final_date)
        # k=str(d)
        
        
       
         
        try:
            scObj=BackupScannerdata.objects.filter(lot=detailsObj.lot).update(update_date=Begindatestring) 
          
            # if  k == final_date :
            #     obj2=BackupScannerdata.objects.filter(lot=detailsObj.lot).delete()
            # else:
            #     print("not that date")                           
        except:
            print("no lot  data")
        
        delete_query = "DELETE FROM serverdataapp_backupscannerdata WHERE send_date < (NOW() - INTERVAL '1 days');"
       
        cursor.execute(delete_query)
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()  
        
        if loginuserrole == "admin":
               admin_controll=1                        
        else:
            admin_controll=0                
        return render(request, 'dashboard2.html',{"id":fgid,"loadbutton":loadbutton,"startbutton":startbutton,"admin_controll":admin_controll})                  
# ..........................................................................
def returnserialnolisting(request):  #for the listing of printer jobs
    # try:
    #     conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")                    
       
        # systemip="192.168.200.131"

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
            return render(request, 'Return-serial-list.html',{'ip':systemip,'ip_error':1})                               
        if(loginname!=""):
            
                posts = ServerPrinterdata.objects.all().order_by('-id')  #every printer jobs corresponding to a particular ipaddress...every jobs will come when printer stopping in normal way                       
                p = Paginator(posts, 5)  # creating a paginator object
                page_num=request.GET.get('page',1)    #page navigation
                le=len(posts)
                try:
                    page=p.page(page_num)
                except EmptyPage:
                    page=p.page(1)
                if le==0:
                    nu=1 
                else:
                    nu=0     
                context = {'page_obj':page,
                           'name':loginname,
                           'nu':nu
                        }            
                return render(request, 'Return-serial-list.html', context)
        else:
            return redirect("signin")
    # except:
    #         return redirect("databaseerror")  
        
def ReturnSerialsearchBar(request):
                        #searchbar in the printer jobs listpage
        # try:
        #     conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")
        # except:
        #     return redirect("databaseerror")      
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
                # print(query)
                if query:
                    jobs = ServerPrinterdata.objects.filter(lot=query)  #check wheather there is any match with searching item
                    return render(request, 'Return-serial-list.html', {'page_obj':jobs,'search':1,"name":loginname})
                else:
                    # print("No information to show")
                    return render(request, 'Return-serial-list.html', {})
        else:
            return redirect("signin") 
    
        
class ReturnsnGet(View):   #get in return page
    def get(self,request,id):
            # try:
            #     conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")  
            # except:
            #     return redirect("databaseerror")                    
            warnings.filterwarnings('ignore')                      
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
                qs=ServerPrinterdata.objects.get(id=id)
                form=PrinterForm(request.POST,instance=qs)
                return render(request,"returnserial.html",{"qs":qs})
            else:
                return redirect("signin")
        
        
class Returnserialnumbers(View):
    def get(self,request,id,lot):
            Acceptednumberslist=[]                    
            try:
                conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")
            except:
                return redirect("databaseerror")                          
            warnings.filterwarnings('ignore')                     
            hostname = socket.gethostname()
            systemip = socket.gethostbyname(hostname) 
            
            Line1 = Loginmodel.objects.get(id=1)
            ip1= Line1.ip_address     
                                   
            Line2 = Loginmodel.objects.get(id=2)
            ip2=Line2.ip_address
            
            Line3=Loginmodel.objects.get(id=3)
            ip3=Line3.ip_address
            if systemip==ip1:
                    
                uname = Loginmodel.objects.get(id=1)
                loginname=uname.loginuname
                loginuserrole=uname.userrole
            
            elif systemip==ip2: 
                uname = Loginmodel.objects.get(id=2)
                loginname=uname.loginuname
                loginuserrole=uname.userrole
            elif systemip==ip3: 
                uname = Loginmodel.objects.get(id=3)
                loginname=uname.loginuname
                loginuserrole=uname.userrole
            else:
                hostname = socket.gethostname()
                systemip = socket.gethostbyname(hostname)                     
                return render(request, 'Ip-error.html',{'ip':systemip,'inside_message':1})                                  
            if(loginname!=""): 
                qs=ServerPrinterdata.objects.get(lot=lot)
                lot=qs.lot
                # form=PrinterForm(request.POST,instance=qs)
                y=[]
                y1=[]
                rejectednumberslist=[]
                acceptednumberslist=[] 
                Notdetectedlist=[]
                detailsObj = ServerPrinterdata.objects.get(lot=lot)
                prodObj=ServerPrinterdata.objects.get(lot=detailsObj.lot)
                # scObj=ScannerTable.objects.filter(gtin=prodObj.gtin).update(finalstatus="Closed") 
            
                serialno=prodObj.numbers
                if(serialno!=[]):
                    detailsObj = ServerPrinterdata.objects.get(lot=lot)
                    prodObj=ServerPrinterdata.objects.get(lot=detailsObj.lot)
                    scObj=ServerScannerdata.objects.filter(lot=prodObj.lot).update(finalstatus="Closed")                     
                    #update by using serialno if there is number in serialno  
                    detailObj2=ServerPrinterdata.objects.filter(lot=prodObj.lot).update(balanced_serialnumbers=serialno,status="Closed")
                    y.clear()
                    obj = ServerPrinterdata.objects.get(lot=lot)
                    detailObj=ServerPrinterdata.objects.filter(lot=prodObj.lot).update(numbers=y) 
                    
                    detailsObj =ServerPrinterdata.objects.get(lot=lot) 
                    prodObj=ProductionOrder.objects.get(batch_number=detailsObj.lot)
                    detailObj=ProductionOrder.objects.filter(batch_number=prodObj.batch_number).update(status="Closed") 
                    try:
                        with open("jsonfiles/"+lot+".csv", 'r') as openfile:
        
                        # Reading from json file
                            csvreader = csv.reader(openfile)
                            for row in csvreader:
                                print(row[0])
                                rejectednumberslist.append(row[0])
                                
                        rejectedjson=json.dumps(rejectednumberslist)
                        obj = ServerPrinterdata.objects.get(lot=lot)
                        detailObj=ServerPrinterdata.objects.filter(lot=obj.lot).update(Rejectednumbers=rejectedjson)  
                    except:
                        print("No DATA AVAILABLE FOR ADDING TO CSV")
                    
                    try:
                        with open("Acceptedjson/"+lot+".csv", 'r') as openfile1:
        
                        # Reading from json file
                            csvreader = csv.reader(openfile1)
                            for row in csvreader:
                                print(row[0])
                                acceptednumberslist.append(row[0])
                                
                        acceptedjson=json.dumps(acceptednumberslist)
                        obj = ServerPrinterdata.objects.get(lot=lot)
                        detailObj=ServerPrinterdata.objects.filter(lot=obj.lot).update(acceptednumbers=acceptedjson)  
                    except:
                        print("No Accepted DATA AVAILABLE FOR ADDING  TO CSV") 
                    try:
                        with open("Notdetectedjson/"+lot+".csv", 'r') as openfile:
                        
                                        # Reading from json file
                            csvreader = csv.reader(openfile)
                            for row in csvreader:
                                print(row[0])
                                Notdetectedlist.append(row[0])
                                print(Notdetectedlist)
                                            
                        Notdetectedjson=json.dumps(Notdetectedlist)
                        obj = ServerPrinterdata.objects.get(lot=lot)
                        detailObj=ServerPrinterdata.objects.filter(lot=obj.lot).update(child_numbers=Notdetectedjson)
                    except:
                        print("No DATA AVAILABLE FOR ADDING TO CSV")             
                    
                
                    
                                         
                    try:          
                        file = "jsonfiles/"+lot+".csv"
                        
                        if(os.path.exists(file) and os.path.isfile(file)): 
                            os.remove(file) 
                            print("file deleted") 
                        else: 
                            print("file not found")     
                    except:
                        print("No Such csv File for deleteing")
                        
                    try:          
                        file1 = "Acceptedjson/"+lot+".csv"
                        
                        if(os.path.exists(file1) and os.path.isfile(file1)): 
                            os.remove(file1) 
                            print("file deleted") 
                        else: 
                            print("file not found")     
                    except:
                        print("No Such csv File for deleteing") 
                     
                    try:          
                        file = "Notdetectedjson/"+lot+".csv"
                                        
                        if(os.path.exists(file) and os.path.isfile(file)): 
                            os.remove(file) 
                            print("file deleted") 
                        else: 
                            print("file not found")     
                    except:
                            print("No Such csv File for deleteing")               
                    
                        # array=openfile.readlines()

                        # array = [row.strip() for row in array]

                        # for temp in array:
                        #     v=temp
                        #     serialnocsv=v[0:14]
                        #     print(serialno)
                                                
                else:
                                      
                    try:
                        detailsObj =ServerPrinterdata.objects.get(lot=lot)
                        prodObj=ServerPrinterdata.objects.get(lot=detailsObj.lot)
                        scObj=ServerScannerdata.objects.filter(lot=prodObj.lot).update(finalstatus="Closed")
                       
                        # no=prodObj.child_numbers
                        # # childnojson=json.loads(no)
                        # obj = PrinterdataTable.objects.get(id=id)
                        # detailObj=PrinterdataTable.objects.filter(lot=obj.lot).update(balanced_serialnumbers=no)#update child numbers to balanced serialno automatically
                        
                       
                      
                        try:
                                with open("jsonfiles/"+lot+".csv", 'r') as openfile:
        
                    
                                    csvreader = csv.reader(openfile)
                                    for row in csvreader:
                                        print(row[0])
                                        rejectednumberslist.append(row[0])   #append rejectednumberslist with serialno in jsonfile
                                                        
                                    rejectedjson=json.dumps(rejectednumberslist)
                                    obj = ServerPrinterdata.objects.get(lot=lot)
                                    detailObj=ServerPrinterdata.objects.filter(lot=obj.lot).update(Rejectednumbers=rejectedjson)   #Rejectednumbers field will update by using rejectedjson
                                    print("Rejectednumbers are updated")
                        except:
                            print("no Rejected json numbers are available .no csv file")
                        try:                 
                                                    
                                  with open("Acceptedjson/"+lot+".csv", 'r') as openfile:
        
                    
                                        csvreader = csv.reader(openfile)
                                        for row in csvreader:
                                            print(row[0])
                                            Acceptednumberslist.append(row[0])   #append rejectednumberslist with serialno in jsonfile
                                                        
                                        acceptedjson=json.dumps(Acceptednumberslist)
                                        obj = ServerPrinterdata.objects.get(lot=lot)
                                        detailObj=ServerPrinterdata.objects.filter(lot=obj.lot).update(acceptednumbers=acceptedjson)   #Rejectednumbers field will update by using rejectedjson
                                        print("Accepted numbers are updated")
                        except:
                            print("No accepeted serialnumbr.so no csv file")  
                        try:
                            with open("Notdetectedjson/"+lot+".csv", 'r') as openfile:
                            
                                            # Reading from json file
                                csvreader = csv.reader(openfile)
                                for row in csvreader:
                                    print(row[0])
                                    Notdetectedlist.append(row[0])
                                    print(Notdetectedlist)
                                                
                            Notdetectedjson=json.dumps(Notdetectedlist)
                            obj = ServerPrinterdata.objects.get(lot=lot)
                            detailObj=ServerPrinterdata.objects.filter(lot=obj.lot).update(child_numbers=Notdetectedjson)
                        except:
                            print("No DATA AVAILABLE FOR ADDING TO CSV")               
                                        
                        detailsObj = ServerPrinterdata.objects.get(lot=lot)
                        prodObj=ServerPrinterdata.objects.get(lot=detailsObj.lot)
                                                       
                        # child_number=prodObj.child_numbers
                        # childnojson=json.loads(child_number)
                        # del  childnojson[:]
                        # obj = PrinterdataTable.objects.get(id=id)
                        # detailObj=PrinterdataTable.objects.filter(lot=obj.lot).update(child_numbers=childnojson)
                        # print("child number delete and updated")
                                                    
                                                    
                               
                        try:    
                            file = "jsonfiles/"+lot+".csv"
                            if(os.path.exists(file) and os.path.isfile(file)):    #remove that json file after updating rejected numbers field
                                os.remove(file) 
                                print("file deleted") 
                            else: 
                                print("file not found")             
                        except:
                                print("No such csv File for delete")
                                            
                        try:
                            file1 = "Acceptedjson/"+lot+".csv"
                            if(os.path.exists(file1) and os.path.isfile(file1)):    #remove that json file after updating rejected numbers field
                                os.remove(file1) 
                                print("file deleted") 
                            else: 
                                print("file not found")             
                        except:
                                print("No such csv File for delete")
                        try:          
                            file = "Notdetectedjson/"+lot+".csv"
                                            
                            if(os.path.exists(file) and os.path.isfile(file)): 
                                os.remove(file) 
                                print("file deleted") 
                            else: 
                                print("file not found")     
                        except:
                                print("No Such csv File for deleteing")  
                                                    
                                            # with open("jsonfiles/"+lot+".json", 'r') as openfile:
    
                                            # # Reading from json file
                                            #    json_object = json.load(openfile)
                                            #    print(json_object["serialnumber"])
                                                    
                    except:
                            print("nochild numbers available")                          
                    obj = ServerPrinterdata.objects.get(lot=lot)
                    detailObj=ServerPrinterdata.objects.filter(lot=obj.lot).update(stop_button_resp=1,status="Closed")  
                    
                    detailsObj =ServerPrinterdata.objects.get(lot=lot) 
                    prodObj=ProductionOrder.objects.get(batch_number=detailsObj.lot)
                    detailObj=ProductionOrder.objects.filter(batch_number=prodObj.batch_number).update(status="Closed")   
                historysave=LocalseverHistory(modelname='PrinterdataTable',
                                    savedid="noid",
                                    operationdone='Batch Returned',
                                    donebyuser=loginname,
                                    donebyuserrole=loginuserrole, 
                                    description="Returned the batch "+lot+" "+"by"+" "+ loginname,
                                    donedatetime=datetime.datetime.now())
                historysave.save()    
                   
                            
                    # all data added to server using below code
                Begindatestring = date.today() 
                print(Begindatestring)
                t = time.localtime()

                    # Format the time as a string
                current_time = time.strftime("%H:%M:%S", t)
                print(current_time)    
                qs=ServerPrinterdata.objects.get(lot=lot)
                # prodObj=ProductionOrder.objects.get(gtin_number=qs.gtin)
                po=qs.processordernumber  
             
                    # obj = Printerdata.objects.get(printer_id=fgid)
                    # prodObj=PrinterdataTable.objects.get(gtin_number=obj.gtin)
                    # print(prodObj.gtin)
                inexid=qs.id
                gtin=qs.gtin
                processordernumber=po
                expiration_date=qs.expiration_date
                lot=qs.lot
                numbers=qs.numbers
                hrf=qs.hrf
                quantity=qs.quantity
                type=qs.type
                status=qs.status
                ip_address=qs.ip_address
                printed_numbers=qs.printed_numbers
                balanced_serialnumbers=qs.balanced_serialnumbers
                # responsefield=qs.responsefield
                    # preparebuttonresponse=qs.preparebuttonresponse
                # stopbtnresponse=qs.stopbtnresponse
                # start_pause_btnresponse=qs.start_pause_btnresponse
                    # pause_stop_btnresponse=qs.pause_stop_btnresponse
                # return_slno_btn_response=qs.return_slno_btn_response
                # batchstopmessage=qs.batchstopmessage
                    # label_response=qs.label_response
                child_numbers=qs.child_numbers
                scannergradefield=qs.scannergradefield
                # loadpause=qs.loadpause
                Rejectednumbers=qs.Rejectednumbers
                acceptednumbers=qs.acceptednumbers
                print(status)
                    # qws=Printerdata.objects.get(printer_id=fgid)
                    # inid=qws.printer_id
                obj = ServerPrinterdata.objects.get(lot=lot)
                # print(obj.gtin)
                # prodObj=PrinterdataTable.objects.get(gtin_number=obj.gtin)
                # print(prodObj.gtin)
                detailObj=PrinterdataTable.objects.filter(lot=obj.lot).update(numbers=numbers,
                                            balanced_serialnumbers=balanced_serialnumbers,
                                            # responsefield=False,
                                            # preparebuttonresponse=preparebuttonresponse,
                                            # stopbtnresponse=True,
                                            # start_pause_btnresponse=start_pause_btnresponse,
                                            # pause_stop_btnresponse=pause_stop_btnresponse,
                                            # return_slno_btn_response=return_slno_btn_response,
                                            # batchstopmessage=batchstopmessage,
                                            # label_response=label_response,
                                            child_numbers=child_numbers,
                                            scannergradefield=scannergradefield,
                                            # loadpause=loadpause,
                                            Rejectednumbers=Rejectednumbers,
                                            acceptednumbers=acceptednumbers,
                                            gtin=gtin,
                                            processordernumber=po,
                                            expiration_date=expiration_date,
                                            lot=lot,
                                            hrf=qs.hrf,
                                            quantity=quantity,
                                            type=type,
                                            status="Closed",
                                            ip_address=ip_address,
                                            printed_numbers=printed_numbers
                                            ),
                                
                    
                    # obj.delete()
                    
           
                scdata=ServerScannerdata.objects.all()
                sclength=len(scdata)
               
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
                # print(scdata[i].gtin)
                ServerScannerdata.objects.all().delete()
                histobj=LocalseverHistory.objects.all()
                historylength=len(histobj)
                print("historylength")
                for i in range(historylength):
                                    
                            history_save_to_server=History(
                                            modelname=histobj[i].modelname,
                                            savedid= histobj[i].savedid,
                                            operationdone=histobj[i].operationdone,
                                            donebyuser=histobj[i].donebyuser,
                                            donebyuserrole=histobj[i].donebyuserrole, 
                                            description=histobj[i].description,
                                            donedatetime=histobj[i].donedatetime,
                                            
                                        )
                                        
                            history_save_to_server.save()
                    # print(histobj[i].modelname)
                            
                histobj=LocalseverHistory.objects.all().delete()
                
                try:
                    conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")                     
                    jobs7 = ScannerTable.objects.filter(lot=lot,status="Accepted")
                    acceptedcount=len(jobs7)
                    scObj7=ProdReport.objects.filter(batch_number=lot).update(accepted=acceptedcount,production_date=Begindatestring,production_time=current_time)
                    print(acceptedcount, 'is last in the list ✅')
                    
                    jobs8 = ScannerTable.objects.filter(lot=lot,status="Rejected")
                    rejectedcount=len(jobs8)
                    scObj7=ProdReport.objects.filter(batch_number=lot).update(rejectedbycamera=rejectedcount,production_date=Begindatestring,production_time=current_time)
                    
                    jobs9 = ScannerTable.objects.filter(lot=lot,status="Damaged")
                    damagedcount=len(jobs9)
                    scObj7=ProdReport.objects.filter(batch_number=lot).update(damaged=damagedcount,production_date=Begindatestring,production_time=current_time)
                                                
                    print(rejectedcount,'is last in the list ✅')
                except:
                   print("Server connection losted so pro report not updata")
                 
               
                obj = Printerdata.objects.get(lot=lot)
                detailObj=Printerdata.objects.filter(lot=obj.lot).update(status="Closed")
                return redirect("return-list")  
                # return render(request,"returnserial.html",{"qs":qs,"returnvariable":1,"ret":1})  #success message after return serialno                            
            else:
                return redirect("signin") 
                         
# ...........................................................................
class Firstpage(View):     
     
    def get(self,request):
                             
        try:
            conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")
            
            try:
                Localapp_Register.objects.all().delete()
                Local_UserrolePermissions.objects.all().delete()
            except:
                print("no data found")    
            robj=Register.objects.all()
             
            userlength=len(robj)
            # print(userlength)
            for i in range(userlength):
                userdata_from_server=Localapp_Register(
                                id= robj[i].id,
                                Name= robj[i].Name,
                                email= robj[i].email,
                                password= robj[i].password,
                                date_birth= robj[i].date_birth,
                                age=robj[i].age,
                                userRole= robj[i].userRole,
                                username=robj[i].username,
                                address=robj[i].address,
                                employeeid=robj[i].employeeid
                                
                                
                                ) 
                userdata_from_server.save()
            uobj=UserrolePermissions.objects.all()
                    
            rolelength=len(uobj)
                    # print(userlength)
            for i in range(rolelength):
                role_from_server=Local_UserrolePermissions(
                                        id= uobj[i].id,
                                       activity_name= uobj[i].activity_name,
                                        admin= uobj[i].admin,
                                        operator= uobj[i].operator,
                                        supervisor= uobj[i].supervisor,
                                        masterdata=uobj[i].masterdata,
                                        
                                      
                                        
                                        
                                        ) 
                role_from_server.save()
            
            LM=Loginmodel.objects.get(id=1)
            inexid1=1
            username=LM.loginuname
            print(username)
            userrole=LM.userrole
            ip_address=LM.ip_address
            line=LM.line
            print("line:"+line)
                                            
            # loginuname=
                                            
            LM2=Loginmodel.objects.get(id=2)
            inexid2=2
            username2=LM2.loginuname
            userrole2=LM2.userrole
            ip_address2=LM2.ip_address
            line2=LM2.line
            print("line2:"+line2)
                                            
            LM3=Loginmodel.objects.get(id=3)
            inexid3=3
            username3=LM3.loginuname
            userrole3=LM3.userrole
            ip_address3=LM3.ip_address
            line3=LM3.line 
            print("line3:"+line3)
                                            
            try: 
                detailObj=LocalappLoginmodel.objects.filter(id=1).update(      
                                                # Login1_data_add_to_local_server = LocalappLoginmodel(
                    login_id=inexid1,
                    loginuname = username,
                    userrole=userrole,
                    ip_address=ip_address,
                    line=line
                )
                # Login1_data_add_to_local_server.save()
                print("saved")        
                detailObj=LocalappLoginmodel.objects.filter(id=2).update(
                # Login2_data_add_to_local_server =LocalappLoginmodel(
                    login_id=inexid2,
                    loginuname=username2,
                    userrole=userrole2,
                    ip_address=ip_address2,
                    line=line2
                )
                # Login2_data_add_to_local_server.save()
                detailObj=LocalappLoginmodel.objects.filter(id=3).update(
                    # Login3_data_add_to_local_server =LocalappLoginmodel(
                    login_id=inexid3,
                    loginuname=username3,
                    userrole=userrole3,
                    ip_address=ip_address3,
                    line=line3
                )
                # Login3_data_add_to_local_server.save()
                # print(Login1_data_add_to_local_server.ip_address)
            except:
                    print("Login Data add To Server have some Problem in Autovision View")                                          
                          
              
           
        except:
            print("haiii")
        return render(request,"firstpage.html")  
#.........................................................................
class StartView(View):
     
    
    def get(self,request,id):   
            
           
           
            qs=Printerdata.objects.get(id=id)
            
            try:    
                    serial=qs.numbers
                    serialnum=qs.numbers
                    serialno=json.loads(serial)
                    sl=json.loads(serialnum)
            except:
                    print("No serialnumber available in viewprinterview")
                    serialno=[]
                    po=qs.processordernumber
                    return render(request, 'Start.html', {'qs': qs,"po":po,"null_serial_number":1})
                    
            try:
                scanner_socket_8 = socket.socket()
                scanner_socket_8.settimeout(1)
                scanner_port_8=2001
        
                scanner_socket_8.connect(('192.168.200.134', scanner_port_8))
                #connecting the scanner to 2001 port 
               
            except socket.timeout: 
                po=qs.processordernumber
                print(po) 
                
                get_scannerconnection=1
                # obj = Printerdata.objects.get(id=id)
                # detailObj=Printerdata.objects.filter(lot=obj.lot).update(preparebuttonresponse=0)  
                # return render(request, 'cu-edit.html', {'qs': qs,'yu':0,'errormess':"data52ex","po":po,"alert":8,"buttonstatus":0}) 
                return render(request, 'Start.html', {'qs': qs,"po":po,"get_scannerconnection":get_scannerconnection})
            try:
                printer_socket_9 = socket.socket()
                printer_socket_9.settimeout(1)
                printer_port_9=34567
        
                printer_socket_9.connect(('192.168.200.150', printer_port_9))
            except:
                printstatus="p"
                qs=Printerdata.objects.get(id=id)
                printer_connection_lost=1
                po=qs.processordernumber  
               
                # Viewprinterview.threadstart=1                  
                # Viewprinterview.q.put(Viewprinterview.threadstart) 
                return render(request, 'Start.html', {'qs': qs,"po":po,"printer_connection_lost":printer_connection_lost})                                        
            try:
                printer_socket_10 = socket.socket()
                printer_socket_10.settimeout(1)
                printer_port_10=34567
        
                printer_socket_10.connect(('192.168.200.150', printer_port_10))
              
            
                printer_status_read_command_2="I2\x04"           
                printer_socket_10.send(printer_status_read_command_2.encode()) 
                status_response_2=printer_socket_10.recv(1024).decode()
                printstatus= status_response_2[1:2]
                
                
                if(qs.load_button_resp == 1):
                                    
                    if(printstatus=="h" or printstatus=="l"):               
                  
                
                    
                        qs=Printerdata.objects.get(id=id)
        
                        po=qs.processordernumber
                    
                        try:
                            serial=qs.numbers
                            serialno=json.loads(serial)
                        except:
                            print("serialnumbers finished")  #if the serialno finished this message will come    
                        form=PrinterForm(request.POST,instance=qs)
                      
                        
                        
                        try:
                            serilength=len(serialno)
                            
                            
                        except:
                            # print("no length")
                            serilength=0
                        
                        return render(request,"Start.html",{"qs":qs,'lp':1,"sc":serilength,"po":po,"pd":-1})
                    else:
                       
                        # return redirect("linkhiding")
                        printer_status_null=1
                        po=qs.processordernumber
                        return render(request, 'Start.html', {'qs': qs,"po":po,"printer_status_null":printer_status_null})                         
                       
                else:
                    qs=Printerdata.objects.get(id=id)
            
                    po=qs.processordernumber                    
                    return render(request,"Start.html",{"qs":qs,"po":po,"pd":5})
                    
                
            except socket.timeout:
                printstatus="p"
                qs=Printerdata.objects.get(id=id)
                printer_status_null=1
                po=qs.processordernumber
               
                # obj = Printerdata.objects.get(id=id)
                # detailObj=Printerdata.objects.filter(lot=obj.lot).update(preparebuttonresponse=0) 
                # return render(request, 'cu-edit.html', {'qs': qs,'yu':0,'errormess':"data52ex","po":po,"alert":4,"buttonstatus":0})   
                return render(request, 'Start.html', {'qs': qs,"po":po,"printer_status_null":printer_status_null})  
                                 
    def startprinter(self,num,serialno,gtin,lot,expire,hrfkey,hrfvalue,type,id): #printing activities are happening in th
        self.serialno=serialno
        self.gtin=gtin
        self.expire=expire
        self.lot=lot
        self.hrfkey=hrfkey
        self.hrfvalue=hrfvalue
        self.type=type  
        self.id=id
       
        slno_length=len(serialno) 
        # print("slno_length",slno_length)
        
        
                              
        printer_socket_11 = socket.socket()
        printer_port_11=34567
        printer_socket_11.connect(('192.168.200.150', printer_port_11)) 
        
        # sp = socket.socket()
        # ports=34567
        # sp.connect(('192.168.200.150', ports))
     
               
        if(type=="type5"):   #type5
                        
                        
                        printer_load_command_3= "L,new8.lbl\x04"
                        printer_socket_11.send(printer_load_command_3.encode()) 
                        load_response_3=printer_socket_11.recv(1024).decode() 
                          
                        printer_prepare_command_3= "E\x04"        
                        printer_socket_11.send(printer_prepare_command_3.encode()) 
                        prepare_response_3=printer_socket_11.recv(1024).decode()
                        
                        detailsobj2 = Printerdata.objects.get(id=id) 
                        slnoli=[]
                        
                        # for ss in range() 
                        n1=2
                        d1=0
                        a1=0
                        b1=1 
                        c1=0
                        d2=5 
                        i=0           
                        upjso=[] 
                       
                       
                        while(i<slno_length):                   
                            qs = Printerdata.objects.get(id=id)
                            # obj = Printerdata.objects.get(id=id)
                            # if()
                            # detailObj=Printerdata.objects.filter(lot=qs.lot).update(trigger_flag=1)                 
                                                             
                            for f in range(c1,d2):
                                               
                                    for sn in serialno[a1:b1]: 
                                                    try:     #if there any issues for ethernet of printer,we should stop printer through plc
                                                      
                                                        printer_socket_12 = socket.socket()
                                                        printer_socket_12.settimeout(1)
                                                        printer_port_12=34567
                                                
                                                        printer_socket_12.connect(('192.168.200.150', printer_port_12)) 
                                                                
                                                                    # print(qs.start_button)
                                                          
                                            
                                                        printer_field_command_3= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x09"+"hrf"+"\x09hrfvalue"+"\x04"
                                                        printer_socket_11.send(printer_field_command_3.encode()) 
                                                        field_response_3=printer_socket_11.recv(1024).decode()
                                                                
                                                        printer_value_command_3= "QAC\x09"  + "(01)" + gtin + "(21)" + sn + "(10)" + lot + "(17)" + expire + "(45)" + hrfvalue + "\x09" + "Exp"+ "\x09" + expire + "\x09" + "Lot" + "\x09" + lot + "\x09" + "Gtin" + "\x09" +  gtin + "\x09" + "Slno" + "\x09" + sn + "\x09" + hrfkey + "\x09" + hrfvalue + "\x04"
                                                        printer_socket_11.send(printer_value_command_3.encode()) 
                                                        value_response_3=printer_socket_11.recv(1024).decode() 
                                                                            
                                                        printer_start_command_3= "F2\x04"
                                                        printer_socket_11.send(printer_start_command_3.encode()) 
                                                        start_response_3=printer_socket_11.recv(1024).decode()
                                                      
                                                        
                                                        
                                                        
                                                       #iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii 
                                                        # message92= "IE\x04"
                                                        # printer_socket_11.send(message92.encode()) 
                                                        # data92=printer_socket_11.recv(1024).decode()
                                                                                                       
                                                                            
                                                        # k=str(data92[0:1])
                                                       
                                                        
                                                        
                                                                            
                                                        # for c in k:
                                                        #     ascii_values=ord(c)
                                                        # # print("ascii_values",ascii_values)
                                                        # # if ascii_values == 2:    
                                                        # #     print("yyy",data92)       
                                                        # # else:
                                                        # #   print("tttttt")                       
                                                        # message931= "I5\x04"
                                                        # printer_socket_11.send(message931.encode()) 
                                                        # belt=printer_socket_11.recv(1024).decode() 
                                                        # # print("message931",belt[0:1])
                                                        # belt_speed=belt[0:1]
                                                        # if(belt_speed=="0"):
                                                        #    if(ascii_values == 1):                     
                                                        #         print("belt speed 0 breaked")
                                                        #         obj = Printerdata.objects.get(id=id)
                                                        #         detailObj=Printerdata.objects.filter(lot=obj.lot).update(start_button_resp=0)                                                           
                                                        #         break                   
                                                         #iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii 
                                                        
                                                        a1=a1+1
                                                        b1=b1+1
                                                    except socket.timeout:
                                                        print("TIMEOUT PRINTER")
                                                
                                                        # break 
                                    try:     #if there any issues for ethernet of printer,we should stop printer through plc
                                        printer_socket_13 = socket.socket()
                                        printer_socket_13.settimeout(1)
                                        printer_port_13=34567
                                                
                                        printer_socket_13.connect(('192.168.200.150', printer_port_13))    
                                        if(qs.start_button_resp == 0):
                                            # i=30001
                                            i=slno_length+1
                                            c1=d2
                                            d2=d2+5
                                            print("breaked")
                                            printer_wait_command="QAF\x04"
                                            printer_socket_13.send(printer_wait_command.encode()) 
                                            wait_response=printer_socket_13.recv(1024).decode()
                                            break
                                        else:
                                            #iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii 
                                            # message92= "IE\x04"
                                            # printer_socket_13.send(message92.encode()) 
                                            # data92=printer_socket_13.recv(1024).decode()
                                                                                                            
                                                                            
                                            # k=str(data92[0:1])
                                            #             # print("viewprinterview loop working")
                                                        
                                                        
                                                                            
                                            # for c in k:
                                            #     ascii_values=ord(c)
                                                         
                                            #     message931= "I5\x04"
                                            #     printer_socket_13.send(message931.encode()) 
                                            #     belt=printer_socket_13.recv(1024).decode() 
                                            #             # print("message931",belt[0:1])
                                            #     belt_speed=belt[0:1]
                                            #     if(belt_speed=="0"):
                                            #                if(ascii_values == 1):                     
                                            #                     print("belt sped 0 breaked")
                                            #                     obj = Printerdata.objects.get(id=id)
                                            #                     detailObj=Printerdata.objects.filter(lot=obj.lot).update(start_button_resp=0)                                                            
                                            #                     break   
                                                #iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii                       
                                            i=i+1                   
                                            c1=d2
                                            d2=d2+5
                                    except socket.timeout:
                                        # print("printer44444444")
                                        dummyflag=0
                            try:         #if there any issues for ethernet of scanner,we should stop printer through plc
                                scanner_socket_9 = socket.socket()
                                scanner_socket_9.settimeout(1)
                                scanner_port_9=2001
       
                                scanner_socket_9.connect(('192.168.200.134', scanner_port_9))
 
                                
                                        # print(qs.start_button)
                            except socket.timeout:
                                print("scanner time out")
                                break 
        
        elif(type=="type2"):   #type2
                        
                        
                        printer_load_command_4= "L,new7.lbl\x04"    #load label
                        printer_socket_11.send(printer_load_command_4.encode()) 
                        load_response_4=printer_socket_11.recv(1024).decode()
                          
                        printer_prepare_command_4= "E\x04"               #prepare printer
                        printer_socket_11.send(printer_prepare_command_4.encode()) 
                        prepare_response_4=printer_socket_11.recv(1024).decode()
                                    
                        detailsobj2 = Printerdata.objects.get(id=id) 
                        slnoli=[]
                        
                        # for ss in range() 
                        n1=2
                        d1=0
                        a1=0
                        b1=1 
                        c1=0
                        d2=5 
                        i=0           
                        upjso=[] 
                        # obj = Printerdata.objects.get(id=id)
                        # detailObj=Printerdata.objects.filter(lot=obj.lot).update(start_button=1,loadpause=1)                                        
                       
                        while(i<slno_length):                   
                            qs = Printerdata.objects.get(id=id)
                            
                            # print(qs.start_button)                                          
                            for f in range(c1,d2):
                                    for sn in serialno[a1:b1]: 
                                                    try:     #if there any issues for ethernet of printer,we should stop printer through plc
                                                        printer_socket_14 = socket.socket()
                                                        printer_socket_14.settimeout(1)
                                                        printer_port_14=34567
                                                    
                                                        printer_socket_14.connect(('192.168.200.150', printer_port_14)) 
                                                                
                                                                    # print(qs.start_button)
                                                          
                                            
                                                        printer_field_command_4= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x04"  #loading field names
                                                        printer_socket_11.send(printer_field_command_4.encode()) 
                                                        field_response_4=printer_socket_11.recv(1024).decode()
                                                    
                                                        printer_value_command_4= "QAC\x09"  + "(01)" + gtin + "(21)" + sn + "(10)" + lot + "(17)" + expire + "\x09" + "Exp\x09" + expire + "\x09Lot" + "\x09" + lot + "\x09" + "Gtin\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"  #loading values
                                                        printer_socket_11.send(printer_value_command_4.encode()) 
                                                        value_response_4=printer_socket_11.recv(1024).decode() 
                                                        
                                                        printer_start_command_4= "F2\x04"   #print values
                                                        printer_socket_11.send(printer_start_command_4.encode()) 
                                                        start_response_4=printer_socket_11.recv(1024).decode()
                                                            
                                                            
                                                        
                                                        a1=a1+1
                                                        b1=b1+1
                                                    except socket.timeout:
                                                        print("TIMEOUT PRINTER")
                                                
                                                        # break 
                                    try:     #if there any issues for ethernet of printer,we should stop printer through plc
                                        printer_socket_15 = socket.socket()
                                        printer_socket_15.settimeout(1)
                                        printer_port_15=34567
       
                                        printer_socket_15.connect(('192.168.200.150', printer_port_15))    
                                        if(qs.start_button_resp == 0):
                                            # i=30001
                                            i=slno_length+1
                                            c1=d2
                                            d2=d2+5
                                            print("breaked")
                                            printer_wait_command_1="QAF\x04"
                                            printer_socket_15.send(printer_wait_command_1.encode()) 
                                            data36=printer_socket_15.recv(1024).decode()
                                            break
                                        else:                       
                                            i=i+1                   
                                            c1=d2
                                            d2=d2+5
                                    except socket.timeout:
                                        print("printer44444444")
                            try:         #if there any issues for ethernet of scanner,we should stop printer through plc
                                scanner_socket_10 = socket.socket()
                                scanner_socket_10.settimeout(1)
                                scanner_port_10=2001
                        
                                scanner_socket_10.connect(('192.168.200.134', scanner_port_10))
 
                                
                                        # print(qs.start_button)
                            except socket.timeout:
                                print("scanner time out")
                                break                                      
        elif(type=="type1"):   #type1
                        
                        
                        printer_load_command_5= "L,new5.lbl\x04"
                        printer_socket_11.send(printer_load_command_5.encode()) 
                        load_response_5=printer_socket_11.recv(1024).decode()
                          
                        printer_prepare_command_5= "E\x04"        
                        printer_socket_11.send(printer_prepare_command_5.encode()) 
                        prepare_response_5=printer_socket_11.recv(1024).decode()
                        
                        detailsobj2 = Printerdata.objects.get(id=id) 
                        slnoli=[]
                        
                        # for ss in range() 
                        n1=2
                        d1=0
                        a1=0
                        b1=1 
                        c1=0
                        d2=5 
                        i=0           
                        upjso=[] 
                        # obj = Printerdata.objects.get(id=id)
                        # detailObj=Printerdata.objects.filter(lot=obj.lot).update(start_button=1,loadpause=1)                                        
                       
                        while(i<slno_length):                   
                            qs = Printerdata.objects.get(id=id)
                            
                            # print(qs.start_button)                                          
                            for f in range(c1,d2):
                                    # serialno1=qs.numbers
                                    # serialno2=json.loads(serialno1)                
                                    for sn in serialno[a1:b1]: 
                                                    try:     #if there any issues for ethernet of printer,we should stop printer through plc
                                                        printer_socket_16 = socket.socket()
                                                        printer_socket_16.settimeout(1)
                                                        printer_port_16=34567
                                                
                                                        printer_socket_16.connect(('192.168.200.150', printer_port_16)) 

                                                                
                                                                    # print(qs.start_button)
                                                          
                                            
                                                        printer_field_command_5= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x04"
                                                        printer_socket_11.send(printer_field_command_5.encode()) 
                                                        field_response_5=printer_socket_11.recv(1024).decode()
                                                        
                                                                # print(slno)                    
                                                                # message6= "QAC\x09" + "55555777779(10)45612(21)\x09GTIN\x09" + gtin+"\x09"+ "lot\x09" + lot +"\x09" +"exp\x09" + expire+"\x09"+"serialno\x09"+sn+"\x04"
                                                        printer_value_command_5= "QAC\x09"  + "(01)" + gtin + "(21)" + sn + "(10)" + lot + "(17)" + expire + "(45)" + hrfvalue + "\x09" + "Exp\x09" + expire + "\x09" + "Lot" + "\x09" + lot + "\x09" + "GTIN\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"
                                                        # message15= "QAC\x09" + "(01)" +  gtin +  "(10)" + lot + "(17)" + expire +  "(21)" + sn +"(45)"+ hrfvalue +  "\x09" + "Exp\x09" + expire + "\x09Lot" + "\x09" + lot + "\x09" + "GTIN\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"
                                                        printer_socket_11.send(printer_value_command_5.encode()) 
                                                        value_response_5=printer_socket_11.recv(1024).decode() 
                                                                        
                                                        printer_start_command_5= "F2\x04"
                                                        printer_socket_11.send(printer_start_command_5.encode()) 
                                                        start_response_5=printer_socket_11.recv(1024).decode()
                                                         
                                                        
                                                        
                                                        a1=a1+1
                                                        b1=b1+1
                                                    except socket.timeout:
                                                        print("TIMEOUT PRINTER")
                                                
                                                        # break 
                                    try:     #if there any issues for ethernet of printer,we should stop printer through plc
                                        printer_socket_17 = socket.socket()
                                        printer_socket_17.settimeout(1)
                                        printer_port_17=34567
                                    
                                        printer_socket_17.connect(('192.168.200.150', printer_port_17))   
                                        if(qs.start_button_resp == 0):
                                            # i=30001
                                            i=slno_length+1
                                            c1=d2
                                            d2=d2+5
                                            print("breaked")
                                            printer_wait_command_2="QAF\x04"
                                            printer_socket_17.send(printer_wait_command_2.encode()) 
                                            wait_response_2=printer_socket_17.recv(1024).decode()
                                            break
                                        else:                       
                                            i=i+1                   
                                            c1=d2
                                            d2=d2+5
                                    except socket.timeout:
                                        # print("printer44444444")
                                        dummy_flag=0
                            try:         #if there any issues for ethernet of scanner,we should stop printer through plc
                                scanner_socket_11 = socket.socket()
                                scanner_socket_11.settimeout(1)
                                scanner_port_11=2001
                        
                                scanner_socket_11.connect(('192.168.200.134', scanner_port_11))
                                
                                        # print(qs.start_button)
                            except socket.timeout:
                                print("scanner time out")
                                break                         
                                                                                    
    def post(self,request,id):
                                
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
                qs=Printerdata.objects.get(id=id)
                form=PrinterForm(request.POST,instance=qs) 
                id=qs.id    
                gtin=qs.gtin 
                ponumber=qs.processordernumber
                expire =str(qs.expiration_date)
                lot=qs.lot
                type=qs.type
                hrf=qs.hrf 
                printednumbers=qs.printed_numbers
                ip_address=qs.ip_address
                child_numbers=qs.child_numbers
                po=qs.processordernumber
                                    
                try: 
                        if(type=="type2"):
                            hrfkey="null"                   
                            hrfvalue="null"                  
                        # print(printednumbers) 
                        else:
                                                    
                            hrfjson=json.loads(hrf) 
                            hrf1value=hrfjson["hrf1value"]
                            hrf1key=hrfjson["hrf1"]
                            hrf2value=hrfjson["hrf2value"]
                            hrf2key=hrfjson["hrf2"]
                            hrf3value=hrfjson["hrf3value"]
                            hrf3key=hrfjson["hrf3"]
                            hrf4value=hrfjson["hrf4value"]
                            hrf4key=hrfjson["hrf4"]
                            hrf5key=hrfjson["hrf5"]
                            hrf5value=hrfjson["hrf5value"]
                            hrf6key=hrfjson["hrf6"]
                            hrf6value=hrfjson["hrf6value"]
                            
                    
                            if(hrf1key!="" or hrf1key!="null"):
                                hrfkey=hrf1key
                            elif(hrf2key!="" or hrf2key!="null"):
                                hrfkey=hrf2key
                            elif(hrf3key!="" or hrf3key!="null"):
                                hrfkey=hrf3key
                            elif(hrf4key!="" or hrf4key!="null"):
                                hrfkey=hrf4key
                            elif(hrf5key!="" or hrf5key!="null"):
                                hrfkey=hrf5key
                            elif(hrf6key!="" or hrf6key!="null"):
                                hrfkey=hrf6key
                            
                        
                            if(hrf1value!="" or hrf1value!="null"):
                                hrfvalue=hrf1value
                            elif(hrf2value!="" or hrf2value!="null"):
                                hrfvalue=hrf2value
                            elif(hrf3value!="" or hrf3value!="null"):
                                hrfvalue=hrf3value
                            elif(hrf4value!="" or hrf4value!="null"):
                                hrfvalue=hrf4value
                            elif(hrf5value!="" or hrf5value!="null"):
                                hrfvalue=hrf5value
                            elif(hrf6value!="" or hrf6value!="null"):
                                hrfvalue=hrf6value
                except:
                    print("no hrf")
                try:
                    serial=qs.numbers
                    serialno=json.loads(serial)
                    serialnum=qs.numbers
                    serilength=len(serialno)
                    
                     
                
                except:
                    print("pause printing because serialnumber are empty")   #if the length zero it will work
                    serilength=0 
                    serialno=[] 
                    
                try:
                    scanner_socket_15 = socket.socket()
                    scanner_socket_15.settimeout(1)
                    scanner_port_15=2001
            
                    scanner_socket_15.connect(('192.168.200.134', scanner_port_15))
                except socket.timeout: 
                    po=qs.processordernumber
                    # print(po) 
                    get_scannerconnection=1
                    # obj = Printerdata.objects.get(id=id)
                    # detailObj=Printerdata.objects.filter(lot=obj.lot).update(preparebuttonresponse=0)  
                    return render(request, 'Start.html', {'qs': qs,"sc":serilength,"po":po,"get_scannerconnection":get_scannerconnection})    
                    # return render(request, 'cu-edit.html', {'qs': qs,'yu':0,'errormess':"data52ex","po":po,"alert":8,"buttonstatus":0})           
                try:
                    printer_socket_19 = socket.socket()
                    printer_socket_19.settimeout(1)
                    printer_port_19=34567
            
                    printer_socket_19.connect(('192.168.200.150', printer_port_19)) 
                except:
                    printer_connection_lost=1
                    po=qs.processordernumber  
                    return render(request, 'Start.html', {'qs': qs,"sc":serilength,"po":po,"printer_connection_lost":printer_connection_lost})
                try:
                    printer_socket_20 = socket.socket()
                    printer_socket_20.settimeout(2)
                    printer_port_20=34567
            
                    printer_socket_20.connect(('192.168.200.150', printer_port_20)) 
                    printer_status_read_command_3="I2\x04"           
                    printer_socket_20.send(printer_status_read_command_3.encode()) 
                    status_response_3= printer_socket_20.recv(1024).decode()
                    printstatus= status_response_3[1:2]
                except socket.timeout:
                       printstatus="kkkk" 
            
                        
            if(qs.load_button_resp == 1):    
                if(printstatus=="h" or printstatus=="l"):                     
                                 
                        x1 = threading.Thread(target=StartView.startprinter,args=(self,10,serialno,gtin,lot,expire,hrfkey,hrfvalue,type,id,))   #invoking printerfun1 thread with arguments from database
                            
                        x1.start()
                       
                        #invoking printerfun1 thread with arguments from database
                        
                        obj = Printerdata.objects.get(id=id)
                        detailObj=Printerdata.objects.filter(lot=obj.lot).update(start_button_resp=1,return_button_resp=0)
                        po=qs.processordernumber 
                        
                     
                            # print("ascii_values",ascii_values)
                        # fg=[4,0,0,0,3,0,0,0,2,0,0,0,1]
                        # by=bytearray(fg)
                        # by[0]=0
                        # by[4]=0
                        # by[8]=2
                        # by[12]=1
                                        
                        # try:
                        #     plc_conn = socket.socket()
                        #     plc_port=12000
                                          
                        #     plc_conn.connect(('192.168.200.55', plc_port))
                        #     s=by
                                        
                                    
                        #     message4556=by     
                        #     plc_conn.send(message4556) 
                        #     data360= plc_conn.recv(1024).decode()
                        #     print(data360)
                                   
                        #     data_to_string=str(data360)
                        #                         # print("viewprinterview loop working")
                                                
                                                
                                                                    
                        #     for c in data_to_string:
                        #         ascii_values_data_to_string=ord(c)
                        #         print(ascii_values_data_to_string)
                        # except:
                        #     print("plc not responding") 
                               
                        try:
                            n=6
                            while(n>5):
                                printer_read_output_command="IE\x04"           
                                printer_socket_20.send(printer_read_output_command.encode()) 
                                read_response=printer_socket_20.recv(1024).decode()
                                
                                                            
                                data_to_string=str(read_response[0:1])
                                # print("output 2 is ", data_to_string)                                                    
                                for c in data_to_string:
                                    ascii_values_data_to_string=ord(c)
                                    
                                if(ascii_values_data_to_string == 2): 
                                    
                                    n=4 
                                    # plc connection for start convare  
                                    fg=[4,0,0,0,3,0,0,0,2,0,0,0,1]
                                    by=bytearray(fg)
                                    by[0]=0
                                    by[4]=0
                                    by[8]=2
                                    by[12]=1
                                        
                                    try:
                                        plc_conn = socket.socket()
                                        plc_port=12000
                                        # plc_conn.settimeout(1)  
                                        plc_conn.connect(('192.168.200.55', plc_port))
                                        s=by
                                        
                                    
                                        message4556=by     
                                        plc_conn.send(message4556) 
                                        data360= plc_conn.recv(1024).decode()
                                        # print(data360)
                                   
                                        data_to_string=str(data360)
                                                # print("viewprinterview loop working")
                                                
                                                
                                                                    
                                        for c in data_to_string:
                                            ascii_values_data_to_string=ord(c)
                                            # print(ascii_values_data_to_string)
                                    except:
                                        print("plc not responding")
                                    return redirect('pauseview',id=id)
                                else:
                                    m=0
                                    print("ascii not 2")
                                    # break                    
                                    # return render(request, 'Start.html', {'qs': qs,'pd':1,"sc":serilength,"po":po,"alert":0})                     
                        except:
                       
                        # '/pauseview/'+id
                           return render(request, 'Start.html', {'qs': qs,'pd':1,"sc":serilength,"po":po,"alert":0}) 
                else:
                        printer_status_null=1
                        po=qs.processordernumber 
                        obj = Printerdata.objects.get(id=id)
                        detailObj=Printerdata.objects.filter(lot=obj.lot).update(start_button_resp=0)
                        return render(request, 'Start.html', {'qs': qs,"po":po," printer_status_null":printer_status_null}) 
            else:
                qs=Printerdata.objects.get(id=id)
            
                po=qs.processordernumber                    
                return render(request,"Start.html",{"qs":qs,"po":po,"pd":5})    
                # except:
                #     # both else and expcept are same condition
                #     printer_status_null=1
                #     po=qs.processordernumber 
                #     obj = Printerdata.objects.get(id=id)
                #     detailObj=Printerdata.objects.filter(lot=obj.lot).update(start_button=0,loadpause=0) 
                #     return render(request, 'Start.html', {'qs': qs,"sc":serilength,"po":po,"printer_status_null":printer_status_null})    
                        
                                                          
           
                   
class Pauseview(View):
    def get(self,request,id):   
            
           
           
            qs=Printerdata.objects.get(id=id)
            try:
                scanner_socket_12 = socket.socket()
                scanner_socket_12.settimeout(1)
                scanner_port_12=2001
        
                scanner_socket_12.connect(('192.168.200.134', scanner_port_12))   #connecting the scanner to 2001 port 
                
            except socket.timeout: 
                po=qs.processordernumber
                printer_status_null=1 
                # obj = Printerdata.objects.get(id=id)
                # detailObj=Printerdata.objects.filter(lot=obj.lot).update(preparebuttonresponse=0)  
                # return render(request, 'cu-edit.html', {'qs': qs,'yu':0,'errormess':"data52ex","po":po,"alert":8,"buttonstatus":0})
                return render(request,"pause.html",{"qs":qs,"po":po,"printer_status_null":printer_status_null})                                                             
            try:
                    printer_socket_21 = socket.socket()
                    printer_socket_21.settimeout(1)
                    printer_port_21=34567
            
                    printer_socket_21.connect(('192.168.200.150', printer_port_21)) 
                    
                    
                    
                    printer_status_read_command_4="I2\x04"           
                    printer_socket_21.send(printer_status_read_command_4.encode()) 
                    status_response_1=printer_socket_21.recv(1024).decode()
                    printstatus= status_response_1[1:2]
            except socket.timeout:
                    printer_connection_lost=1
                    po=qs.processordernumber
                    # Viewprinterview.threadstart=1                   
                    # Viewprinterview.q.put(Viewprinterview.threadstart) 
                    return render(request,"pause.html",{"qs":qs,"po":po,"printer_connection_lost":printer_connection_lost})  
                
            # message320="I2\x04"           
            # s.send(message320.encode()) 
            # data360=s.recv(1024).decode()
            # printstatus=data360[1:2]
                
                
            if(qs.load_button_resp == 1):
                                    
                if(printstatus=="h" or printstatus=="l"):               
                    
                    
                        
                            qs=Printerdata.objects.get(id=id)
            
                            po=qs.processordernumber
                        
                            try:
                                serial=qs.numbers
                                serialno=json.loads(serial)
                            except:
                                print("serialnumbers finished")  #if the serialno finished this message will come    
                            form=PrinterForm(request.POST,instance=qs)
                        
                            
                            
                            try:
                                serilength=len(serialno)
                                
                                
                            except:
                                # print("no length")
                                serilength=0
                            
                            return render(request,"pause.html",{"qs":qs,'lp':1,"sc":serilength,"po":po,"pd":-1})
                else:
                        
                        
                            po=qs.processordernumber
                            printer_status_null=1
                        
                            return render(request,"pause.html",{"qs":qs,"po":po,"printer_status_null":printer_status_null})
                        
            else:
                qs=Printerdata.objects.get(id=id)
                
                po=qs.processordernumber                    
                return render(request,"pause.html",{"qs":qs,"po":po,"pd":5})
                        
                
            # except socket.timeout:
            #     printstatus="p"
            #     qs=Printerdata.objects.get(id=id)
            
            #     po=qs.processordernumber  
            #     printer_status_null=0 
            #     # obj = Printerdata.objects.get(id=id)
            #     # detailObj=Printerdata.objects.filter(lot=obj.lot).update(preparebuttonresponse=0) 
            #     # return render(request, 'cu-edit.html', {'qs': qs,'yu':0,'errormess':"data52ex","po":po,"alert":4,"buttonstatus":0}) 
            #     return render(request,"pause.html",{"qs":qs,"po":po,"printer_status_null":printer_status_null})                                                      
    def post(self,request,id):
            qs=Printerdata.objects.get(id=id)
            po=qs.processordernumber 
            
            try:
                scanner_socket_13 = socket.socket()
                scanner_socket_13.settimeout(1)
                scanner_port_13=2001
        
                scanner_socket_13.connect(('192.168.200.134', scanner_port_13))
  #connecting the scanner to 2001 port 
                
            except socket.timeout: 
                po=qs.processordernumber
                get_scannerconnection=1 
                # obj = Printerdata.objects.get(id=id)
                # detailObj=Printerdata.objects.filter(lot=obj.lot).update(preparebuttonresponse=0)  
                # return render(request, 'cu-edit.html', {'qs': qs,'yu':0,'errormess':"data52ex","po":po,"alert":8,"buttonstatus":0}) 
                return render(request,"pause.html",{"qs":qs,"po":po,"get_scannerconnection":get_scannerconnection})        
            try:
                printer_socket_22 = socket.socket()
                printer_socket_22.settimeout(1)
                printer_port_22=34567
        
                printer_socket_22.connect(('192.168.200.150', printer_port_22)) 
                
                belt_speed_command= "I5\x04"
                printer_socket_22.send(belt_speed_command.encode()) 
                belt=printer_socket_22.recv(1024).decode() 
                        # print("message931",belt[0:1])
                belt_speed=belt[0:1]
            except:
                printer_connection_lost=1 
                po=qs.processordernumber
               
                return render(request,"pause.html",{"qs":qs,"po":po,"printer_connection_lost":printer_connection_lost})    
            try:
               
                printer_socket_23 = socket.socket()
                printer_socket_23.settimeout(1)
                printer_port_23=34567
                
        
                printer_socket_23.connect(('192.168.200.150', printer_port_23))   
                printer_status_read_command_5="I2\x04"           
                printer_socket_23.send(printer_status_read_command_5.encode()) 
                status_response_5=printer_socket_23.recv(1024).decode()
                printstatus= status_response_5[1:2]
            except socket.timeout:
                printstatus="kkkk"
                
            if(printstatus=="h" or printstatus=="l"):    
                
           
                    obj = Printerdata.objects.get(id=id)
                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(start_button_resp=0)
                    # start_button,loadpause are same use 
                    # print("work loadpause 0")
                    printer_wait_command_4="QAF\x04"
                    printer_socket_23.send(printer_wait_command_4.encode()) 
                    wait_response_4=printer_socket_23.recv(1024).decode()
                    # print("data36",data36)                                                   
                    data_to_string=str(wait_response_4[0]) 
                    for c1 in data_to_string:
                        ascii_values_data_to_string=ord(c1)
                    # print("ascii",ascii_values_data_to_string)
                    try:
                        if(ascii_values_data_to_string==4):
                            if(belt_speed!="0"):                   
                                # plc connection for stopping convire                     
                                fg=[4,0,0,0,3,0,0,0,2,0,0,0,1]
                                by=bytearray(fg)
                                by[0]=1
                                by[4]=0
                                by[8]=2
                                by[12]=1
                                try:
                                    plc_conn = socket.socket()
                                    plc_port=12000
                                    plc_conn.settimeout(1)  
                                    plc_conn.connect(('192.168.200.55', plc_port))
                                    s=by
                                    
                                    
                                    message4556=by     
                                    plc_conn.send(message4556) 
                                    data360= plc_conn.recv(1024).decode()
                                    # print(data360)
                                    
                                    
                                    data_to_string=str(data360)
                                            
                                                
                                                
                                                                    
                                    for c in data_to_string:
                                        ascii_values_data_to_string=ord(c)
                                        # print(ascii_values_data_to_string)
                                except:
                                    print(" plc not responding")                     
                            return redirect('start',id=id) 
                        else:
                            m=7                    
                    except:
                     
                        return render(request, 'pause.html', {'qs': qs,'pd':1,"po":po,"alert":0})  
            else:
                    printer_status_null=1
                    po=qs.processordernumber 
                    
                    obj = Printerdata.objects.get(id=id)
                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(start_button_resp=0)                   
                    return render(request,"pause.html",{"qs":qs,"po":po,"printer_status_null":printer_status_null})
            
#----------------------------------------------------------------------------------------------------

class NotScanView(View):   #getting datas
    def get(self,request,id):
       
                            
            hostname = socket.gethostname()
            systemip = socket.gethostbyname(hostname) 
            
            Line1 =LocalappLoginmodel.objects.get(id=1)
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
                qs=ServerScannerdata.objects.get(id=id)
            
            # form=PrinterForm(request.POST,instance=qs)
                return render(request,"Rescan.html",{"qs":qs})
            else:
                return redirect("signin")
        # except:
        #     return redirect("databaseerror")  
        

        #     return redirect("databaseerror")   
#---------------------------------------------------------------                
def Rescan(request,id):
                   
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
                            qs= ServerScannerdata.objects.get(id=id)
                            try: 
                                scanner_socket_14 = socket.socket()
                                scanner_port_14=2001
                                scanner_socket_14.connect(('192.168.200.134', scanner_port_14))
  
                            except:
                              
                                return redirect("scanner-message") 
                            try:         
                                dummycount = 8
                                scanner_data=scanner_socket_14.recv(1024).decode()
                                print(scanner_data)
                                decoded_grade=scanner_data[0]
                                if(decoded_grade=="4"):
                                    grade="A"
                                    status="Accepted"
                                elif(decoded_grade=="3"):
                                    grade="B"
                                    status="Accepted"
                                elif (decoded_grade=="2"):
                                    grade="C"
                                    status="Rejected"
                                elif (decoded_grade=="1"):
                                    grade="D"
                                    status="Rejected"
                                elif (decoded_grade=="0"):
                                    grade="F"
                                    status="Rejected"    
                                else:
                                    grade="NO"
                                    status="Not Detected" 
                                type=qs.type
                                if(type=="type2"):
                                    h=scanner_data[38:]    #data from scanner is coming in decoded textbox
                                    decoded_serialnumber=scanner_data[29:38]
                                    print(decoded_serialnumber)
                                elif(type=="type5" or type=="type1"):
                                    h=scanner_data[38:]    #data from scanner is coming in decoded textbox
                                    decoded_serialnumber=scanner_data[25:34]
                                    print(decoded_serialnumber)                   
                                # decodedtext=data
                                # print(decodedtext)
                                # print(v)
                                # print(h)
                                if (decoded_serialnumber== qs.serialnumber):   #serialno from database serialno from sacnner are checking(whather any match is there ) 
                                
                                    ghi=1 
                                
                                else:
                                
                                    ghi=0 
                                   
                                    
                                                        
                                
                                
                                r={"serialnumber":h,
                                        "decodedtext":scanner_data}
                               
                                try:
                                    conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")                    
                                    historysave=History(modelname='ScannerTable',
                                                savedid="noid",
                                                operationdone='rescan',
                                                donebyuser=loginname,
                                                donebyuserrole=loginuserrole, 
                                                description="Rescan of serial number "+h+" "+"by"+" "+ loginname,
                                                donedatetime=datetime.datetime.now())
                                    historysave.save()
                                except:
                                    historysave=LocalseverHistory(modelname='ScannerTable',
                                                savedid="noid",
                                                operationdone='rescan',
                                                donebyuser=loginname,
                                                donebyuserrole=loginuserrole, 
                                                description="Rescan of serial number "+h+" "+"by"+" "+ loginname,
                                                donedatetime=datetime.datetime.now())
                                    historysave.save()
                                b=json.dumps(r)
                                #  context = {'page_obj':b
                                #     } 
                                return render(request,'Rescan.html',{"qs":qs,"decodedtext":scanner_data,"grade":grade,"ghi":ghi,"newstatus":status}) 
                            except:
                                print("data didnt receive")
                                               
            else:
                            return redirect("signin")
       
def RescanUpdate(request,id):
                        
   
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
                uname =LocalappLoginmodel.objects.get(id=2)
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
                qs= ServerScannerdata.objects.get(id=id) 
                lot=qs.lot 
                gtin=qs.gtin
                lines=[]
            if request.method == 'GET':
                query1 = request.GET.get('query') 
                newgrade = request.GET.get('grade')      
                print("newgrade", newgrade)   #updating old status with new status
                if( newgrade =="A" ):
                    status="Accepted"
                elif(newgrade=="B" ):
                    status="Accepted"
                elif (newgrade=="C" ):
                    status="Rejected"
                elif (newgrade=="D" ):
                    status="Rejected"
                elif (newgrade=="F" ):
                    status="Rejected"    
                elif(newgrade=="Not Detected"):
                    status="Not Detected" 
                else:
                      status="Not Scanned"                            
                
                if (query1 ==""):
                    return render(request, 'Rescan.html', {"qs":qs,"updatestatus":0})                      
                try:
                    obj = ServerScannerdata.objects.get(id=id)
                    detailObj=ServerScannerdata.objects.filter(id=id).update(status=status,gradevalue=newgrade)
                    
                    
                    
                    sl=obj.serialnumber
                   
                    if(newgrade=="A" or newgrade=="B" ):
                        try:                    
                            with open("NotScannedjson/"+lot+".csv", 'r') as readFile:
                                reader = csv.reader(readFile)
                                for row in reader:
                                    lines.append(row)
                                    for field in row:
                                                            # print(field)                    
                                        if field == sl:
                                            lines.remove(row)
                                            print("deleted")
                            with open("NotScannedjson/"+lot+".csv", 'w',newline='') as writeFile:
                                writer = csv.writer(writeFile)
                                writer.writerows(lines)                
                            with open("Acceptedjson/"+lot+".csv", 'a', newline='\n') as file:
                                      
                                            writer = csv.writer(file)
                                   
                                            valuelist = [sl,newgrade,"Accepted",lot,gtin],
                                            writer.writerows(valuelist)
                         
                        except:
                            print("File not Found")        
                    
                    elif(newgrade=="C" or newgrade=="D" or newgrade=="F"):
                        try:                    
                            with open("NotScannedjson/"+lot+".csv", 'r') as readFile:
                                reader = csv.reader(readFile)
                                for row in reader:
                                    lines.append(row)
                                    for field in row:
                                                            # print(field)                    
                                        if field == sl:
                                            lines.remove(row)
                                            print("deleted")
                            with open("NotScannedjson/"+lot+".csv", 'w',newline='') as writeFile:
                                writer = csv.writer(writeFile)
                                writer.writerows(lines)                       
                            with open("jsonfiles/"+lot+".csv", 'a', newline='\n') as file:
                                      
                                            writer = csv.writer(file)
                                   
                                            valuelist = [sl,newgrade,"Rejected",lot,gtin],
                                            writer.writerows(valuelist)  
                        except:
                            print("File not Found")  
                    elif(newgrade=="Not Detected"):
                        try:                    
                            with open("NotScannedjson/"+lot+".csv", 'r') as readFile:
                                reader = csv.reader(readFile)
                                for row in reader:
                                    lines.append(row)
                                    for field in row:
                                                            # print(field)                    
                                        if field == sl:
                                            lines.remove(row)
                            with open("Notdetectedjson/"+lot+".csv", 'a', newline='\n') as file:
                                      
                                            writer = csv.writer(file)
                                   
                                            valuelist = [sl,newgrade,"Not Detected",lot,gtin],
                                            writer.writerows(valuelist)     
                        except:
                            print("File not Found")   
                                   
                    else:
                       print ("not challenged") 
                   
                    try:
                        conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")                    
                        obj = ServerScannerdata.objects.get(id=id)
                        detailObj=ServerScannerdata.objects.filter(id=id).update(gradevalue=newgrade,)
                        
                        jobs1 = ServerScannerdata.objects.filter(lot=lot,status="Rejected")
                        rejectedcount=len(jobs1)
                        scObj7=ProdReport.objects.filter(batch_number=lot).update(rejectedbycamera=rejectedcount)
                        
                        jobs2 = ServerScannerdata.objects.filter(lot=lot,status="challenged")
                        challengedcount=len(jobs2)
                        print(challengedcount)
                        scObj7=ProdReport.objects.filter(batch_number=lot).update(challenged=challengedcount)
                        
                        jobs3 = ServerScannerdata.objects.filter(lot=lot,status="Accepted")
                        acceptedcount=len(jobs3)
                        print(acceptedcount)
                        scObj7=ProdReport.objects.filter(batch_number=lot).update(accepted=acceptedcount)
                        
                        
                        
                        
                    except:
                        print("grade not update") 
                    
                     
                     
                            
                                   
                    else:
                       print ("not challenged" )                     
                except:
                    print("query not update")    
              
                    
                                        
            
                        
                return render(request, 'Rescan.html', {"qs":qs,"updatestatus":1,"grade":newgrade,"newstatus":status})               
            else:
                return redirect("signin")
            
def NotScansearchBar(request):   #searchbar in scanner page 
                    
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
                    query = request.GET.get('query')
                    # print(query)
                    if query:
                       
                        jobs = ServerScannerdata.objects.filter(lot=query,status="Not Scanned") 
                        # if(jobs):
                            #  jobs = ScannerTable.objects.exclude(status="NO")                   
                        return render(request, 'notscanned-list.html', {'page_obj':jobs,'search':1,'name':loginname})
                    else:
                        print("No information to show")
                        return render(request, 'notscanned-list.html', {})
            else:
                return redirect("signin")
# ..................................................................................
class StopBatchView(View):
                      
    def get(self,request,id):  
       
        qs=Printerdata.objects.get(id=id)
        po=qs.processordernumber
        intid=qs.id
        rows=[intid]
        if qs.load_button_resp==0:   
          os.system('start D:\Omron\AutoVision\AutoVISION.exe') 
        try:
                   
            with open("jobid.csv", 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                          
                csvwriter.writerow(rows)
            with open('jobid.csv', mode='r') as file:
                csvreader = csv.reader(file)
                for row in csvreader:
                    m=(row[0])
        except:
            print("job.csv file not found") 
            
        try:
                   
            with open("data.csv", 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                            # csvwriter.writerow(fields)
                csvwriter.writerow(rows)
            with open('data.csv', mode='r') as file:
                csvreader = csv.reader(file)
                for row in csvreader:
                    m=(row[0])
               
        except:
            print("data.csv file not found")    
                                                       
           
        return render(request,"Stop-Batch.html",{"qs":qs,"po":po}) 

    def post(self,request,id):
                         
                qs=Printerdata.objects.get(id=id)
                form=PrinterForm(request.POST,instance=qs)
                form2=PrinterForm(request.POST,instance=qs)
                id=qs.id    
                gtin=qs.gtin 
                ponumber=qs.processordernumber
                expire =str(qs.expiration_date)
                lot=qs.lot
                type=qs.type
                hrf=qs.hrf 
                printednumbers=qs.printed_numbers
                ip_address=qs.ip_address
                child_numbers=qs.child_numbers
                po=qs.processordernumber
                # prodObj=ProductionOrder.objects.get(gtin_number=qs.gtin)
                # po=prodObj.process_order_number 
                Begindatestring = date.today() 
        
                t = time.localtime()

                # Format the time as a string
                current_time = time.strftime("%H:%M:%S", t)
                
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
                    print(systemip)
                    return redirect("ip-error",ip=systemip)
                try: 
                    if(type=="type2"):
                        hrfkey="null"                   
                        hrfvalue="null"                  
                    # print(printednumbers) 
                    else:
                                                
                        hrfjson=json.loads(hrf) 
                        hrf1value=hrfjson["hrf1value"]
                        hrf1key=hrfjson["hrf1"]
                        hrf2value=hrfjson["hrf2value"]
                        hrf2key=hrfjson["hrf2"]
                        hrf3value=hrfjson["hrf3value"]
                        hrf3key=hrfjson["hrf3"]
                        hrf4value=hrfjson["hrf4value"]
                        hrf4key=hrfjson["hrf4"]
                        hrf5key=hrfjson["hrf5"]
                        hrf5value=hrfjson["hrf5value"]
                        hrf6key=hrfjson["hrf6"]
                        hrf6value=hrfjson["hrf6value"]
                        
                
                        if(hrf1key!="" or hrf1key!="null"):
                            hrfkey=hrf1key
                        elif(hrf2key!="" or hrf2key!="null"):
                            hrfkey=hrf2key
                        elif(hrf3key!="" or hrf3key!="null"):
                            hrfkey=hrf3key
                        elif(hrf4key!="" or hrf4key!="null"):
                            hrfkey=hrf4key
                        elif(hrf5key!="" or hrf5key!="null"):
                            hrfkey=hrf5key
                        elif(hrf6key!="" or hrf6key!="null"):
                            hrfkey=hrf6key
                        
                    
                        if(hrf1value!="" or hrf1value!="null"):
                            hrfvalue=hrf1value
                        elif(hrf2value!="" or hrf2value!="null"):
                            hrfvalue=hrf2value
                        elif(hrf3value!="" or hrf3value!="null"):
                            hrfvalue=hrf3value
                        elif(hrf4value!="" or hrf4value!="null"):
                            hrfvalue=hrf4value
                        elif(hrf5value!="" or hrf5value!="null"):
                            hrfvalue=hrf5value
                        elif(hrf6value!="" or hrf6value!="null"):
                            hrfvalue=hrf6value
                except:
                    print("no hrf")        
            
                # print(hrfkey)
                # print(hrfvalue)
                try:    
                    serial=qs.numbers
                    serialnum=qs.numbers
                    serialno=json.loads(serial)
                    sl=json.loads(serialnum)
                except:
                    print("No serialnumber available in viewprinterview")
                    serialno=[]    
                
                try:
                    scanner_socket = socket.socket()
                    scanner_socket.settimeout(2)  
                    scanner_port=2001
                    scanner_socket.connect(('192.168.200.134', scanner_port))
                except socket.timeout:
                    # return redirect("scanner-message") 
                    # obj = Printerdata.objects.get(id=id)
                    # detailObj=Printerdata.objects.filter(lot=obj.lot).update(preparebuttonresponse=0)
                                        
                    return render(request, 'Stop-Batch.html', {'qs': qs,'errormess':"data52ex","po":po,"alert":0}) 
                           
                try:
                    printer_socket = socket.socket()
                    printer_port=34567
                    printer_socket.settimeout(1)  
                    printer_socket.connect(('192.168.200.150', printer_port))
                    
                    message52= "K7\x04"   #cartridge expiration alert
                    printer_socket.send(message52.encode()) 
                    cartridge_expiration=printer_socket.recv(1024).decode() 
                    cartridge_expiration_data=cartridge_expiration[:-1]
                    if(qs.start_button_resp == 0):
                        print("printer paused")
                    else:
                                        
                        return render(request, 'Stop-Batch.html', {'qs': qs,'yu':0,'errormess':"cartridge_expiration_data","po":po,"loadpausealert":1}) 
                     
                    
                       
                    time.sleep(7)
                      
                    try:
                        oh=9
                        
                        try:
                                       
                            printer_socket_3 = socket.socket()
                            printer_port_3=34567
                            printer_socket_3.connect(('192.168.200.150', printer_port_3)) 
                                        
                                        
                                        
                                         
                                        
                            print("Batch stop But Not update")
                                        
                            printer_stop_command= "F0\x04"
                            printer_socket_3.send(printer_stop_command.encode()) 
                            stop_command_response=printer_socket_3.recv(1024).decode()
                                       
                        except:
                                      
                            print("Printer connection losted but Batch stop successfully")  
                            
                        if(serialno==[]):
                            # print("444444444444")
                            obj = Printerdata.objects.get(id=id)
                            detailObj=Printerdata.objects.filter(lot=obj.lot).update(stop_button_resp=1,return_button_resp=0,status="Printing Finished")                  
                                       
                                        
                        else:
                            obj = Printerdata.objects.get(id=id)
                            detailObj=Printerdata.objects.filter(lot=obj.lot).update(stop_button_resp=1,status="Stopped")
                                         
                        detailsObj1 = Printerdata.objects.get(id=id)  
                                           
                        obj = Printerdata.objects.get(id=id)
                        detailObj=Printerdata.objects.filter(lot=obj.lot).update(load_button_resp=0,stop_button_resp=1,return_button_resp=0) 
                        Line_historysave=ServerHistory(modelname='PrinterdataTable',
                                            savedid="noid",
                                            operationdone='Batch Stoped',
                                            donebyuser=loginname,
                                            donebyuserrole=loginuserrole, 
                                            description="Stopped the batch "+ lot +" "+"by"+" "+ loginname,
                                            donedatetime=datetime.datetime.now())
                        Line_historysave.save() 
                        try:
                                conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")                    
                                historysave=History(modelname='PrinterdataTable',
                                            savedid="noid",
                                            operationdone='Batch Stoped',
                                            donebyuser=loginname,
                                            donebyuserrole=loginuserrole, 
                                            description="Stopped the batch "+ lot +" "+"by"+" "+ loginname,
                                            donedatetime=datetime.datetime.now())
                                historysave.save()
                        except:
                                Local_historysave=LocalseverHistory(modelname='PrinterdataTable',
                                            savedid="noid",
                                            operationdone='Batch Stoped',
                                            donebyuser=loginname,
                                            donebyuserrole=loginuserrole, 
                                            description="Stopped the batch "+ lot +" "+"by"+" "+ loginname,
                                            donedatetime=datetime.datetime.now())
                                Local_historysave.save()   
                                        
                        y=[]
                        y1=[]
                        try:          
                                        file = "jobid.csv"
                                        
                                        if(os.path.exists(file) and os.path.isfile(file)): 
                                            os.remove(file) 
                                            print("file deleted") 
                                        else: 
                                            print("file not found")     
                        except:
                                    print("No Such csv File for deleteing")
                        try: 
                                      conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")                          
                                      scObj7=ProdReport.objects.filter(batch_number=lot).update(acceptedcount=0,damagedcount=0,rejectedbycameracount=0,challengedcount=0,current_production_date=Begindatestring,current_production_time=current_time)
                        except:
                                    print("pro Report Not Update because server connection losted")
                        scOb45=Inproperly_Closed.objects.filter(id=1).update(close_update=0)      
                        return redirect("batch-stop-message")
                           
                      
                    except:
                            
                            return render(request, 'Stop-Batch.html', {'loadstopvariable':1,'qs': qs,'yu':0,'errormess':cartridge_expiration_data,"po":po,"alert":3})             
                    
                    
                except socket.timeout:
                    
                    print("An exception occurred true")
                    
                   
                                               
                    return render(request, 'Stop-Batch.html', {'qs': qs,'yu':0,'errormess':"cartridge_expiration_data","po":po,"alert":1})   
                      
    
class LoadBatchView(View):
                      
    def get(self,request,id):  
       
        qs=Printerdata.objects.get(id=id)
        po=qs.processordernumber
        intid=qs.id
        rows=[intid]
        if qs.load_button_resp==0:   
          os.system('start D:\Omron\AutoVision\AutoVISION.exe') 
        try:
                   
            with open("jobid.csv", 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                          
                csvwriter.writerow(rows)
            with open('jobid.csv', mode='r') as file:
                csvreader = csv.reader(file)
                for row in csvreader:
                    m=(row[0])
        except:
            print("job.csv file not found") 
            
        try:
                   
            with open("data.csv", 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                            # csvwriter.writerow(fields)
                csvwriter.writerow(rows)
            with open('data.csv', mode='r') as file:
                csvreader = csv.reader(file)
                for row in csvreader:
                    m=(row[0])
               
        except:
            print("data.csv file not found")     
                                  
           
        return render(request,"Load-Batch.html",{"qs":qs,"po":po})    
    
    def printerfun(self,num,serialno,q,event,gtin,lot,expire,hrfkey,hrfvalue,type,id):   #load everything in the starting ...in program load batch button is working here
        self.serialno=serialno
        self.gtin=gtin
        self.expire=expire
        self.lot=lot
    
                                
        self.hrfkey=hrfkey
        self.hrfvalue=hrfvalue
        self.type=type 
        self.id=id
                    
        printer_socket_4 = socket.socket()
        printer_port_4=34567
        printer_socket_4.connect(('192.168.200.150', printer_port_4))

        if(type=="type2"):
                                
                    printer_load_command= "L,new7.lbl\x04"
                    printer_socket_4.send(printer_load_command.encode()) 
                    load_response=printer_socket_4.recv(1024).decode()
                      
                    printer_prepare_command= "E\x04"        
                    printer_socket_4.send(printer_prepare_command.encode()) 
                    prepare_response=printer_socket_4.recv(1024).decode()
                    uy1=serialno[0:1]
                    
                    for sn in uy1:                
                 
                                   printer_field_send_command= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x04"
                                   printer_socket_4.send(printer_field_send_command.encode()) 
                                   field_response=printer_socket_4.recv(1024).decode()
                                                
                                   printer_value_send_command= "QAC\x09"+"(17)"+expire+"(10)"+lot + "(01)" +  gtin + "(21)" + sn +  "\x09" + "Exp\x09" + expire + "\x09Lot" + "\x09" + lot + "\x09" + "Gtin\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"
                                   printer_socket_4.send(printer_value_send_command.encode()) 
                                   value_response=printer_socket_4.recv(1024).decode() 
                                          
                                   printer_start_command= "F2\x04"
                                   printer_socket_4.send(printer_start_command.encode()) 
                                   start_response=printer_socket_4.recv(1024).decode()
                     
                    print('Received from server: ' + field_response)
                    print('Received from server: ' + value_response)         
                    print('Received from server: ' + start_response)
           
        elif(type=="type5"):
                     printer_load_command_1= "L,new8.lbl\x04"
                     printer_socket_4.send(printer_load_command_1.encode()) 
                     load_response_1=printer_socket_4.recv(1024).decode()  
                     
                     printer_prepare_command_1= "E\x04"        
                     printer_socket_4.send(printer_prepare_command_1.encode()) 
                     prepare_response_1=printer_socket_4.recv(1024).decode()
                     
                     uy2=serialno[0:1]     
                     for sn in uy2: 
                        printer_field_send_command_1= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x09"+"hrf"+"\x09hrfvalue"+"\x04"
                        printer_socket_4.send(printer_field_send_command_1.encode()) 
                        field_response_1=printer_socket_4.recv(1024).decode()
                                                   
                                   # message6= "QAC\x09" + "55555777779(10)45612(21)\x09GTIN\x09" + gtin+"\x09"+ "lot\x09" + lot +"\x09" +"exp\x09" + expire+"\x09"+"serialno\x09"+sn+"\x04"
                        printer_value_send_command_1= "QAC\x09" + "(17)" + expire + "(10)" + lot + "(01)" +  gtin + "(21)" + sn + "(45)"+ hrfvalue+ "\x09" + "Exp\x09" + expire + "\x09"+"Lot" + "\x09" + lot + "\x09" + "Gtin"+ "\x09" +  gtin + "\x09" + "Slno" + "\x09" + sn + "\x09" + hrfkey + "\x09" + hrfvalue + "\x04"
                        printer_socket_4.send(printer_value_send_command_1.encode()) 
                        value_response_1=printer_socket_4.recv(1024).decode() 
                                          
                        printer_start_command_1= "F2\x04"
                        printer_socket_4.send(printer_start_command_1.encode()) 
                        start_response_1=printer_socket_4.recv(1024).decode()
                                        
                     print('Received from server: ' + load_response_1)
                     print('Received from server: ' + prepare_response_1) 
                     print('Received from server: ' + field_response_1)
                     print('Received from server: ' + value_response_1)         
                     print('Received from server: ' + start_response_1)
                  
        elif(type=="type1"):
                     printer_load_command_2= "L,new5.lbl\x04"
                     printer_socket_4.send(printer_load_command_2.encode()) 
                     load_response_2=printer_socket_4.recv(1024).decode()  
                     
                     printer_prepare_command_2= "E\x04"        
                     printer_socket_4.send(printer_prepare_command_2.encode()) 
                     prepare_response_2=printer_socket_4.recv(1024).decode()
                     
                     uy=serialno[0:1] 
                                   
                     for sn in uy:
                                   printer_field_send_command_2= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x04"
                                   printer_socket_4.send(printer_field_send_command_2.encode()) 
                                   field_response_2=printer_socket_4.recv(1024).decode()
                                                  
                                   # message6= "QAC\x09" + "55555777779(10)45612(21)\x09GTIN\x09" + gtin+"\x09"+ "lot\x09" + lot +"\x09" +"exp\x09" + expire+"\x09"+"serialno\x09"+sn+"\x04"
                                   printer_value_send_command_2= "QAC\x09" + "(17)" + expire + "(10)" + lot + "(01)" +  gtin + "(21)" + sn +"(45)"+ hrfvalue +  "\x09" + "Exp\x09" + expire + "\x09Lot" + "\x09" + lot + "\x09" + "GTIN\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"
                                   printer_socket_4.send(printer_value_send_command_2.encode()) 
                                   value_response_2=printer_socket_4.recv(1024).decode() 
                                          
                                   printer_start_command_2= "F2\x04"
                                   printer_socket_4.send(printer_start_command_2.encode()) 
                                   start_response_2=printer_socket_4.recv(1024).decode()
       
                     print('Received from server: ' + field_response_2)
                     print('Received from server: ' + value_response_2)         
                     print('Received from server: ' + start_response_2)
    def scannerfun(self,num,id,gtin,serialno,sl,printednumbers,q,event,lot,expire,hrfkey,hrfvalue,ip_address,child_numbers,type):
        self.id=id                    
        self.serialno=serialno
        self.sl=sl
        self.printednumbers=printednumbers
        self.gtin=gtin
        self.lot=lot
        self.expire=expire
        self.hrfkey=hrfkey
        self.hrfvalue=hrfvalue
        self.ip_address=ip_address
        self.child_numbers=child_numbers 
        self.type= type                
        counter=0
        d=0
        co=-1
        n=1
        # s3 = socket.socket()
       
        # printer_socket_1 = socket.socket()
        # printer_port_1=34567
        
        # printer_socket_1.connect(('192.168.200.150',printer_port_1))   #connecting the printer to 34567 port
        
        Begindatestring = date.today() 
        # print(Begindatestring)
        t = time.localtime()

        # Format the time as a string
        current_time = time.strftime("%H:%M:%S", t)
        # print(current_time)
          
        obj = Printerdata.objects.get(id=id)
        detailObj=Printerdata.objects.filter(lot=obj.lot)
      
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
            print(systemip)
            return redirect("ip-error",ip=systemip)
            # return render(request, 'Ip-error.html', {'ip': systemip,'inside_message':1})
                                        
        sllen=len(sl)
        # print("sllen count")
        # print(sllen)
        upjso=[]
        cd=0
        drg=[] 
        rejectednumberslist=[]
        Acceptednumberslist=[]
        
        Notdetectedlist=[]
        childnumberslist=[]
        
                 
        Line_historysave=ServerHistory( modelname='PrinterdataTable',
                                        savedid="noid",
                                        operationdone='Batch Loaded',
                                        donebyuser=loginname,
                                        donebyuserrole=loginuserrole, 
                                        description="Loaded the batch of  "+ lot +" "+"by"+" "+ loginname,
                                        donedatetime=datetime.datetime.now())
        Line_historysave.save() 
        try:
            conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")                    
            historysave=History(modelname='PrinterdataTable',
                                savedid="noid",
                                operationdone='Batch Loaded',
                                donebyuser=loginname,
                                donebyuserrole=loginuserrole, 
                                description="Loaded the batch of  "+ lot +" "+"by"+" "+ loginname,
                                donedatetime=datetime.datetime.now())
            historysave.save()
            print("history for load batch saved")
        except:
            Local_historysave=LocalseverHistory(modelname='PrinterdataTable',
                                savedid="noid",
                                operationdone='Batch Loaded',
                                donebyuser=loginname,
                                donebyuserrole=loginuserrole, 
                                description="Loaded the batch of  "+ lot +" "+"by"+" "+ loginname,
                                donedatetime=datetime.datetime.now())
            Local_historysave.save()
   
        while True:
                    qs = Printerdata.objects.get(id=id)
                  
                   
                    if(qs.stop_button_resp == 1):
                        print("Load page Breaked")                    
                                          
                        break  
                    
                    # try:
                    #     printer_socket_2 = socket.socket()
                    #     printer_port_2=34567
                    #     printer_socket_2.settimeout(0.5)
                    #     printer_socket_2.connect(('192.168.200.150', printer_port_2))
                    # except:
                    #     print("printer conn lost detected in scanerfun")
                        
                    #     try:
                    #         scn_conn = socket.socket()
                    #         scn_conn_port_1=2001
                    #         # scanner_socket_1.settimeout(1)  
                    #         scn_conn.connect(('192.168.200.134', scn_conn_port_1))
                    #         scanner_decode_data=scn_conn.recv(1024).decode()
                    #         qs = Printerdata.objects.get(id=id)
                                    
                                
                                    
                                                                    
                                                        
                    #         print("printer connection lost except is working")            
                    #         if(type=="type2"):
                    #                     try:                    
                    #                         decoded_grade=scanner_decode_data[0] 
                    #                         confidence=scanner_decode_data[1] 
                    #                         decoded_gtin=scanner_decode_data[11:25]
                    #                         meanconfidence=scanner_decode_data[2:7]
                    #                         scanned_serial_number=scanner_decode_data[29:38]
                    #                     except:
                    #                         print("data didnot decode in scannerfunn")
                    #                 # print(meanconfidence)
                    #         elif(type== "type1" or type== "type5"):
                    #                     try:                    
                    #                         decoded_grade=scanner_decode_data[0]
                    #                         confidence=scanner_decode_data[1]
                    #                         decoded_gtin=scanner_decode_data[9:23]
                    #                         meanconfidence=scanner_decode_data[2:7]
                    #                         scanned_serial_number=scanner_decode_data[25:34]
                    #                     except:
                    #                         print("data didnot decode in scannerfunn")   
                                    
                    #                     # print(textbatch)  
                    #                     # print(meanconfidence)                                     
                    #                 # if d==1:
                    #         try:
                    #             upjso.append(sl[counter])
                    #         except:
                    #             print("No serialnumbers available for printing")   
                    #         serilength=len(serialno)
                                    
                    #         try:
                    #                         # if(v=="4" and confidence=="1" and meanconfidence>="0.800"):
                    #                         #             grade="A"
                    #                         # elif(v=="3" and confidence=="1" and meanconfidence>="0.800"):
                    #                         #             grade="B"
                    #                         # elif (v=="2" and confidence=="1" and meanconfidence>="0.800"):
                    #                         #             grade="C"
                    #                         # elif (v=="1" and confidence=="1" and meanconfidence>="0.800"):
                    #                         #             grade="D"
                    #                         # else:
                    #                         #             grade="F" 
                    #                         if(decoded_grade=="4" ):
                    #                                     grade="A"
                    #                         elif(decoded_grade=="3" ):
                    #                                     grade="B"
                    #                         elif (decoded_grade=="2" ):
                    #                                     grade="C"
                    #                         elif (decoded_grade=="1" ):
                    #                                     grade="D"
                    #                         else:
                    #                                     grade="F" 
                                                    
                    #                         r={"serialnumber":sl[counter],
                    #                                     "grade":grade}
                    #                         print("1111111111111111111111")
                    #                         if(scanned_serial_number==sl[counter] and gtin==decoded_gtin):
                    #                             # if(scanned_serial_number==sl[counter]):                    
                    #                                 if(decoded_grade=="4" or decoded_grade=="3"):                
                    #                                     print(r)
                    #                                     b=json.dumps(r)
                    #                                     gradeupdation=Scannerdata(
                    #                                     gtin=gtin,
                    #                                     ip_address=ip_address,
                    #                                     grade=b,
                    #                                     status="Accepted",
                    #                                     serialnumber=sl[counter],
                    #                                     gradevalue=grade,
                    #                                     lot=lot,
                    #                                     type=type
                    #                                     )
                    #                                     gradeupdation.save()
                    #                                     obj = Printerdata.objects.get(id=id)
                    #                                     # print(obj.lot)
                    #                                     detailObj=Printerdata.objects.filter(lot=obj.lot).update(scannergradefield=b)
                    #                                     jso=json.dumps(upjso)
                    #                                     serialvar3=sl[counter]
                    #                                     serialno.remove(sl[counter])
                    #                                     gh=json.dumps(serialno)
                    #                                     print(sl[counter])
                    #                                     obj = Printerdata.objects.get(id=id)
                    #                                     detailObj=Printerdata.objects.filter(lot=obj.lot).update(printed_numbers=jso,numbers=gh)
                                                    
                    #                                     with open("Acceptedjson/"+lot+".csv", 'a', newline='') as file:
                                                    
                    #                                         writer = csv.writer(file)
                                                
                    #                                         valuelist = [serialvar3,grade,"Accepted",lot,gtin],
                                                        
                    #                                         writer.writerows(valuelist)
                    #                                     # updatedjson=json.loads(jso)
                                                    
                    #                                     df = pd.read_csv("Acceptedjson/"+lot+".csv")
                    #                                     row_count = len(df)
                    #                                     row_count1= row_count+1 
                                                        

                    #                                     print("Number of rows:", row_count1)
                    #                                     try:
                    #                                         conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1")
                                                            
                                                        
                                                            
                    #                                         jobs7 = Scannerdata.objects.filter(lot=lot,status="Accepted")
                    #                                         acceptedcount=len(jobs7)
                    #                                         scObj7=ProdReport.objects.filter(batch_number=lot).update(acceptedcount=acceptedcount,current_production_date=Begindatestring,current_production_time=current_time)
                    #                                         print(acceptedcount, 'is last in the list ✅')                
                                                        
                                                            
                    #                                     except:
                    #                                         print("server connection losted in between the process of reports data add to server") 
                    #                                     try:
                    #                                         scObj7=Printerdata.objects.filter(lot=lot).update(current_production_date=Begindatestring,current_production_time=current_time)
                    #                                         print( 'curent date time updated ✅')                    
                    #                                     except:
                    #                                         print("current time not update")       
                    #                                     if(counter==sllen-1):           #If the last number is detecting it will clear the serialno
                    #                                         print(serialno)                    
                    #                                         del serialno[:]
                    #                                         obj = Printerdata.objects.get(id=id)
                    #                                         detailObj=Printerdata.objects.filter(gtin=obj.gtin).update(numbers=serialno)                  
                    #                                         print("detect serialnumber cleared")     
                    #                                     counter=counter+1
                    #                                 else:    
                    #                                     print("grade less then B")
                    #                                     print(r)
                    #                                     b=json.dumps(r)
                    #                                     gradeupdation=Scannerdata(
                    #                                     gtin=gtin,
                    #                                     ip_address=ip_address,
                    #                                     grade=b,
                    #                                     status="Rejected",
                    #                                     serialnumber=sl[counter],
                    #                                     gradevalue=grade,
                    #                                     lot=lot,
                    #                                     type=type
                    #                                     )
                    #                                     gradeupdation.save()
                                                    
                                                        
                    #                                     obj = Printerdata.objects.get(id=id)
                    #                                     detailObj=Printerdata.objects.filter(lot=obj.lot).update(scannergradefield=b)
                    #                                     jso=json.dumps(upjso)
                    #                                     serialvar2=sl[counter]
                    #                                     serialno.remove(sl[counter])
                    #                                     gh=json.dumps(serialno)
                    #                                     print(sl[counter])
                    #                                     obj = Printerdata.objects.get(id=id)
                    #                                     detailObj=Printerdata.objects.filter(lot=obj.lot).update(printed_numbers=jso,numbers=gh)
                                                        
                                                        
                    #                                     with open("jsonfiles/"+lot+".csv", 'a', newline='') as file:
                                                    
                    #                                         writer = csv.writer(file)
                                                
                    #                                         valuelist = [serialvar2,grade,"Rejected",lot,gtin],
                    #                                         writer.writerows(valuelist)    
                    #                                     df1 = pd.read_csv("jsonfiles/"+lot+".csv")
                    #                                     row_count1 = len(df1)
                    #                                     row_count2= row_count1+1 

                    #                                     print("Number of rejected rows:", row_count2)
                    #                                     try:
                    #                                         conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1")
                                                        
                                                        
                                                            
                    #                                         jobs7 = Scannerdata.objects.filter(lot=lot,status="Rejected")
                    #                                         rejectedcount=len(jobs7)
                    #                                         scObj7=ProdReport.objects.filter(batch_number=lot).update(rejectedbycameracount=rejectedcount,current_production_date=Begindatestring,current_production_time=current_time)
                                                            
                    #                                         print(rejectedcount,'is last in the list ✅')
                                                                        
                                                        
                                                            
                                                        
                                                            
                    #                                     except:
                    #                                         print("server connection losted in between the process of reports data add to server")    
                    #                                     try:    
                    #                                         scObj7=Printerdata.objects.filter(lot=lot).update(current_production_date=Begindatestring,current_production_time=current_time)
                    #                                         print( 'curent date time updated ✅')     
                    #                                     except:
                    #                                         print("current time not updated")
                                                        
                    #                                     if(counter==sllen-1):           #If the last number is detecting it will clear the serialno
                    #                                         print(serialno)                    
                    #                                         del serialno[:]
                    #                                         obj = Printerdata.objects.get(id=id)
                    #                                         detailObj=Printerdata.objects.filter(lot=obj.lot).update(numbers=serialno)                  
                    #                                         print("detect serialnumber cleared")
                    #                                     counter=counter+1
                    #                             # else: 
                    #                             #    print("serialnumber not equal")
                    #                             #    counter=counter+1 
                                                                
                    #                         else:
                    #                             print("else of after printer connection lost ") 
                    #                             if(qs.return_button_resp==0):
                    #                                 print("Serialnumber and gtin miss match so added to notdetected csv")
                    #                                 r={"serialnumber":sl[counter],
                    #                                         "grade":"Not Detected"}
                    #                                 print(r)
                    #                                 b=json.dumps(r)
                    #                                 gradeupdation=Scannerdata(
                    #                                 gtin=gtin,
                    #                                 ip_address=ip_address,
                    #                                 numbers=b,
                    #                                 status="Damaged",
                    #                                 serialnumber=sl[counter],
                    #                                 gradevalue="Not Detected",
                    #                                 lot=lot,
                    #                                 type=type
                    #                                 )
                    #                                 gradeupdation.save()
                    #                                 obj = Printerdata.objects.get(id=id)
                    #                                 detailObj=Printerdata.objects.filter(lot=obj.lot).update(scannergradefield=b)
                    #                                 jso=json.dumps(upjso)
                    #                                 serialvar1=sl[counter]
                    #                                 serialno.remove(sl[counter])
                    #                                 gh=json.dumps(serialno)
                    #                                 obj = Printerdata.objects.get(id=id)
                    #                                 detailObj=Printerdata.objects.filter(lot=obj.lot).update(numbers=gh)
                    #                                 try:
                    #                                     with open("Notdetectedjson/"+lot+".csv", 'a', newline='') as file:
                                                    
                    #                                         writer = csv.writer(file)
                                                
                    #                                         valuelist = [serialvar1,"Not Detected",gtin,lot],
                                                        
                    #                                         writer.writerows(valuelist)
                                                    
                    #                                 except:
                    #                                     print("No DATA AVAILABLE FOR ADDING TO CSV")
                    #                                 try:
                    #                                     conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1")                
                    #                                     jobs9 = Scannerdata.objects.filter(lot=lot,status="Damaged")
                    #                                     damagedcount=len(jobs9)
                    #                                     print(damagedcount)
                    #                                     scObj7=ProdReport.objects.filter(batch_number=lot).update(damagedcount=damagedcount,current_production_date=Begindatestring,current_production_time=current_time)
                    #                                 except:
                    #                                     print("database connection lost")
                                                        
                    #                                 try:
                    #                                     scObj7=Printerdata.objects.filter(lot=lot).update(current_production_date=Begindatestring,current_production_time=current_time)
                    #                                     print( 'curent date time updated ✅') 
                    #                                 except:
                    #                                     print("current time not update")
                    #                                 if(counter==sllen-1):     #if the last number is not detecting it will clear the serialno
                    #                                     print(serialno)                    
                    #                                     del serialno[:]
                    #                                     obj = Printerdata.objects.get(id=id)
                    #                                     detailObj=Printerdata.objects.filter(lot=obj.lot).update(numbers=serialno)
                    #                                     print("not detecte serialnumber cleared")                  
                    #                                 counter=counter+1
                    #                             else:
                    #                                 print("return buttn_resp == 1")                        
                                                        
                                            
                                                
                    #         except:
                    #             print("serialnumbers finished")
                                        
                    #     except:
                                                
                                                                    
                    #         print("Didn't receive  data! [Timeout 5s]")   
                                       
              
                    try: 
                        printer_socket_2 = socket.socket()
                        printer_port_2=34567
                        printer_socket_2.settimeout(2)
                        printer_socket_2.connect(('192.168.200.150', printer_port_2))
                        
                        belt_speed_command= "I5\x04"
                        printer_socket_2.send(belt_speed_command.encode()) 
                        belt=printer_socket_2.recv(1024).decode() 
                        # print("message931",belt[0:1])
                        belt_speed=belt[0:1]
                                           
                        read_output_command= "IE\x04"
                        printer_socket_2.send(read_output_command.encode()) 
                        read_output_data=printer_socket_2.recv(1024).decode()
                                                                            
                                            
                        data_to_string=str(read_output_data[0:1])
                        # print("viewprinterview loop working")
                        
                        
                                            
                        for c in data_to_string:
                            ascii_values_data_to_string=ord(c)
                       
                    except socket.timeout:
                        print("printer connection losted and detected in  scannerfunn") 
                        ascii_values_data_to_string=0 
                    # if(belt_speed == "0"):
                    #     print("00000000")
                    # else:
                    #     print("8888888888")  
                    # if(belt_speed=="0"):
                    #     if(ascii_values == 1): 
                    #         jso=json.dumps(upjso)
                    #         serialvar=sl[counter]
                    #         serialno.remove(sl[counter])
                    #         gh=json.dumps(serialno)
                    #         obj = Printerdata.objects.get(id=id)
                    #         detailObj=Printerdata.objects.filter(lot=obj.lot).update(numbers=gh)
                    #         try:
                    #             with open("Missingjson/"+lot+".csv", 'a', newline='') as file:
                                                        
                    #                 writer = csv.writer(file)
                                                    
                    #                 valuelist = [serialvar,"Missed",gtin,lot],
                                                            
                    #                 writer.writerows(valuelist)
                                                        
                    #         except:
                    #                 print("No DATA AVAILABLE FOR ADDING TO CSV") 
                    #         counter=counter-1   
                    
                                        
                                                     
                    if(ascii_values_data_to_string == 3 and belt_speed != "0") :
                                           
                            try:
                                scanner_socket_1 = socket.socket()
                                scanner_port_1=2001
                                # scanner_socket_1.settimeout(2)  
                                scanner_socket_1.connect(('192.168.200.134', scanner_port_1))  #connecting the scanner to 2001 port
                                
                                Begindatestring = date.today() 
      
                                t = time.localtime()

                                
                                current_time = time.strftime("%H:%M:%S", t)                    
                           
                                try:
                                    scanner_decode_data=scanner_socket_1.recv(1024).decode()
                                    print("normal condition,this is  data",scanner_decode_data)
                                    
                                    if(type=="type2"):
                                        try:                    
                                            decoded_grade=scanner_decode_data[0] 
                                            confidence=scanner_decode_data[1] 
                                            decoded_gtin=scanner_decode_data[11:25]
                                            meanconfidence=scanner_decode_data[2:7]
                                            scanned_serial_number=scanner_decode_data[29:38]
                                        except:
                                            print("data didnot decode in scannerfunn")
                                    # print(meanconfidence)
                                    elif(type== "type1" or type== "type5"):
                                        try:                    
                                            decoded_grade=scanner_decode_data[0]
                                            confidence=scanner_decode_data[1]
                                            decoded_gtin=scanner_decode_data[9:23]
                                            meanconfidence=scanner_decode_data[2:7]
                                            scanned_serial_number=scanner_decode_data[25:34]
                                        except:
                                            print("data didnot decode in scannerfunn")   
                                    
                                        # print(textbatch)  
                                        # print(meanconfidence)                                     
                                    # if d==1:
                                    try:
                                        upjso.append(sl[counter])
                                    except:
                                        print("No serialnumbers available for printing")   
                                    serilength=len(serialno)
                                    
                                    try:
                                            # if(v=="4" and confidence=="1" and meanconfidence>="0.800"):
                                            #             grade="A"
                                            # elif(v=="3" and confidence=="1" and meanconfidence>="0.800"):
                                            #             grade="B"
                                            # elif (v=="2" and confidence=="1" and meanconfidence>="0.800"):
                                            #             grade="C"
                                            # elif (v=="1" and confidence=="1" and meanconfidence>="0.800"):
                                            #             grade="D"
                                            # else:
                                            #             grade="F" 
                                            if(decoded_grade=="4" ):
                                                        grade="A"
                                            elif(decoded_grade=="3" ):
                                                        grade="B"
                                            elif (decoded_grade=="2" ):
                                                        grade="C"
                                            elif (decoded_grade=="1" ):
                                                        grade="D"
                                            else:
                                                        grade="F" 
                                                    
                                            r={"serialnumber":sl[counter],
                                                        "grade":grade}
                                            # print("333333333333333",r)
                                            if(scanned_serial_number==sl[counter] and gtin==decoded_gtin):
                                                # if(scanned_serial_number==sl[counter]):                    
                                                    if(decoded_grade=="4" or decoded_grade=="3"):                
                                                        print(r)
                                                        b=json.dumps(r)
                                                        gradeupdation=Scannerdata(
                                                        gtin=gtin,
                                                        ip_address=ip_address,
                                                        grade=b,
                                                        status="Accepted",
                                                        serialnumber=sl[counter],
                                                        gradevalue=grade,
                                                        lot=lot,
                                                        type=type
                                                        )
                                                        gradeupdation.save()
                                                        obj = Printerdata.objects.get(id=id)
                                                        # print(obj.lot)
                                                        detailObj=Printerdata.objects.filter(lot=obj.lot).update(scannergradefield=b)
                                                        jso=json.dumps(upjso)
                                                        serialvar3=sl[counter]
                                                        serialno.remove(sl[counter])
                                                        gh=json.dumps(serialno)
                                                        print(sl[counter])
                                                        obj = Printerdata.objects.get(id=id)
                                                        detailObj=Printerdata.objects.filter(lot=obj.lot).update(printed_numbers=jso,numbers=gh)
                                                    
                                                        with open("Acceptedjson/"+lot+".csv", 'a', newline='') as file:
                                                    
                                                            writer = csv.writer(file)
                                                
                                                            valuelist = [serialvar3,grade,"Accepted",lot,gtin],
                                                        
                                                            writer.writerows(valuelist)
                                                        # updatedjson=json.loads(jso)
                                                    
                                                        df = pd.read_csv("Acceptedjson/"+lot+".csv")
                                                        row_count = len(df)
                                                        row_count1= row_count+1 
                                                        

                                                        print("Number of rows:", row_count1)
                                                        try:
                                                            conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1")
                                                            
                                                        
                                                            
                                                            jobs7 = Scannerdata.objects.filter(lot=lot,status="Accepted")
                                                            acceptedcount=len(jobs7)
                                                            scObj7=ProdReport.objects.filter(batch_number=lot).update(acceptedcount=acceptedcount,current_production_date=Begindatestring,current_production_time=current_time)
                                                            print(acceptedcount, 'is last in the list ✅')                
                                                        
                                                            
                                                        except:
                                                            print("server connection losted in between the process of reports data add to server") 
                                                        try:
                                                            scObj7=Printerdata.objects.filter(lot=lot).update(current_production_date=Begindatestring,current_production_time=current_time)
                                                            print( 'curent date time updated ✅')                    
                                                        except:
                                                            print("current time not update")       
                                                        if(counter==sllen-1):           #If the last number is detecting it will clear the serialno
                                                            print(serialno)                    
                                                            del serialno[:]
                                                            obj = Printerdata.objects.get(id=id)
                                                            detailObj=Printerdata.objects.filter(gtin=obj.gtin).update(numbers=serialno)                  
                                                            print("detect serialnumber cleared")     
                                                        counter=counter+1
                                                    else:    
                                                        print("grade less then B")
                                                        print(r)
                                                        b=json.dumps(r)
                                                        gradeupdation=Scannerdata(
                                                        gtin=gtin,
                                                        ip_address=ip_address,
                                                        grade=b,
                                                        status="Rejected",
                                                        serialnumber=sl[counter],
                                                        gradevalue=grade,
                                                        lot=lot,
                                                        type=type
                                                        )
                                                        gradeupdation.save()
                                                    
                                                        
                                                        obj = Printerdata.objects.get(id=id)
                                                        detailObj=Printerdata.objects.filter(lot=obj.lot).update(scannergradefield=b)
                                                        jso=json.dumps(upjso)
                                                        serialvar2=sl[counter]
                                                        serialno.remove(sl[counter])
                                                        gh=json.dumps(serialno)
                                                        print(sl[counter])
                                                        obj = Printerdata.objects.get(id=id)
                                                        detailObj=Printerdata.objects.filter(lot=obj.lot).update(printed_numbers=jso,numbers=gh)
                                                        
                                                        
                                                        with open("jsonfiles/"+lot+".csv", 'a', newline='') as file:
                                                    
                                                            writer = csv.writer(file)
                                                
                                                            valuelist = [serialvar2,grade,"Rejected",lot,gtin],
                                                            writer.writerows(valuelist)    
                                                        df1 = pd.read_csv("jsonfiles/"+lot+".csv")
                                                        row_count1 = len(df1)
                                                        row_count2= row_count1+1 

                                                        print("Number of rejected rows:", row_count2)
                                                        try:
                                                            conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1")
                                                        
                                                        
                                                            
                                                            jobs7 = Scannerdata.objects.filter(lot=lot,status="Rejected")
                                                            rejectedcount=len(jobs7)
                                                            scObj7=ProdReport.objects.filter(batch_number=lot).update(rejectedbycameracount=rejectedcount,current_production_date=Begindatestring,current_production_time=current_time)
                                                            
                                                            print(rejectedcount,'is last in the list ✅')
                                                                        
                                                        
                                                            
                                                        
                                                            
                                                        except:
                                                            print("server connection losted in between the process of reports data add to server")    
                                                        try:    
                                                            scObj7=Printerdata.objects.filter(lot=lot).update(current_production_date=Begindatestring,current_production_time=current_time)
                                                            print( 'curent date time updated ✅')     
                                                        except:
                                                            print("current time not updated")
                                                        
                                                        if(counter==sllen-1):           #If the last number is detecting it will clear the serialno
                                                            print(serialno)                    
                                                            del serialno[:]
                                                            obj = Printerdata.objects.get(id=id)
                                                            detailObj=Printerdata.objects.filter(lot=obj.lot).update(numbers=serialno)                  
                                                            print("detect serialnumber cleared")
                                                        counter=counter+1
                                                # else: 
                                                #    print("serialnumber not equal")
                                                #    counter=counter+1 
                                                                
                                            else:
                                                print("else of notdetected") 
                                                print("Serialnumber and gtin miss match so added to notdetected csv")
                                                r={"serialnumber":sl[counter],
                                                        "grade":"Not Detected"}
                                                print(r)
                                                b=json.dumps(r)
                                                gradeupdation=Scannerdata(
                                                gtin=gtin,
                                                ip_address=ip_address,
                                                numbers=b,
                                                status="Damaged",
                                                serialnumber=sl[counter],
                                                gradevalue="Not Detected",
                                                lot=lot,
                                                type=type
                                                )
                                                gradeupdation.save()
                                                obj = Printerdata.objects.get(id=id)
                                                detailObj=Printerdata.objects.filter(lot=obj.lot).update(scannergradefield=b)
                                                jso=json.dumps(upjso)
                                                serialvar1=sl[counter]
                                                serialno.remove(sl[counter])
                                                gh=json.dumps(serialno)
                                                obj = Printerdata.objects.get(id=id)
                                                detailObj=Printerdata.objects.filter(lot=obj.lot).update(numbers=gh)
                                                try:
                                                    with open("Notdetectedjson/"+lot+".csv", 'a', newline='') as file:
                                                
                                                        writer = csv.writer(file)
                                            
                                                        valuelist = [serialvar1,"Not Detected",gtin,lot],
                                                    
                                                        writer.writerows(valuelist)
                                                
                                                except:
                                                    print("No DATA AVAILABLE FOR ADDING TO CSV")
                                                try:
                                                    conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1")                
                                                    jobs9 = Scannerdata.objects.filter(lot=lot,status="Damaged")
                                                    damagedcount=len(jobs9)
                                                    print(damagedcount)
                                                    scObj7=ProdReport.objects.filter(batch_number=lot).update(damagedcount=damagedcount,current_production_date=Begindatestring,current_production_time=current_time)
                                                except:
                                                    print("database connection lost")
                                                    
                                                try:
                                                    scObj7=Printerdata.objects.filter(lot=lot).update(current_production_date=Begindatestring,current_production_time=current_time)
                                                    print( 'curent date time updated ✅') 
                                                except:
                                                    print("current time not update")
                                                if(counter==sllen-1):     #if the last number is not detecting it will clear the serialno
                                                    print(serialno)                    
                                                    del serialno[:]
                                                    obj = Printerdata.objects.get(id=id)
                                                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(numbers=serialno)
                                                    print("not detecte serialnumber cleared")                  
                                                counter=counter+1
                                                    
                                            
                                                
                                    except:
                                            print("serialnumbers finished")
                                        
                                except:
                                            print("data did not decode so except condition added data to not detected csv")
                                            print("not equal")
                                            r={"serialnumber":sl[counter],
                                                    "grade":"Not Detected"}
                                            print(r)
                                            b=json.dumps(r)
                                            gradeupdation=Scannerdata(
                                            gtin=gtin,
                                            ip_address=ip_address,
                                            numbers=b,
                                            status="Damaged",
                                            serialnumber=sl[counter],
                                            gradevalue="Not Detected",
                                            lot=lot,
                                            type=type
                                            )
                                            gradeupdation.save()
                                            obj = Printerdata.objects.get(id=id)
                                            detailObj=Printerdata.objects.filter(lot=obj.lot).update(scannergradefield=b)
                                            jso=json.dumps(upjso)
                                            serialvar1=sl[counter]
                                            serialno.remove(sl[counter])
                                            gh=json.dumps(serialno)
                                            obj = Printerdata.objects.get(id=id)
                                            detailObj=Printerdata.objects.filter(lot=obj.lot).update(numbers=gh)
                                            try:
                                                with open("Notdetectedjson/"+lot+".csv", 'a', newline='') as file:
                                            
                                                    writer = csv.writer(file)
                                        
                                                    valuelist = [serialvar1,"Not Detected",gtin,lot],
                                                
                                                    writer.writerows(valuelist)
                                            
                                            except:
                                                print("No DATA AVAILABLE FOR ADDING TO CSV")
                                            try:
                                                conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1")                
                                                jobs9 = Scannerdata.objects.filter(lot=lot,status="Damaged")
                                                damagedcount=len(jobs9)
                                                print(damagedcount)
                                                scObj7=ProdReport.objects.filter(batch_number=lot).update(damagedcount=damagedcount,current_production_date=Begindatestring,current_production_time=current_time)
                                            except:
                                                print("database connection lost")
                                                
                                            try:
                                                scObj7=Printerdata.objects.filter(lot=lot).update(current_production_date=Begindatestring,current_production_time=current_time)
                                                print( 'curent date time updated ✅') 
                                            except:
                                                print("current time not update")
                                            if(counter==sllen-1):     #if the last number is not detecting it will clear the serialno
                                                print(serialno)                    
                                                del serialno[:]
                                                obj = Printerdata.objects.get(id=id)
                                                detailObj=Printerdata.objects.filter(lot=obj.lot).update(numbers=serialno)
                                                print("not detecte serialnumber cleared")                  
                                            counter=counter+1 
                            except:
                                print("Not Scanned")
                                r={"serialnumber":sl[counter],
                                        "grade":"Not Scanned"}
                                print(r)
                                b=json.dumps(r)
                                gradeupdation=Scannerdata(
                                    gtin=gtin,
                                    ip_address=ip_address,
                                    numbers=b,
                                    status="Not Scanned",
                                    serialnumber=sl[counter],
                                    gradevalue="Not Scanned",
                                    lot=lot,
                                    type=type
                                )
                                gradeupdation.save()
                                obj = Printerdata.objects.get(id=id)
                                detailObj=Printerdata.objects.filter(lot=obj.lot).update(scannergradefield=b)
                                jso=json.dumps(upjso)
                                serialvar=sl[counter]
                                serialno.remove(sl[counter])
                                gh=json.dumps(serialno)
                                obj = Printerdata.objects.get(id=id)
                                detailObj=Printerdata.objects.filter(lot=obj.lot).update(numbers=gh)
                                try:
                                        with open("NotScannedjson/"+lot+".csv", 'a', newline='') as file:
                                                                
                                            writer = csv.writer(file)
                                                            
                                            valuelist = [serialvar,"Not Scanned",gtin,lot],
                                                                    
                                            writer.writerows(valuelist)
                                                                
                                except:
                                    print("No DATA  ADDING TO NotscannedCSV after printer conn lost") 
                                if(counter==sllen-1):     #if the last number is not detecting it will clear the serialno
                                                    print(serialno)                    
                                                    del serialno[:]
                                                    obj = Printerdata.objects.get(id=id)
                                                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(numbers=serialno)
                                                    print("not detecte serialnumber cleared")
                                else:                                  
                                    counter=counter+1 
                                                
                           
                           
                                
                                # obj = Printerdata.objects.get(id=id)
                                # detailObj=Printerdata.objects.filter(lot=obj.lot).update(trigger_flag=0) 
                                
                                
                            
                    else:
                            
                        nj=0
                        
                        if(counter==sllen-1):
                            print("working assci not equal else condition")                    
                            scanner_socket_1 = socket.socket()
                            scanner_port_1=2001
                            scanner_socket_1.settimeout(8)  
                            scanner_socket_1.connect(('192.168.200.134', scanner_port_1))  #connecting the scanner to 2001 port 
                           
                            Begindatestring = date.today() 
      
                            t = time.localtime()

                               
                            current_time = time.strftime("%H:%M:%S", t)                    
                            try: 
                                
                                scanner_decode_data=scanner_socket_1.recv(1024).decode()
                                print("inside ascii not equal condition,this is  data",scanner_decode_data)
                                # print(type)
                                obj = Printerdata.objects.get(id=id)
                                detailObj=Printerdata.objects.filter(lot=obj.lot).update(trigger_flag=0) 
                                
                                if(type=="type2"):
                                    decoded_grade=scanner_decode_data[0] 
                                    confidence=scanner_decode_data[1] 
                                    decoded_gtin=scanner_decode_data[11:25]
                                    meanconfidence=scanner_decode_data[2:7]
                                    scanned_serial_number=scanner_decode_data[29:38]
                                    
                                    # print(meanconfidence)
                                elif(type== "type1" or type== "type5"):
                                    decoded_grade=scanner_decode_data[0]
                                    confidence=scanner_decode_data[1]
                                    decoded_gtin=scanner_decode_data[9:23]
                                    meanconfidence=scanner_decode_data[2:7]
                                    scanned_serial_number=scanner_decode_data[25:34]
                                   
                                    # print(textbatch)  
                                    # print(meanconfidence)                                     
                                # if d==1:
                                try:
                                    upjso.append(sl[counter])
                                except:
                                    print("No serialnumbers available for printing")   
                                serilength=len(serialno)
                                   
                                try:
                                        # if(v=="4" and confidence=="1" and meanconfidence>="0.800"):
                                        #             grade="A"
                                        # elif(v=="3" and confidence=="1" and meanconfidence>="0.800"):
                                        #             grade="B"
                                        # elif (v=="2" and confidence=="1" and meanconfidence>="0.800"):
                                        #             grade="C"
                                        # elif (v=="1" and confidence=="1" and meanconfidence>="0.800"):
                                        #             grade="D"
                                        # else:
                                        #             grade="F" 
                                        if(decoded_grade=="4" ):
                                                    grade="A"
                                        elif(decoded_grade=="3" ):
                                                    grade="B"
                                        elif (decoded_grade=="2" ):
                                                    grade="C"
                                        elif (decoded_grade=="1" ):
                                                    grade="D"
                                        else:
                                                    grade="F" 
                                                
                                        r={"serialnumber":sl[counter],
                                                    "grade":grade}
                                        # print("333333333333333",r)
                                        if(gtin==decoded_gtin):
                                            if(scanned_serial_number==sl[counter]):                    
                                                if(decoded_grade=="4" or decoded_grade=="3"):                
                                                    print(r)
                                                    b=json.dumps(r)
                                                    gradeupdation=Scannerdata(
                                                    gtin=gtin,
                                                    ip_address=ip_address,
                                                    grade=b,
                                                    status="Accepted",
                                                    serialnumber=sl[counter],
                                                    gradevalue=grade,
                                                    lot=lot,
                                                    type=type
                                                    )
                                                    gradeupdation.save()
                                                    obj = Printerdata.objects.get(id=id)
                                                    # print(obj.lot)
                                                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(scannergradefield=b)
                                                    jso=json.dumps(upjso)
                                                    serialvar3=sl[counter]
                                                    serialno.remove(sl[counter])
                                                    gh=json.dumps(serialno)
                                                    print(sl[counter])
                                                    obj = Printerdata.objects.get(id=id)
                                                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(printed_numbers=jso,numbers=gh)
                                                
                                                    with open("Acceptedjson/"+lot+".csv", 'a', newline='') as file:
                                                
                                                        writer = csv.writer(file)
                                            
                                                        valuelist = [serialvar3,grade,"Accepted",lot,gtin],
                                                    
                                                        writer.writerows(valuelist)
                                                    # updatedjson=json.loads(jso)
                                                
                                                    df = pd.read_csv("Acceptedjson/"+lot+".csv")
                                                    row_count = len(df)
                                                    row_count1= row_count+1 
                                                    

                                                    print("Number of rows:", row_count1)
                                                    try:
                                                        conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1")
                                                        
                                                    
                                                        
                                                        jobs7 = Scannerdata.objects.filter(lot=lot,status="Accepted")
                                                        acceptedcount=len(jobs7)
                                                        scObj7=ProdReport.objects.filter(batch_number=lot).update(acceptedcount=acceptedcount,current_production_date=Begindatestring,current_production_time=current_time)
                                                        print(acceptedcount, 'is last in the list ✅')                
                                                    
                                                        
                                                    except:
                                                        print("server connection losted in between the process of reports data add to server") 
                                                    try:
                                                        scObj7=Printerdata.objects.filter(lot=lot).update(current_production_date=Begindatestring,current_production_time=current_time)
                                                        print( 'curent date time updated ✅')                    
                                                    except:
                                                        print("current time not update")       
                                                    if(counter==sllen-1):           #If the last number is detecting it will clear the serialno
                                                        print(serialno)                    
                                                        del serialno[:]
                                                        obj = Printerdata.objects.get(id=id)
                                                        detailObj=Printerdata.objects.filter(gtin=obj.gtin).update(numbers=serialno)                  
                                                        print("detect serialnumber cleared")     
                                                    counter=counter+1
                                                else:    
                                                    print("grade less then B")
                                                    print(r)
                                                    b=json.dumps(r)
                                                    gradeupdation=Scannerdata(
                                                    gtin=gtin,
                                                    ip_address=ip_address,
                                                    grade=b,
                                                    status="Rejected",
                                                    serialnumber=sl[counter],
                                                    gradevalue=grade,
                                                    lot=lot,
                                                    type=type
                                                    )
                                                    gradeupdation.save()
                                                
                                                    
                                                    obj = Printerdata.objects.get(id=id)
                                                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(scannergradefield=b)
                                                    jso=json.dumps(upjso)
                                                    serialvar2=sl[counter]
                                                    serialno.remove(sl[counter])
                                                    gh=json.dumps(serialno)
                                                    print(sl[counter])
                                                    obj = Printerdata.objects.get(id=id)
                                                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(printed_numbers=jso,numbers=gh)
                                                    
                                                    
                                                    with open("jsonfiles/"+lot+".csv", 'a', newline='') as file:
                                                
                                                        writer = csv.writer(file)
                                            
                                                        valuelist = [serialvar2,grade,"Rejected",lot,gtin],
                                                        writer.writerows(valuelist)    
                                                    df1 = pd.read_csv("jsonfiles/"+lot+".csv")
                                                    row_count1 = len(df1)
                                                    row_count2= row_count1+1 

                                                    print("Number of rejected rows:", row_count2)
                                                    try:
                                                        conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1")
                                                    
                                                    
                                                        
                                                        jobs7 = Scannerdata.objects.filter(lot=lot,status="Rejected")
                                                        rejectedcount=len(jobs7)
                                                        scObj7=ProdReport.objects.filter(batch_number=lot).update(rejectedbycameracount=rejectedcount,current_production_date=Begindatestring,current_production_time=current_time)
                                                        
                                                        print(rejectedcount,'is last in the list ✅')
                                                                    
                                                    
                                                        
                                                    
                                                        
                                                    except:
                                                        print("server connection losted in between the process of reports data add to server")    
                                                    try:    
                                                        scObj7=Printerdata.objects.filter(lot=lot).update(current_production_date=Begindatestring,current_production_time=current_time)
                                                        print( 'curent date time updated ✅')     
                                                    except:
                                                        print("current time not updated")
                                                    
                                                    if(counter==sllen-1):           #If the last number is detecting it will clear the serialno
                                                        print(serialno)                    
                                                        del serialno[:]
                                                        obj = Printerdata.objects.get(id=id)
                                                        detailObj=Printerdata.objects.filter(lot=obj.lot).update(numbers=serialno)                  
                                                        print("detect serialnumber cleared")
                                                    counter=counter+1
                                            else: 
                                               print("serialnumber not equal")
                                            #    counter=counter+1 
                                                            
                                        else:                   
                                            print("not equal")
                                            r={"serialnumber":sl[counter],
                                                    "grade":"Not Detected"}
                                            print(r)
                                            b=json.dumps(r)
                                            gradeupdation=Scannerdata(
                                            gtin=gtin,
                                            ip_address=ip_address,
                                            numbers=b,
                                            status="Damaged",
                                            serialnumber=sl[counter],
                                            gradevalue="Not Detected",
                                            lot=lot,
                                            type=type
                                            )
                                            gradeupdation.save()
                                            obj = Printerdata.objects.get(id=id)
                                            detailObj=Printerdata.objects.filter(lot=obj.lot).update(scannergradefield=b)
                                            jso=json.dumps(upjso)
                                            serialvar1=sl[counter]
                                            serialno.remove(sl[counter])
                                            gh=json.dumps(serialno)
                                            obj = Printerdata.objects.get(id=id)
                                            detailObj=Printerdata.objects.filter(lot=obj.lot).update(numbers=gh)
                                            try:
                                                with open("Notdetectedjson/"+lot+".csv", 'a', newline='') as file:
                                            
                                                    writer = csv.writer(file)
                                        
                                                    valuelist = [serialvar1,"Not Detected",gtin,lot],
                                                
                                                    writer.writerows(valuelist)
                                            
                                            except:
                                                print("No DATA AVAILABLE FOR ADDING TO CSV")
                                            try:
                                                conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1")                
                                                jobs9 = Scannerdata.objects.filter(lot=lot,status="Damaged")
                                                damagedcount=len(jobs9)
                                                print(damagedcount)
                                                scObj7=ProdReport.objects.filter(batch_number=lot).update(damagedcount=damagedcount,current_production_date=Begindatestring,current_production_time=current_time)
                                            except:
                                                print("database connection lost")
                                                
                                            try:
                                                scObj7=Printerdata.objects.filter(lot=lot).update(current_production_date=Begindatestring,current_production_time=current_time)
                                                print( 'curent date time updated ✅') 
                                            except:
                                                print("current time not update")
                                            if(counter==sllen-1):     #if the last number is not detecting it will clear the serialno
                                                print(serialno)                    
                                                del serialno[:]
                                                obj = Printerdata.objects.get(id=id)
                                                detailObj=Printerdata.objects.filter(lot=obj.lot).update(numbers=serialno)
                                                print("not detecte serialnumber cleared")                  
                                            counter=counter+1
                                            
                                except:
                                        print("serialnumbers finished")
                            except socket.timeout:
                            
                            
                            
                                qs = Printerdata.objects.get(id=id)
                                
                            
                                
                                                                
                                                    
                                    
                                print("Not Scanned")
                                r={"serialnumber":sl[counter],
                                    "grade":"Not Scanned"}
                                print(r)
                                b=json.dumps(r)
                                gradeupdation=Scannerdata(
                                                    gtin=gtin,
                                                    ip_address=ip_address,
                                                    numbers=b,
                                                    status="Not Scanned",
                                                    serialnumber=sl[counter],
                                                    gradevalue="Not Scanned",
                                                    lot=lot,
                                                    type=type
                                                    )
                                gradeupdation.save()
                                obj = Printerdata.objects.get(id=id)
                                detailObj=Printerdata.objects.filter(lot=obj.lot).update(scannergradefield=b)
                                jso=json.dumps(upjso)
                                serialvar=sl[counter]
                                serialno.remove(sl[counter])
                                gh=json.dumps(serialno)
                                obj = Printerdata.objects.get(id=id)
                                detailObj=Printerdata.objects.filter(lot=obj.lot).update(numbers=gh)
                                try:
                                        with open("NotScannedjson/"+lot+".csv", 'a', newline='') as file:
                                                    
                                            writer = csv.writer(file)
                                                
                                            valuelist = [serialvar,"Not Scanned",gtin,lot],
                                                        
                                            writer.writerows(valuelist)
                                                    
                                except:
                                        print("No DATA AVAILABLE FOR ADDING TO CSV") 
                                if(counter==sllen-1):     #if the last number is not detecting it will clear the serialno
                                        print(serialno)                    
                                        del serialno[:]
                                        obj = Printerdata.objects.get(id=id)
                                        detailObj=Printerdata.objects.filter(lot=obj.lot).update(numbers=serialno)
                                        print("not detecte serialnumber cleared")                  
                                counter=counter+1 
                                    
                                        
                                                                    
                                print("Didn't receive  data! [Timeout 5s]") 
                         
                       
    def post(self,request,id):
                         
                qs=Printerdata.objects.get(id=id)
                form=PrinterForm(request.POST,instance=qs)
                form2=PrinterForm(request.POST,instance=qs)
                id=qs.id    
                gtin=qs.gtin 
                ponumber=qs.processordernumber
                expire =str(qs.expiration_date)
                lot=qs.lot
                type=qs.type
                hrf=qs.hrf 
                printednumbers=qs.printed_numbers
                ip_address=qs.ip_address
                child_numbers=qs.child_numbers
                po=qs.processordernumber
                # prodObj=ProductionOrder.objects.get(gtin_number=qs.gtin)
                # po=prodObj.process_order_number 
                try: 
                    if(type=="type2"):
                        hrfkey="null"                   
                        hrfvalue="null"                  
                    # print(printednumbers) 
                    else:
                                                
                        hrfjson=json.loads(hrf) 
                        hrf1value=hrfjson["hrf1value"]
                        hrf1key=hrfjson["hrf1"]
                        hrf2value=hrfjson["hrf2value"]
                        hrf2key=hrfjson["hrf2"]
                        hrf3value=hrfjson["hrf3value"]
                        hrf3key=hrfjson["hrf3"]
                        hrf4value=hrfjson["hrf4value"]
                        hrf4key=hrfjson["hrf4"]
                        hrf5key=hrfjson["hrf5"]
                        hrf5value=hrfjson["hrf5value"]
                        hrf6key=hrfjson["hrf6"]
                        hrf6value=hrfjson["hrf6value"]
                        
                
                        if(hrf1key!="" or hrf1key!="null"):
                            hrfkey=hrf1key
                        elif(hrf2key!="" or hrf2key!="null"):
                            hrfkey=hrf2key
                        elif(hrf3key!="" or hrf3key!="null"):
                            hrfkey=hrf3key
                        elif(hrf4key!="" or hrf4key!="null"):
                            hrfkey=hrf4key
                        elif(hrf5key!="" or hrf5key!="null"):
                            hrfkey=hrf5key
                        elif(hrf6key!="" or hrf6key!="null"):
                            hrfkey=hrf6key
                        
                    
                        if(hrf1value!="" or hrf1value!="null"):
                            hrfvalue=hrf1value
                        elif(hrf2value!="" or hrf2value!="null"):
                            hrfvalue=hrf2value
                        elif(hrf3value!="" or hrf3value!="null"):
                            hrfvalue=hrf3value
                        elif(hrf4value!="" or hrf4value!="null"):
                            hrfvalue=hrf4value
                        elif(hrf5value!="" or hrf5value!="null"):
                            hrfvalue=hrf5value
                        elif(hrf6value!="" or hrf6value!="null"):
                            hrfvalue=hrf6value
                except:
                    print("no hrf")        
            
                # print(hrfkey)
                # print(hrfvalue)
                try:    
                    serial=qs.numbers
                    serialnum=qs.numbers
                    serialno=json.loads(serial)
                    sl=json.loads(serialnum)
                except:
                    print("No serialnumber available in viewprinterview")
                    serialno=[]
                    sl=[]   
                
                try:
                    scanner_socket = socket.socket()
                    scanner_socket.settimeout(2)  
                    scanner_port=2001
                    scanner_socket.connect(('192.168.200.134', scanner_port))
                except socket.timeout:
                    # return redirect("scanner-message") 
                    # obj = Printerdata.objects.get(id=id)
                    # detailObj=Printerdata.objects.filter(lot=obj.lot).update(preparebuttonresponse=0)
                    # if (qs.load_button_resp == 0):
                    #            loadstopvariable=0
                    # else:
                    #     loadstopvariable=1                        
                    return render(request, 'Load-Batch.html', {'qs': qs,'errormess':"data52ex","po":po,"alert":0}) 
                           
                try:
                    printer_socket = socket.socket()
                    printer_port=34567
                    printer_socket.settimeout(1)  
                    printer_socket.connect(('192.168.200.150', printer_port))
                    
                    message52= "K7\x04"   #cartridge expiration alert
                    printer_socket.send(message52.encode()) 
                    cartridge_expiration=printer_socket.recv(1024).decode() 
                    cartridge_expiration_data=cartridge_expiration[:-1]
                    
                    obj = Printerdata.objects.get(id=id)
                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(stop_button_resp=0)
                    y = threading.Thread(target=self.scannerfun,args=(10,id,gtin,serialno,sl,printednumbers,Viewprinterview.q,Viewprinterview.event,lot,expire,hrfkey,hrfvalue,ip_address,child_numbers,type))  #initialising 2 threads
                    x = threading.Thread(target=self.printerfun,args=(10,serialno,Viewprinterview.q,Viewprinterview.event,gtin,lot,expire,hrfkey,hrfvalue,type,id))
                    y.start() 
                        
                    x.start() 
                                        
                   
                    
                    time.sleep(10)
                    loadstopvariable=1
                    obj = Printerdata.objects.get(id=id)
                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(load_button_resp=1,start_button_resp=0,status="Running")
                    
                
                
                                            
                    return redirect('start',id=id)
                   
                except socket.timeout:
                    
                    print("An exception occurred true")
                    
                  
                                               
                    return render(request, 'Load-Batch.html', {'qs': qs,'yu':0,'errormess':"cartridge_expiration_data","po":po,"alert":1})                                
                                                
# ....................................................................................

class Scannerdelete(View):
    def get(self,request):
            fg=[4,0,0,0,3,0,0,0,2,0,0,0,1]
            by=bytearray(fg)
            by[0]=0
            by[4]=0
            by[8]=2
            by[12]=1
                 
            try:
                plc_conn = socket.socket()
                plc_port=12000
                # plc_conn.settimeout(1)  
                plc_conn.connect(('192.168.200.55', plc_port))
                s=by
                
            
                message4556=by     
                plc_conn.send(message4556) 
                data360= plc_conn.recv(1024).decode()
                print(data360)
            # message4556=data360     
            # plc_conn.send(message4556.encode()) 
            
                data_to_string=str(data360)
                        # print("viewprinterview loop working")
                        
                        
                                            
                for c in data_to_string:
                    ascii_values_data_to_string=ord(c)
                    print(ascii_values_data_to_string)
            except:
                print("not connect")     
            return HttpResponse(200)                
                            
class Workview(View):
      def get(self,request):
                           
        fg=[4,0,0,0,3,0,0,0,2,0,0,0,1]
        by=bytearray(fg)
        by[0]=1
        by[4]=0
        by[8]=2
        by[12]=1
        try:
            plc_conn = socket.socket()
            plc_port=12000
            plc_conn.settimeout(1)  
            plc_conn.connect(('192.168.200.55', plc_port))
            s=by
             
            
            message4556=by     
            plc_conn.send(message4556) 
            data360= plc_conn.recv(1024).decode()
            print(data360)
            # message4556=data360     
            # plc_conn.send(message4556.encode()) 
            
            data_to_string=str(data360)
                        # print("viewprinterview loop working")
                        
                        
                                            
            for c in data_to_string:
                ascii_values_data_to_string=ord(c)
                print(ascii_values_data_to_string)
        except:
            print("not connect on plc")     
        return HttpResponse(200)
    # def get(self,request):
                       
    #     try:                    
    #         scanner_socket_2 = socket.socket()
    #         scanner_socket_2.settimeout(1)
    #         scanner_port_2=2001
       
    #         scanner_socket_2.connect(('192.168.200.134', scanner_port_2))
    #         scannerlost=0
              
            
            
    #     except socket.timeout:
    #         scannerlost=1
           
    #         s2 = socket.socket()
    #         port2=34567
    #         s2.settimeout(1) 
    #         s2.connect(('192.168.200.150', port2))
    #         belt_speed_command= "I5\x04"
    #         s2.send(belt_speed_command.encode()) 
    #         belt=s2.recv(1024).decode() 
                       
    #         belt_speed=belt[0:1]
    #         if(belt_speed!="0"):
    #         # plc connection for stopping covire
            
    #             fg=[4,0,0,0,3,0,0,0,2,0,0,0,1]
    #             by=bytearray(fg)
    #             by[0]=1
    #             by[4]=0
    #             by[8]=2
    #             by[12]=1
    #             try:
    #                 plc_conn = socket.socket()
    #                 plc_port=12000
    #                 plc_conn.settimeout(1)  
    #                 plc_conn.connect(('192.168.200.55', plc_port))
    #                 s=by
    #                 plc_stop_message=by     
    #                 plc_conn.send(plc_stop_message) 
    #                 plc_data= plc_conn.recv(1024).decode()
    #                 # print("workview",plc_data)
    #                 data_to_string=str(plc_data)
    #                 for c in data_to_string:
    #                     ascii_values_data_to_string=ord(c)
    #                     # print(ascii_values_data_to_string)
    #             except:
    #                 print(" work view plc not responding")
    #         else:
    #             print("work view belt speed is zero") 
    #     try:                    
    #         printer_socket_5 = socket.socket()
    #         printer_socket_5.settimeout(0.4)
    #         printer_port_5=34567
       
    #         printer_socket_5.connect(('192.168.200.150', printer_port_5))
    #         printerlost=0  
                
    #     except socket.timeout:
    #         printerlost=1 
    #         # plc connection for convire stopping
    #         fg=[4,0,0,0,3,0,0,0,2,0,0,0,1]
    #         by=bytearray(fg)
    #         by[0]=1
    #         by[4]=0
    #         by[8]=2
    #         by[12]=1
    #         try:
    #             plc_conn = socket.socket()
    #             plc_port=12000
    #             plc_conn.settimeout(0.6)  
    #             plc_conn.connect(('192.168.200.55', plc_port))
    #             s=by
    #             message4556=by     
    #             plc_conn.send(message4556) 
    #             data360= plc_conn.recv(1024).decode()
    #             # print(data360)
    #             data_to_string=str(data360)
    #             for c in data_to_string:
    #                 ascii_values_data_to_string=ord(c)
    #                 # print(ascii_values_data_to_string)
    #         except socket.timeout:
    #             print(" plc not responding")
                                                    
      
    #     return redirect("dashboard")
        # return render(request,"work.html",{"scannerlost":scannerlost})                     
class deletealldataview(View):
    def get(self,request):
        obj=ServerHistory.objects.all()
        obj.delete() 
        return HttpResponse(200)                                                 