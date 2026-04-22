from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Authenticate with either username or email in the "username" field.
    Keeps compatibility with Django auth while enabling email login.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        login_value = (username or kwargs.get(UserModel.USERNAME_FIELD) or "").strip()
        if not login_value or password is None:
            return None

        user = None
        if "@" in login_value:
            try:
                user = UserModel._default_manager.get(email__iexact=login_value)
            except UserModel.DoesNotExist:
                return None
        else:
            try:
                user = UserModel._default_manager.get_by_natural_key(login_value)
            except UserModel.DoesNotExist:
                return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
