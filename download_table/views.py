from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import psycopg2
import pandas as pd

def get_connection():
     conn = psycopg2.connect(host='203.112.158.89',
                                user='analytics',
                                password='analytics',
                                database='ratings')
     return conn

def table_data(request):

    unmaped_start_dates = request.POST.get('start_date')
    unmaped_end_date = request.POST.get('end_date')
    company = request.POST.get('company_Name')
    
    q='''Select  to_char(newsdate,'yyyy-mm-dd') newsdate, newssource, newstitle, newsdetail, companyname,newsurl, sentiment, sentimentscore
        FROM analytics.tblnewsdetails''' + "  where newsdate BETWEEN '" + unmaped_start_dates + "' AND '" + unmaped_end_date + " ' and LOWER(companyname) like '" + company.lower() +  "%'"
    conn=get_connection()
    data=pd.read_sql_query(q,con=conn)
    data['newstitle'] = data['newstitle'].apply(lambda x : x.replace(",",""))
    
    data=data.to_dict('records')
    return render(request,'table_data.html',{"data" : data})



def index(request):
    return render(request,'index.html')