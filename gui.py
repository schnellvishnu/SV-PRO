import os
import sys
import time
from threading import Thread
import webview
import socket
import subprocess
import csv
import psycopg2


def start_webview():
    try:        
        s = socket.socket()
        port=34567
        s.settimeout(1)  
        s.connect(('192.168.200.150', port))
        message30= "F0\x04"
        s.send(message30.encode()) 
        data30=s.recv(1024).decode()
        # print("offed")
    except socket.timeout:
        # print("printer not on")
        demmy=1
    # try:          
    #         file = "jobid.csv"
                                        
    #         if(os.path.exists(file) and os.path.isfile(file)):
                                     
    #             os.remove(file) 
    #             print("file deleted") 
    #         else: 
    #             print("file not found")     
    # except:
    #         print("No Such csv File for deleteing")    
    # time.sleep(3)                    
    window = webview.create_window('Track & Trace Application', 'http://localhost:8000/firstpage/', confirm_close=True, width=1200, height=700,maximized=200)
    webview.start()
    
    try:
       
        window.confirm_close==True
       
        
      
                           
      
        try:
            with open('jobid.csv', mode='r') as file:
                csvreader = csv.reader(file)
                for row in csvreader:
                    fgid=row[0]
                    j=str(fgid)
                    try:
                        conn = psycopg2.connect(
                        database="Line_DB2",#enter your database name
                        user='postgres',#enter your postgres username
                        password='1234',#enter your password
                        host='localhost',#enter your host name
                        port='5432'#port number
                        )
                        mycursor =conn.cursor()
                        var4=1
                        var5=1
                        

                        # mycursor.execute("UPDATE public.localapp_inproperly_closed set close_update = %s where id = 1",[fgid])
                        mycursor.execute("UPDATE public.localapp_printerdata set start_button_resp = false where id = %s",[j])
                        conn.commit() 
                    except:
                        print("not update")        
            
            
            # update_tab(1,1)
           
            conn = psycopg2.connect(
            database="Line_DB2",#enter your database name
            user='postgres',#enter your postgres username
            password='1234',#enter your password
            host='localhost',#enter your host name
            port='5432'#port number
            )
            mycursor =conn.cursor()
            var4=1
            var5=1
            

            mycursor.execute("UPDATE public.localapp_inproperly_closed set close_update = 1 where id = 1")
          
            conn.commit() 
            fg=[4,0,0,0,3,0,0,0,2,0,0,0,1]
            by=bytearray(fg)
            by[0]=1
            by[4]=0
            by[8]=2
            by[12]=1
                                            
            try:
                plc_conn = socket.socket()
                plc_port=12000
                                            
                plc_conn.connect(('192.168.200.55', plc_port))
                s=by
                                            
                                        
                message4556=by     
                plc_conn.send(message4556) 
                data360= plc_conn.recv(1024).decode()
                print(data360)
                                    
                data_to_string=str(data360)
                                                    # print("viewprinterview loop working")
                                                    
                                                    
                                                                        
                for c in data_to_string:
                    ascii_values_data_to_string=ord(c)
                    print(ascii_values_data_to_string)
            except:
                print("plc not responding")            
                    
        except:
            print("job.csv not found") 
                       
        try:        
            s2 = socket.socket()
            port2=34567
            s2.settimeout(1) 
            s2.connect(('192.168.200.150', port2))
          
            message30= "F0\x04"
            s2.send(message30.encode()) 
            data31=s2.recv(1024).decode()
        except socket.timeout:
            print("printer not on")        
        # bat_file_path =r"D:\19-2-24\18-4-24\BACKEND\webapplication\33.bat"
        
        # bat_file_path =r"D:\PROJECT-MULTIPLE-SCANN-PRINT\visionsetup\34.bat"
        bat_file_path =r"34.bat"
        
        bat_file=bat_file_path
        subprocess.run([bat_file])
        # s = socket.socket()
        
                
    except:
       
        print("hi")
            




def start_startdjango():
    if sys.platform in ['win32', 'win64']:
        os.system("python manage.py runserver {}:{}".format('127.0.0.1', '8000'))
        # time.sleep(10)
    else:
        os.system("python3 manage.py runserver {}:{}".format('127.0.0.1', '8000'))
        # time.sleep(10)


if __name__ == '__main__':
    Thread(target=start_startdjango).start()
    start_webview()
    