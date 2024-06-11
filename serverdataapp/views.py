from django.shortcuts import render
import psycopg2
import csv
from models import ServerPrinterdata,ServerScannerdata
import time
from datetime import date 
from masterapp.models import PrinterdataTable,ScannerTable
# Create your views here.
from django.shortcuts import render,HttpResponse,redirect        
# class sendServer(View):
