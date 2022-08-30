from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, mobile, first_name, last_name, country, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        
        if not mobile:
            raise ValueError(_('The Mobile must be set'))

        if not first_name:
            raise ValueError(_('The First Name must be set'))

        if not last_name:
            raise ValueError(_('The Last Name must be set'))

        if not country:
            raise ValueError(_('The Country must be set'))

        email = self.normalize_email(email)
        user = self.model(
            email=email, mobile=mobile, 
            first_name=first_name, last_name=last_name,
            country=country, **extra_fields
            )
        user.set_unusable_password()
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        if not email:
            raise ValueError(_('The Email must be set'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    mobile = models.CharField(_("mobile number"), max_length=10, unique=True, null=True, blank=True)
    first_name = models.CharField(_("first name"), max_length=100, null=True, blank=True)
    last_name = models.CharField(_("last name"), max_length=100, null=True, blank=True)
    country = models.CharField(_("country"), max_length=255, null=True, blank=True)
    mobile_otp = models.PositiveIntegerField(_("mobile otp"), max_length=6,  null=True, blank=True)
    email_verified = models.BooleanField(_("email verified"), default=False,
    help_text=_(
            "Designates whether this users email is verified. "
        )
    )
    mobile_verified = models.BooleanField(_("mobile verified"), default=False,
    help_text=_(
            "Designates whether this users mobile is verified. "
        )
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile', 'first_name', 'last_name', 'country']
    
    def __str__(self):
        return self.email