from core_manager.models import IncomingPayments, User, CircleCurrency
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions
import datetime
from django.db import IntegrityError
from utils import get_activation_code
    
class ValidateUserSerializer(serializers.ModelSerializer):
    owed_payment = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField('owed_payment_currency')
    
    def owed_payment_currency(self, obj):          
        view = self.context['view']      
        currency_id =  view.kwargs['currency_id'] if 'currency_id' in view.kwargs else "2" 
        user_currency = CircleCurrency.objects.filter(pk=currency_id).first()
        return user_currency.currency_code

    
    def get_owed_payment(self, obj):        
        import math
        view = self.context['view']
        currency_id =  view.kwargs['currency_id'] if 'currency_id' in view.kwargs else "1"        
        from chama.models import Invoices
        from chama.models import ChamaMembership
        total_payable = 0
        all_invoices = Invoices.objects.filter(is_paid = False, payer = obj, chama_account__is_closed = False)
        for invoice in all_invoices:
            membership = ChamaMembership.objects.filter(chama_account = invoice.chama_account, member = invoice.payer).first()
            if membership.is_active:
                total_payable +=(invoice.amount_required/float(invoice.chama_account.circle_currency.conversion_rate))
                
        
        user_currency = CircleCurrency.objects.filter(pk=currency_id).first()
        
        converted_amount = total_payable*float(user_currency.conversion_rate)

        return int(math.ceil(converted_amount))

    class Meta:
        model = get_user_model()
        fields = ('mobile_number', 'identity_number', 'first_name', 'other_names', 'member_code', 'owed_payment', 'currency')
        #read_only_fields = ('id', 'email', 'photo')
        
class PostTransactionSerializer(serializers.Serializer):
    """payment_day = serializers.CharField(max_length=128, allow_blank=True, required=False)
    currency_code = serializers.CharField(required=False, allow_blank=True)"""
    transaction_reference = serializers.CharField(source="transaction_id")
    membership_number = serializers.CharField(source="mpesa_acc")
    currency_code = serializers.CharField(allow_blank=False, write_only = True)
    amount_paid = serializers.CharField(source="mpesa_amt")
    timestamp = serializers.CharField(source="tstamp", write_only = True)
    confirmation_reference = serializers.CharField(allow_blank=True, required=False, read_only = True)
    class Meta:
        model = IncomingPayments
        fields = ('transaction_reference', 'membership_number', 'currency_code', 'amount_paid', 'timestamp', 'confirmation_reference')
        #read_only_fields = ('id', 'transaction_reference')
        
    def validate(self, attrs):
        import time
        membership_number = attrs.get('mpesa_acc')
        mpesa_amt = attrs.get('mpesa_amt')
        timestamp = attrs.get('tstamp')
        member = User.objects.filter(member_code = membership_number).first()
        
        def is_number(s):
            try:
                float(s) # for int, long and float
            except ValueError:
                try:
                    complex(s) # for complex
                except ValueError:
                    return False

            return True

        if not member:
            msg = _('Invalid membership number.')
            raise exceptions.ValidationError(msg)
            
        if not is_number(mpesa_amt):
            msg = _('Invalid Amount.')
            raise exceptions.ValidationError({'amount_paid': msg})
            
        
        date_string = ""
        try:
            date_object = datetime.datetime.fromtimestamp(int(timestamp))
            date_string = date_object.strftime('%Y-%m-%d %H:%M:%S')
            
            days_past = ((datetime.datetime.now() - date_object).days)

            if days_past > 2:
                msg = _('Invalid Timestamp - Attempt to push a very old transaction')
                raise exceptions.ValidationError({'timestamp': msg})
            
        except ValueError:
            msg = _('Invalid Timestamp.')
            raise exceptions.ValidationError({'timestamp': msg})
        
        return attrs
        
    
    def create(self, validated_data):
        payment = None
        try:
            payment = IncomingPayments.objects.create(
                transaction_id = validated_data['transaction_id'],
                mpesa_acc = validated_data['mpesa_acc'],
                currency_code = validated_data['currency_code'],
                mpesa_amt = validated_data['mpesa_amt'],
                source = 'ECB_BC', #eCOBANK BANK COLLECT
                tstamp = validated_data['tstamp'],
            )
            payment.save()
            payment.confirmation_reference = "%s%s" %(payment.id, get_activation_code(size = 6))
            payment.save()
        except IntegrityError as error:
            raise exceptions.ValidationError({'error': "Data Integrity Error: duplicate transaction"})
        
        return payment
