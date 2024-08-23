from django.db import models


class ServerPrinterdata(models.Model):
                    
                    id=models.AutoField(primary_key=True)
                    printer_id=models.IntegerField(max_length =100,default=False)
                    
                    processordernumber=models.CharField(max_length=100,default=False,unique= True)
        
        
      
        
                    expiration_date = models.DateField(null=True)
        # gtin = models.ForeignKey(Gtins, on_delete= models.CASCADE)
                    lot=models.CharField(max_length=100,null=True,unique=True)
                    gtin=models.CharField(max_length=100,null=True)
                    numbers=models.JSONField(null=True,blank=True)
                    quantity= models.CharField(max_length=20,null=True)
                    hrf= models.JSONField(null=True,blank=True)
                    type=models.CharField(max_length=100,null=True)
                    status=models.CharField(max_length=100,null=True)
                    ip_address=models.CharField(max_length=100,null=True)
                    printed_numbers=models.JSONField(null=True)
                    balanced_serialnumbers=models.JSONField(null=True)
                   
                    child_numbers=models.JSONField(null=True,blank=True)
                    scannergradefield=models.JSONField(null=True,blank=True)
                    
                    
                    Rejectednumbers=models.JSONField(null=True,blank=True)
                    acceptednumbers=models.JSONField(null=True,blank=True)
                    load_button_resp=models.BooleanField(default=False)
                    stop_button_resp=models.BooleanField(default=False)
                    start_button_resp=models.BooleanField(default=False)
                    return_button_resp=models.BooleanField(default=False)
                    server_button_resp=models.BooleanField(default=False)
                    
                    production_date = models.DateField(null=True)
                    production_time=models.TimeField(null=True)
                    
                    
                   
                    def __str__(self):
                                return self.processordernumber
                    

class ServerScannerdata(models.Model):
                        id=models.AutoField(primary_key=True)
                        # processordernumber=models.CharField(max_length=100,unique= True)
                        gtin=models.CharField(max_length=100,null=True)
                        numbers=models.JSONField(null=True,blank=True)
                        ip_address=models.CharField(max_length=100,null=True)
                        grade = models.JSONField(blank=True,default="[{\"serialnumber\":\"grade\"}]")
                        status=models.CharField(max_length=100,null=True)
                        serialnumber=models.CharField(max_length=100,null=True)
                        gradevalue=models.CharField(max_length=100,null=True)
                        lot=models.CharField(max_length=100,null=True)
                        finalstatus=models.CharField(max_length=100,null=True)
                        type=models.CharField(max_length=100,null=True,blank=True)
                        def __str__(self):
                                return self.lot 
                                   
class BackupScannerdata(models.Model):
                        id=models.AutoField(primary_key=True)
                        # processordernumber=models.CharField(max_length=100,unique= True)
                        gtin=models.CharField(max_length=100,null=True)
                        numbers=models.JSONField(null=True,blank=True)
                        ip_address=models.CharField(max_length=100,null=True)
                        grade = models.JSONField(blank=True,default="[{\"serialnumber\":\"grade\"}]")
                        status=models.CharField(max_length=100,null=True)
                        serialnumber=models.CharField(max_length=100,null=True)
                        gradevalue=models.CharField(max_length=100,null=True)
                        lot=models.CharField(max_length=100,null=True)
                        finalstatus=models.CharField(max_length=100,null=True)
                        type=models.CharField(max_length=100,null=True,blank=True)
                        
                        send_date =models.DateField(null=True)
                        send_time=models.TimeField(null=True)
                        update_date=models.DateField(null=True)
                        def __str__(self):
                                return self.lot                         

class ServerLoginmodel(models.Model):  
    id=models.AutoField(primary_key=True) 
    login_id=models.IntegerField(max_length =100,default=False)
    loginuname = models.CharField(max_length=100,null=True)
    userrole=models.CharField(max_length=100)
    ip_address=models.CharField(max_length=100,null=True)
    line =models.CharField(max_length=20,default="noline")
    def __str__(self):
            return self.loginuname
   
            
class ServerHistory(models.Model):
                      
    modelname = models.CharField(max_length=100)
    savedid = models.CharField(max_length=100)
    operationdone = models.CharField(max_length=100)
    donebyuser = models.CharField(max_length=100)
    donebyuserrole = models.CharField(max_length=100)
    donedatetime = models.DateTimeField(max_length=100)
    description=models.CharField(max_length=300,default="True")
    donebyemployeeid=models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.donebyuser 
    
class BackupHistory(models.Model):
                      
    modelname = models.CharField(max_length=100)
    savedid = models.CharField(max_length=100)
    operationdone = models.CharField(max_length=100)
    donebyuser = models.CharField(max_length=100)
    donebyuserrole = models.CharField(max_length=100)
    donedatetime = models.DateTimeField(max_length=100)
    description=models.CharField(max_length=300,default="True")
    donebyemployeeid=models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.donebyuser     
                                                                 
                                                                 

    