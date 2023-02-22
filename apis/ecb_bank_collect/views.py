from django.shortcuts import render
from django.db import IntegrityError
from django.conf import settings
from django.http import Http404
from io import BytesIO
import re
import time
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from django.utils.translation import ugettext_lazy as _
from core_manager.models import User, CircleCurrency
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from django.contrib.auth import get_user_model 
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.authtoken.models import Token
from .serializers import ValidateUserSerializer, PostTransactionSerializer
           
class ECBAuth(BasePermission):

    model = Token
    
    def get_authorization_header(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        if isinstance(auth, type('')):
            # Work around django test client oddness
            auth = auth.encode(HTTP_HEADER_ENCODING)
        return auth
    
    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.select_related('user').get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return (token.user, token)
    def authenticate_header(self, request):
        auth = self.get_authorization_header(request).split()
        
        if len(auth) < 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)

        if not auth or auth[0].lower() != b'oauth':
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)
        

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)
    def has_permission(self, request, view):
        self.authenticate_header(request)
        return True
           
            
class ValidateUserView(RetrieveAPIView):
    serializer_class = ValidateUserSerializer
    permission_classes = (ECBAuth, )
    
    def get_object(self):
        try:
            member_code = self.kwargs['membership_code'];
            return User.objects.get(member_code = member_code, is_active = True)
        except User.DoesNotExist:
            raise Http404
            
class PostTransactionView(CreateAPIView):

    """
    Returns the success/fail message.
    """

    serializer_class = PostTransactionSerializer
    permission_classes = (ECBAuth, )

    def get(self, request):
        serializer = self.get_serializer(data=request.data)
        print request.data
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        print serializer.data
        return Response({"message": "Transaction Successful.", "results" : serializer.data})
