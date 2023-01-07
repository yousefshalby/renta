from django.contrib import admin
from project.models import ContactUs, ContactInfo, AboutUs, User, PropertyType, Area, Properties, UserContract
from solo.admin import SingletonModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TabbedTranslationAdmin
from import_export.admin import ImportExportMixin

from project.resources import AreaResource, PropertyResource, PropertyTypeResource, UserContractResource


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        "id",
        "email",
        "first_name",
        "last_name",
        "phone",
        'address'
    ]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", 'address', "password_reset_code", 'phone',)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_app_user",
                    "groups",
                    "user_permissions",
                    
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


@admin.register(ContactInfo)
class ContactInfoAdmin(SingletonModelAdmin):
    pass


@admin.register(AboutUs)
class AboutUsAdmin(SingletonModelAdmin, TabbedTranslationAdmin):
    pass


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone_number")
    search_fields = ("name", "email", "phone_number")
    
    
@admin.register(Area)
class AreaAdmin(ImportExportMixin, TabbedTranslationAdmin):
    list_display = ("id", "name")
    search_fields = ("name_en", "name_ar")    
    resource_class = AreaResource
    
    
@admin.register(PropertyType)
class PropertyTypeAdmin(ImportExportMixin, TabbedTranslationAdmin):
    list_display = ("id", "name")
    search_fields = ("name_en", "name_ar")    
    resource_class = PropertyTypeResource
    
@admin.register(Properties)
class PropertiesAdmin(ImportExportMixin, TabbedTranslationAdmin):
    list_display = [ 'title', 'address', 'price', 'Bedrooms','Bathrooms', 'listing_date']
    search_fields = [ 'title_en', 'title_ar','area__name', 'property_type__name']
    resource_class = PropertyResource
    
    
@admin.register(UserContract)
class UserContractAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = [ 'renter_name', 'rent_amount_per_month', 'contract_start', 'contract_end']
    search_fields = [ 'renter_name', 'property_id__title']
    resource_class = UserContractResource
    