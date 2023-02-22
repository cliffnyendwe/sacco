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

from core_manager.models import IncomingPayments, User, CommisionTable
from promotions.models import Promotion, PromotionBonus
from chama.models import ChamaMembership, ChamaContributions, Invoices
from utils.gcm_module import android_notification


#import core.signals
from django.db.models import Q
from django.db.utils import IntegrityError

def commission_table():
    return CommisionTable.objects.all().order_by('minimum')
    
def calculate_commission(amount_required, commisions):
    commission_amount = 0
    for comm in commisions:        
        commission_amount = comm.commission
        if float(amount_required) <= float(comm.maximum):            
            break
            
    return commission_amount
    
def allocate_promotion_allowances(promotions, amount_required):
    valid_bonuses = []
    total_bonus = 0
    
    for promo in promotions:
        if promo.reward_percentage:
            amount_awarded = (float(promo.reward_percentage)/100.0)*float(amount_required)
            total_bonus = total_bonus + amount_awarded
            valid_bonuses.append({
                'promotion_id' : promo.id,
                'comission_amount' : amount_awarded,
            })
            
        if promo.reward_amount:
            total_bonus = total_bonus + promo.reward_amount            
            valid_bonuses.append({
                'promotion_id' : promo.id,
                'comission_amount' : promo.reward_amount,
            })
            
        """print payment.mpesa_amt
        print total_comission
        print type(total_comission)
        print type(payment.mpesa_amt)"""
    
    return valid_bonuses, total_bonus

def allocate_available_balance(user, total_available_amount, commisions, payment = None):
    pending_invoices = Invoices.objects.filter(payer= user, is_paid = False, chama_account__is_closed = False, is_archived = False).order_by('due_date')
    promotions = Promotion.objects.filter(active = True)
    
    payment_settled = False 
    
    if pending_invoices:    
        
        for invoice in pending_invoices:
            if total_available_amount >= invoice.amount_required:
                payment_settled = True
                total_bonus = 0
                total_available_amount = total_available_amount - invoice.amount_required
                amount_required = invoice.amount_required
                comission_amount = calculate_commission(amount_required, commisions)
                if promotions:
                    bonuses, total_bonus = allocate_promotion_allowances(promotions, amount_required)
                    for bonus in bonuses:
                        promotion_bonus = PromotionBonus(
                            circle_member_id = invoice.payer.id,
                            promotion_id = bonus['promotion_id'],
                            bonus_amount = bonus['comission_amount'],
                            invoice_id = invoice.id,
                        )
                        promotion_bonus.save()
                invoice.is_paid = True
                invoice.save()
                contribution = ChamaContributions(            
                    chama_account = invoice.chama_account,
                    paid_by = user,
                    mobile_number = payment.mpesa_msisdn if payment else None,
                    amount_paid = invoice.amount_required,
                    comission_amount = comission_amount,
                    bonus_amount = total_bonus,
                    transaction_type = 'Debit',
                )
                contribution.save()
                all_members = invoice.chama_account.chama_members
                for member in all_members:
                    if member.id == user.id:
                        notification_data = {
                            'amount' : invoice.amount_required,
                            'title' : "Payment Received",
                            'message' : "Ksh %s has been paid for %s membership" %(invoice.amount_required, invoice.chama_account.chama_name),
                        }            
                        android_notification("new_payment", invoice.chama_account.id, member, notification_data)
                    else:
                        notification_data = {
                            'amount' : invoice.amount_required,
                            'title' : "Payment Received",
                            'message' : "Ksh %s has been received from %s %s" %(invoice.amount_required, invoice.payer.first_name, invoice.payer.other_names),
                        }            
                        android_notification("new_payment", invoice.chama_account.id, member, notification_data)
                    if total_bonus:
                        notification_data = {
                            'amount' : comission_amount,
                            'title' : "Bonus Earned",
                            'message' : "Congratulations! %s circle has earned a bonus of Ksh %s" %(invoice.chama_account.chama_name, total_bonus),
                        }            
                        android_notification("bonus_earned", invoice.chama_account.id, member, notification_data)
                    
        user.suspense_balance = total_available_amount
        user.save()
    else:
        user.suspense_balance = total_available_amount
        user.save()
        
    if not payment_settled and payment: # meaning no invoice is due or the amount is too little to settle any
        notification_data = {
            'amount' : payment.mpesa_amt,
            'title' : "Payment Received",
            'message' : "Ksh %s has been received." %(float(payment.mpesa_amt)),
        }
        if not user.owed_payment:
            notification_data['message'] = "%s Since all your bills have been settled, the extra Ksh %s has been placed in a suspense account for future use" %(notification_data['message'], float(payment.mpesa_amt))
        else:            
            notification_data['message'] = "%s Kindly deposit an extra Ksh %s to clear all amounts due" %(notification_data['message'], (user.owed_payment - user.suspense_balance))        
        android_notification("new_payment", None, user, notification_data)


def process_incoming_payments():  

    commisions = commission_table()
    # process incoming payments
    unprocessed_payments = IncomingPayments.objects.filter(processed = False)
    for payment in unprocessed_payments:
        user = User.objects.filter(member_code = payment.mpesa_acc.strip()).first()
        if user:
            total_available_amount = user.suspense_balance + float(payment.mpesa_amt)
            allocate_available_balance(user, total_available_amount, commisions, payment)            
        else:
            # payments that didnt match existing user
            payment.pending = True
        payment.processed = True
        payment.save()
        
    # try settle invoiceswith suspense balances
    suspense_accounts = User.objects.filter(suspense_balance__gt=0)
    for user in suspense_accounts:
        allocate_available_balance(user, user.suspense_balance, commisions) 
    
if __name__ == '__main__':
    while True:        
        try:
            process_incoming_payments()
        except Exception, e:
            print e
        finally:
            print "completed processing"
        time.sleep(5) 
    
