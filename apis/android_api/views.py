from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.conf import settings
from django.http import Http404
from io import BytesIO
import re
import time

from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from core_manager.forms import AuthenticationForm, RegistrationForm
from core_manager.models import User, CircleCurrency
from chama.models import *
from utils.gcm_module import *
from django.db.models import Q

from rest_framework import viewsets, status
from rest_framework.views import APIView
from django.views.generic import View
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model 

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import detail_route, list_route

#rest
from chama.models import ChamaAccount, ChamaMembership, ChamaEmails
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from .serializers import ChamaAccountSerializer, LoginSerializer, TokenSerializer, \
    ChamaMembershipSerializer, RegisterChamaSerializer, InviteMemberChamaSerializer, \
    RegisterMemberSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, \
    ChamaContributionsSerializer, MemberSubscriptionsSerializer, UserDetailsSerializer, \
    MemberInvitationsSerializer, InviteApprovalsSerializer, DeviceIDSerializer, \
    UpdateProfileSerializer, CloseCircleSerializer, CreatePasswordSerializer, \
    ReLoginSerializer, ExitCircleSerializer, CardPaymentSerializer, CurrenciesSerializer
from rest_framework.pagination import PageNumberPagination

from .permissions import IsOwnerOrReadOnly
from rest_framework import generics
from reportlab.pdfgen import canvas
import reportlab
from reportlab.lib.units import mm, inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.colors import black, lightgrey
#from django.core.mail import send_mail
from random import randint

def clean_mobile_number(mobile_number):
    if not mobile_number:
        return None
    clean_mobile = re.sub("[^0-9]", "", mobile_number)
    """if clean_mobile[:1] == '0':
        clean_mobile = "254" + clean_mobile[1:] """
    return clean_mobile

class MinimalResultsSetPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page': self.page.number,
            'results': data
        })
    page_size = 10
    
class LargeResultsSetPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page': self.page.number,
            'results': data
        })
    page_size = 100
    
class ForgotPasswordView(GenericAPIView):

    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordSerializer

    response_serializer = ForgotPasswordSerializer

    def create_reset_code(self):
        self.user = self.serializer.validated_data['user']
        #self.reset_code = randint(10000, 99999)
        self.user.reset_code = randint(10000, 99999)
        self.user.save()
        
        reset_message = """
Hi %s,

Somebody recently asked to reset your Circle password.

Enter the following password reset code:
%s

Didn't request this change?
If you didn't request a new password, please ignore this message.
        """ %(self.user.first_name, self.user.reset_code)
        
        e_mail = ChamaEmails(
            mail_subject = 'Somebody requested a new password for your Circle account',
            mail_message = reset_message,
            from_address = 'circle@imaginarium.co.ke',
            to_address = self.user.email,        
        )
        e_mail.save()
        
        #send_mail'Somebody requested a new password for your Circle account', reset_message, 'circle@imaginarium.co.ke', [self.user.email], fail_silently=False)
        
    def get_response(self):
        return Response(
            self.response_serializer(self.user).data, status=status.HTTP_200_OK
        )

    def get_error_response(self):
        response_data = self.serializer.errors
        key, value = self.serializer.errors.popitem()
        response_data['message'] = value[0]
        return Response(
            response_data, status=status.HTTP_400_BAD_REQUEST
        )

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=self.request.data)
        if not self.serializer.is_valid():
            return self.get_error_response()
            
        reset_code = request.data.get("reset_code", None)
            
        if reset_code:
            self.user = self.serializer.validated_data['user']
        else:
            self.create_reset_code()
        return self.get_response()
    
    
class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response({"success": "Password changed successfully."})
    
class TransactionsViewSet(generics.ListAPIView):  

    queryset = ChamaContributions.objects.all()
    serializer_class = ChamaContributionsSerializer
    pagination_class = LargeResultsSetPagination   
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        try:
            chama_id = self.kwargs['chama_id']
            #trans = ChamaContributions.objects.filter(paid_by=self.request.user, chama_account_id = chama_id)
            
            trans = ChamaContributions.objects.filter(chama_account_id = chama_id)
            return trans  
        except ChamaContributions.DoesNotExist:
            raise Http404
            
class CardPaymentView(CreateAPIView):
    serializer_class = CardPaymentSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response({"success": "Card payment sync is successful.", "results" : serializer.data})
            
class MemberSubscriptionsView(generics.ListAPIView): 

    queryset = ChamaMembership.objects.all()
    serializer_class = MemberSubscriptionsSerializer
    pagination_class = MinimalResultsSetPagination   
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        try:
            is_closed = 1 if self.kwargs['is_closed'] == 'true' else 0
            membership = ChamaMembership.objects.filter(member__id=self.request.user.id, chama_account__is_closed = is_closed, is_active = True)
            return membership  
        except ChamaMembership.DoesNotExist:
            raise Http404

class ConfirmLoginView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReLoginSerializer
    response_serializer = ReLoginSerializer

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=self.request.data)
        user_password = request.data.get("password")
        
        if not self.serializer.is_valid():
            return self.get_error_response()
        
        try:
            if request.user.check_password(user_password):
                return Response(
                    {"message": "User access confirmed."},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"message": "User confirmation failed."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                {"message": "User confirmation failed."},
                status=status.HTTP_400_BAD_REQUEST
            )

class DeviceIDView(UpdateAPIView):

    """
    Registers device ID 
    Accepts the following PUT parameters: android_device_id
    Returns the success/fail message.
    """

    queryset = User.objects.all()
    serializer_class = DeviceIDSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        print request.data
        instance = self.get_object()
        instance.android_device_id = request.data.get("android_device_id")
        instance.save()

        return Response(
            {"success": "Device ID registered successfully."},
            status=status.HTTP_200_OK
        )
        
class ExitCircleView(UpdateAPIView):

    queryset = ChamaMembership.objects.all()
    serializer_class = ExitCircleSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        circle_id = request.data.get("circle_id");
        instance = self.get_object()
        
        user_exists = ChamaMembership.objects.filter(chama_account__id = circle_id, member__id = instance.id).first()
        
        Invoices.objects.filter(payer = instance, chama_account_id = circle_id, is_paid = False).update(is_archived = True)
        user_exists.is_active = False
        user_exists.save()
        
        existing_members = ChamaMembership.objects.filter(
            chama_account__id = circle_id,
            is_active = True
        )
        if instance.total_active_memberships < 1:
            member_notification = "You have left %s Circle" %(user_exists.chama_account.chama_name)
            if user_exists.member.suspense_balance > 0.0:
                member_notification = "%s. Your excess balance of Ksh %s is still in your excess funds account for future use." %(member_notification, user_exists.member.suspense_balance)
                
                notification_data = {
                    'title' : "You have left Circle",
                    'message': member_notification
                }
                
            
                android_notification("member_left", self.request.user.id, user_exists.member, notification_data)
                
                exit_message = """
Hi %s,

%s""" %(user_exists.member, member_notification)
                e_mail = ChamaEmails(
                    mail_subject = "You have left Circle %s" %(user_exists.chama_account.chama_name),
                    mail_message = exit_message,
                    from_address = 'circle@imaginarium.co.ke',
                    to_address = user_exists.member.email,        
                )
                e_mail.save()

        for membership in existing_members:
            notification_data = {
                'title' : "Member has left Circle",
                'message': "%s has left %s Circle" %(self.request.user, membership.chama_account.chama_name)
            }
            android_notification("member_left", self.request.user.id, membership.member, notification_data)
            
            exit_message = """
Hi %s,

%s has left %s Circle""" %(membership.member, self.request.user, membership.chama_account.chama_name)
            e_mail = ChamaEmails(
                mail_subject = "Member has left Circle",
                mail_message = exit_message,
                from_address = 'circle@imaginarium.co.ke',
                to_address = membership.member.email,        
            )
            e_mail.save()

        return Response(
            {"success": "Exit Circle Successfully."},
            status=status.HTTP_200_OK
        )
            
class CloseCircleView(UpdateAPIView):

    queryset = ChamaAccount.objects.all()
    serializer_class = CloseCircleSerializer
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        response_data = serializer.data
        
        existing_members = ChamaMembership.objects.filter(chama_account__id = response_data['chama_account'], is_active = True)  
        
        send_admin_email = False # send if there is atleast one member
        
        for membership in existing_members:  
            extra_notification = ""
            send_admin_email = True
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
            e_mail.save()
                      
            notification_data = {
                'title' : "Circle %s Closed" %(membership.chama_account.chama_name),
                'message' : "Circle %s is about to be closed in the next 24 hours. %s If you are not aware of this request, please contact us at 0724639639" \
                    %(membership.chama_account.chama_name, extra_notification),
            }
            android_notification("close_circle", self.request.user.id, membership.member, notification_data)
            
        if send_admin_email:
        
            if len(request.data['national_id']) > 0:
                self.request.user.identity_number = request.data['national_id']
                self.request.user.save()

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


                e_mail = ChamaEmails(
                    mail_subject = 'Request to close a Circle Account',
                    mail_message = close_message,
                    from_address = 'circle@imaginarium.co.ke',
                    to_address = 'circle@imaginarium.co.ke',        
                )
                e_mail.save()
        
        #send_mail'Request to close a Circle Account', close_message, 'circle@imaginarium.co.ke', ['circle@imaginarium.co.ke'], fail_silently=False)
        
        return Response(
            {"message": "Circle Closed Successfully.", "results" : response_data},
            status=status.HTTP_200_OK,
        )
               
            

            
class InviteApprovalsViewSet(viewsets.ReadOnlyModelViewSet):  

    queryset = MemberAppprovals.objects.all()
    serializer_class = InviteApprovalsSerializer
    pagination_class = MinimalResultsSetPagination   
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        try:
            approvals = MemberAppprovals.objects.filter(member_to_approve__id=self.request.user.id)
            return approvals  
        except MemberAppprovals.DoesNotExist:
            raise Http404
            
    @detail_route(methods=['put'])
    def approve(self, request, pk=None):       

        try:
            invite = self.queryset.get(id=pk)
            instance = invite
            if request.data.get("approved") == 'true':
                instance.approved = True
                instance.save()
                pending_approvals = MemberAppprovals.objects.filter(invited_member = instance.invited_member, chama_account = instance.chama_account, approved = False)
                if not pending_approvals:
                    membership = ChamaMembership(
                        chama_account = instance.chama_account,
                        member = instance.invited_member,
                    )
                    membership.save()
                return Response(
                    {"success": "Approval Accepted."},
                    status=status.HTTP_200_OK
                )
            else:
                instance.approved = False
                instance.save()
                return Response(
                    {"success": "Approval Declined."},
                    status=status.HTTP_200_OK
                )

        except MemberAppprovals.DoesNotExist:
            raise Http404
        except IntegrityError as error:
            raise Http404
            
class MemberInvitationsViewSet(viewsets.ReadOnlyModelViewSet):  
    queryset = ChamaInvitations.objects.all()
    serializer_class = MemberInvitationsSerializer
    pagination_class = MinimalResultsSetPagination   
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        try:
            invitations = ChamaInvitations.objects.filter(member_mobile=self.request.user.mobile_number, invite_accepted = False, invite_rejected = False)
            return invitations  
        except ChamaInvitations.DoesNotExist:
            raise Http404
            
    @detail_route(methods=['put'])
    def accept(self, request, pk=None):       

        try:
            invite = self.queryset.get(id=pk)
            instance = invite
            if request.data.get("invite_accepted") == 'true':
                instance.invite_accepted = True
                instance.invited_member = self.request.user
                instance.save()

                existing_members = ChamaMembership.objects.filter(
                    chama_account = instance.chama_account
                )                    
                membership, found_status = ChamaMembership.objects.get_or_create(
                    chama_account = instance.chama_account,
                    member = self.request.user,
                )                
                for membership in existing_members:
                    notification_data = {
                        'title' : "New Member Joined",
                        'message': "%s has joined %s Circle" %(instance.invited_member, membership.chama_account.chama_name)
                    }
                    android_notification("new_member", self.request.user.id, membership.member, notification_data)
                if found_status:
                    return Response(
                        {"success": "Invite Accepted."},
                        status=status.HTTP_200_OK
                    )
                    
                else: 
                    return Response(
                        {"success": "Invite has been accepted before."},
                        status=status.HTTP_200_OK
                    )  
                    
            else:
                instance.invite_rejected = True
                instance.save()
                return Response(
                    {"success": "Invite Declined."},
                    status=status.HTTP_200_OK
                )

        except ChamaInvitations.DoesNotExist:
            raise Http404
        except IntegrityError as error:
            raise Http404
    
class MembersViewSet(generics.ListAPIView):  

    queryset = ChamaMembership.objects.all()
    serializer_class = ChamaMembershipSerializer
    pagination_class = MinimalResultsSetPagination   
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        try:
            chama_id = self.kwargs['chama_id']
            membership = ChamaMembership.objects.filter(member__id=self.request.user.id, chama_account_id = chama_id).first()
            if membership:
                members = ChamaMembership.objects.filter(chama_account=membership.chama_account)
            else:
                members = []
            return members  
        except ChamaMembership.DoesNotExist:
            raise Http404
        
class LoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = Token
    response_serializer = TokenSerializer

    def login(self):
        self.user = self.serializer.validated_data['user']
        self.token, created = self.token_model.objects.get_or_create(
            user=self.user)
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            django_login(self.request, self.user)

    def get_response(self):
        response_data = self.response_serializer(self.token).data
        response_data['total_circle_membership'] = self.user.total_memberships
        #response_data['total_invites'] = self.user.total_invites
        return Response(response_data, status=status.HTTP_200_OK)

    def get_error_response(self):
        response_errors = self.serializer.errors
        response_errors['message'] = "Incorrect login details. Please try again."
        return Response(
            response_errors, status=status.HTTP_400_BAD_REQUEST
        )

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=self.request.data)
        if not self.serializer.is_valid():
            return self.get_error_response()
        self.login()
        return self.get_response()


class LogoutView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except:
            pass
        django_logout(request)
        return Response({"success": "Successfully logged out."},
                        status=status.HTTP_200_OK)

class RegisterChamaView(CreateAPIView):

    """
    Returns the success/fail message.
    """

    serializer_class = RegisterChamaSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        #print request.data
        serializer = self.get_serializer(data=request.data)
        print request.data
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response({"success": "Chama registered successfully.", "results" : serializer.data})
        
class InviteMemberView(GenericAPIView):

    """
    Returns the success/fail message.
    """

    serializer_class = InviteMemberChamaSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        response_data = serializer.data
        response_data["success"] = "Member has been succesfully invited."
        return Response(response_data)
            
   
class RegisterMemberView(CreateAPIView):

    """
    Returns the success/fail message.
    """
    model = get_user_model()
    serializer_class = RegisterMemberSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get("email")
        username = clean_mobile_number(request.data.get("username"))

        user_exists = User.objects.filter(Q(username=username) | Q(email=email))
        
        if user_exists:
            return Response({"message": "Account already exists."}, status=status.HTTP_400_BAD_REQUEST) 
            

            
        data=request.data  
        data['username'] = username
        data['mobile_number'] = username
        
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response({"success": "Registration Successful.", "results" : serializer.data})  
        
class CreatePasswordView(UpdateAPIView):

    """
    Returns the success/fail message.
    """
    queryset = User.objects.all()
    serializer_class = CreatePasswordSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        reset_code = self.request.data['reset_code']
        mobile_number = clean_mobile_number(self.request.data['mobile_number'])
        email = self.request.data['email']
        user = User.objects.filter(username = mobile_number, email = email, reset_code = reset_code).first()
        return user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response(
                {"error": "Error creating password. Invalid details."},
                status=status.HTTP_400_BAD_REQUEST
            ) 
        instance.reset_code = ''
        instance.set_password(self.request.data['password'])
        instance.save()
        return Response({"success": "New password created successfully."}, status=status.HTTP_200_OK)
  
        
class UpdateProfileView(CreateAPIView):

    """
    Returns the success/fail message.
    """
    model = get_user_model()
    serializer_class = UpdateProfileSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(request.user, data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            serializer.save()
        except Exception as e:
            print e
        return Response({"success": "Profile Updated Successfully.", "results" : serializer.data})    
        
class UserDetailsView(RetrieveAPIView):
    serializer_class = UserDetailsSerializer
    permission_classes = (IsAuthenticated,)
    
    """def get_serializer_context(self):
        print self
        return {"currency_id": self.kwargs['currency_id']}"""

    def get_object(self):
        return self.request.user
    
    
class ChamaExportPDFView(View):

    def get(self, request, circle_id):
        
        chama = ChamaAccount.objects.get(pk = circle_id)
        logo_filename = settings.MEDIA_ROOT+"circle_logo.png"

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='right_align', alignment=TA_RIGHT))

        buf = BytesIO()
        elements = []
        margin = 12 * mm
        doc = SimpleDocTemplate(buf, rightMargin=margin, leftMargin=margin,
                                topMargin=margin, bottomMargin=margin, pagesize=A4)
        logo = Image(logo_filename)
        logo.drawHeight = 1.25*inch*logo.drawHeight / logo.drawWidth
        logo.drawWidth = 1.25*inch
        letterhead = [
            [logo, Paragraph('<font size=24><b>%s</b></font>' % chama.chama_name, styles['right_align'])]
        ]
        l_table = Table(letterhead, colWidths=[doc.width / 2.06] * 2)
        l_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), 
        ]))
        elements.append(l_table)
        elements.append(Paragraph('', styles['Heading2']))  # Space after the table
        col_1 = doc.width / 2
        col_2 = doc.width / 2
        
        col_widths = [col_1, col_2]
        owed_table = []
        owed_table.append([Paragraph('Circle Name', styles['right_align']), chama.chama_name])
        owed_table.append([Paragraph('Account Number', styles['right_align']), chama.account_number])
        owed_table.append([Paragraph('Description', styles['right_align']), chama.description])
        owed_table.append([Paragraph('Date Created', styles['right_align']), chama.date_created])
        owed_table.append([Paragraph('Administrator', styles['right_align']), chama.administrator])
        owed_table.append([Paragraph('Rotating Amount', styles['right_align']), chama.rotating_amount])

        owed_table.append([Paragraph('Total Contribution', styles['right_align']), chama.total_contribution])
        owed_table.append([Paragraph('Total Members', styles['right_align']), chama.total_members])


        o_table = Table(owed_table, colWidths=col_widths)
        o_table.setStyle(TableStyle([
            #('BACKGROUND', (0, 0), (-1, 0), lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, lightgrey),
            ('BOX', (0, 0), (-1, -1), 0.25, lightgrey),
        ]))
        elements.append(o_table)
        elements.append(Paragraph('', styles['Heading2']))

        doc.build(elements)

        pdf = buf.getvalue()
        buf.close()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s.pdf"' %chama.chama_name
        return response
        
class CurrenciesView(generics.ListAPIView): 

    queryset = CircleCurrency.objects.all()
    serializer_class = CurrenciesSerializer
    pagination_class = LargeResultsSetPagination   
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        try:
            currencies = CircleCurrency.objects.filter(is_active=True)
            return currencies  
        except CircleCurrency.DoesNotExist:
            raise Http404

