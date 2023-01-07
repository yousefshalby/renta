from rest_framework.response import Response
from rest_framework import status, generics, viewsets, mixins
from rest_framework.generics import CreateAPIView
from project.filters import PropertiesFilter
from project.models import ContactUs, ContactInfo, AboutUs, User, Area, PropertyType, Properties, UserContract
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.views import ObtainAuthToken
from project.serializers import (
    ContactUsSerializer, 
    ContactInfoSerializer, 
    AboutUsSerializer, 
    CustomAuthTokenSerializer, 
    TokenSerializer,
    UserSerializer,
    AreaSerializer,
    PropertyTypeSerializer,
    PropertiesSerializer,
    UserContractSerializer
)
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import gettext as _


class AreaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    pagination_class = None

class PropertyTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer
    pagination_class = None

class ContactInfoAPI(generics.RetrieveAPIView):
    serializer_class = ContactInfoSerializer

    def get_object(self):
        return ContactInfo.get_solo()


class ContactUsCreateView(CreateAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer.instance.send_notification_email()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class AboutUsListingAPIView(generics.RetrieveAPIView):
    serializer_class = AboutUsSerializer

    def get_object(self):
        return AboutUs.get_solo()


class LoginView(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def _get_user(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data["user"]

    def post(self, request, *args, **kwargs):
        user = self._get_user(request)
        refersh_token = RefreshToken.for_user(user)
        access_token = refersh_token.access_token
        token_serializer = TokenSerializer(
            data={
                "refresh_token": str(refersh_token),
                "access_token": str(access_token),
            }
        )
        token_serializer.is_valid()
       
        return Response(
            {"token": token_serializer.data, "user": UserSerializer(user).data}
        )
    
        
# class ForgetPasswordViewSet(viewsets.GenericViewSet):
#     serializer_class = None

#     def get_serializer_class(self):
#         if self.action == "send_reset_sms":
#             return PhoneSerializer
#         if self.action == "check_reset_code":
#             return SendCodeResetPasswordSerializer
#         if self.action == "reset_password":
#             return PasswordCodePhoneSerializer        

#     @swagger_auto_schema(responses={200: "email sent", 404: "no user with this email"})
#     @action(methods=["post"], detail=False)
#     def send_reset_sms(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = get_object_or_404(User, email=serializer.data.get("email"))
#         # _send_reset_password_code(user)
#         return Response({"details": _("email has been sent with reset code.")})

#     @swagger_auto_schema(
#         responses={200: "code valid", 404: "no user with this email and code"}
#     )
#     @action(methods=["post"], detail=False)
#     def check_reset_code(self, request):
#         """ check code validity """
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         get_object_or_404(
#             User,
#             password_reset_code=serializer.data.get("code"),
#             email=serializer.data.get("email"),
#         )
#         return Response({"detail": _("correct")})

#     @swagger_auto_schema(
#         responses={
#             200: "password has been reset successfully",
#             404: "no user with this phone and code",
#         }
#     )
#     @action(methods=["post"], detail=False)
#     def reset_password(self, request):
#         """ reset password """
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = self._get_user_by_reset_code_phone(serializer)
#         user.set_password(serializer.data.get("password"))
#         user.password_reset_code = None
#         user.save()
#         # self._send_confirmation_email(user)
#         return Response({"details": _("password has been reset successfully.")})
    
    
class PropertyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PropertiesSerializer
    filter_class = PropertiesFilter
    queryset = Properties.objects.select_related('area', 'property_type').all()
    search_fields = ['area__name', 'property_type__name', 'price']
    
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)
    
class UserContractViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UserContractSerializer
    queryset = UserContract.objects.all()                
    
    def get_queryset(self):
        user = self.request.user
        return UserContract.objects.select_related('property_id', 'property_id__area', 'property_id__property_type').filter(user=user)
    