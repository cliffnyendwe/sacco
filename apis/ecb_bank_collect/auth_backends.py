from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class AuthenticationBackend(ModelBackend):

    def authenticate(self, **credentials):
        User = get_user_model()
        username = credentials.get('username')
        password = credentials.get('password')

        try:
            # Username query is case insensitive
            user = User.objects.get(username__iexact=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            try:
                user = User.objects.get(mobile_number__iexact=username)
                if user.check_password(credentials["password"]):
                    return user
            except User.DoesNotExist:
                try:
                    user = User.objects.get(email__iexact=username)
                    if user.check_password(credentials["password"]):
                        return user
                except User.DoesNotExist:
                    return None
