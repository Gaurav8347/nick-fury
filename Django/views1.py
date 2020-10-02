from django.shortcuts import render, redirect
from .models import customer_dictionary
from django.contrib import messages
from django.contrib.auth.models import User, auth
import psycopg2
import mysql.connector
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def login(request):
    if request.method == 'POST':
        custid = request.POST['cid']
        pwd = request.POST['pwd']

        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="final year project"
            )
            mycursor = mydb.cursor()
            sql = "SELECT *  FROM registration "
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            for row in myresult:
                print(row)
                print("Name = ", row[0],
                      "id = ", row[1])
            val = row[1]
            mydb.commit()

            print("the value of value is", {'name:', 'val'})

        except (Exception, mysql.connector.Error) as error:
                print("Error while fetching data ", error)
        # closing database connection.


        return render(request, 'welcome.html', {'name': val})
    else:

        return render(request, 'login.html')
    #


