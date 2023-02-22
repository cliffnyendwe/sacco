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

from core_manager.models import IncomingPayments, User
from chama.models import ChamaMembership, ChamaContributions, Invoices, ChamaNotifications, NotificationLog
from utils.gcm_module import android_notification

from datetime import date, timedelta    
#import core.signals
from django.db.models import Q
from django.db.utils import IntegrityError


def dispatch_manual_notifications():   

    pending_notifications = ChamaNotifications.objects.filter(sent = False)
    
    for notification in pending_notifications:
        notification_data = {
            'message' : notification.message,
            'title' : notification.title,
        }
        if notification.chama_account:
            members = notification.chama_account.chama_members
        elif notification.recipient:
            members = [notification.recipient,]
        else:
            members = User.objects.all()
          
         
        for member in members:
            notification_log, found_status  = NotificationLog.objects.get_or_create(   
                sent_to_id = member.id,
                message = notification.message,                
            )
            if found_status:
                android_notification("manual_notification", None, member, notification_data)
                notification.total_recipients +=1
                notification.save()
                
        notification.sent = True
        notification.save()
                            
      
if __name__ == '__main__':
    while True:
        try:
            dispatch_manual_notifications()
        except Exception, e:
            print e
        finally:
            print "completed processing"
        time.sleep(30) 
    
