from django.contrib import admin
from masterapp import views
from django.urls import path
urlpatterns = [
      path("signin/",views.Signinview.as_view(),name="signin"),
      path("signout/",views.signout_view,name="signout"),  
      
      path("dashboard/",views.Dashboard.as_view(),name="dashboard"),
      path("dashboard2/",views.Dashboard2.as_view(),name="dashboard2"),
       
      path('indexpage/', views.listing, name='indexpage'),
      path('search/', views.searchBar, name='search'),
   
      path("autovisionopen/<int:id>",views.Autovisionopenview.as_view(),name="autovision"), 
     
      path("printer/change/<int:id>",views.Viewprinterview.as_view(),name="emp-editjob"),
   
      path('serial/<int:id>',views.Serialcount.as_view(),name="serial"),
      path('datafromscanner/<int:id>',views.Data_Recive_From_scanner.as_view(),name="datafromscanner"),
      path('cu-connection-issue/<int:id>',views.CU_edit_ConnectionIssue.as_view(),name="cu-connection-issue"),
       path('common-ajax/<int:id>',views.Common_Connection_Ajax_View.as_view(),name="common-ajax"),
     
      path('reportget/', views.ReportGetview.as_view(), name='reportget'),
      path('productionreport/', views.ProductionReport, name='productionreport'),
      path('productionreportafterstop/', views.ProductionReport_Aftet_Stop_Batch, name='productionreportafterstop'),
      
      path("batchstopmess/",views.Batchstopmessageview.as_view(),name="batch-stop-message"),
     
      path("home",views.Candidatehomeview.as_view(),name="cand-home"),  
      path("servererror2/",views.ServerError2.as_view(),name="servererror2"), 
      
      path("firstpage/",views.Firstpage.as_view(),name="firstpage"),
      
      path('tasklist/', views.JobList, name='tasklist'), 
      path('tasklistsearch/', views.JoblistsearchBar, name='tasklistsearch'),
      # path('jobaddedsuccess/<int:id>', views.LoadJobpageview.as_view(), name='jobaddedsuccess'), 
      path('serverdatalist/',views.ServerView.as_view(), name='serverdatalist'), 
      path('sendserver/<int:id>', views.sendServer, name='sendserver'),
      path('getserverdata/<int:id>', views.Send_to_Servergetview.as_view(), name='getserverdata'), 
      path('serverlistsearch/', views.ServerlistsearchBar, name='serverlistsearch'), 
      
      path("history/",views.Historyview,name="history"),
      path('historysearch/', views.HistorysearchBar, name='historysearch'),  
      
      path('scannerlist/', views.Scannerlisting, name='scannerlist'),
      
      path('scannersearch/', views.ScannersearchBar, name='scannersearch'),   
      path("rework/<int:id>",views.ScannerReworkView.as_view(),name="rework"),
      path("reworkscan/<int:id>",views.Reworkscan,name="reworkscan"),  
      path("reworkstatusupdate/<int:id>",views.ReworkUpdate,name="reworkupdate"), 
      
      
      path("returnserialget/<int:id>",views.ReturnsnGet.as_view(),name="return-get"),
      path("returnserialno/<int:id>/<lot>",views.Returnserialnumbers.as_view(),name="return-numbers"),
      path("returnseriallist/",views.returnserialnolisting,name="return-list"),
      path('returnlistsearch/', views.ReturnSerialsearchBar, name='returnsearch'),
      
      path("databaseerror/",views.DatabaseError.as_view(),name="databaseerror"),
       
      path("information/",views.Informationpage.as_view(),name="information"),
      path("about1/",views.Aboutpage.as_view(),name="about"), 
      path("servererror3/",views.ServerError3.as_view(),name="servererror3"),
      path("ip-error/",views.Ip_error.as_view(),name="ip-error"),
      
      path('start/<int:id>',views.StartView.as_view(),name="start"),
      path('pauseview/<int:id>',views.Pauseview.as_view(),name="pauseview"),
      
      
      path('notscannedlist/', views.NotScannedlisting, name='notscannedlist'), 
      path("notscan/<int:id>",views.NotScanView.as_view(),name="notscan"),
      path("rescan/<int:id>",views.Rescan,name="rescan"),  
      path("rescanstatusupdate/<int:id>",views.RescanUpdate,name="rescanupdate"),
      path('notscansearch/', views.NotScansearchBar, name='notscansearch'),
      
      path("load/<int:id>",views.LoadBatchView.as_view(),name="load"),
      path("stop/<int:id>",views.StopBatchView.as_view(),name="stop"), 
      
      path("delete/",views.Scannerdelete.as_view(),name="delete"),
      path("work/",views.Workview.as_view(),name="work"),
      path("alldata/",views.deletealldataview.as_view(),name="alldata"),
      
      
     
]     
  

  