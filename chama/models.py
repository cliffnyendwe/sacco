from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from core_manager.models import Transaction
from utils import get_activation_code, ordinal_day
from core_manager.models import User
from django.db.models import Sum

class ChamaAccount(models.Model):
    chama_name = models.CharField(max_length=200, unique=False)
    account_number = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=False, null=True)
    date_created = models.DateTimeField(_('date created'), default=timezone.now)
    administrator = models.ForeignKey(User)
    rotating_amount = models.FloatField(blank=True, default=0)
    #total_contribution = models.FloatField(blank=True, default=0)
    members = models.ManyToManyField(User, related_name="chama_member", through='ChamaMembership')
    contributions = models.ForeignKey('ChamaContributions', null=True)
    payment_day = models.CharField(max_length=150, null=True) # payment date every month - restore to 5 after adding to api
    circle_currency = models.ForeignKey('core_manager.CircleCurrency', null=True)
    payment_cycle_option = models.CharField(max_length=150, null=True)
    payment_cycle_choice = models.CharField(max_length=150, null=True)
    is_closed = models.IntegerField(blank=True, default=0) # 0 - closed, 1- awaiting close processing - members nitified, 2 - filly closed 
    
    class Meta:
        verbose_name = 'Chama Account'
        verbose_name_plural = 'Chama Accounts'
        
    def __str__(self):             
        return "%s" %(self.chama_name)
        
    def __unicode__(self):
        return "%s" %(self.chama_name)
        
    def dayNameFromWeekday(self, weekday):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        return days[int(weekday)-1]
        
    def ordinal(self, n):

        suffix = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th']

        if n < 0:
            n *= -1

        n = int(n)

        if n % 100 in (11,12,13):
            s = 'th'
        else:
            s = suffix[n % 10]

        return str(n) + s
        
    @property   
    def contribution_cycle(self):
        cycle_label = self.payment_cycle_option
        if(cycle_label == 'Weekly') :
            cycle_label = "%s (%s)" %(cycle_label, self.dayNameFromWeekday(self.payment_cycle_choice))
        if(cycle_label == 'Monthly') :
            cycle_label = "%s (%s)" %(cycle_label, ordinal_day(self.payment_cycle_choice))
        return cycle_label
     
    @property   
    def total_commission(self):
        comission_amount = ChamaContributions.objects.filter(chama_account__id=self.id).aggregate(total_comission = Sum('comission_amount'))
        return comission_amount['total_comission'] or 0.0
        
    @property   
    def total_bonus(self):
        bonus_amount = ChamaContributions.objects.filter(chama_account__id=self.id).aggregate(total_bonus = Sum('bonus_amount'))
        return bonus_amount['total_bonus'] or 0.0
    
    @property   
    def is_admin_active(self):
        active_admin = ChamaMembership.objects.filter(chama_account__id=self.id, member_id = self.administrator_id, is_active = True).first()
        
        return True if active_admin else False
        
    @property
    def total_contribution(self):
        total_contribution = ChamaContributions.objects.filter(chama_account__id=self.id).aggregate(total_contribution = Sum('amount_paid'))
        amount_deposited = total_contribution['total_contribution'] or 0.0
        return amount_deposited - self.total_commission + self.total_bonus
        
    @property
    def chama_members(self):
        members = []
        memberships = ChamaMembership.objects.filter(chama_account = self)
        for membership in memberships:
            members.append(membership.member)
        return members
        
    @property    
    def total_members(self):
        return self.members.count()

    def save(self, * args, ** kwargs):
        if not self.account_number:
            self.account_number = get_activation_code(size = 6)        
        super(ChamaAccount, self).save( * args, ** kwargs)

class ChamaMembership(models.Model):
    chama_account = models.ForeignKey('ChamaAccount')
    member = models.ForeignKey(User)
    date_joined = models.DateTimeField(_('date_joined'), default=timezone.now)
    current_balance = models.FloatField(default=0, blank=True)
    approved = models.BooleanField(default=False)
    last_invoice_date =  models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('chama_account', 'member')
        verbose_name = 'Chama Membership'
        verbose_name_plural = 'Chama Memberships'
        
    def __str__(self):             
        return "%s - %s" %(self.chama_account, self.member)
        
    def __unicode__(self):
        return "%s - %s" %(self.chama_account, self.member)
        
    @property
    def is_closed(self):
        return True if self.chama_account.is_closed else False
        
    @property
    def is_active_status(self):
        return 1 if self.is_active else 0
        
    @property
    def due_date(self):
        total_payable = 0
        #total_contribution = ChamaContributions.objects.filter(paid_by__id=self.member.id, chama_account = self.chama_account).aggregate(total_contribution = Sum('amount_paid'))
        last_invoice = Invoices.objects.filter(payer = self.member, chama_account = self.chama_account, is_archived = False).order_by('-due_date').first()
        
        if last_invoice:
            if(self.chama_account.payment_cycle_option == 'Weekly'):
                formatted_date = last_invoice.due_date.strftime("%a, >> %b '%y")
            else:
                formatted_date = last_invoice.due_date.strftime(">> %b '%y")
                
            ordial_string = ordinal_day(last_invoice.due_date.day)
            formatted_date = formatted_date.replace(">>", ordial_string)
            return formatted_date
        return ""
        
    @property
    def owed_payment(self):
        total_payable = 0
        all_invoices = Invoices.objects.filter(is_paid = False, payer = self.member, chama_account = self.chama_account, is_archived = False)
        for invoice in all_invoices:
            total_payable +=invoice.amount_required
        return total_payable
        

    def withdrawn_amount(self):   
        total_withdrawn = 0 
        closed_circle = ClosedCircles.objects.filter(is_paid = True, chama_account = self.chama_account).first()
        
        if closed_circle:
            total_contribution = ChamaContributions.objects.filter(paid_by__id=self.member.id, \
                chama_account = closed_circle.chama_account).aggregate(total_contribution = Sum('amount_paid'))
                
            tc = total_contribution['total_contribution'] or 0.0
            total_withdrawn = tc - self.total_commission + self.total_bonus
        return total_withdrawn
        

    def total_reminders(self):
    
        reminders = Invoices.objects.filter(is_paid = False, payer = self.member, chama_account = self.chama_account).aggregate(reminders_sum = Sum('total_reminders'))
        
        return reminders['reminders_sum'] if reminders['reminders_sum'] else 0
        
        
    @property   
    def total_commission(self):
        comission_amount = ChamaContributions.objects.filter(paid_by__id=self.member.id, chama_account = self.chama_account).aggregate(total_comission = Sum('comission_amount'))
        return comission_amount['total_comission'] or 0.0
        
    @property   
    def total_bonus(self):
        bonus_amount = ChamaContributions.objects.filter(paid_by__id=self.member.id, chama_account = self.chama_account).aggregate(total_bonus = Sum('bonus_amount'))
        return bonus_amount['total_bonus'] or 0.0
        
    @property
    def total_contribution(self):
        total_contribution = ChamaContributions.objects.filter(paid_by__id=self.member.id, chama_account = self.chama_account).aggregate(total_contribution = Sum('amount_paid'))
        amount_deposited = total_contribution['total_contribution'] or 0.0
        return amount_deposited - self.total_commission + self.total_bonus
        
class InactiveMembership(ChamaMembership):
    class Meta:
        verbose_name = 'Inactive Membership'
        verbose_name_plural = 'Inactive Memberships'
        default_permissions = ('add', 'change', 'delete', 'view')
        proxy = True

class ChamaContributions(models.Model):
    chama_account = models.ForeignKey('ChamaAccount')
    paid_by = models.ForeignKey(User)
    mobile_number = models.CharField(max_length=150, blank = True, null = True)
    amount_paid = models.FloatField(default=0, blank=True)
    transaction_type = models.CharField(_('transaction_type'), max_length=6, blank=True,
                              choices=(('Debit', 'Debit'), ('Credit', 'Credit')))
                              
    comission_amount = models.FloatField(default=0, blank=True)
    
    bonus_amount = models.FloatField(default=0, blank=True)
    
    date_paid = models.DateTimeField(_('date paid'), default=timezone.now)

    class Meta:
        verbose_name = 'Chama Contribution'
        verbose_name_plural = 'Chama Contributions'
    def __str__(self):             
        return "%s - %s" %(self.chama_account, self.amount_paid)

class ChamaInvitations(models.Model):
    chama_account = models.ForeignKey('ChamaAccount')
    member_mobile = models.CharField(max_length=100, unique=False)
    invited_by = models.ForeignKey(User, related_name="invite_by")
    invited_member = models.ForeignKey(User, related_name="invite_member", blank=True, null=True) # this will be filled after member registration/acceptance of invite
    notified = models.BooleanField(default=False)
    invite_accepted = models.BooleanField(default=False)
    invite_rejected = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'Chama Invitation'
        verbose_name_plural = 'Chama Invitations'
        unique_together = (("chama_account", "member_mobile"),)

    def send_invitations(self):
        for member in self.chama_account.chamamembership_set.all():
            approval = MemberAppprovals(
                invited_member = self.invited_member,
                chama_account = self.chama_account,
                member_to_approve = member.member,
            )
            approval.save()
        
    def __init__(self, *args, **kwargs):
        super(ChamaInvitations, self).__init__(*args, **kwargs)
        #self.invite_accepted_previous = self.invite_accepted
    def save(self, * args, ** kwargs):
        super(ChamaInvitations, self).save( * args, ** kwargs)
        """if self.invite_accepted:
            self.send_invitations()"""


# member will signup to chama system, get invite after loogin. When invite is accepted, 
# member approvalsare recorder and sent out to already registered members for that chama
class MemberAppprovals(models.Model):
    invited_member = models.ForeignKey(User, related_name="invited_member")
    chama_account = models.ForeignKey('ChamaAccount')
    member_to_approve = models.ForeignKey(User, related_name="member_to_approve")
    approved = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Chama Member Approval'
        verbose_name_plural = 'Chama Member Approvals'
        unique_together = (("invited_member", "chama_account", "member_to_approve"),)
        

class Invoices(models.Model):
    payer = models.ForeignKey(User)
    chama_account = models.ForeignKey('ChamaAccount')
    amount_required = models.FloatField(default=0, blank=True)
    is_paid = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    due_date = models.DateField()
    last_notification_date =  models.DateField(blank=True, null=True)
    total_reminders = models.IntegerField(blank=True, default=0)
    #invoice_currency = models.ForeignKey('core_manager.CircleCurrency', null=True)

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
    def __str__(self):             
        return "%s - %s" %(self.payer, self.chama_account)
        
class ChamaEmails(models.Model):
    mail_subject = models.CharField(max_length=255,blank=False)
    mail_message = models.TextField(blank=False)    
    from_address = models.CharField(max_length=255,blank=False)
    response_status = models.CharField(max_length=255,blank=False)
    to_address = models.CharField(max_length=255,blank=False)
    sent = models.BooleanField(default=False)
    date_created = models.DateTimeField(_('date created'), default=timezone.now)
    date_sent = models.DateTimeField(_('date sent'), null=True)
    class Meta:
        verbose_name = 'Chama Emails'
        verbose_name_plural = 'Chama Emails'  
        
        
class ChamaNotifications(models.Model):
    chama_account = models.ForeignKey('ChamaAccount', blank=True, null=True)
    recipient = models.ForeignKey(User, related_name="recipient", blank=True, null=True)
    sent_by = models.ForeignKey(User, related_name="sent_by", blank=True, null=True)
    title = models.CharField(max_length=255,blank=False)
    message = models.TextField(blank=False)
    sent = models.BooleanField(default=False)
    date_created = models.DateTimeField(_('date created'), default=timezone.now)
    total_recipients = models.IntegerField(blank=True, default=0)
    class Meta:
        verbose_name = 'Chama Notifications'
        verbose_name_plural = 'Chama Notifications'  
        
class NotificationLog(models.Model):
    sent_to = models.ForeignKey(User, related_name="sent_to", blank=True, null=True)
    message = models.TextField()
    date_sent = models.DateTimeField(_('date sent'), default=timezone.now)
    
    class Meta:
        verbose_name = 'Notification Log'
        verbose_name_plural = 'Notification Log'
        
class UnpaidInvoices(User):
    class Meta:
        verbose_name = 'Unpaid Invoice'
        verbose_name_plural = 'Unpaid Invoices'
        default_permissions = ('add', 'change', 'delete', 'view')
        proxy = True
        
    @property
    def unpaid_invoices(self):    
        unpaid_inv_counter = Invoices.objects.filter(is_paid = False, payer = self).count()
        return unpaid_inv_counter
        
class SurveyList(models.Model):
    survey_user = models.ForeignKey(User)
    unpaid_invoices = models.IntegerField(blank=True, default=0)
    completed = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'Survey List'
        verbose_name_plural = 'Survey List'
        default_permissions = ('add', 'change', 'delete', 'view')
        
        
class NoticeList(models.Model):
    notice_user = models.ForeignKey(User)
    unpaid_invoices = models.IntegerField(blank=True, default=0)
    delivered = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'Notice List'
        verbose_name_plural = 'Notice List'
        default_permissions = ('add', 'change', 'delete', 'view')
   
        
class ClosedCircles(models.Model):
    chama_account = models.ForeignKey('ChamaAccount', blank=False, null=True)
    payment_option = models.CharField(max_length=255, blank=True, null=True,
        choices=(
            ('BANK', _("Bank")),
            ('MPESA', _("M-Pesa")),
        ),
    )
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_name = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=255, blank=True, null=True)
    bank_branch = models.CharField(max_length=255, blank=True, null=True)
    swift = models.CharField(max_length=255, blank=True, null=True)
    mpesa_number = models.CharField(max_length=255, blank=True, null=True)
    national_id = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(blank=True)
    closed_by = models.ForeignKey(User)
    date_closed = models.DateTimeField(_('date closed'), default=timezone.now)
    date_paid = models.DateTimeField(_('date paid'), blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Closed Circle'
        verbose_name_plural = 'Closed Circle'
