from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from models import *


class IncomingPaymentsAdmin(admin.ModelAdmin): 
    fieldsets = [
        (None, {'fields': ['transaction_id', 'orig', 'dest', 'tstamp', 'mpesa_acc', 'mpesa_code', 'mpesa_msisdn' 'mpesa_amt', 'processed', 'pending']}),         
    ]
    list_display = ('transaction_id', 'orig', 'dest', 'tstamp', 'mpesa_acc', 'mpesa_code', 'mpesa_msisdn', 'mpesa_amt', 'currency_code', 'processed', 'pending')
    
    list_filter = ('processed', 'pending')
    
    search_fields = ('orig', 'dest', 'mpesa_acc', 'mpesa_msisdn')
  
class PaymentAccountAdmin(admin.ModelAdmin): 
    fieldsets = [
        (None, {'fields': ['account_number', 'account_name', 'date_created']}),         
    ]
    list_display = ('account_number', 'account_name', 'date_created')
    
class UserAdminCustom(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'other_names', 'email',
                                         'mobile_number', 'identity_number', 'photo')}),
        (_('Financial info'), {'fields': ('suspense_balance', 'android_device_id')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),

        (_('Personal info'), {'fields': ('other_names', 'first_name', 'email',
                                         'mobile_number', 'identity_number', 'photo')}),
        (_('Financial info'), {'fields': ('suspense_balance',)}),
                                         
                                         
    )
    
        
    
    
    list_display = ('photo_inline', 'username', 'email', 'mobile_number', 'identity_number', 'first_name', 'other_names', 'member_code', 'suspense_balance', 'owed_payment', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active',
                   'groups')
    search_fields = ('username', 'other_names', 'first_name', 'email',
                     'mobile_number', 'identity_number', 'member_code')
    ordering = ('-is_superuser', '-is_staff', 'username')
    filter_horizontal = ('groups', 'user_permissions',)
    
    def photo_inline(self, obj):
        if obj.photo:
            return render_to_string('thumbnail.html', {
                'photo': obj.photo
            })
    photo_inline.short_description = "Photo"
    photo_inline.allow_tags = False
    
class CommisionTableAdmin(admin.ModelAdmin): 
    fieldsets = [
        (None, {'fields': ['minimum', 'maximum', 'commission']}),         
    ]
    list_display = ('minimum', 'maximum', 'commission')
    
class CardPaymentRequestsAdmin(admin.ModelAdmin): 
    fieldsets = [
        (None, {'fields': ['token_id', 'live_mode', 'token_used', 'date_created', 'trans_type', 'card_brand', 'amount', 'card_owner', 'card_number', 'automatically_deduct', 'remember_card_details', 'is_processed']}),         
    ]
    list_display = ('token_id', 'live_mode', 'token_used', 'date_created', 'trans_type', 'card_brand', 'amount', 'card_owner', 'card_number', 'automatically_deduct', 'remember_card_details', 'is_processed')
    
class ClientCardAdmin(admin.ModelAdmin): 
    fieldsets = [
        (None, {'fields': ['card_owner', 'customer_id', 'card_number', 'automatically_deduct', 'remember_card_details', 'date_created']}),         
    ]
    list_display = ('card_owner', 'customer_id', 'card_number', 'automatically_deduct', 'remember_card_details', 'date_created')
    
class PesaPalTransactionsAdmin(admin.ModelAdmin):    
    list_display = ('currency', 'amount', 'status', 'reference_number', 'tracking_id', 'payment_method', 'user_id', 'member_code', 'date_initiated', 'is_processed')

class PesaPalTransactionUsersAdmin(admin.ModelAdmin):    
    list_display = ('first_name', 'last_name', 'email', 'phone_number')
    
class CurrencyAdminCustom(admin.ModelAdmin):    
    fieldsets = [
        (None, {
            'fields': ['currency_code', 'currency_name', 'currency_symbol', 'conversion_rate', 'is_base_currency', 'is_active']
        })
    ]   

    list_display = ('currency_code', 'currency_name', 'currency_symbol', 'conversion_rate', 'is_base_currency', 'is_active')
    search_fields = ('currency_code', 'currency_name', 'currency_symbol', 'conversion_rate', 'is_base_currency')

admin.site.register(PesaPalTransactions, PesaPalTransactionsAdmin)
admin.site.register(PesaPalTransactionUsers, PesaPalTransactionUsersAdmin)
admin.site.register(IncomingPayments, IncomingPaymentsAdmin)
admin.site.register(PaymentAccount, PaymentAccountAdmin)
admin.site.register(CommisionTable, CommisionTableAdmin)
admin.site.register(ClientCard, ClientCardAdmin)
admin.site.register(User, UserAdminCustom)
admin.site.register(CardPaymentRequests, CardPaymentRequestsAdmin)
admin.site.register(CircleCurrency, CurrencyAdminCustom)
