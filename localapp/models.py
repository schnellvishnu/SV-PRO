from django.db import models


class Printerdata(models.Model):
                    
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
                    trigger_flag=models.BooleanField(default=False)
                    
                    current_production_date =models.DateField(null=True)
                    current_production_time=models.TimeField(null=True)
                    def __str__(self):
                            return self.processordernumber
                  
                   
                  
                    

                    # class Meta:
       
                    #                     app_label = 'localapp'

class Scannerdata(models.Model):
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
                        
                        # class Meta:
       
                        #                 app_label = 'localapp'     
                                        

class LocalappLoginmodel(models.Model):  
    id=models.AutoField(primary_key=True) 
    login_id=models.IntegerField(max_length =100,default=False)
    loginuname = models.CharField(max_length=100,null=True)
    userrole=models.CharField(max_length=100)
    ip_address=models.CharField(max_length=100,null=True)
    line =models.CharField(max_length=20,default="noline")
   
    # class Meta:
                           
    #         app_label = 'localapp'   
            
class LocalseverHistory(models.Model):
                      
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
  
class Localapp_Register(models.Model):
    id = models.AutoField(primary_key=True)
    employeeid=models.CharField(max_length=100,default="e101",unique=True)
    Name=models.CharField(max_length=100)
    date_birth=models.DateField(null=True)
    age=models.CharField(max_length=100,default="age")
    place=models.CharField(max_length=100,default="place")
    email=models.EmailField(max_length=100,unique=True)
    address=models.TextField(default="address")
    mobile=models.CharField(max_length=100,default="phone")
    date_join=models.DateField(null=True)
    eduqu=models.CharField(max_length=100,default="qualification")
    userRole=models.CharField(max_length=100,default='admin')
    username=models.CharField(max_length=100,default="username")
    password=models.CharField(max_length=100,default="password")
    conpass=models.CharField(max_length=100,default="confirm password")
    dummy1=models.CharField(max_length=100,default="dummy1")
    dummy2=models.CharField(max_length=100,default="dummy2")
    dummy3=models.CharField(max_length=100,default="dummy3")
    dummy4=models.CharField(max_length=100,default="dummy4")
    key = models.CharField(max_length=500, default="key")   
    
class Local_UserrolePermissions(models.Model):
    id=models.AutoField(primary_key=True)
    activity_name=models.CharField(max_length=100)
    admin=models.JSONField(default={'CREATE':'Checked', 'READ': 'Checked', 'UPDATE':'Checked', 'DELETE':'Checked'}) 
    operator=models.JSONField(default={'CREATE':'Checked', 'READ': 'Checked', 'UPDATE':'Checked', 'DELETE':'Checked'}) 
    masterdata=models.JSONField(default={'CREATE':'Checked', 'READ': 'Checked', 'UPDATE':'Checked', 'DELETE':'Checked'}) 
    supervisor=models.JSONField(default={'CREATE':'Checked', 'READ': 'Checked', 'UPDATE':'Checked', 'DELETE':'Checked'})
    def __str__(self):
    	return self.activity_name      
 
class Inproperly_Closed(models.Model):
        id = models.AutoField(primary_key=True)
        close_update=models.CharField(max_length=100,null= True)                 
                                                            