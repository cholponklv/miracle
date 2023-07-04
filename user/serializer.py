
from rest_framework import serializers
from .models import User
from phonenumber_field.serializerfields import PhoneNumberField


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length = 255)
    password = serializers.CharField(max_length = 255)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'phone_number', 'email', 'chat_id','password')

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'phone_number', 'email' ,'password')
        extra_kwargs = {'password':{'write_only':True}}

