from django.db import models
from project.custom_Models import CustomModel
from project.helpers import file_upload
from solo.models import SingletonModel
from functools import partial
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import ugettext_lazy as _
from project.model_mixin import ContactUsMixin


# Create your models here.
class Properties(models.Model):
    title = models.CharField(max_length=500, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True, default="",
                                   help_text="description of property",
                                   )
    area = models.CharField(max_length=500, blank=True, null=True)
    Bedrooms = models.PositiveIntegerField(blank=True, null=True)
    Bathrooms = models.PositiveIntegerField(blank=True, null=True)
    listing_date = models.CharField(max_length=500, blank=True, null=True)
    price = models.CharField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=500, blank=True, null=True)
    property_type = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title

class ContactInfo(SingletonModel):
    address = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    contact_no = models.CharField(max_length=12)
    find_us = models.CharField(max_length=250)
    
    def __str__(self):
        return "Contact Info"

    class Meta:
        verbose_name = "Contact Information"

class ContactUs(ContactUsMixin, models.Model):   
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=12)

    class Meta:
        verbose_name = "Contact us"
        verbose_name_plural = "Contact Us"

    def __str__(self):
        return f"{self.name}"
    
class AboutUs(SingletonModel):
    first_paragraph_title = models.CharField(
        max_length=50,
        default="",
        help_text="title of first paragraph in about us page",
    )
    first_paragraph_text = models.TextField(
        max_length=1000,
        default="",
        help_text="description of first paragraph in about us page",
    )
    second_paragraph_title = models.CharField(
        max_length=50,
        default="",
        help_text="title of second paragraph in about us page",
    )
    second_paragraph_text = models.TextField(
        max_length=1000,
        default="",
        help_text="description of second paragraph in about us page",
    )
    third_paragraph_title = models.CharField(
        max_length=50,
        default="",
        help_text="title of third paragraph in about us page",
    )
    third_paragraph_text = models.TextField(
        max_length=1000,
        default="",
        help_text="description of third paragraph in about us page",
    )
    forth_paragraph_title = models.CharField(
        max_length=50,
        default="",
        help_text="title of forth paragraph in about us page",
    )
    forth_paragraph_text = models.TextField(
        max_length=1000,
        default="",
        help_text="description of forth paragraph in about us page",
    )
    

    def __str__(self):
        return "About Us"

    class Meta:
        verbose_name = "About Us"
    
    
class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields["is_active"] = True
        return super().create_superuser(username, email, password, **extra_fields)


class User(CustomModel, AbstractUser):
    gender = (
        ('male', 'male'),
        ('female', 'female'),
    )
    email = models.EmailField(
        verbose_name="email address",
        unique=True, null=True
    )
    username = models.CharField(
        _("username"),
        max_length=150,
        null=True, blank=True
    )
    phone = models.CharField(_("Phone"), max_length=50, null=True, unique=True)
    gender = models.CharField(_("Gender"), choices=gender, max_length=50, null=True, blank=True)
    # verification
    address = models.TextField(_("Address"), max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_app_user = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)
    password_reset_code = models.CharField(max_length=10, null=True, blank=True)
   
    objects = CustomUserManager()
    
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]