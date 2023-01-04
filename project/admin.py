from django.contrib import admin
from project.models import ContactUs, ContactInfo, AboutUs
from solo.admin import SingletonModelAdmin


@admin.register(ContactInfo)
class ContactInfoAdmin(SingletonModelAdmin):
    pass


@admin.register(AboutUs)
class AboutUsAdmin(SingletonModelAdmin):
    pass


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone_number")
    search_fields = ("name", "email", "phone_number")