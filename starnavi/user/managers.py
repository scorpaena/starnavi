from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
 
class UserManager(BaseUserManager):

    def create_user(self, email, nickname, password, **extra_fields):
        if not email or not nickname:
            raise ValidationError('email/nickname cannot be empty')
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, nickname, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValidationError('superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValidationError('superuser must have is_superuser=True')
        return self.create_user(email, nickname, password, **extra_fields)
