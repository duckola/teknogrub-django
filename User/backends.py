from django.contrib.auth.backends import ModelBackend
from .models import Users
from django.db.models import Q


class IdNumberBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        login_identifier = username

        try:
            # Search for User by id_number (which is now the USERNAME_FIELD)
            user = Users.objects.get(id_number__iexact=login_identifier)

        except Users.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None