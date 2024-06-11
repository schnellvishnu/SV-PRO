from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import View,ListView,CreateView,DetailView,UpdateView,DeleteView,FormView,TemplateView

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

from datetime import date 
import time
# import console
# import shutup
# Create your views here.
import sys
import psycopg2
import pandas as pd
import subprocess
from localapp.models import Printerdata,Scannerdata,LocalappLoginmodel,LocalseverHistory,Localapp_Register,Local_UserrolePermissions
from serverdataapp .models import ServerPrinterdata,ServerScannerdata,ServerHistory,ServerLoginmodel
from masterapp.forms import PrinterForm,Loginform

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
                                        
                    print("iP NOT fOUND")
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
                                        
                    print("Local iP NOT fOUND")  
                
                    
                
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
            except:
            
                return redirect("databaseerror") 
                    
        
                        
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
                
        
            if(loginname!=""):
                
              
                                       
                
             
                    
                posts1 = PrinterdataTable.objects.all().filter(status="Running",ip_address=systemip) #list only the jobs with running status(when the printer didnt stop in proper manner)
                le=len(posts1)
                if posts1:
                                
                    p = Paginator(posts1, 5)           #navigating to the previous and after pages
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
                               "nu":nu
                        }
                
                    
                        
                    return render(request, 'cu-list.html',{'page_obj':page, "name":loginname}) 
            
                else:
                    
                    
                       
                                
                    
                
                
                            
                        posts = PrinterdataTable.objects.all().filter(ip_address=systemip) #every printer jobs corresponding to a particular ipaddress...every jobs will come when printer stopping in normal way                       
                        p = Paginator(posts, 5)  # creating a paginator object
                        page_num=request.GET.get('page',1)
                        #page navigation
                        le=len(posts)
                        if le==0:
                            nu=1 
                        else:
                            nu=0     
                        try:
                            page=p.page(page_num)
                        except EmptyPage:
                            page=p.page(1)
                        # context = {'page_obj':page
                        
                        #         } 
                        return render(request, 'cu-list.html', {'page_obj':page,"name":loginname,"nu":nu})    
                    
            else:
                return redirect("signin")
        
    
def searchBar(request):   #searchbar in the printer jobs listpage
  
       
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
#------------------------------------------------------


 
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
                                           
                                            responsefield=responsefield,
                                            
                                           
                                            stopbtnresponse=stopbtnresponse,
                                           
                                            return_slno_btn_response=return_slno_btn_response,
                                            batchstopmessage=batchstopmessage,
                                            loadpause=loadpause,
                                            
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
                
            
                return  render(request,"scannersoftware.html",{"job":qs})
        else:
            return redirect("signin")

#.............................................................................. 

class Viewprinterview(View):  #load the values to printer
    threadstart=0
    # pausestart=0

    q=Queue()   #queue initialisation
    event=Event()
    
    def get(self,request,id):  
        # try:
        #     qs=Printerdata.objects.get(id=id)
                  
        #     po=qs.processordernumber
           
        # except:
        #     print("view page not working")
        #     return redirect("servererror")        
        # qs=Printerdata.objects.get(id=id)
        # form=PrinterForm(request.POST,instance=qs)
        # inexid=qs.id
           
        # rows=[inexid]
        # return render(request,"cu-edit.html",{"qs":qs,"po":po})
        qs=Printerdata.objects.get(id=id)
        po=qs.processordernumber
        intid=qs.id
        rows=[intid]
        if qs.responsefield==0:   
          os.system('start D:\Omron\AutoVision\AutoVISION.exe') 
        try:
                   
            with open("jobid.csv", 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                            # csvwriter.writerow(fields)
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
                    
        s2 = socket.socket()
        port2=34567
        s2.connect(('192.168.200.150', port2))

        if(type=="type2"):
                                
                    message= "L,new7.lbl\x04"
                    s2.send(message.encode()) 
                    data=s2.recv(1024).decode()  
                    message1= "E\x04"        
                    s2.send(message1.encode()) 
                    data1=s2.recv(1024).decode()
                    uy1=serialno[0:1]
                    
                    for sn in uy1:                
                 
                                   message5= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x04"
                                   s2.send(message5.encode()) 
                                   data5=s2.recv(1024).decode()
                                                
                                   message6= "QAC\x09"+"(17)"+expire+"(10)"+lot + "(01)" +  gtin + "(21)" + sn +  "\x09" + "Exp\x09" + expire + "\x09Lot" + "\x09" + lot + "\x09" + "Gtin\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"
                                   s2.send(message6.encode()) 
                                   data6=s2.recv(1024).decode() 
                                          
                                   message4= "F2\x04"
                                   s2.send(message4.encode()) 
                                   data4=s2.recv(1024).decode()
                     
                    print('Received from server: ' + data5)
                    print('Received from server: ' + data6)         
                    print('Received from server: ' + data4)
           
        elif(type=="type5"):
                     message7= "L,new8.lbl\x04"
                     s2.send(message7.encode()) 
                     data7=s2.recv(1024).decode()  
                     
                     message8= "E\x04"        
                     s2.send(message8.encode()) 
                     data8=s2.recv(1024).decode()
                     
                     uy2=serialno[0:1]     
                     for sn in uy2: 
                        message9= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x09"+"hrf"+"\x09hrfvalue"+"\x04"
                        s2.send(message9.encode()) 
                        data9=s2.recv(1024).decode()
                                                   
                                   # message6= "QAC\x09" + "55555777779(10)45612(21)\x09GTIN\x09" + gtin+"\x09"+ "lot\x09" + lot +"\x09" +"exp\x09" + expire+"\x09"+"serialno\x09"+sn+"\x04"
                        message10= "QAC\x09" + "(17)" + expire + "(10)" + lot + "(01)" +  gtin + "(21)" + sn + "(45)"+ hrfvalue+ "\x09" + "Exp\x09" + expire + "\x09"+"Lot" + "\x09" + lot + "\x09" + "Gtin"+ "\x09" +  gtin + "\x09" + "Slno" + "\x09" + sn + "\x09" + hrfkey + "\x09" + hrfvalue + "\x04"
                        s2.send(message10.encode()) 
                        data10=s2.recv(1024).decode() 
                                          
                        message11= "F2\x04"
                        s2.send(message11.encode()) 
                        data11=s2.recv(1024).decode()
                                        
                     print('Received from server: ' + data7)
                     print('Received from server: ' + data8) 
                     print('Received from server: ' + data9)
                     print('Received from server: ' + data10)         
                     print('Received from server: ' + data11)
                  
        elif(type=="type1"):
                     message12= "L,new5.lbl\x04"
                     s2.send(message12.encode()) 
                     data12=s2.recv(1024).decode()  
                     
                     message13= "E\x04"        
                     s2.send(message13.encode()) 
                     data13=s2.recv(1024).decode()
                     
                     uy=serialno[0:1] 
                                   
                     for sn in uy:
                                   message14= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x04"
                                   s2.send(message14.encode()) 
                                   data14=s2.recv(1024).decode()
                                                  
                                   # message6= "QAC\x09" + "55555777779(10)45612(21)\x09GTIN\x09" + gtin+"\x09"+ "lot\x09" + lot +"\x09" +"exp\x09" + expire+"\x09"+"serialno\x09"+sn+"\x04"
                                   message15= "QAC\x09" + "(17)" + expire + "(10)" + lot + "(01)" +  gtin + "(21)" + sn +"(45)"+ hrfvalue +  "\x09" + "Exp\x09" + expire + "\x09Lot" + "\x09" + lot + "\x09" + "GTIN\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"
                                   s2.send(message15.encode()) 
                                   data15=s2.recv(1024).decode() 
                                          
                                   message16= "F2\x04"
                                   s2.send(message16.encode()) 
                                   data16=s2.recv(1024).decode()
       
                     print('Received from server: ' + data14)
                     print('Received from server: ' + data15)         
                     print('Received from server: ' + data16)

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
        s3 = socket.socket()
        port4=2001
       
        s3.connect(('192.168.200.134', port4))  #connecting the scanner to 2001 port 
        s3.settimeout(5)      #for timeouting the socket...break is working by using this
        s4 = socket.socket()
        port=34567
        s4.connect(('192.168.200.150', port))   #connecting the printer to 34567 port
        
        Begindatestring = date.today() 
        print(Begindatestring)
        t = time.localtime()

        # Format the time as a string
        current_time = time.strftime("%H:%M:%S", t)
        print(current_time)
          
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
                if(Viewprinterview.q.empty()):
                    try: 
                        
                        data=s3.recv(1024).decode()
                        # print(data)
                        # print(type)
                          
                        if(type=="type2"):
                            v=data[0] 
                            confidence=data[1] 
                            textbatch=data[11:25]
                            meanconfidence=data[2:7]
                            # print(textbatch) 
                            # print(meanconfidence)
                        elif(type== "type1" or type== "type5"):
                            v=data[0]
                            confidence=data[1]
                            textbatch=data[9:23]
                            meanconfidence=data[2:7]
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
                                if(v=="4" ):
                                            grade="A"
                                elif(v=="3" ):
                                            grade="B"
                                elif (v=="2" ):
                                            grade="C"
                                elif (v=="1" ):
                                            grade="D"
                                else:
                                            grade="F" 
                                            
                                r={"serialnumber":sl[counter],
                                            "grade":grade}
                                
                                if(gtin==textbatch):
                                    if(v=="4" or v=="3"):                
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
                                        serialno.remove(sl[counter])
                                        gh=json.dumps(serialno)
                                        print(sl[counter])
                                        obj = Printerdata.objects.get(id=id)
                                        detailObj=Printerdata.objects.filter(lot=obj.lot).update(printed_numbers=jso,numbers=gh)
                                      
                                        with open("Acceptedjson/"+lot+".csv", 'a', newline='') as file:
                                      
                                            writer = csv.writer(file)
                                   
                                            valuelist = [sl[counter],grade,"Accepted",lot,gtin],
                                         
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
                                        serialno.remove(sl[counter])
                                        gh=json.dumps(serialno)
                                        print(sl[counter])
                                        obj = Printerdata.objects.get(id=id)
                                        detailObj=Printerdata.objects.filter(lot=obj.lot).update(printed_numbers=jso,numbers=gh)
                                        
                                        
                                        with open("jsonfiles/"+lot+".csv", 'a', newline='') as file:
                                      
                                            writer = csv.writer(file)
                                   
                                            valuelist = [sl[counter],grade,"Rejected",lot,gtin],
                                            writer.writerows(valuelist)    
                                        df1 = pd.read_csv("jsonfiles/"+lot+".csv")
                                        row_count1 = len(df1)
                                        row_count2= row_count1+1 

                                        print("Number of rejected rows:", row_count2)
                                        try:
                                            conn = psycopg2.connect("dbname='Db6' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1")
                                           
                                           
                                            
                                            jobs7 = Scannerdata.objects.filter(lot=lot,status="Rejected")
                                            rejectedcount=len(jobs7)
                                            scObj7=ProdReport.objects.filter(batch_number=lot).update(rejectedbycameracount=rejectedcount,current_production_date=Begindatestring,current_production_time=current_time)
                                            
                                            print(rejectedcount,'is last in the list ✅')
                                                           
                                           
                                            
                                           
                                            
                                        except:
                                            print("server connection losted in between the process of reports data add to server")    
                                            
                                            
                                           
                                        
                                        if(counter==sllen-1):           #If the last number is detecting it will clear the serialno
                                            print(serialno)                    
                                            del serialno[:]
                                            obj = Printerdata.objects.get(id=id)
                                            detailObj=Printerdata.objects.filter(lot=obj.lot).update(numbers=serialno)                  
                                            print("detect serialnumber cleared")
                                        counter=counter+1
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
                                    serialvar=sl[counter]
                                    serialno.remove(sl[counter])
                                    gh=json.dumps(serialno)
                                    obj = Printerdata.objects.get(id=id)
                                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(numbers=gh)
                                    try:
                                        with open("Notdetectedjson/"+lot+".csv", 'a', newline='') as file:
                                      
                                            writer = csv.writer(file)
                                   
                                            valuelist = [serialvar,"Not Detected",gtin,lot],
                                           
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
                        
                        
                        print("Didn't receive  data! [Timeout 5s]")
                           
                else:
                        d=Viewprinterview.q.get()
                        print(d)
                        if d==0:
                                    # try:
                                    #     s4 = socket.socket()
                                    #     port=34567
                                    #     s4.connect(('192.168.200.150', port)) 
                                       
                                    # except:
                                    #     obj = Printerdata.objects.get(id=id)
                                    #     detailObj=Printerdata.objects.filter(lot=obj.lot).update(loadpause=0) 
                                    #     print("Printer connection losted loadpaue change to 0") 
                                         
                                    try:
                                        print("yess")
                                        s4 = socket.socket()
                                        port=34567
                                        s4.connect(('192.168.200.150', port)) 
                                        
                                        
                                        
                                        message93="I2\x04"   
                                        s4.send(message93.encode()) 
                                        data94=s4.recv(1024).decode()
                                        data94r=data94[1:2]     
                                        # print(data94r)  
                                        
                                        print("Batch stop But Not update")
                                        
                                        message30= "F0\x04"
                                        s4.send(message30.encode()) 
                                        data30=s4.recv(1024).decode()
                                    except:
                                        print("nooooo")
                                        print("Printer connection losted but Batch stop successfully")    
                                    if(serialno==[]):
                                        obj = Printerdata.objects.get(id=id)
                                        detailObj=Printerdata.objects.filter(lot=obj.lot).update(stopbtnresponse=1,return_slno_btn_response=0,status="Printing Finished")                  
                                       
                                        
                                    else:
                                        obj = Printerdata.objects.get(id=id)
                                        detailObj=Printerdata.objects.filter(lot=obj.lot).update(stopbtnresponse=1,return_slno_btn_response=0,status="Stopped")
                                         
                                    detailsObj1 = Printerdata.objects.get(id=id) 
                                 
                                            
                                    obj = Printerdata.objects.get(id=id)
                                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(responsefield=0,stopbtnresponse=1,preparebuttonresponse=0) 
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
                    s5 = socket.socket()
                    s5.settimeout(2)  
                    port1=2001
                    s5.connect(('192.168.200.134', port1))
                except socket.timeout:
                    # return redirect("scanner-message") 
                    obj = Printerdata.objects.get(id=id)
                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(preparebuttonresponse=0)
                    if (qs.responsefield==0):
                               sd=0
                    else:
                        sd=1                        
                    return render(request, 'cu-edit.html', {'sd':sd,'qs': qs,'yu':0,'errormess':"data52ex","po":po,"alert":0}) 
                  
                #if the scanner have any issue this alert will come
                # try:
                #     if(qs.loadpause == 0):
                #            print("printer paused")
                #     else:
                #         return render(request, 'cu-edit.html', {'sd':1,'qs': qs,'yu':0,'errormess':"data52ex","po":po,"loadpausealert":1}) 
                # except:
                #     print("load pause ok")                             
                try:
                    s4 = socket.socket()
                    port=34567
                    s4.settimeout(1)  
                    s4.connect(('192.168.200.150', port))
                    
                    message52= "K7\x04"   #cartridge expiration alert
                    s4.send(message52.encode()) 
                    data52=s4.recv(1024).decode() 
                    data52ex=data52[:-1]
                    if(qs.loadpause == 0):
                        print("printer paused")
                    else:
                        return render(request, 'cu-edit.html', {'sd':1,'qs': qs,'yu':0,'errormess':"data52ex","po":po,"loadpausealert":1}) 
                     
                    if(Viewprinterview.threadstart==0):  #if the value  is 0 then set to 1
                        if  TimeoutError:
                            messages.success(request,"your application has posted successfully")                                    
                        obj = Printerdata.objects.get(id=id)
                        detailObj=Printerdata.objects.filter(lot=obj.lot).update(responsefield=1,stopbtnresponse=0,loadpause=0,return_slno_btn_response=1,batchstopmessage=0,preparebuttonresponse=1,status="Running")
                        
                        detailsObj = Printerdata.objects.get(id=id) 
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
                        obj = Printerdata.objects.get(id=id)
                        detailObj=Printerdata.objects.filter(lot=obj.lot).update(batchstopmessage=1) 
                       
                        time.sleep(7) 
                        try:
                            # s4 = socket.socket()
                            # port=34567
                            # s4.connect(('192.168.200.150', port))                   
                            return redirect("batch-stop-message")
                        except:
                            
                            return render(request, 'cu-edit.html', {'sd':1,'qs': qs,'yu':0,'errormess':data52ex,"po":po,"alert":3})             
                    
                    time.sleep(10)
                    sd=1
                    
                
                
                                            
                    
                    return render(request, 'cu-edit.html', {'sd':sd,'qs': qs,'yu':0,'errormess':data52ex,"po":po,"alert":2})
                except socket.timeout:
                    
                    print("An exception occurred true")
                    # return redirect("cand-home")
                    PauseClassview.pausestart=0  
                    obj = Printerdata.objects.get(id=id)
                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(preparebuttonresponse=0) 
                    if (qs.responsefield==0):
                        sd=0
                    else:
                        sd=1 
                    obj = Printerdata.objects.get(id=id)
                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(loadpause=0)     
                                               
                    return render(request, 'cu-edit.html', {'sd':sd,'qs': qs,'yu':0,'errormess':"data52ex","po":po,"alert":1})   
                   
            
#............................................................................

class PauseClassview(View):  #actual printing start and pause will happen in this view
    pausestart=0
    qu=Queue()
    event=Event()
    warnings.filterwarnings('ignore') 
    
    def get(self,request,id):   
            
           
           
            qs=Printerdata.objects.get(id=id)
            try:
                s3 = socket.socket()
                port4=2001
                
                s3.connect(('192.168.200.134', port4))  #connecting the scanner to 2001 port 
                s3.settimeout(1)
            except socket.timeout: 
                po=qs.processordernumber
                print(po) 
                obj = Printerdata.objects.get(id=id)
                detailObj=Printerdata.objects.filter(lot=obj.lot).update(preparebuttonresponse=0)  
                return render(request, 'cu-edit.html', {'qs': qs,'yu':0,'errormess':"data52ex","po":po,"alert":8,"buttonstatus":0})       
            try:
                s = socket.socket()
                s.settimeout(2)  
                port=34567
                s.connect(('192.168.200.150', port))
              
            
                message320="I2\x04"           
                s.send(message320.encode()) 
                data360=s.recv(1024).decode()
                printstatus=data360[1:2]
                
                
                if(qs.preparebuttonresponse == 1):
                                    
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
                        
                        return render(request,"pause-start.html",{"qs":qs,'lp':1,"sc":serilength,"po":po,"pd":-1})
                    else:
                       
                        # return redirect("linkhiding")
                        po=qs.processordernumber
                        return render(request,"pause-start.html",{"qs":qs,"po":po,"alert":4})
                       
                else:
                    qs=Printerdata.objects.get(id=id)
            
                    po=qs.processordernumber                    
                    return render(request,"pause-start.html",{"qs":qs,"po":po,"pd":5})
                    
                
            except socket.timeout:
                printstatus="p"
                qs=Printerdata.objects.get(id=id)
            
                po=qs.processordernumber  
                obj = Printerdata.objects.get(id=id)
                detailObj=Printerdata.objects.filter(lot=obj.lot).update(preparebuttonresponse=0) 
                return render(request, 'cu-edit.html', {'qs': qs,'yu':0,'errormess':"data52ex","po":po,"alert":4,"buttonstatus":0})    
          
            # if(qs.responsefield==1):
                                    
            #         if(printstatus=="h" or printstatus=="l"):               
                  
                
                    
            #             qs=Printerdata.objects.get(id=id)
        
            #             po=qs.processordernumber
                    
            #             try:
            #                 serial=qs.numbers
            #                 serialno=json.loads(serial)
            #             except:
            #                 print("serialnumbers finished")  #if the serialno finished this message will come    
            #             form=PrinterForm(request.POST,instance=qs)
                      
                        
                        
            #             try:
            #                 serilength=len(serialno)
                            
                            
            #             except:
            #                 # print("no length")
            #                 serilength=0
                        
            #             return render(request,"pause-start.html",{"qs":qs,'lp':1,"sc":serilength,"po":po,"pd":-1})
            #         else:
                       
            #             # return redirect("linkhiding")
            #             po=qs.processordernumber
            #             return render(request,"pause-start.html",{"qs":qs,"po":po,"alert":4})
                       
            # else:
            #     qs=Printerdata.objects.get(id=id)
        
            #     po=qs.processordernumber                    
            #     return render(request,"pause-start.html",{"qs":qs,"po":po,"pd":5})
              
    def printerfun1(self,num,serialno,qu,event,gtin,lot,expire,hrfkey,hrfvalue,type,id): #printing activities are happening in this
        self.serialno=serialno
        self.gtin=gtin
        self.expire=expire
        self.lot=lot
        self.hrfkey=hrfkey
        self.hrfvalue=hrfvalue
        self.type=type  
        self.id=id
       
        slle=len(serialno) 
        
        
                              
        s = socket.socket()
        port=34567
        s.connect(('192.168.200.150', port)) #connecting printer to a port number 34567
       
        if(type=="type2"):    #if it is type2, then it will enter in it
                                    
                message= "L,new7.lbl\x04"    #load label
                s.send(message.encode()) 
                data=s.recv(1024).decode()  
                message1= "E\x04"               #prepare printer
                s.send(message1.encode()) 
                data1=s.recv(1024).decode()
                n=2
                d1=0
                a=0
                b=1 
                c=0
                d=5             
                upjso=[]  

                                      
                while(n>0):
                              
                            if(PauseClassview.qu.empty()):
                          
                                #check the queue is empty or not                                    
                                if d1==1:  # checking value is one in queue 
                                                      
                                        for f in range(c,d):
                                            for sn in serialno[a:b]: 
                                                
                                                                                    
                                                    message5= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x04"  #loading field names
                                                    s.send(message5.encode()) 
                                                    data5=s.recv(1024).decode()
                                                
                                                    message6= "QAC\x09"  + "(01)" + gtin + "(21)" + sn + "(10)" + lot + "(17)" + expire + "\x09" + "Exp\x09" + expire + "\x09Lot" + "\x09" + lot + "\x09" + "Gtin\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"  #loading values
                                                    s.send(message6.encode()) 
                                                    data6=s.recv(1024).decode() 
                                                    
                                                    message4= "F2\x04"   #print values
                                                    s.send(message4.encode()) 
                                                    data4=s.recv(1024).decode()
                                                    
                                                    a=a+1
                                                    b=b+1   
                                            c=d
                                            d=d+5   
                            else:
                                d1=PauseClassview.qu.get() #getting value from queue
                                if d1==0:  #check wheather it is zero or not
                                        a=0
                                        b=1 
                                        c=0
                                        d=5
                                      
                                        
                                        detailsObj = Printerdata.objects.get(id=id) 
                                        # prodObj=ProductionOrder.objects.get(gtin_number=detailsObj.gtin)
                                        # detailObj=ProductionOrder.objects.filter(gtin_number=prodObj.gtin_number).update(status="Paused") #update status in po table
                                        message32="QAF\x04"   #pause the printer
                                        s.send(message32.encode()) 
                                        data36=s.recv(1024).decode()
                                        
                                        break   #break from the loop
        elif(type=="type5"):   #type5
                        message07="QAM,5\x04"
                        s.send(message07.encode()) 
                        data07=s.recv(1024).decode() 
                        
                        message7= "L,new8.lbl\x04"
                        s.send(message7.encode()) 
                        data7=s.recv(1024).decode() 
                         
                        message8= "E\x04"        
                        s.send(message8.encode()) 
                        data8=s.recv(1024).decode()
                        
                        detailsobj2 = Printerdata.objects.get(id=id) 
                        # prodObj=ProductionOrder.objects.get(gtin_number=detailsobj2.gtin)
                        # detailObj3=ProductionOrder.objects.filter(gtin_number=prodObj.gtin_number).update(status="Running")            
                        n1=2
                        d1=0
                        a1=0
                        b1=1 
                        c1=0
                        d2=5             
                        upjso=[]                    
                        while (n1>0):
                                    if(PauseClassview.qu.empty()):                                   
                                        if d1==1:
                                                # obj = PrinterdataTable.objects.get(id=id)
                                                # detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(loadpause=1)  
                                                # print("d1==1 annu")                                  
                                                for f in range(c1,d2):
                                                    for sn in serialno[a1:b1]:              
                                                        message9= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x09"+"hrf"+"\x09hrfvalue"+"\x04"
                                                        s.send(message9.encode()) 
                                                        data9=s.recv(1024).decode()
                                                
                                                        message10= "QAC\x09"  + "(01)" + gtin + "(21)" + sn + "(10)" + lot + "(17)" + expire + "(45)" + hrfvalue + "\x09" + "Exp"+ "\x09" + expire + "\x09" + "Lot" + "\x09" + lot + "\x09" + "Gtin" + "\x09" +  gtin + "\x09" + "Slno" + "\x09" + sn + "\x09" + hrfkey + "\x09" + hrfvalue + "\x04"
                                                        s.send(message10.encode()) 
                                                        data10=s.recv(1024).decode() 
                                                              
                                                        message11= "F2\x04"
                                                        s.send(message11.encode()) 
                                                        data11=s.recv(1024).decode()
                                                        
                                                        print(data11)
                                                
                                                        
                                                        
                                                        a1=a1+1
                                                        b1=b1+1
                                                        
                                                    c1=d2
                                                    d2=d2+5 
                                                    
                                    else:
                                        d1=PauseClassview.qu.get()
                                        if d1==0:
                                                a1=0
                                                b1=1 
                                                c1=0
                                                d2=5
                                                
                                                message32="QAF\x04"
                                                s.send(message32.encode()) 
                                                data36=s.recv(1024).decode()
                                                
                                                break
        elif(type=="type1"):   #type1
                        message12= "L,new5.lbl\x04"
                        s.send(message12.encode()) 
                        data12=s.recv(1024).decode()
                          
                        message13= "E\x04"        
                        s.send(message13.encode()) 
                        data13=s.recv(1024).decode()
                        n2=2
                        d1=0
                        a2=0
                        b2=1 
                        c2=0
                        d3=5 
                        # ho=  PauseClassview.qu.get()                              
                        while (n2>0):
                                    if(PauseClassview.qu.empty()): 
                                        # print(ho)                                  
                                        if d1==1:
                                                # obj = PrinterdataTable.objects.get(id=id)
                                                # detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(loadpause=1)                                    
                                                for f in range(c2,d3):
                                                    for sn in serialno[a2:b2]:              
                                                        message14= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x04"
                                                        s.send(message14.encode()) 
                                                        data14=s.recv(1024).decode()
                                                        
                                                                # print(slno)                    
                                                                # message6= "QAC\x09" + "55555777779(10)45612(21)\x09GTIN\x09" + gtin+"\x09"+ "lot\x09" + lot +"\x09" +"exp\x09" + expire+"\x09"+"serialno\x09"+sn+"\x04"
                                                        message15= "QAC\x09"  + "(01)" + gtin + "(21)" + sn + "(10)" + lot + "(17)" + expire + "(45)" + hrfvalue + "\x09" + "Exp\x09" + expire + "\x09" + "Lot" + "\x09" + lot + "\x09" + "GTIN\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"
                                                        # message15= "QAC\x09" + "(01)" +  gtin +  "(10)" + lot + "(17)" + expire +  "(21)" + sn +"(45)"+ hrfvalue +  "\x09" + "Exp\x09" + expire + "\x09Lot" + "\x09" + lot + "\x09" + "GTIN\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"
                                                        s.send(message15.encode()) 
                                                        data15=s.recv(1024).decode() 
                                                                        
                                                        message16= "F2\x04"
                                                        s.send(message16.encode()) 
                                                        data16=s.recv(1024).decode()
                                                            
                                                        a2=a2+1
                                                        b2=b2+1
                                                        
                                                    c2=d3
                                                    d3=d3+5      
                                    else:
                                        d1=PauseClassview.qu.get()
                                        if d1==0:
                                                a2=0
                                                b2=1 
                                                c2=0
                                                d3=5
                                               
                                                
                                                detailsObj = Printerdata.objects.get(id=id) 
                                                # prodObj=ProductionOrder.objects.get(gtin_number=detailsObj.gtin)
                                                # detailObj=ProductionOrder.objects.filter(gtin_number=prodObj.gtin_number).update(status="Paused")
                                                message32="QAF\x04"
                                                s.send(message32.encode()) 
                                                data36=s.recv(1024).decode()
                                                
                                              
                                                break
    def scannerfun1(self,num,serialno,qu,event):  #nothing special is happening
                   #every scanner activities is happening in scannerfun(viewprinterview)
        self.serialno=serialno                  
        counter=0
        d=0
        n=1
        s1 = socket.socket()
        port1=2001
        s1.connect(('192.168.200.134', port1))
        
        s = socket.socket()
        port=34567
        s.connect(('192.168.200.150', port))
        while True: 
            if(PauseClassview.qu.empty()):
                if d==1:
                    data=s1.recv(1024).decode() 
                    print(serialno[counter]) 
                    counter=counter+1    
                time.sleep(1)    
            else:
                d=PauseClassview.qu.get()
                if d==0:         
                    break
                time.sleep(1)  
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
            if(loginname!=""):                 
                qs=Printerdata.objects.get(id=id)
                form=PrinterForm(request.POST,instance=qs) 
                gtin=qs.gtin 
                ponumber=qs.processordernumber
                expire =str(qs.expiration_date)
                lot=qs.lot 
                type=qs.type
                hrf=qs.hrf                            
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
                    serilength=len(serialno)   #length of serialno
                
                except:
                    print("pause printing because serialnumber are empty")   #if the length zero it will work
                    serilength=0 
                    serialno=[]  
                try:     
                    s = socket.socket()
                    s.settimeout(5)
                    port=34567
                    s.connect(('192.168.200.150', port))
                        
                    message51= "I6\x04"    #ink level of printer
                        # "I6\x04"
                    s.send(message51.encode()) 
                    data51=s.recv(1024).decode() 
                    dataex=int(data51[:-1])  
                        # print("ink")   
                        # print(dataex)     
                    message53= "K8\x04"     #cartridge expiration
                    s.send(message53.encode()) 
                    data53=s.recv(1024).decode() 
                    data53ex=data53[:-1] 
                        # prodObj=ProductionOrder.objects.get(gtin_number=qs.gtin)
                    po=qs.processordernumber   
                    
                    message32="I2\x04"  
                    s.send(message32.encode()) 
                    data36=s.recv(1024).decode()
                    printstatus=data36[1:2]
                    print(data36)
                except socket.timeout:
                    print("printer connection error")
                    po=qs.processordernumber  
                    obj = Printerdata.objects.get(id=id)
                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(loadpause=0,preparebuttonresponse=0) 
                    return render(request, 'cu-edit.html', {'qs': qs,'yu':0,'errormess':"data52ex","po":po,"alert":5,"buttonstatus":0})    
                try:
                    s3 = socket.socket()
                    s3.settimeout(2)
                    port4=2001
                    s3.connect(('192.168.200.134', port4))         
                except socket.timeout: 
                    obj = Printerdata.objects.get(id=id)
                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(loadpause=0,preparebuttonresponse=0) 
                    return render(request, 'cu-edit.html', {'qs': qs,'yu':0,'errormess':"data52ex","po":po,"alert":7,"buttonstatus":0})                      
                if(PauseClassview.pausestart==0): 
                    try:
                            s = socket.socket()
                            port=34567
                            s.connect(('192.168.200.150', port))
                        
                            PauseClassview.pausestart=1   #if the value is  0 then it will convert to  1
                            PauseClassview.qu.put(PauseClassview.pausestart)   #inserting value to queue
                            # print(PauseClassview.pausestart)
                            print(PauseClassview.pausestart, 'is pausestart response the list ✅')
                            
                        
                                
                            message92="I2\x04"   #pause the printer
                            s.send(message92.encode()) 
                            data96=s.recv(1024).decode()
                            data96r=data96[1:2]
                            x1 = threading.Thread(target=PauseClassview.printerfun1,args=(self,10,serialno, PauseClassview.qu, PauseClassview.event,gtin,lot,expire,hrfkey,hrfvalue,type,id,))   #invoking printerfun1 thread with arguments from database
                            # y1 = threading.Thread(target=PauseClassview.seriallength)
                            
                            # print( data96)
                            
                            message32="I2\x04" 
                            s.send(message32.encode()) 
                            data36=s.recv(1024).decode()
                            # printstatus=data36[1:2]
                            # print(data36)
                            
                            
                            if printstatus=="l" or printstatus=="h":
                                try:
                                    s3 = socket.socket()
                                    port4=2001
                                    s3.connect(('192.168.200.134', port4)) 
                                    x1.start()
                                    obj = Printerdata.objects.get(id=id)
                                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(loadpause=1)
                                    
                                    
                                    
                                except:
                                    PauseClassview.pausestart=0  
                                    
                                    
                                    return render(request, 'pause-start.html', {'qs': qs,'pd':5,'gf':"gf","sc":serilength,"prer":"dataex","warningmess":"data53ex","po":po,"scanneralert":0})                                             
                                return render(request, 'pause-start.html', {'qs': qs,'pd':1,'gf':"gf","sc":serilength,"prer":dataex,"warningmess":data53ex,"po":po,"alert":1})   
                                
                            #navigating to pausestart page with arguments
                            PauseClassview.pausestart=0  
                            # return redirect("linkhiding")
                    except: 
                                po=qs.processordernumber   
                            
                                return render(request, 'pause-start.html', {'qs': qs,'pd':2,'gf':"gf","sc":serilength,"prer":"dataex","warningmess":"data53ex","po":po,"alert":0})                       
                        
                elif(PauseClassview.pausestart==1):
                            #if the value is  1 then it will convert to  0
                        try:
                                s = socket.socket()
                                s.settimeout(5)
                                port=34567
                                s.connect(('192.168.200.150', port))
                            
                                PauseClassview.pausestart=0                    
                                PauseClassview.qu.put(PauseClassview.pausestart) 
                                print(PauseClassview.pausestart, 'is pausestart response the list ✅')
                            
                            
                                message32="I2\x04" 
                                s.send(message32.encode()) 
                                data36=s.recv(1024).decode()
                                printstatus=data36[1:2]
                                print(data36)
                            
                                if printstatus=="h" or printstatus=="l":
                                    
                                    obj = Printerdata.objects.get(id=id)
                                    detailObj=Printerdata.objects.filter(lot=obj.lot).update(loadpause=0)
                                    
                                    return render(request, 'pause-start.html', {'qs': qs,'pd':2,'dp':2,'gf':"gf","sc":serilength,"prer":dataex,"warningmess":data53ex,"po":po,"alert":1})
                                else:
                                
                                    print("normal except")
                                    PauseClassview.qu.queue.clear()
                                
                                
                        except socket.timeout: 
                            po=qs.processordernumber 
                            PauseClassview.pausestart=0 
                                    
                            return render(request, 'cu-edit.html', {'qs': qs,'yu':0,'errormess':"data52ex","po":po,"alert":6,"buttonstatus":0})    
                            # return render(request, 'pause-start.html', {'qs': qs,'pd':1,'gf':"gf","sc":serilength,"prer":"dataex","warningmess":"data53ex","po":po,"alert":0}) 
                obj = Printerdata.objects.get(id=id)
                detailObj=Printerdata.objects.filter(lot=obj.lot).update(loadpause=0)                              
                return render(request, 'pause-start.html', {'qs': qs,'pd':5,'gf':"gf","sc":serilength,"prer":"dataex","warningmess":"data53ex","po":po,"alert":0})                   
            else:
                                    return redirect("signin") 
                
                
        
         
    def get_queryset(self):
        return Printerdata.objects.all()
    
class Serialcount(View):
    def get(self,request,id):
        try:                    
            s3 = socket.socket()
            s3.settimeout(1)
            port4=2001
       
            s3.connect(('192.168.200.134', port4))
            scannerlost=0      
        except socket.timeout:
            scannerlost=1
            obj = Printerdata.objects.get(id=id)
            detailObj=Printerdata.objects.filter(lot=obj.lot).update(preparebuttonresponse=0,loadpause=0)
          
             
        
        try:                    
            s4 = socket.socket()
            s4.settimeout(1)
            port5=34567
       
            s4.connect(('192.168.200.150', port5))
            printerlost=0      
        except socket.timeout:
            printerlost=1 
            obj = Printerdata.objects.get(id=id)
            detailObj=Printerdata.objects.filter(lot=obj.lot).update(preparebuttonresponse=0,loadpause=0)     
            
       
        # try:
        #     s5 = socket.socket()
            
        #     s5.settimeout(6)
        #     port6=2001
       
        #     s5.connect(('192.168.200.134', port6))
        # except:
        #     print("okk")   
        # try:
        #     data=s5.recv(1024).decode()   
            
            
        #     scannerdataerror=0                               
        # except socket.timeout:
        #     qs=Printerdata.objects.get(id=id)
        #     if qs.loadpause == 1:
        #        scannerdataerror=1        
        #     else:
        #         scannerdataerror=0                                  
        
        qs=Printerdata.objects.get(id=id)
        serialno=qs.numbers
            
            
        po=qs.processordernumber
        if serialno==[]:
            serilength=0 
        else :                   
            serial=json.loads(serialno)
            
            serilength=len(serial)
            print(serilength)
            print(scannerlost)
            # mess="server connection ok"
          
        return render(request,"Length.html",{"qs":qs,"sc":serilength,"scannerlost":scannerlost,"printerlost":printerlost,"scannerdataerror":"scannerdataerror"})   
       
class Data_Recive_From_scanner(View):
    def get(self,request,id):
        try:                    
            s3 = socket.socket()
            s3.settimeout(1)
            port4=2001
       
            s3.connect(('192.168.200.134', port4))
            scannerlost=0      
        except socket.timeout:
            scannerlost=1
            obj = Printerdata.objects.get(id=id)
            detailObj=Printerdata.objects.filter(lot=obj.lot).update(preparebuttonresponse=0,loadpause=0)
          
             
        
        try:                    
            s4 = socket.socket()
            s4.settimeout(1)
            port5=34567
       
            s4.connect(('192.168.200.150', port5))
            printerlost=0      
        except socket.timeout:
            printerlost=1 
            obj = Printerdata.objects.get(id=id)
            detailObj=Printerdata.objects.filter(lot=obj.lot).update(preparebuttonresponse=0,loadpause=0)     
            
       
        try:
            s5 = socket.socket()
            
            s5.settimeout(6)
            port6=2001
       
            s5.connect(('192.168.200.134', port6))
        except:
            print("okk")   
        try:
            data=s5.recv(1024).decode()   
            
            
            scannerdataerror=0                               
        except socket.timeout:
            qs=Printerdata.objects.get(id=id)
            if qs.loadpause == 1:
               scannerdataerror=1        
            else:
                scannerdataerror=0                                  
        
        qs=Printerdata.objects.get(id=id)
        serialno=qs.numbers
            
            
        po=qs.processordernumber
        if serialno==[]:
            serilength=0 
        else :                   
            serial=json.loads(serialno)
            
            serilength=len(serial)
            print(serilength)
            print(scannerlost)
            # mess="server connection ok"
                                  
        return render(request,"Datafromscanner.html",{"qs":qs,"sc":serilength,"scannerlost":scannerlost,"printerlost":printerlost,"scannerdataerror":scannerdataerror})   
          
           
                   
                 
         
                   
#  . ................................................................................ 

class Batchstopmessageview(View) :
    def get(self,request):  
     
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
                print(current_time)    
                qs=Printerdata.objects.get(id=fgid)
                # prodObj=ProductionOrder.objects.get(gtin_number=qs.gtin)
                po=qs.processordernumber  
                print(po)
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
                responsefield=qs.responsefield
                # preparebuttonresponse=qs.preparebuttonresponse
                stopbtnresponse=qs.stopbtnresponse
                # start_pause_btnresponse=qs.start_pause_btnresponse
                # pause_stop_btnresponse=qs.pause_stop_btnresponse
                return_slno_btn_response=qs.return_slno_btn_response
                batchstopmessage=qs.batchstopmessage
                # label_response=qs.label_response
                child_numbers=qs.child_numbers
                scannergradefield=qs.scannergradefield
                loadpause=qs.loadpause
                Rejectednumbers=qs.Rejectednumbers
                acceptednumbers=qs.acceptednumbers
                # print(status)
                # qws=Printerdata.objects.get(printer_id=fgid)
                # inid=qws.printer_id
                obj = Printerdata.objects.get(id=fgid)
                # print(obj.gtin)
                # prodObj=PrinterdataTable.objects.get(gtin_number=obj.gtin)
                # print(prodObj.gtin)
                try:
                    printerdata_to_server=ServerPrinterdata(printer_id=fgid,numbers=numbers,
                                            balanced_serialnumbers=balanced_serialnumbers,
                                            responsefield=False,
                                            # preparebuttonresponse=preparebuttonresponse,
                                            stopbtnresponse=True,
                                            # start_pause_btnresponse=start_pause_btnresponse,
                                            # pause_stop_btnresponse=pause_stop_btnresponse,
                                            return_slno_btn_response=return_slno_btn_response,
                                            batchstopmessage=batchstopmessage,
                                            # label_response=label_response,
                                            child_numbers=child_numbers,
                                            scannergradefield=scannergradefield,
                                            loadpause=loadpause,
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
                                            pause_stop_btnresponse=1
                                            )
                    printerdata_to_server.save() 
                      
                except:
                    detailObj=ServerPrinterdata.objects.filter(lot=lot).update(printer_id=fgid,numbers=numbers,
                                        balanced_serialnumbers=balanced_serialnumbers,
                                        responsefield=False,
                                        # preparebuttonresponse=preparebuttonresponse,
                                        stopbtnresponse=True,
                                        # start_pause_btnresponse=start_pause_btnresponse,
                                        # pause_stop_btnresponse=pause_stop_btnresponse,
                                        return_slno_btn_response=return_slno_btn_response,
                                        batchstopmessage=batchstopmessage,
                                        # label_response=label_response,
                                        child_numbers=child_numbers,
                                        scannergradefield=scannergradefield,
                                        loadpause=loadpause,
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
                                        pause_stop_btnresponse=1
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
            if(loginname!=""): 
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
                            return render(request, 'Report.html', {'qs':jobs,"name":loginname,'damagedcount':damagedcount,"challengedcount":challengedcount,"otherscount":otherscount,"samplecount":samplecount,"specimencount":specimencount,"acceptedcount":acceptedcount,"rejectedcount":rejectedcount})
                        else:
                            print("No information to show")
                            return render(request, 'Report.html', {"name":loginname})
                    except:
                        print("no report available")
                        return render(request, 'Report.html', {"mess":500})
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
            if(loginname!=""): 
                if request.method == 'GET':
                    lot = request.GET.get('lot')
                   
                    try:
                        if lot:
                            jobs =ServerPrinterdata.objects.get(lot=lot) 
                            # print(jobs.gtin)
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
                            
                            jobs7 = ServerScannerdata.objects.filter(lot=lot).filter(status="Accepted")
                            acceptedcount=len(jobs7)
                            
                            jobs8 = ServerScannerdata.objects.filter(lot=lot).filter(status="Rejected")
                            rejectedcount=len(jobs8)
                            
                            # jobs6 = ScannerTable.objects.filter(lot=lot,status="rejected")
                            # rejectedcount=len(jobs6)
                            return render(request, 'Report.html', {'qs':jobs,"name":loginname,'damagedcount':damagedcount,"challengedcount":challengedcount,"otherscount":otherscount,"samplecount":samplecount,"specimencount":specimencount,"acceptedcount":acceptedcount,"rejectedcount":rejectedcount})
                        else:
                            print("No information to show")
                            return render(request, 'Report.html', {"name":loginname,"headname":2})
                    except:
                        print("no report available")
                        return render(request, 'Report.html', {"mess":500})
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
        if(loginname!=""):
            posts1 = Printerdata.objects.all()#list only the jobs with running status(when the printer didnt stop in proper manner)
            le=len(posts1)
            if posts1:
                                
                    p = Paginator(posts1, 5)           #navigating to the previous and after pages
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
                    
                    
                      
                    
                                
                    
                
                
                            
                        posts = Printerdata.objects.all() #every printer jobs corresponding to a particular ipaddress...every jobs will come when printer stopping in normal way                       
                        p = Paginator(posts, 5)  # creating a paginator object
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
        if(loginname!=""): 
            if request.method == 'GET':
                query = request.GET.get('query')    #searching item
                # print(query)
                if query:
                    jobs = PrinterdataTable.objects.filter(lot=query)  #check wheather there is any match with searching item
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
            i=0
            if(loginname!=""):
            
                
                posts = ServerHistory.objects.all().filter(donebyuserrole="operator") 
                # print(posts)
                le=len(posts)
                historypost=posts.order_by('-id')
               
                         
                p = Paginator(historypost, 5)  # creating a paginator object
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
                           "name":loginname,
                           "nu":nu
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
            if(loginname!=""): 
                if request.method == 'GET':
                    query = request.GET.get('query')
                    print(query)
                    if query:
                            jobs = History.objects.filter(donebyuser=query) 
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
            i=0
            if(loginname!=""):
            
                # ,status = "Challenged",status="Damaged"
                
                # posts=ScannerTable.objects.all()
              
                posts = ServerScannerdata.objects.exclude(status="Damaged")
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
                p = Paginator(posts, 5)  # creating a paginator object
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
        
def ScannersearchBar(request):   #searchbar in scanner page 
        # try:
        #     conn = psycopg2.connect("dbname='Db6' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")  
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
            if(loginname!=""): 
                if request.method == 'GET':
                    query = request.GET.get('query')
                    print(query)
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
            if(loginname!=""): 
                qs=ServerScannerdata.objects.get(id=id)
            
            # form=PrinterForm(request.POST,instance=qs)
                return render(request,"rework.html",{"qs":qs})
            else:
                return redirect("signin")
        # except:
        #     return redirect("databaseerror")  
        
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
            if(loginname!=""):     
                            qs= ServerScannerdata.objects.get(id=id)
                            try: 
                                s = socket.socket()
                                port=2001
                                s.connect(('192.168.200.134', port))   
                            except:
                                # print("data not recived")
                                return redirect("scanner-message") 
                            try:         
                                dummycount = 8
                                data=s.recv(1024).decode()
                                # print(data)
                                v=data[0]
                                if(v=="4"):
                                    grade="A"
                                elif(v=="3"):
                                    grade="B"
                                elif (v=="2"):
                                    grade="C"
                                elif (v=="1"):
                                    grade="D"
                                else:
                                    grade="F" 
                                type=qs.type
                                if(type=="type2"):
                                    h=data[38:]    #data from scanner is coming in decoded textbox
                                    seri=data[29:38]
                                    print(seri)
                                elif(type=="type5" or type=="type1"):
                                    h=data[38:]    #data from scanner is coming in decoded textbox
                                    seri=data[25:34]
                                    print(seri)                   
                                decodedtext=data
                                # print(decodedtext)
                                # print(v)
                                # print(h)
                                if (seri== qs.serialnumber):   #serialno from database serialno from sacnner are checking(whather any match is there ) 
                                
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
            if(loginname!=""):
                qs= ServerScannerdata.objects.get(id=id) 
                lot=qs.lot 
                gtin=qs.gtin
                lines=[]
            if request.method == 'GET':
                query1 = request.GET.get('query') 
                newgrade = request.GET.get('grade')      
                print(newgrade)   #updating old status with new status
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
                       print ("not challenged" ) 
                   
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
        except:
            print("Login model data have some issue in Autovision view") 
        if(loginname!=""):                     
            posts1 = ServerPrinterdata.objects.all()
            le=len(posts1)
            if posts1:
                                    
                p = Paginator(posts1, 5)           #navigating to the previous and after pages
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
                return render(request, 'ServerDatalist.html',{'page_obj':page, "name":loginname})     
            else:
                                            
                    posts = ServerPrinterdata.objects.all() #every printer jobs corresponding to a particular ipaddress...every jobs will come when printer stopping in normal way                       
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
                    return render(request, 'ServerDatalist.html',{'page_obj':page, "name":loginname,"nu":nu})     
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
                    print("IP NOT fOUND") 
            except:
                return redirect("databaseerror")                         
            s = ServerPrinterdata.objects.get(id=id)
               
            return  render(request,"Serverdata-send.html",{"qs":s})                    
        
                               




    
    
    
def sendServer(request,id):  
    
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
                    print(current_time)    
                    qs=ServerPrinterdata.objects.get(id=id)
                    # prodObj=ProductionOrder.objects.get(gtin_number=qs.gtin)
                    po=qs.processordernumber  
                    print(po)
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
                    responsefield=qs.responsefield
                    # preparebuttonresponse=qs.preparebuttonresponse
                    stopbtnresponse=qs.stopbtnresponse
                    # start_pause_btnresponse=qs.start_pause_btnresponse
                    # pause_stop_btnresponse=qs.pause_stop_btnresponse
                    return_slno_btn_response=qs.return_slno_btn_response
                    batchstopmessage=qs.batchstopmessage
                    # label_response=qs.label_response
                    child_numbers=qs.child_numbers
                    scannergradefield=qs.scannergradefield
                    loadpause=qs.loadpause
                    Rejectednumbers=qs.Rejectednumbers
                    acceptednumbers=qs.acceptednumbers
                    print(status)
                    # qws=Printerdata.objects.get(printer_id=fgid)
                    # inid=qws.printer_id
                    obj = ServerPrinterdata.objects.get(id=id)
                    # print(obj.gtin)
                    # prodObj=PrinterdataTable.objects.get(gtin_number=obj.gtin)
                    # print(prodObj.gtin)
                    detailObj=PrinterdataTable.objects.filter(lot=obj.lot).update(numbers=numbers,
                                            balanced_serialnumbers=balanced_serialnumbers,
                                            responsefield=False,
                                            # preparebuttonresponse=preparebuttonresponse,
                                            stopbtnresponse=True,
                                            # start_pause_btnresponse=start_pause_btnresponse,
                                            # pause_stop_btnresponse=pause_stop_btnresponse,
                                            return_slno_btn_response=return_slno_btn_response,
                                            batchstopmessage=batchstopmessage,
                                            # label_response=label_response,
                                            child_numbers=child_numbers,
                                            scannergradefield=scannergradefield,
                                            loadpause=loadpause,
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
                    detailObj2=ServerPrinterdata.objects.filter(lot=obj.lot).update(pause_stop_btnresponse=0)    
                    
            
            scdata=ServerScannerdata.objects.all()
            sclength=len(scdata)
            print(sclength)
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
                    obj = ServerPrinterdata.objects.get(id=id)
                    jobs10 =  ServerPrinterdata.objects.filter(id=id,status="Closed").update(start_pause_btnresponse=1)
                    # # damagedcount=len(jobs9)
            historysave=History(modelname='ServerPrinterdata',
                                        savedid="noid",
                                        operationdone='Send to server',
                                        donebyuser=loginname,
                                        donebyuserrole=loginuserrole, 
                                        description="Send The Batch Details Of  "+lot+" To Server "+"by"+" "+ loginname,
                                        donedatetime=datetime.datetime.now())
            historysave.save()            
            ServerScannerdata.objects.all().delete()
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
                                            
            # return redirect("serverdatalist")
            return  render(request,"Serverdata-send.html",{"qs":qs,"message":1})
           
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
            ref=detailsObj.responsefield 
                              
        except:
            print("jobid.csv not found")
            fgid=0
            try:
                with open('data.csv', mode='r') as file:
                    csvreader = csv.reader(file)
                    for row in csvreader:
                       dataid=row[0]
                        
                detailsObj =Printerdata.objects.get(id=dataid)
                prodObj=Printerdata.objects.get(lot=detailsObj.lot)
                scObj=Printerdata.objects.filter(lot=prodObj.lot).update(responsefield=0)
                if(detailsObj.status=="Running"):
                    detailsObj =Printerdata.objects.get(id=dataid)
                    prodObj=Printerdata.objects.get(lot=detailsObj.lot)
                    scObj=Printerdata.objects.filter(lot=prodObj.lot).update(loadpause=0,status="Stopped")                                    
                
                detailsObj =Printerdata.objects.get(id=dataid)
                ref=detailsObj.responsefield                          
            except:
                print("data.csv not found")
                ref=0
                 
            
        return render(request, 'dashboard.html',{"id":fgid,"resf":ref})        
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
        if(loginname!=""):
            
                posts = ServerPrinterdata.objects.all()  #every printer jobs corresponding to a particular ipaddress...every jobs will come when printer stopping in normal way                       
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
        try:
            conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")
        except:
            return redirect("databaseerror")      
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
        try:
            conn = psycopg2.connect("dbname='Db8' user='postgres' host='192.168.200.30' password='admin' connect_timeout=1 ")                     
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
            if(loginname!=""): 
                qs=ServerPrinterdata.objects.get(id=id)
                form=PrinterForm(request.POST,instance=qs)
                return render(request,"returnserial.html",{"qs":qs})
            else:
                return redirect("signin")
        except:
            return redirect("databaseerror") 
        
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
                    detailObj=ServerPrinterdata.objects.filter(lot=obj.lot).update(stopbtnresponse=1,return_slno_btn_response=0,status="Closed")  
                    
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
                responsefield=qs.responsefield
                    # preparebuttonresponse=qs.preparebuttonresponse
                stopbtnresponse=qs.stopbtnresponse
                # start_pause_btnresponse=qs.start_pause_btnresponse
                    # pause_stop_btnresponse=qs.pause_stop_btnresponse
                return_slno_btn_response=qs.return_slno_btn_response
                batchstopmessage=qs.batchstopmessage
                    # label_response=qs.label_response
                child_numbers=qs.child_numbers
                scannergradefield=qs.scannergradefield
                loadpause=qs.loadpause
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
                                            responsefield=False,
                                            # preparebuttonresponse=preparebuttonresponse,
                                            stopbtnresponse=True,
                                            # start_pause_btnresponse=start_pause_btnresponse,
                                            # pause_stop_btnresponse=pause_stop_btnresponse,
                                            return_slno_btn_response=return_slno_btn_response,
                                            batchstopmessage=batchstopmessage,
                                            # label_response=label_response,
                                            child_numbers=child_numbers,
                                            scannergradefield=scannergradefield,
                                            loadpause=loadpause,
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
                return render(request,"returnserial.html",{"qs":qs,"returnmessa":1,"ret":1})  #success message after return serialno                            
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
           
                           