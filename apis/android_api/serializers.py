from chama.models import ChamaAccount, ChamaContributions, ChamaMembership, \
    ChamaInvitations, MemberAppprovals, ClosedCircles
from core_manager.models import User, CardPaymentRequests, CircleCurrency
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions
from core_manager.forms import AuthenticationForm, RegistrationForm
from utils.gcm_module import *
import re
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django import VERSION
from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField

from chama.models import Invoices
from chama.models import ChamaMembership

def clean_mobile_number(mobile_number, country_code = ""):
    if not mobile_number:
        return None
    clean_mobile = re.sub("[^0-9]", "", mobile_number)
    
    if clean_mobile[:1] == '0':
        clean_mobile = country_code + clean_mobile[1:]
    elif not clean_mobile[:len(country_code)] == country_code:
        clean_mobile = country_code + clean_mobile
        
    return clean_mobile
    
class ForgotPasswordSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(required=False, max_length=128, allow_blank=True)
    email = serializers.CharField(required=False, max_length=128, allow_blank=True)
    reset_code = serializers.CharField(required=False, max_length=128, allow_blank=True)

    def validate(self, attrs):
        mobile_number = clean_mobile_number(attrs.get('mobile_number'))
        email = attrs.get('email')
        reset_code = attrs.get('reset_code')
        user = User.objects.filter(username = mobile_number, email = email).first()
           
        if reset_code:        
            if user.reset_code != reset_code:            
                msg = _('Invalid reset code.')
                raise exceptions.ValidationError(msg)        
        elif mobile_number and email:            
            if not user:
                msg = _('User does not exist.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Invalid request.')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        #attrs['reset_code'] = reset_code
        return attrs


class ChangePasswordSerializer(serializers.Serializer):

    """
    Serializer for changing a password.
    """

    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def __init__(self, *args, **kwargs):
        self.old_password_field_enabled = getattr(
            settings, 'OLD_PASSWORD_FIELD_ENABLED', False
        )
        self.logout_on_password_change = getattr(
            settings, 'LOGOUT_ON_PASSWORD_CHANGE', False
        )
        super(ChangePasswordSerializer, self).__init__(*args, **kwargs)

        if not self.old_password_field_enabled:
            self.fields.pop('old_password')

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)
        

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password(value)
        )

        if all(invalid_password_conditions):
            raise serializers.ValidationError('Invalid password')
        return value

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()
        if VERSION[1] > 6 and not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(self.request, self.user)

class RegisterChamaSerializer(serializers.ModelSerializer):
    payment_day = serializers.CharField(max_length=128, allow_blank=True, required=False)
    circle_currency = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = ChamaAccount
        fields = ('id', 'chama_name', 'rotating_amount', 'payment_day', 'description', 'account_number', 'circle_currency', 'payment_cycle_option', 'payment_cycle_choice')
        read_only_fields = ('id', 'account_number')

    def create(self, validated_data):
        administrator = User.objects.get(pk = self.context.get('request').user.id)    
        
        print validated_data
        
        if 'payment_day' in validated_data and not validated_data['payment_day']:
            payment_day = 0
        elif 'payment_day' in validated_data:
            payment_day = validated_data['payment_day']
        else:
            payment_day = 1
            
        rotating_amount = validated_data['rotating_amount'] if 'rotating_amount' in validated_data else 0
               
        chama = ChamaAccount.objects.create(
            chama_name = validated_data['chama_name'],
            rotating_amount = rotating_amount,
            payment_day = payment_day,
            description = validated_data['description'] if 'description' in validated_data else "",
            payment_cycle_option = validated_data['payment_cycle_option'] if 'payment_cycle_option' in validated_data else "Monthly",
            payment_cycle_choice = validated_data['payment_cycle_choice'] if 'payment_cycle_choice' in validated_data else payment_day,
            administrator = administrator,
            circle_currency_id = validated_data['circle_currency'] if 'circle_currency' in validated_data else 1,
        )
        membership = ChamaMembership(
            chama_account = chama,
            member = administrator,
        )
        membership.save()
        return chama
        

"""class AcceptInviteSerializer(serializers.ModelSerializer):

    invitation_id = serializers.CharField(max_length=128, allow_blank=False, write_only=True)
    member_code = serializers.CharField(max_length=128, allow_blank=False, write_only=True)
    chama_name = serializers.CharField(read_only=True, source="chama_account.chama_name")
    chama_id = serializers.CharField(read_only=True, source="chama_account.id")
    

    rotating_amount = serializers.CharField(read_only=True, source="chama_account.rotating_amount")
    description = serializers.CharField(read_only=True, source="chama_account.description")
    account_number = serializers.CharField(read_only=True, source="chama_account.account_number")
    
    
    class Meta:
        model = ChamaInvitations
        
        fields = ('id', 'member_code', 'invitation_id', 'chama_name', 'chama_id', 'rotating_amount', 'description', 'account_number')
        read_only_fields = ('id', 'chama_account')


    def create(self, validated_data):
        invitation_id = validated_data['invitation_id']
        member_code = validated_data['member_code']
        invited_member = User.objects.get(member_code = member_code)
        invitation = ChamaInvitations.objects.get(pk = invitation_id)        
        invitation.invite_accepted = True
        invitation.invited_member = invited_member
        
        invitation.save()
        
        return invitation"""
        
        
class InviteApprovalsSerializer(serializers.ModelSerializer):

    #invitation_id = serializers.CharField(max_length=128, allow_blank=False, write_only=True)
    
    first_name = serializers.CharField(read_only=True, source="invited_member.first_name")
    other_names = serializers.CharField(read_only=True, source="invited_member.other_names")
    mobile_number = serializers.CharField(read_only=True, source="invited_member.mobile_number")
    member_code = serializers.CharField(read_only=True, source="invited_member.member_code")
    
    
    
    """invited_member = models.ForeignKey(User, related_name="invited_member")
    chama_account = models.ForeignKey('ChamaAccount')
    member_to_approve = models.ForeignKey(User, related_name="member_to_approve")
    approved = models.BooleanField(default=False) """
    
    
    class Meta:
        model = MemberAppprovals
        
        fields = ('id', 'approved', 'first_name', 'member_code', 'mobile_number', 'other_names', 'first_name')
        read_only_fields = ('id', 'chama_account')


    """def create(self, validated_data):
        invitation_id = validated_data['invitation_id']
        invitation = MemberAppprovals.objects.get(pk = invitation_id)        
        invitation.approved = True        
        invitation.save()        
        return invitation"""
        
"""class ApproveInviteSerializer(serializers.ModelSerializer):

    invitation_id = serializers.CharField(max_length=128, allow_blank=False, write_only=True)
    
    class Meta:
        model = MemberAppprovals
        
        fields = ('id', 'invitation_id')
        read_only_fields = ('id', 'chama_account')


    def create(self, validated_data):
        invitation_id = validated_data['invitation_id']
        invitation = MemberAppprovals.objects.get(pk = invitation_id)        
        invitation.approved = True        
        invitation.save()        
        return invitation"""
        
class InviteMemberChamaSerializer(serializers.ModelSerializer):

    """
    Serializer for registering a chama member.
    """
    chama_code = serializers.CharField(max_length=128)
    member_code = serializers.CharField(max_length=128, allow_blank=True, read_only=True)

    class Meta:
        model = ChamaInvitations
        
        fields = ('id', 'member_mobile', 'chama_code', 'member_code')
        read_only_fields = ('id', 'member_code')


    def create(self, validated_data): 
       
        chama_code = validated_data['chama_code']
        
        chama = ChamaAccount.objects.get(account_number = chama_code)
        invited_by = User.objects.get(pk = self.context.get('request').user.id)
        member_mobile = clean_mobile_number(validated_data['member_mobile'])
        invite, found_status = ChamaInvitations.objects.get_or_create(
            chama_account = chama,
            member_mobile = member_mobile,
            invited_by = invited_by
        )
        existing_member = User.objects.filter(mobile_number = clean_mobile_number(validated_data['member_mobile'])).first()

        if existing_member:
            notification_data = {
                'title' : "New Invitation",
                'message': "You have received a request to join %s Circle from %s" %(chama.chama_name, invited_by)
            }
            android_notification("new_invite", existing_member.id, existing_member, notification_data)
            

        return {
            'chama_code' : chama_code, 'member_mobile' : member_mobile, 
            'member_code' : existing_member.member_code if existing_member else '',
        }
        
class RegisterMemberSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = get_user_model()        
        fields = ('id', 'member_code', 'username', 'password', 'first_name', 'other_names', 'mobile_number', 'email')
        write_only_fields = ('password',)
        read_only_fields = ('id', 'member_code')
    
    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
            first_name = validated_data['first_name'],
            other_names = validated_data['other_names'],
            email = validated_data['email'],
            mobile_number = validated_data['mobile_number'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
        
def base_64_photo(imagestr):
    from PIL import Image
    from base64 import decodestring
    
    image = Image.frombytes('RGB',(100,100),decodestring(imagestr))
    image.save("foo.png")
    return image
        
    """with open("/home/micmukima/Desktop/foo.png","wb") as f:
        f.write(decodestring(photo_string))"""
        
        
class Base64ImageField(serializers.ImageField): # possibly remove

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            # base64 encoded image - decode

            format, imgstr = data.split(';base64,') # format ~= data:image/X,

            ext = format.split('/')[-1] # guess file extension

            id = uuid.uuid4()

            data = ContentFile(base64.b64decode(imgstr), name = id.urn[9:] + '.' + ext)

        return super(Base64ImageField, self).to_internal_value(data)
        
        
        
class CreatePasswordSerializer(serializers.ModelSerializer):			
    password = serializers.CharField(style={'input_type': 'password'}, required=False)
    class Meta:
        model = get_user_model()        
        fields = ('id', 'password', 'email', 'mobile_number', 'reset_code')
        read_only_fields = ('id', 'password')
        
        
class UpdateProfileSerializer(serializers.ModelSerializer):
    #password = serializers.CharField(write_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, required=False)
    #photo = Base64ImageField(write_only=True)
    class Meta:
        model = get_user_model()
        
        fields = ('id', 'member_code', 'username', 'password', 'first_name', 'other_names', 'mobile_number', 'identity_number', 'email', 'photo')
        #write_only_fields = ('password',)
        read_only_fields = ('id', 'member_code')
    
    def update(self, instance, validated_data):  

        instance.username = clean_mobile_number(validated_data['username'])
        instance.mobile_number = clean_mobile_number(validated_data['mobile_number'])
        instance.first_name = validated_data['first_name']
        instance.other_names = validated_data['other_names']
        instance.email = validated_data['email']
        instance.identity_number = validated_data['identity_number'] if 'identity_number' in validated_data else ''
                
        if 'photo' in validated_data:
            instance.photo = validated_data['photo']        
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        instance.password = ''
        return instance
            
class LoginSerializer(serializers.Serializer):
    """
    Serializer for login 
    """
    username = serializers.CharField(required=True, allow_blank=False) # username accepts username, email or phone number
    password = serializers.CharField(style={'input_type': 'password'}, required=True)
    country_code = serializers.CharField(required=False, allow_blank=True) # username accepts username, email or phone number

    def validate(self, attrs):
        country_code = attrs.get('country_code')
        username = clean_mobile_number(attrs.get('username'), country_code)
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
        else:
            msg = _('Must include "username/phone" and "password".')
            raise exceptions.ValidationError(msg)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs
        
class ReLoginSerializer(serializers.Serializer):

    """
    Serializer for re-login 
    """
    password = serializers.CharField(style={'input_type': 'password'}, required=True)

    def validate(self, attrs):
        password = attrs.get('password')
        if not password:            
            msg = _('Must include a "password".')
            raise exceptions.ValidationError(msg)       
        return {}

class UserDetailsSerializer(serializers.ModelSerializer):
    owed_payment = serializers.SerializerMethodField()
    owed_payment_local = serializers.SerializerMethodField('owed_payment_local_curr')
    #suspense_balance = serializers.CharField(read_only=True, source="member.suspense_balance")
    #currency_id = serializers.CharField(read_only=False)
    
    """ currency_id = serializers.SerializerMethodField()

    def get_currency_id(self, obj):
        view = self.context['view']
        return view.kwargs['currency_id'] """

    """
    User model without password
    """
    
    photo_thumbnail = HyperlinkedSorlImageField(
        '250x250',
        options={"crop": "center"},
        source='photo',
        read_only=True
    )
    
    def owed_payment_local_curr(self, obj):        
        import math
        view = self.context['view']
        currency_id =  "2" #view.kwargs['currency_id'] if 'currency_id' in view.kwargs else "2"        
        from chama.models import Invoices
        from chama.models import ChamaMembership
        total_payable = 0
        all_invoices = Invoices.objects.filter(is_paid = False, payer = obj, chama_account__is_closed = False)
        for invoice in all_invoices:
            membership = ChamaMembership.objects.filter(chama_account = invoice.chama_account, member = invoice.payer).first()
            if membership.is_active:
                total_payable +=(invoice.amount_required/float(invoice.chama_account.circle_currency.conversion_rate))
                
        
        #print currency_id
        user_currency = CircleCurrency.objects.filter(pk=currency_id).first()
        
        """print total_payable
        print user_currency
        print user_currency.conversion_rate """
        
        converted_amount = total_payable*float(user_currency.conversion_rate)



        return int(math.ceil(converted_amount))

    
    def get_owed_payment(self, obj):        
        import math
        view = self.context['view']
        currency_id =  view.kwargs['currency_id'] if 'currency_id' in view.kwargs else "1"        
        
        total_payable = 0
        all_invoices = Invoices.objects.filter(is_paid = False, payer = obj, chama_account__is_closed = False)
        for invoice in all_invoices:
            membership = ChamaMembership.objects.filter(chama_account = invoice.chama_account, member = invoice.payer).first()
            if membership.is_active:
                total_payable +=(invoice.amount_required/float(invoice.chama_account.circle_currency.conversion_rate))
                
        
        #print currency_id
        user_currency = CircleCurrency.objects.filter(pk=currency_id).first()
        
        """print total_payable
        print user_currency
        print user_currency.conversion_rate """
        
        converted_amount = total_payable*float(user_currency.conversion_rate)



        return int(math.ceil(converted_amount))

    class Meta:
        model = get_user_model()
        fields = ('id', 'mobile_number', 'identity_number', 'email', 'first_name', 'other_names', 'member_code', 'owed_payment', 'owed_payment_local', 'is_active', 'photo', 'photo_thumbnail', 'suspense_balance')
        read_only_fields = ('email', 'photo')
        
        
class TokenSerializer(serializers.ModelSerializer):

    """
    Serializer for Token model.
    """

    class Meta:
        model = Token
        fields = ('key',)

class ContributionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChamaContributions
        fields = ('chama_account', 'paid_by','mobile_number', 'amount_paid' , 'transaction_type', 'date_paid')

#class ChamaAccountSerializer(serializers.HyperlinkedModelSerializer):
class ChamaAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChamaAccount
        fields = ('chama_name', 'account_number','description', 'administrator' , 'rotating_amount', 'members', 'contributions')
        
class ChamaMembershipSerializer(serializers.ModelSerializer):
    
    first_name = serializers.CharField(read_only=True, source="member.first_name")
    other_names = serializers.CharField(read_only=True, source="member.other_names")
    mobile_number = serializers.CharField(read_only=True, source="member.mobile_number")
    member_code = serializers.CharField(read_only=True, source="member.member_code")
    photo = serializers.ImageField(read_only=True, source="member.photo")
    
    photo_thumbnail = HyperlinkedSorlImageField(
        '250x250',
        options={"crop": "center"},
        source='member.photo',
        read_only=True
    )

    class Meta:
        model = ChamaMembership
        fields = ('id', 'first_name', 'other_names', 'mobile_number', 'member_code', \
            'chama_account', 'date_joined', 'current_balance', 'approved', \
            'photo', 'photo_thumbnail', 'total_contribution', 'is_active_status')
                   
class ExitCircleSerializer(serializers.Serializer):

    """
    Serializer for registering device id
    """

    circle_id = serializers.CharField(max_length=200)

    class Meta:
        model = ChamaMembership
        
class DeviceIDSerializer(serializers.Serializer):

    """
    Serializer for registering device id
    """

    android_device_id = serializers.CharField(max_length=200)

    class Meta:
        model = User
        
class CloseCircleSerializer(serializers.ModelSerializer):
    """
    Serializer for closing a circle
    """
    class Meta:
        model = ClosedCircles
        
        fields = ('id', 'chama_account', 'payment_option', 'bank_name', \
            'account_name', 'account_number', 'bank_branch', 'swift', \
            'mpesa_number', 'national_id', 'comments', 'date_closed', 'closed_by')
        read_only_fields = ('id', 'date_closed', 'comments', 'closed_by')
        
    def create(self, validated_data):
        self.request = self.context.get('request')
        user = getattr(self.request, 'user', None)
        
        closed_circle = ClosedCircles.objects.create(
            chama_account = validated_data.get("chama_account"),
            payment_option = validated_data.get("payment_option", ''),
            bank_name = validated_data.get("bank_name", ''),
            account_name = validated_data.get("account_name", ''),
            account_number = validated_data.get("account_number", ''),
            bank_branch = validated_data.get("bank_branch", ''),
            swift = validated_data.get("swift", ''),
            mpesa_number = validated_data.get("mpesa_number", ''),    
            national_id = validated_data.get("national_id", ''),
            closed_by = user,
        )
        closed_circle.save()
        return closed_circle
        
        
class MemberSubscriptionsSerializer(serializers.ModelSerializer):
    chama_id = serializers.CharField(read_only=True, source="chama_account.id")
    #administrator_name = serializers.CharField(read_only=True, source="chama_account.administrator")
    administrator_id = serializers.CharField(read_only=True, source="chama_account.administrator_id")
    member_id = serializers.CharField(read_only=True, source="member.id")
    chama_name = serializers.CharField(read_only=True, source="chama_account.chama_name")
    account_number = serializers.CharField(read_only=True, source="chama_account.account_number")
    description = serializers.CharField(read_only=True, source="chama_account.description")
    rotating_amount = serializers.CharField(read_only=True, source="chama_account.rotating_amount")
    currency_code = serializers.CharField(read_only=True, source="chama_account.circle_currency.currency_code")
    currency_id = serializers.CharField(read_only=True, source="chama_account.circle_currency.id")
    currency_name = serializers.CharField(read_only=True, source="chama_account.circle_currency.currency_name")
    currency_symbol = serializers.CharField(read_only=True, source="chama_account.circle_currency.currency_symbol")
    payment_day = serializers.CharField(read_only=True, source="chama_account.payment_cycle_choice")
    date_created = serializers.CharField(read_only=True, source="chama_account.date_created")
    total_contribution = serializers.CharField(read_only=True, source="chama_account.total_contribution")
    #owed_payment = serializers.CharField(read_only=True, source="chama_account.owed_payment")
    total_members = serializers.CharField(read_only=True, source="chama_account.total_members")
    payment_cycle_option = serializers.CharField(read_only=True, source="chama_account.payment_cycle_option")
    member_code = serializers.CharField(read_only=True, source="member.member_code")
    suspense_balance = serializers.CharField(read_only=True, source="member.suspense_balance")
    #is_closed = serializers.CharField(read_only=True, source="chama_account.is_closed")
    
    #is_closed = True if is_closed == "1" else False

    class Meta:
        model = ChamaMembership
        fields = ('id', 'approved', 'chama_id', 'chama_name', 'account_number', 'description', \
            'date_created', 'currency_id', 'currency_code', 'currency_name', 'currency_symbol', \
            'rotating_amount', 'member_code', 'payment_cycle_option', 'due_date', 'payment_day', \
            'total_contribution', 'owed_payment', 'total_members', 'administrator_id', 'member_id', \
            'is_closed', 'suspense_balance', 'withdrawn_amount')
        
class MemberInvitationsSerializer(serializers.ModelSerializer):
    chama_id = serializers.CharField(read_only=True, source="chama_account.id")
    chama_name = serializers.CharField(read_only=True, source="chama_account.chama_name")
    account_number = serializers.CharField(read_only=True, source="chama_account.account_number")
    rotating_amount = serializers.CharField(read_only=True, source="chama_account.rotating_amount")
    date_created = serializers.CharField(read_only=True, source="chama_account.date_created")
    description = serializers.CharField(read_only=True, source="chama_account.description")

    class Meta:
        model = ChamaInvitations
        fields = ('id', 'invite_accepted', 'chama_id', 'chama_name', 'account_number', 'description', 'date_created', 'rotating_amount')
        
class ChamaContributionsSerializer(serializers.ModelSerializer):
    chama_account = serializers.CharField(read_only=True, source="chama_account.chama_name")   
    first_name = serializers.CharField(read_only=True, source="paid_by.first_name") 
    other_names = serializers.CharField(read_only=True, source="paid_by.other_names") 
    photo = serializers.ImageField(read_only=True, source="paid_by.photo")
    
    photo_thumbnail = HyperlinkedSorlImageField(
        '250x250',
        options={"crop": "center"},
        source='paid_by.photo',
        read_only=True
    )
    
    class Meta:
        model = ChamaContributions
        fields = ('chama_account', 'first_name', 'other_names', 'amount_paid', 'transaction_type', 'date_paid', 'photo', 'photo_thumbnail')
        
class CardPaymentSerializer(serializers.ModelSerializer):    
    class Meta:
        model = CardPaymentRequests
        fields = ('token_id', 'live_mode', 'token_used', 'date_created', 'trans_type', 'card_brand', 'card_number', 'amount', 'automatically_deduct', 'remember_card_details')
        read_only_fields = ('id', )

    def create(self, validated_data):
        self.request = self.context.get('request')
        user = getattr(self.request, 'user', None)
        
        card = CardPaymentRequests.objects.create(
            token_id = validated_data['token_id'],
            live_mode = validated_data['live_mode'],
            token_used = validated_data['token_used'],
            date_created = validated_data['date_created'],
            trans_type = validated_data['trans_type'],
            amount = validated_data['amount'],
            automatically_deduct = validated_data['automatically_deduct'],
            remember_card_details = validated_data['remember_card_details'],
            card_brand = validated_data['card_brand'],
            card_number = validated_data['card_number'],
            card_owner = user,
        )
        
        card.save()     
        return card
        
class CurrenciesSerializer(serializers.ModelSerializer):
    #currency_id = serializers.CharField(read_only=True, source="id")
    class Meta:
        model = CircleCurrency
        fields = ('id', 'currency_code', 'currency_name', 'currency_symbol')  
