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

from core_manager.models import IncomingPayments, CardPaymentRequests, ClientCard
from utils.gcm_module import android_notification

from datetime import date, timedelta    
#import core.signals
from django.db.models import Q
from django.db.utils import IntegrityError
from django.core.mail import send_mail
import stripe


def process_card_payments():   
    stripe.api_key = "sk_test_PjihBU7d9QSj3d1qGpb5Tq74"

    pending_payments = CardPaymentRequests.objects.filter(is_processed = False)
    
    for payment in pending_payments:
        try:
            if payment.remember_card_details or payment.automatically_deduct:
                customer = stripe.Customer.create(
                  email=payment.card_owner.email,
                  source=payment.token_id,
                )
                
                card_, found_status = ClientCard.objects.get_or_create(  
                    card_owner = payment.card_owner
                )
                

                card_.customer_id = customer.id
                card_.card_number  = payment.card_number
                card_.automatically_deduct = payment.automatically_deduct
                card_.remember_card_details = payment.remember_card_details
                card_.save()
            
                #  date_created  = models.CharField(max_length=255)
            """charge = stripe.Charge.create(
              amount=payment.amount,
              currency="usd",
              description="Circle payment charge",
              source=payment.token_id,
            )
            if charge.paid:
                ip = IncomingPayments(
                    source = charge.source.object,
                    transaction_type = charge.source['brand'],
                    mpesa_amt = charge.amount,
                    tstamp = charge.created,
                    text = charge.description,
                    transaction_id = charge.id,
                    mpesa_acc = payment.card_owner.member_code
           
                )
                ip.save()      """      
            
        except Exception, e:
            notification_data = {
                'title' : "Error Processing Card Payment",
                'message' : "Error Processing Card Payment - %s" %str(e),
            }            
            android_notification("card_payment", payment.card_owner.id, payment.card_owner, notification_data)
        finally:
            payment.is_processed = True
            payment.save()

        
       
    
if __name__ == '__main__':
    while True:
        try:
            process_card_payments()
        except Exception, e:
            print e
        finally:
            print "completed processing"
        time.sleep(5)
