from django.contrib import admin
from serverdataapp import views
from django.urls import path
urlpatterns = [
    
    
 path('restore_scannerdata/', views.Restore_BackupdataView, name='restore_scannerdata'), 
  path('csv/', views.Export_csv, name='csv'),  
  path('restore_server/', views.Restoredata_to_server, name='restore_server'),           
]     
  

  