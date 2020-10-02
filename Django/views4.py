from __future__ import print_function, unicode_literals
from django.shortcuts import render, redirect
from .models import customer_dictionary
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.views.decorators.csrf import csrf_exempt

import regex
from pprint import pprint
import psycopg2
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
from pyfiglet import Figlet
import numpy as np
import pandas as pd
import os
import pickle
import warnings
import mysql.connector
# Create your views here.
indexi = ""
freq_fraud = 0
val = 0
#variables
customer_id = ""
gender = ""
average_amount = ""
average_tx_per_month = 0.0
dob = ""
pob = ""
mmn = ""
category = ""
tx_this_month = 0.0
current_month = ""
def carryt(request):
        if request.method == 'POST':
            aid = request.POST['aid']
            amt = request.POST['amt']

        warnings.filterwarnings('ignore')
        path = 'C:/Users/ADMIN/PycharmProjects/ftd/ftd/accounts/'
        df = pd.read_csv(os.path.join(path, 'transactions.csv'))
        #customer_df = pd.read_csv(os.path.join(path, 'customer_dictionary1.csv'))
        #data base connection
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="final year project"
            )
            print("connection established")
            cursor = mydb.cursor()
            sql = "SELECT   customer_id ,gender, average_amount ,average_tx_per_month ,dob ,pob ,mmn ,category ,tx_this_month, current_month,indexi FROM customer_main WHERE customer_id=%s  "
            cursor.execute(sql, (aid,))
            customer_df = cursor.fetchall()
            for row in customer_df:
                print("id = ", row[0],
                      "gender = ", row[1],
                      "index = ", row[10])
            global customer_id
            customer_id = row[0]
            global gender
            gender = row[1]
            global average_amount
            average_amount = row[2]
            global average_tx_per_month
            average_tx_per_month = float(row[3])
            global dob
            dob = row[4]
            global pob
            pob = row[5]
            global mmn
            mmn = row[6]
            global category
            category = int(row[7])
            global tx_this_month
            tx_this_month = int(row[8])
            global current_month
            current_month = int(row[9])
            global indexi
            indexi = row[10]

        except(Exception, mysql.connector.Error) as error:
                print("Error while fetching data ", error)
        # closing database connection.
        finally:
            if mydb:
                cursor.close()
                mydb.close()
                print("PostgreSQL connection is closed")

        freq_fraud = 0
        # Load Models from file
        pkl_filename = os.path.join(path, 'log_model.pkl')
        with open(pkl_filename, 'rb') as file:
            logmodel = pickle.load(file)
        pkl_filename = os.path.join(path, "svm_model.pkl")
        with open(pkl_filename, 'rb') as file:
            classifier_svm_linear = pickle.load(file)
        f = Figlet(font='slant')
        print(f.renderText('Smart  Banking'))
        #df = pd.read_csv('transactions.csv')
        #customer_df = pd.read_csv('customer_dictionary1.csv')

        style = style_from_dict({
            Token.QuestionMark: '#E91E63 bold',
            Token.Selected: '#673AB7 bold',
            Token.Instruction: '',  # default
            Token.Answer: '#2196f3 bold',
            Token.Question: '',
        })

        class PhoneNumberValidator(Validator):
            def validate(self, document):
                # ok = regex.match('^([01]{1})?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\s?((?:#|ext\.?\s?|x\.?\s?){1}(?:\d+)?)?$', document.text)
                ok = regex.match('^(\d{9})$', document.text)
                if not ok:
                    raise ValidationError(
                        message='Please enter a valid account number',
                        cursor_position=len(document.text))  # Move cursor to end

        class NumberValidator(Validator):
            def validate(self, document):
                try:
                    int(document.text)
                except ValueError:
                    raise ValidationError(
                        message='Please enter a number',
                        cursor_position=len(document.text))  # Move cursor to end

        class AmountValidator(Validator):
            def validate(self, document):
                ok = regex.match('^(\d*\.)?\d+$', document.text)
                if not ok:
                    raise ValidationError(
                        message='Please enter a valid amount',
                        cursor_position=len(document.text))  # Move cursor to end

        class CustomerValidator(Validator):
            def validate(self, document):
                # ok = regex.match('^([01]{1})?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\s?((?:#|ext\.?\s?|x\.?\s?){1}(?:\d+)?)?$', document.text)
                # ok = regex.match('^(\d{9})$', document.text)
                try:
                    int(document.text)
                except ValueError:
                    raise ValidationError(
                        message='Please enter a number',
                        cursor_position=len(document.text))  # Move cursor to end
                ok = regex.match('^(\d{9})$', document.text)
                if not ok:
                    raise ValidationError(
                        message='Please enter your 9 digit account number',
                        cursor_position=len(document.text))  # Move cursor to end
                ok = int(document.text) in list(customer_df['customer_id'])

                if not ok:
                    raise ValidationError(
                        message='Please enter a valid account number',
                        cursor_position=len(document.text))

        questions = [

            {
                'type': 'input',
                'name': 'customer_id',
                'message': 'Please enter your account number:',
                'validate': CustomerValidator
            },
            {
                'type': 'input',
                'name': 'amount',
                'message': 'Please enter the amount to be withdrawn:',
                'validate': AmountValidator
            }

        ]

        security_questions = [

            {
                'type': 'input',
                'name': 'dob',
                'message': 'Please enter your date of birth (dd/mm/yyyy):'
            },
            {
                'type': 'input',
                'name': 'pob',
                'message': 'Please enter your city of birth:'
            },
            {
                'type': 'input',
                'name': 'mmn',
                'message': 'Please enter your Mother\'s maiden name:'
            }

        ]

        print('Hi, welcome to Smart Banking System')
        #answers = prompt(questions, style=style)

        answers = []
        answers.append(aid)
        answers.append(amt)
        print(answers)
        print("This cust id is done", answers[0])
        #answers = prompt(questions, style=style)  # answer is dict
        # print("This is answer",answers)
        #index = list(np.where(customer_df == int(answers[0]))[0])[0]
        index = indexi
        print("index value 2 time", )
        df_predict = pd.DataFrame()
        print(df_predict)
        gender = 1 if gender == 'Male' else 0
        amount = float(answers[1])
        df_predict['gender'] = None
        df_predict['amount'] = None
        df_predict['average_amount'] = None
        df_predict['customer_category'] = None
        customer_category = category
        df_predict = df_predict.append({'gender': int(gender), 'amount': amount, 'average_amount': average_amount,
                                        'customer_category': int(customer_category)}, ignore_index=True)
        print(df_predict)  # printing the values
        SVM_prediction = classifier_svm_linear.predict(df_predict)
        log_prediction = logmodel.predict(df_predict)
        print(SVM_prediction,
              log_prediction)  # you can comment out this line if you don't want to see the model predictions
        # global current_month
        current_month1 = int(pd.datetime.now().strftime("%m"))
        print(current_month)
        tx_this_month = tx_this_month+1
        print("*****", tx_this_month)
        #if (int(current_month) == int(customer_df['current_month'].iloc[index])):
        if int(amount) < float(average_amount) :
            if (tx_this_month <3):
                try:
                    mydb = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        passwd="",
                        database="final year project"
                    )
                    print("connection established")
                    cursor = mydb.cursor()
                    sql = "UPDATE customer_main Set tx_this_month=%s   Where customer_id =%s  "
                    cursor.execute(sql, (tx_this_month, customer_id))
                except(Exception, psycopg2.Error) as error:
                    print("Error while fetching data ", error)
                    # closing database connection.
                finally:
                    if mydb:
                        cursor.close()
                        mydb.close()
                    print("SQL connection is closed")
                return render(request, 'done.html')
            else:
                 return render(request, 'securityq.html')
        else:
            if (int(current_month1) == int(current_month)):
                if customer_df['tx_this_month'] <= customer_df['average_tx_per_month']:
                    pass
                else:
                    freq_fraud = 1
            else:
                tx_this_month = 0
                current_month = current_month1

            if (SVM_prediction == 1 or log_prediction == 1 or freq_fraud == 1 or tx_this_month > 3):
                print(
                    'Something\'s doesn\'t seem right. would you mind answering a few security questions so that we know it\'s really you.\n'
                    '')


            return render(request, 'securityq.html')

def securityq(request):
    path = 'C:/Users/ADMIN/PycharmProjects/ftd/ftd/accounts/'
    customer_df = pd.read_csv(os.path.join(path, 'customer_dictionary1.csv'))
    df = pd.read_csv(os.path.join(path, 'transactions.csv'))
    index = indexi
    global pob, dob, mmn, customer_id

    if request.method == 'POST':
        dob1 = request.POST['dob']
        pob1 = request.POST['pob']
        mmn1 = request.POST['mmn']
        security_answers = []
        security_answers.append(dob1)
        security_answers.append(pob1)
        security_answers.append(mmn1)
        print("The input value", security_answers)
        print("This is actual value", dob, pob, mmn)
        #security_answers = prompt(security_questions, style=style)
        if ((security_answers[0] == dob) and
            (security_answers[1] == pob) and
            security_answers[2] == mmn):
            print('Credentials verified. Transaction not fraud')
            global tx_this_month
            tx_this_month = int(tx_this_month) + 1
            print(tx_this_month)
            print(customer_id)
            try:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    passwd="",
                    database="final year project"
                )
                print("connection established")
                cursor = mydb.cursor()
                sql = "UPDATE customer_main Set tx_this_month=%s   Where customer_id =%s  "
                cursor.execute(sql, (tx_this_month, customer_id))
            except(Exception, psycopg2.Error) as error:
                print("Error while fetching data from PostgreSQL", error)
                # closing database connection.
            finally:
                if mydb:
                    cursor.close()
                    mydb.close()
                print("PostgreSQL connection is closed")

            global current_month
            current_month = int(pd.datetime.now().strftime("%m"))
            current_month = current_month
            global freq_fraud
            freq_fraud = 0
            if freq_fraud == 1:
                average_tx_per_month += 1
            return render(request, 'done.html')

        else:
            print('Credentials mismatch. Transaction fraud.')
            return render(request, 'notdone.html')
    else:
        print('Transaction not fraud')
        tx_this_month = int(tx_this_month) + 1
        customer_df.to_csv(os.path.join(path, 'customer_dictionary1.csv'))
        return render(request, 'done.html')




#UPDATE `customer_main` SET tx_this_month =0 WHERE indexi=


