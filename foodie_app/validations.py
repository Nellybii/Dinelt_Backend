from foodie_app.models import User

from django.contrib.auth.backends import ModelBackend
import logging

logger = logging.getLogger(__name__)

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        logger.debug(f"Authenticating user with email: {email}")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            logger.debug(f"No user found with email: {email}")
            return None

        if user.check_password(password):
            return user
        logger.debug(f"Password mismatch for user: {email}")
        return None
