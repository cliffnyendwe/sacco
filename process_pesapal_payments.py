#!/usr/bin/env python
import os
import sys

import datetime

from os import path
from django.utils import timezone
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "circle.settings")

from django.core.management import execute_from_command_line

import django; django.setup()

from core_manager.models import IncomingPayments, PesaPalTransactions, PesaPalTransactionUsers, CircleCurrency

def process_incoming_payments():  

    unprocessed_payments = PesaPalTransactions.objects.filter(status = "COMPLETED", is_processed = False)
    #unprocessed_payments = PesaPalTransactions.objects.all().order_by('-id')
    
    for payment in unprocessed_payments:

        payment_user = PesaPalTransactionUsers.objects.filter(pk = payment.user_id).first()
        

        trans_timestamp = time.mktime(payment.date_initiated.timetuple())
        
        amount_before_commission = round((payment.amount * 100)/(100+4.5))
        
        currency = CircleCurrency.objects.filter(currency_code = payment.currency).first()
        try:
            incoming_p = IncomingPayments(            
                transaction_type = 'Pesapal',
                transaction_id = payment.tracking_id,
                tstamp = (int(trans_timestamp) * int('10000')),
                mpesa_amt = amount_before_commission,
                business_number = "",
                mpesa_acc = payment.member_code,
                mpesa_msisdn = payment_user.phone_number,
                mpesa_sender = "%s %s" %(payment_user.first_name, payment_user.last_name),
                source = payment.payment_method,
            )
            incoming_p.save()
            payment.is_processed = True
            payment.save()
        except Exception, e:
            print e
        finally:
            pass
        
    
    
if __name__ == '__main__':
    while True:   
             
        try:
            process_incoming_payments()
        except Exception, e:
            print e
        finally:
            print "completed processing"
        time.sleep(10) 
    
