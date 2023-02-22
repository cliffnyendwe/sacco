from django.db import models
from django.conf import settings
import re
 
from django.core import validators
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django import forms
from sorl.thumbnail import ImageField



from utils import get_activation_code

USER = settings.AUTH_USER_MODEL

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, first_name, other_names, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username, first_name=first_name, other_names=other_names,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, first_name, other_names, password=None, **extra_fields):
        return self._create_user(username, first_name, other_names, password, False, False, **extra_fields)

    def create_superuser(self, username, first_name, other_names, password, **extra_fields):
        return self._create_user(username, first_name, other_names, password, True, True, **extra_fields)
        
    class Meta:
        verbose_name = 'Payment Accousnt'
        verbose_name_plural = 'Payment Asccounts'

class User(AbstractBaseUser, PermissionsMixin):
    username = models.SlugField(_('username'), max_length=50, unique=True,
        help_text=_('Required. 50 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$',
                                      _('Enter a valid username. '
                                        'This value may contain only letters, numbers '
                                        'and @/./+/-/_ characters.'), 'invalid'),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        })
    other_names = models.CharField(_('other names'), max_length=255, blank=True)
    member_code = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    gender = models.CharField(_('gender'), max_length=6, blank=True,
                              choices=(('male', 'Male'), ('female', 'Female')))
    email = models.EmailField(_('email address'), blank=True, null=True,
                              unique=True)
    mobile_number = models.CharField(_('phone number'), max_length=20, blank=True, 
        null=True, unique=True) 
                               
    identity_number = models.CharField(_('identity number'), max_length=50, 
        blank=True, null=True, unique=False)
                               
    reset_code = models.CharField(_('pasword reset code'), max_length=20, blank=True, null=True,
                               unique=False)
    #subscriptions = models.ManyToManyField('Product', blank=True)
    """profile_picture = models.ImageField(upload_to='profile', blank=True)"""
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Only staff an directly login to the admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user can login to the system. Deactivate users instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    
    suspense_balance = models.FloatField(default=0, blank=True)
    
    #currency = models.ForeignKey('core_manager.CircleCurrency', null=True)
    
    android_device_id = models.CharField(max_length=200,blank=True)
    
    photo = ImageField(upload_to='images/member_photos/%Y/%m', default=None, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'other_names']
    
    class Meta:
        verbose_name = 'System User'
        verbose_name_plural = 'System Users'

    def __str__(self):
        return "%s %s" %(self.first_name, self.other_names)

    def __unicode__(self):
        return "%s %s" %(self.first_name, self.other_names)

    def get_full_name(self):
        """
        Returns the other_names plus the first_name, with a space in between.
        """
        full_name = '%s %s' % (self.other_names, self.first_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Sends an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
       


    @property
    def owed_payment(self):
        from chama.models import Invoices
        from chama.models import ChamaMembership
        total_payable = 0
        all_invoices = Invoices.objects.filter(is_paid = False, payer = self, chama_account__is_closed = False)
        for invoice in all_invoices:
            membership = ChamaMembership.objects.filter(chama_account = invoice.chama_account, member = invoice.payer).first()
            if membership.is_active:
                total_payable +=invoice.amount_required
        return total_payable
        
    @property
    def total_memberships(self):
        from chama.models import ChamaMembership
        return ChamaMembership.objects.filter(member = self).count()
        
    @property
    def total_active_memberships(self):
        from chama.models import ChamaMembership
        return ChamaMembership.objects.filter(member = self, is_active = True, chama_account__is_closed = False).count()
        
    @property
    def unpaid_invoices(self): 
        from chama.models import Invoices   
        unpaid_inv_counter = Invoices.objects.filter(is_paid = False, payer = self).count()
        return unpaid_inv_counter
        
    """@property
    def total_invites(self):
        from chama.models import ChamaInvitations
        return ChamaInvitations.objects.filter(member_mobile = self.mobile_number).count()"""

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.username:
            max_length = self.__class__._meta.get_field('username').max_length
            self.username = orig = slugify(self.first_name)[:max_length]
            for x in itertools.count(1):
                if not self.__class__.objects.filter(username=self.username).exists():
                    break
                self.username = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)
        else:
            self.username = slugify(self.username)
        if not self.email:
            self.email = None
        if not self.mobile_number:
            self.mobile_number = None

        if not self.member_code:
            self.member_code = get_activation_code(size = 5)

        super(User, self).save(force_insert=force_insert,
            force_update=force_update, using=using, update_fields=update_fields)

class PaymentAccount(models.Model):
    account_number = models.CharField(max_length=150)
    account_name = models.CharField(max_length=150)
    date_created = models.DateTimeField(_('date created'), default=timezone.now)
    #account_owner = models.ForeignKey('User')
    #product = models.ForeignKey('Product')
    class Meta:
        verbose_name = 'Payment Account'
        verbose_name_plural = 'Payment Accounts'
    def __str__(self):             
        return "%s - %s" %(self.account_number, self.account_name)
        
class CommisionTable(models.Model):
    minimum = models.IntegerField()
    maximum = models.IntegerField()
    commission = models.IntegerField()
    
    class Meta:
        verbose_name = 'Commision Table'
        verbose_name_plural = 'Commision Table'
    def __str__(self):             
        return "%s - %s - %s" %(self.minimum, self.maximum, self.commission)

# not beeded - remove
class Transaction(models.Model):
    #product = models.ForeignKey('Product')
    account = models.ForeignKey('PaymentAccount') # products associated account
    paid_by = models.ForeignKey('User')
    mobile_number = models.CharField(max_length=150)
    amount_paid = models.IntegerField(default=0, blank=True)
    transaction_type = models.CharField(_('transaction_type'), max_length=6, blank=True,
                              choices=(('Debit', 'Debit'), ('Credit', 'Credit')))
    date_paid = models.DateTimeField(_('date paid'), default=timezone.now)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
    def __str__(self):             
        return "%s - %s" %(self.mobile_number, self.account)
        
        
class IncomingPayments(models.Model):
  transaction_id  = models.CharField(max_length=255)
  transaction_type = models.CharField(max_length=255)
  orig  = models.CharField(max_length=255)
  dest  = models.CharField(max_length=255)
  tstamp  = models.CharField(max_length=255)
  text  = models.CharField(max_length=255) #, unique=True
  customer_id  = models.CharField(max_length=255)
  mpesa_code  = models.CharField(max_length=255)
  mpesa_acc  = models.CharField(max_length=255)
  mpesa_msisdn  = models.CharField(max_length=255)
  mpesa_trx_date  = models.CharField(max_length=255)
  mpesa_trx_time  = models.CharField(max_length=255)
  mpesa_amt  = models.CharField(max_length=255)
  mpesa_sender  = models.CharField(max_length=255)
  business_number  = models.CharField(max_length=255)
  source  = models.CharField(max_length=255)
  processed = models.BooleanField(default=False)
  pending = models.BooleanField(default=False)
  currency_code = models.CharField(max_length=255)
  confirmation_reference  = models.CharField(max_length=255, blank=True) # transaction reference - for returning to external integrators
  #currency = models.ForeignKey('core_manager.CircleCurrency', default=2, null=True)
  
  class Meta:
        unique_together = ('transaction_id', 'source')
        verbose_name = 'Incoming Payment'
        verbose_name_plural = 'Incoming Payments'
  
class CardPaymentRequests(models.Model):
  token_id  = models.CharField(max_length=255)
  live_mode = models.CharField(max_length=255)
  token_used  = models.CharField(max_length=255)
  date_created  = models.CharField(max_length=255)
  trans_type  = models.CharField(max_length=255)
  card_brand  = models.CharField(max_length=255)
  card_number  = models.CharField(max_length=255)
  amount  = models.CharField(max_length=255)
  card_owner = models.ForeignKey('User')
  is_processed = models.BooleanField(default=False)
  automatically_deduct = models.BooleanField(default=False)
  remember_card_details = models.BooleanField(default=False)
  
  class Meta:
        unique_together = ('token_id', 'card_owner')
        verbose_name = 'Card Payment Request'
        verbose_name_plural = 'Card Payment Requests'
        
class ClientCard(models.Model):
    card_owner = models.OneToOneField('User', primary_key=True,)
    customer_id = models.CharField(max_length=255)
    card_number  = models.CharField(max_length=255)
    automatically_deduct = models.BooleanField(default=False)
    remember_card_details = models.BooleanField(default=False)    
    date_created  = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Client Card'
        verbose_name_plural = 'Client Cards'
        
class PesaPalTransactions(models.Model):
    currency  = models.CharField(max_length=255)
    amount = models.FloatField(default=0, blank=True)
    status  = models.CharField(max_length=255)
    reference_number  = models.CharField(max_length=255)
    tracking_id  = models.CharField(max_length=255)
    payment_method  = models.CharField(max_length=255) #, unique=True
    user_id  = models.CharField(max_length=255)
    member_code  = models.CharField(max_length=255)
    date_initiated  = models.DateTimeField(default=timezone.now)
    is_processed = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'PesaPal Transaction'
        verbose_name_plural = 'PesaPal Transactions'
        
class PesaPalTransactionUsers(models.Model):
    first_name  = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email  = models.CharField(max_length=255)
    phone_number  = models.CharField(max_length=255)
    
    
    class Meta:
        verbose_name = 'PesaPal Transaction User'
        verbose_name_plural = 'PesaPal Transaction Users'
        
class CircleCurrency(models.Model):    
    currency_code = models.CharField(max_length=150)
    currency_name = models.CharField(max_length=150)
    currency_symbol = models.CharField(max_length=150)
    is_base_currency = models.BooleanField(default=False)
    conversion_rate = models.FloatField(default=0, blank=True)
    is_active = models.BooleanField(_('active'), default=True)

    class Meta:
        verbose_name = 'Circle Currency'
        verbose_name_plural = 'Circle Currencies'
    def __str__(self):             
        return "%s (%s)" %(self.currency_name, self.currency_code)
