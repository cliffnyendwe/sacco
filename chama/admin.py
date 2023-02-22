from django.contrib import admin

from models import *
from utils.gcm_module import *
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django import forms
import time

class ChamaMembershipInline(admin.TabularInline):
    model = ChamaMembership
    #fields = ('amount_paid', 'is_penalty', 'date_paid', 'payment_notes')
    extra = 1

class ChamaAccountAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Create a new chama', 
            {
                'fields': ('chama_name', 'date_created', 'administrator', 'circle_currency', 'rotating_amount', 'payment_day', 'description', 'is_closed'),
                'classes': ('wide'),
            },
        )
    ]

    list_display = ('chama_name', 'description', 'date_created', 'administrator',
                    'rotating_amount', 'total_contribution', 'total_bonus', 'total_commission', 'contribution_cycle', 'payment_cycle_option', 'payment_cycle_choice', 'payment_day', 'close_circle')
    list_filter = ('date_created', )
    search_fields = ('chama_name', 'administrator__first_name', 'administrator__other_names')
    
    def close_circle(self, obj):
        if obj.is_admin_active or obj.is_closed == 1:
            return obj.is_closed
        else:
            return '<a href="../closedcircles/add/?chama_account=%s">Close Circle&raquo;</a>' % (obj.id)
    close_circle.short_description = "Is Closed"
    close_circle.allow_tags = True

class ChamaInvitationsAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Send Chama Invitation', 
            {
                'fields': ('chama_account', 'member_mobile', 'invited_by', 'invited_member', 'notified', 'invite_accepted', 'invite_rejected'),
                'classes': ('wide'),
            },
        )
    ]

    list_display = ('chama_account', 'member_mobile', 'invited_by', 'invited_member', 'notified', 'invite_accepted', 'invite_rejected')

    list_filter = ('chama_account', 'notified', 'invite_accepted', 'invite_rejected')
    search_fields = ('member_mobile', 'chama_account__chama_name')

class MemberAppprovalsAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Add Approval Request', 
            {
                'fields': ('chama_account', 'invited_member', 'member_to_approve', 'approved'),
                'classes': ('wide'),
            },
        )
    ]

    list_display = ('chama_account', 'invited_member', 'member_to_approve', 'approved')

    list_filter = ('chama_account', 'approved')
    search_fields = ('chama_account', 'invited_member__first_name', 'invited_member__other_names')

class ChamaContributionsCustom(admin.ModelAdmin):
    list_display = ('chama_account', 'paid_by', 'mobile_number', 'amount_paid', 'comission_amount', 'bonus_amount', 'transaction_type')

    list_filter = ('chama_account', 'paid_by', 'mobile_number', 'amount_paid', 'transaction_type')
    search_fields = ('chama_account__chama_name', 'paid_by__first_name', 'paid_by__other_names', 'paid_by__member_code', 'mobile_number', 'amount_paid', 'transaction_type')

class ChamaMembershipCustom(admin.ModelAdmin):
    list_display = ('member', 'chama_account', 'date_joined', 'total_contribution', 'last_invoice_date', 'total_reminders', 'is_active', 'approved')
    list_filter = ('date_joined', 'is_active')
    search_fields = ('member__first_name', 'member__other_names', 'chama_account__chama_name')
    
class InactiveMembershipCustom(admin.ModelAdmin):
    list_display = ('member', 'chama_account', 'date_joined', 'total_contribution', 'last_invoice_date', 'total_reminders', 'is_active', 'reactivate_membership')
    list_filter = ('date_joined', )
    search_fields = ('member__first_name', 'member__other_names', 'chama_account__chama_name')
    
    
    def reactivate_membership(self, obj):
        return '<a href="reactivate_member/%s/">Reactivate</a>' % (obj.id)
    reactivate_membership.short_description = ""
    reactivate_membership.allow_tags = True
    
    def get_queryset(self, request):
        qs = super(InactiveMembershipCustom, self).get_queryset(request)
        qs = qs.filter(is_active=False)   
        return qs
        
    def get_urls(self):
        from django.conf.urls import patterns, url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name
        urls = patterns('',
            url(r'^reactivate_member/(.+)/$', self.reactivate_member, name='%s_%s_reactivate_member' % info),
        )

        super_urls = super(InactiveMembershipCustom, self).get_urls()

        return urls + super_urls
        
    def reactivate_member(self, request, membership_id, form_url='', extra_context=None):
    
        membership = InactiveMembership.objects.filter(pk=membership_id).first()
        membership.is_active = True
        membership.save()
        
        Invoices.objects.filter(payer = membership.member, chama_account = membership.chama_account).update(is_archived=False, total_reminders = 0)
         
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
class InvoicesAdmin(admin.ModelAdmin): 
    list_display = ('payer', 'chama_account', 'currency', 'amount_required', 'due_date', 'contribution_cycle', 'is_paid', 'is_archived', 'last_notification_date')
    list_filter = ('payer', 'chama_account', 'due_date', 'is_paid', 'last_notification_date')
    search_fields = ('payer__first_name', 'payer__other_names','chama_account__chama_name')
    
    def currency(self, obj):
        return obj.chama_account.circle_currency.currency_code
        
    def contribution_cycle(self, obj):
        return obj.chama_account.contribution_cycle
    
        
class ChamaEmailsAdmin(admin.ModelAdmin): 
    
    list_display = ('mail_subject', 'mail_message', 'from_address', 'to_address', 'sent', 'response_status', 'date_created', 'date_sent')
    list_filter = ('sent', 'date_created', 'date_sent')
    search_fields = ('mail_subject', 'mail_message', 'from_address', 'to_address', 'sent', 'response_status', 'date_created', 'date_sent')
    
class ChamaNotificationsAdmin(admin.ModelAdmin): 
    fieldsets = [
        (
            'Add Notification', 
            {
                'fields': ('chama_account', 'recipient', 'title', 'message',),
                'classes': ('wide'),
            },
        )
    ]   
    list_display = ('chama_account', 'recipient', 'sent_by', 'title', 'message', 'sent', 'date_created', 'total_recipients')
    list_filter = ('sent', 'date_created')
    search_fields = ('sent_by__first_name', 'sent_by__other_names','chama_account__chama_name','title', 'message')
    
    def save_model(self, request, obj, form, change):
        #obj.save()
        obj.sent_by = request.user
        obj.save()
        
class NotificationLogAdmin(admin.ModelAdmin):    
    list_display = ('sent_to', 'message', 'date_sent')
    list_filter = ('date_sent',)
    
class UnpaidInvoicesAdmin(admin.ModelAdmin):
    list_display = ('photo_inline', 'username', 'email', 'mobile_number', 'first_name', 'other_names', 'member_code', 'unpaid_invoices', 'is_active')
    def photo_inline(self, obj):
        if obj.photo:
            return render_to_string('thumbnail.html', {
                'photo': obj.photo
            })
    photo_inline.short_description = "Photo"
    photo_inline.allow_tags = False
    
    def get_queryset(self, request):
        from django.db.models import F
        qs = super(UnpaidInvoicesAdmin, self).get_queryset(request)
        
        filtered = [x.pk for x in qs if x.unpaid_invoices > 0]
        
        qs = qs.filter(pk__in=filtered)   
        
        return qs
       

class ClosedCirclesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
      
       
        if not kwargs.get('initial'):
            kwargs['initial'] = {}
        
        #kwargs['initial'].update({'chama_account': kwargs.pop('circle_id')})
        super(ClosedCirclesForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ClosedCircles
        exclude = ('closed_by', 'date_closed', 'date_paid')

    def clean(self):
        payment_option = self.cleaned_data.get('payment_option')

        if not payment_option or len(payment_option) < 1:
            self.add_error('payment_option', "Payment option required")


        if(payment_option == 'BANK'):
            bank_name = self.cleaned_data.get('bank_name')
            account_name = self.cleaned_data.get('account_name')
            account_number = self.cleaned_data.get('account_number')
            bank_branch = self.cleaned_data.get('bank_branch')

            
            if(len(bank_name) < 1):            
                self.add_error('bank_name', "Bank name required")
            if(len(account_name) < 1):            
                self.add_error('account_name', "Account name required")
            if(len(account_number) < 1):            
                self.add_error('account_number', "Account number required")
            if(len(bank_branch) < 1):            
                self.add_error('bank_branch', "Bank branch required")
            
        if(payment_option == 'MPESA'):
            mpesa_number = self.cleaned_data.get('mpesa_number')
            national_id = self.cleaned_data.get('national_id')
            
            if(len(mpesa_number) < 1):            
                self.add_error('mpesa_number', "Mpesa number required")
            if(len(national_id) < 1):            
                self.add_error('national_id', "National ID required")
            
        return self.cleaned_data

    
class ClosedCirclesAdmin(admin.ModelAdmin):    
    list_display = ('chama_account', 'payment_option', 'bank_name', 'account_name', 'account_number', 'bank_branch', 'swift', 'mpesa_number', 'national_id',
    'closed_by', 'date_closed', 'is_paid', 'date_paid', 'comments')
    list_filter = ('is_paid', 'date_closed')
    
    form = ClosedCirclesForm
    
    #exclude = ('closed_by',)
    
    def save_model(self, request, obj, form, change):
        obj.closed_by = request.user
        obj.save()
        
        
        existing_members = ChamaMembership.objects.filter(chama_account__id = obj.chama_account.id, is_active = True)  

        membership1 = existing_members.first()
        extra_notification = ""
        for membership in existing_members:  
            if membership.member.total_active_memberships < 2:
                if membership.member.suspense_balance > 0.0:
                    extra_notification = "Your excess balance of Ksh %s is still in your excess funds account for future use." %(membership.member.suspense_balance)
                   
                
                
            close_message = close_message = """
Hi %s,

Circle %s is about to be closed in the next 24 hours. %s If you are not aware of this request, please contact us at 0724639639.""" %(membership.member, membership.chama_account, extra_notification)
            e_mail = ChamaEmails(
                mail_subject = "Circle %s Closed" %(membership.chama_account.chama_name),
                mail_message = close_message,
                from_address = 'circle@imaginarium.co.ke',
                to_address = membership.member.email,        
            )
            #e_mail.save()

            notification_data = {
                'title' : "Circle %s Closed" %(membership.chama_account.chama_name),
                'message' : "Circle %s is about to be closed in the next 24 hours. %s If you are not aware of this request, please contact us at 0724639639" \
                    %(membership.chama_account.chama_name, extra_notification),
            }
            #android_notification("close_circle", request.user.id, membership.member, notification_data)
            
            
        if membership1:
            closed_circle = membership.chama_account
            closed_circle.is_closed = True            
            closed_circle.save() 
            
            if float(membership.chama_account.total_contribution) > 0.0:  
                close_message = """
Hi Support,

A request has been placed to close a Circle with the following details:

Circle Name           : %s
Total Contribution    : %s
Date Closed           : %s

Please Log in to the system to process the request.""" %(closed_circle.chama_name, closed_circle.total_contribution, time.strftime("%d/%m/%Y %H:%M:%S"))


                """e_mail = ChamaEmails(
                    mail_subject = 'Request to close a Circle Account',
                    mail_message = close_message,
                    from_address = 'circle@imaginarium.co.ke',
                    to_address = 'circle@imaginarium.co.ke',        
                )
                e_mail.save() """
       

    
    
class SurveyListAdmin(admin.ModelAdmin):    
    list_display = ('survey_user', 'unpaid_invoices', 'completed')
    list_filter = ('completed', )
    
    change_list_template = 'surveylist_change_list.html'
    
    def surverlist_summary(self):
        s_list = {}
        survey_list = SurveyList.objects.filter()
        for s in survey_list:
            s_list[s.survey_user.id] = s.completed
        
        new = {}
        qs = User.objects.all()
        for x in qs:
            if x.unpaid_invoices > 4 and x.unpaid_invoices <= 8:
                new[x.id] = {
                    'member_names' : "%s %s" %(x.first_name, x.other_names),
                    'mobile_number' : x.mobile_number,
                    'unpaid_invoices' : x.unpaid_invoices,
                    'completed' : True if x.id in s_list else False
                }
          
        return new
        
    def get_urls(self):
        from django.conf.urls import patterns, url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name
        urls = patterns('',
            url(r'^(.+)/(.+)/complete_survey/$', self.complete_survey, name='%s_%s_complete_survey' % info),
        )

        super_urls = super(SurveyListAdmin, self).get_urls()

        return urls + super_urls
        
    def complete_survey(self, request, user_id, pending_count, form_url='', extra_context=None):
        sl = SurveyList.objects.create(
            survey_user_id = user_id, 
            unpaid_invoices=pending_count, 
            completed = True
        )
         
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    def changelist_view(self, request, extra_context=None):    
        extra_context = extra_context or {}                
        
        response = super(SurveyListAdmin, self).changelist_view(request, extra_context)        
        grade_scores = response.context_data["cl"].queryset
        
        extra_context['survey_list'] = self.surverlist_summary()
                
        return super(SurveyListAdmin, self).changelist_view(request, extra_context=extra_context)
        
class NoticeListAdmin(admin.ModelAdmin):    
    list_display = ('notice_user', 'unpaid_invoices', 'delivered')
    list_filter = ('delivered', )
    
    change_list_template = 'noticelist_change_list.html'
    
    def noticelist_summary(self):
        s_list = {}
        notice_list = NoticeList.objects.filter()
        for s in notice_list:
            s_list[s.notice_user.id] = s.delivered
        
        new = {}
        qs = User.objects.all()
        for x in qs:
            if x.unpaid_invoices > 8:
                new[x.id] = {
                    'member_names' : "%s %s" %(x.first_name, x.other_names),
                    'mobile_number' : x.mobile_number,
                    'unpaid_invoices' : x.unpaid_invoices,
                    'completed' : True if x.id in s_list else False
                }
          
        return new
        
    def get_urls(self):
        from django.conf.urls import patterns, url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name
        urls = patterns('',
            url(r'^(.+)/(.+)/deliver_notice/$', self.deliver_notice, name='%s_%s_deliver_notice' % info),
        )

        super_urls = super(NoticeListAdmin, self).get_urls()

        return urls + super_urls
        
    def deliver_notice(self, request, user_id, pending_count, form_url='', extra_context=None):
        sl = NoticeList.objects.create(
            notice_user_id = user_id, 
            unpaid_invoices=pending_count, 
            delivered = True
        )
         
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    def changelist_view(self, request, extra_context=None):    
        extra_context = extra_context or {}                
        
        response = super(NoticeListAdmin, self).changelist_view(request, extra_context)        
        grade_scores = response.context_data["cl"].queryset
        
        extra_context['notice_list'] = self.noticelist_summary()
                
        return super(NoticeListAdmin, self).changelist_view(request, extra_context=extra_context)

admin.site.register(ChamaContributions, ChamaContributionsCustom)
admin.site.register(ChamaAccount, ChamaAccountAdmin)
admin.site.register(ChamaInvitations, ChamaInvitationsAdmin)
admin.site.register(MemberAppprovals, MemberAppprovalsAdmin)
admin.site.register(ChamaMembership, ChamaMembershipCustom)
admin.site.register(InactiveMembership, InactiveMembershipCustom)
admin.site.register(Invoices, InvoicesAdmin)
admin.site.register(ChamaNotifications, ChamaNotificationsAdmin)
admin.site.register(ChamaEmails, ChamaEmailsAdmin)
admin.site.register(NotificationLog, NotificationLogAdmin)
admin.site.register(ClosedCircles, ClosedCirclesAdmin)
admin.site.register(UnpaidInvoices, UnpaidInvoicesAdmin)
admin.site.register(SurveyList, SurveyListAdmin)
admin.site.register(NoticeList, NoticeListAdmin)
