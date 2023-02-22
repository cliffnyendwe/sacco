#!/usr/bin/env python
import os
import sys

import datetime
import uuid
from os import path
from django.utils import timezone
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "circle.settings")

from django.core.management import execute_from_command_line

import django; django.setup()

from core_manager.models import IncomingPayments, User
from chama.models import ChamaMembership, ChamaContributions, Invoices
from chama.models import ChamaEmails
from utils.gcm_module import android_notification

from datetime import date, timedelta    
#import core.signals
from django.db.models import Q
from django.db.utils import IntegrityError
from django.core.mail import send_mail

today_ = date.today()

def generate_invoices():   

    
    
    ###notification_days = (0, 1, 2, 3, 4)
    notification_days = (0, 1, 2, 3, 4, -7, -14, -21, -28)

    pending_invoices = Invoices.objects.filter(is_paid = False, chama_account__is_closed = False, is_archived = False, chama_account__payment_cycle_option = 'Monthly')
    
    #print pending_invoices
    
    for invoice in pending_invoices:
        negative_notification_day = False
        
        if invoice.last_notification_date == today_:
            continue
        
        notification_interval = invoice.due_date - today_
        notification_interval = notification_interval.days
        
        notification_data = {
            'amount' : invoice.amount_required,
            'title' : "Payment Reminder",
            'message': "Kindly pay %s. %s for your %s membership and earn your Circle bonus!" %(invoice.chama_account.circle_currency.currency_code, invoice.amount_required, invoice.chama_account.chama_name)

        }
       

        if(notification_interval < 0):
            negative_notification_day = (abs(notification_interval) % 7) == 0 # remove negative            

        ####if notification_interval in notification_days or notification_interval < 0:
        if (notification_interval in notification_days) or negative_notification_day:
            android_notification("payment_reminder", invoice.chama_account.id, invoice.payer, notification_data)
            
            invoice.total_reminders = invoice.total_reminders + 1

            if invoice.total_reminders > 12:

                m = ChamaMembership.objects.filter(chama_account=invoice.chama_account, member = invoice.payer).first()
                m.is_active = False
                m.save()
                invoice.total_reminders = 12
                invoice.is_archived = True
                invoice.save()
                
                email_message = """
Dear %s,

We have noticed that your %s membership has been inactive for some time. Your membership has been suspended.

In order to reactivate your membership, please contact us as soon as possible and share your feedback, and we shall be happy to restore your membership. We would like to help you commit to your saving goals better.

Thanks for using Circle and we hope to hear from you again soon.

Regards,

Circle Team.""" %(invoice.payer.first_name, invoice.chama_account.chama_name)

                
                e_mail = ChamaEmails(
                    mail_subject = "Inactive Membership",
                    mail_message = email_message,
                    from_address = 'circle@imaginarium.co.ke',
                    to_address = invoice.payer.email,        
                )
                e_mail.save()

                continue
                
            #print invoice.payer, "--", negative_notification_day, "--", invoice.total_reminders
            invoice.last_notification_date = today_
            invoice.save()
            
            reference_hash = str(uuid.uuid4())
            
            if invoice.payer.email:
                pesapal_link = "http://146.185.169.101:8083/pesapal/pesapal_iframe.php?amount=%s&first_name=%s&last_name=%s&email=%s&phone_number=%s&currency=%s&member_code=%s&reference=%s%s" %(invoice.chama_account.rotating_amount, invoice.payer.first_name, invoice.payer.other_names, invoice.payer.email, invoice.payer.mobile_number, invoice.chama_account.circle_currency.currency_code, invoice.payer.member_code,  invoice.payer.member_code, reference_hash)
                email_message = """
Hi %s,

Please pay %s %s for your %s circle and earn your bonus instantly!

Paybill number: 179126

Your M-pesa account number: %s

OR: You can use Airtel money or your credit/debit card by following this link: %s 

Your due date for payment is %s.

Happy saving!
                """ %(invoice.payer.first_name, invoice.chama_account.circle_currency.currency_code, invoice.amount_required, invoice.chama_account.chama_name, invoice.payer.member_code, pesapal_link, invoice.due_date)

                
                e_mail = ChamaEmails(
                    mail_subject = "Payment Reminder",
                    mail_message = email_message,
                    from_address = 'circle@imaginarium.co.ke',
                    to_address = invoice.payer.email,        
                )
                e_mail.save()
    
if __name__ == '__main__':
    while True:
        today_ = date.today()
        #today_ += datetime.timedelta(days=1)

        try:
            generate_invoices()
        except Exception, e:
            print e
        finally:
            print "completed processing"
        time.sleep(2)
    
