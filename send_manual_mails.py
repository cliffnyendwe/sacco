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

from chama.models import ChamaEmails


from datetime import date, timedelta    

from django.core.mail import send_mail



def dispatch_manual_emails():   

    pending_mails = ChamaEmails.objects.filter(sent = False)
    
    for e_mail in pending_mails:
        status = send_mail(e_mail.mail_subject, e_mail.mail_message, e_mail.from_address, [e_mail.to_address], fail_silently=False)
	print status, e_mail.mail_subject
        e_mail.date_sent = datetime.datetime.now()
        e_mail.sent = True
        e_mail.response_status = status
        e_mail.save()
                            
      
if __name__ == '__main__':
    while True:
        try:
            dispatch_manual_emails()
        except Exception, e:
            print e
        finally:
            print "completed processing"
        time.sleep(30) 
    
