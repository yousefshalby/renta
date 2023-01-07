from rest_framework import serializers
from project.models import Area, ContactUs, ContactInfo, AboutUs, UserContract, User, PropertyType, Properties
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from project.services import CustomModelSerializer


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = "__all__"

class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = ["address", "email", "contact_no", 'find_us']


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = "__all__"

class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = "__all__"

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = "__all__"


class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=200)
    refresh_token = serializers.CharField(max_length=200)


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(
        trim_whitespace=False,
    )

    def validate(self, attrs):
        password = attrs.get("password", None)
        email = attrs.get("email")
        user = self._login_by_login_phone(email, password)
        attrs["user"] = user
        return attrs

    def _login_by_login_phone(self, email, password):
        user = User.objects.filter(email=email).first()

        if user is None:
            self._raise_login_validation_error()

        if user and not user.check_password(password):
            self._raise_login_validation_error()

        return user

    def _raise_login_validation_error(self):
        msg = {"details": [_("Unable to log in with provided credentials.")]}
        raise serializers.ValidationError(msg, code="authorization")



class UserSerializer(CustomModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    class Meta:
        model = User
        fields = (
            "id",
            "phone",
            "password",
            'email', 
            'gender',
            'date_of_birth',
            'first_name',
            'last_name',
            'address',
            
        )
    
    def validate(self, validated_data):
        if self.context['request'].method == "POST":
            if 'email' not in validated_data:
                    raise ValidationError(_("you must provide email to signUp")) 
                
            if User.objects.filter(email=validated_data['email'], is_active=True).exists():
                raise serializers.ValidationError(_("Email already exist"))
            
        elif self.context['request'].method == "PUT":
            if (
                'email' in validated_data
                and User.objects.filter(
                    email=validated_data['email'], is_active=True
                ).exists()
            ):
                raise serializers.ValidationError(_("Email already exist"))
                    
            if "password" in validated_data:
                raise serializers.ValidationError(_("can not update password."))
        return validated_data
    

class PropertiesSerializer(serializers.ModelSerializer):
    area = AreaSerializer(many=True, read_only=True)
    property_type = PropertyTypeSerializer(many=True, read_only=True)
    class Meta:
        model = Properties
        fields = "__all__"

    
    
class UserContractSerializer(serializers.ModelSerializer):
    area = PropertiesSerializer(many=True, read_only=True)
    property_type = PropertyTypeSerializer(many=True, read_only=True)
    class Meta:
        model = UserContract
        fields = "__all__"
    