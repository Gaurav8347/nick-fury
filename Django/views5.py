from django.shortcuts import render, redirect
from .models import customer_dictionary
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import os
import numpy as np
import pandas as pd
def securityq(request):
    freq_fraud = 0
    path = 'C:/Users/ADMIN/PycharmProjects/ftd/ftd/accounts/'

    df = pd.read_csv(os.path.join(path, 'transactions.csv'))
    customer_df = pd.read_csv(os.path.join(path, 'customer_dictionary1.csv'))
    index=1
    if request.method == 'POST':
        dob = request.POST['dob']
        pob = request.POST['pob']
        mmn = request.POST['mmn']
        security_answers = []
        security_answers.append(dob)
        security_answers.append(pob)
        security_answers.append(mmn)

        # security_answers = prompt(security_questions, style=style)
        if ((security_answers[0] == customer_df['dob'].iloc[index]) and
                (security_answers[1] == customer_df['pob'].iloc[index]) and
                security_answers[2] == customer_df['mmn'].iloc[index]):
            print('Credentials verified. Transaction not fraud')
            customer_df['tx_this_month'].iloc[index] += 1
            #customer_df['current_month'].iloc[index] = current_month
            if freq_fraud == 1:
                customer_df['average_tx_per_month'].iloc[index] += 1

        else:
            print('Credentials mismatch. Transaction fraud.')
            return render(request, 'notdone.html')
    else:
        print('Transaction not fraud')
        # customer_df['tx_this_month'].iloc[index] += 1
        # customer_df['current_month'].iloc[index] = current_month
        # customer_df.to_csv(os.path.join(path, 'customer_dictionary1.csv'))


    return render(request, 'done.html')



