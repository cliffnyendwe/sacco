#!/usr/bin/env python
import os
import sys

import datetime

import uuid

from dateutil import relativedelta

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
from calendar import monthrange

def get_last_day_of_current_date():
    date_ = date.today()
    range_date = monthrange(date_.year, date_.month)
    return range_date[1]
    

def generate_incoice_date(last_invoice_date, payment_day):
    last_day_of_month = get_last_day_of_current_date()
    
    if payment_day == 1:
        payment_day = 2
    
    if not last_invoice_date:
        
        date_ = date.today()
        try:
            due_date = date(date_.year, date_.month, payment_day or 1)
        except ValueError, e:

            range_date = monthrange(date_.year, date_.month)
            payment_day =  range_date[1]
            due_date = date(date_.year, date_.month, payment_day or 1)
        
    else:
        #next_month = last_invoice_date + timedelta(days=last_day_of_month)
        next_month = last_invoice_date + relativedelta.relativedelta(months=1)
        try:
            due_date = date(next_month.year, next_month.month, payment_day or 1)
        except ValueError, e:
            range_date = monthrange(next_month.year, next_month.month)
            payment_day =  range_date[1]
            due_date = date(next_month.year, next_month.month, payment_day or 1)    
        delta = due_date - date.today()

        if delta.days > 5:
            return False
        else:
            return due_date
        
    return due_date

def generate_invoices():   
    
    #memberships = ChamaMembership.objects.filter(chama_account__is_closed = False)
    memberships = ChamaMembership.objects.filter(chama_account__is_closed = False, is_active = True)
    
    for membership in memberships:
    
        """if not (membership.id == 218 or membership.id == 219 or membership.id == 257):
            continue """
        """if not (membership.id == 422):
            continue"""
        due_date = generate_incoice_date(membership.last_invoice_date, membership.chama_account.payment_day)
        if due_date:
            invoice = Invoices(
                payer = membership.member,
                chama_account = membership.chama_account,
                amount_required = membership.chama_account.rotating_amount,
                due_date = due_date,
            )
            invoice.save()
            membership.last_invoice_date = due_date
            membership.save()
            notification_data = {
                'amount' : membership.chama_account.rotating_amount,
                'title' : "Payment Required",
                'message' : "Kindly pay Ksh. %s for your %s membership and earn your Circle bonus!" %(membership.chama_account.rotating_amount, membership.chama_account.chama_name)
            }
            
            reference_hash = str(uuid.uuid4())
            android_notification("new_invoice", membership.chama_account.id, membership.member, notification_data)
            
            if membership.member.email:
                pesapal_link = "http://146.185.169.101:8083/pesapal/pesapal_iframe.php?amount=%s&first_name=%s&last_name=%s&email=%s&phone_number=%s&currency=%s&member_code=%s&reference=%s%s" %(membership.chama_account.rotating_amount, membership.member.first_name, membership.member.other_names, membership.member.email, membership.member.mobile_number, membership.chama_account.circle_currency.currency_code, membership.member.member_code,  membership.member.member_code, reference_hash)
                
                email_message = """
Hi %s,

Please pay %s %s for your %s circle and earn your bonus instantly!

Paybill number: 179126

Your M-pesa account number: %s

OR: You can use Airtel money or your credit/debit card by following this link: %s 

Your due date for payment is %s.

Happy saving!
                """ %(membership.member.first_name, membership.chama_account.circle_currency.currency_symbol, membership.chama_account.rotating_amount, membership.chama_account.chama_name, membership.member.member_code, pesapal_link, due_date)

                
                e_mail = ChamaEmails(
                    mail_subject = "Payment Required",
                    mail_message = email_message,
                    from_address = 'circle@imaginarium.co.ke',
                    to_address = membership.member.email,        
                )
                e_mail.save()
    
if __name__ == '__main__':
    
    while True:
        try:
            generate_invoices()
        except Exception, e:
            print e
        finally:
            print "completed processing"
        time.sleep(15) 
    
