import os
import sys
import time
from threading import Thread
import webview
import socket
import subprocess

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
    try:          
            file = "jobid.csv"
                                        
            if(os.path.exists(file) and os.path.isfile(file)):
                                     
                os.remove(file) 
                print("file deleted") 
            else: 
                print("file not found")     
    except:
            print("No Such csv File for deleteing")    
    time.sleep(3)                    
    window = webview.create_window('Track & Trace Application', 'http://localhost:8000/firstpage/', confirm_close=True, width=1200, height=700,maximized=200)
    webview.start()
    
    try:
       
        window.confirm_close==True
        # bat_file_path =r"D:\11.bat" 
        
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
            s = socket.socket()
            port=34567
            s.connect(('192.168.200.150', port))
            message30= "F0\x04"
            s.send(message30.encode()) 
            data30=s.recv(1024).decode()
        except:
            print("printer not on")        
        # bat_file_path =r"D:\19-2-24\18-4-24\BACKEND\webapplication\33.bat"
        bat_file_path =r"D:\PROJECT-MULTIPLE-SCANN-PRINT\visionsetup\34.bat"
        
        bat_file=bat_file_path
        subprocess.run([bat_file])
        s = socket.socket()
        
        
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