from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework.exceptions import NotFound
from .serializer import LoginSerializer, UserSerializer,UserRegisterSerializer

from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics,mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from .models import User
import telebot
import datetime
from rest_framework.decorators import action
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
# Create your views here.
bot_token = "6067726634:AAHTmPG2RnXttGKu75pC502kAYs2L56AP5Y"  
bot = telebot.TeleBot(bot_token)

class LoginApiView(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = LoginSerializer


    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        password = serializer.validated_data['password']
        user = authenticate(request=request, phone_number=phone_number, password=password) 

        if not user:
            raise AuthenticationFailed()
        
        token, _ = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'user': UserSerializer(user).data,
        }
        

        emails = User.objects.filter(is_staff=True).values_list('email', flat=True)
        message = f'Пользователь {user.pk} {user.phone_number} {user.username} авторизовался' \
                f' в системе в {datetime.now()}'
        send_mail('Авторизация', message, settings.EMAIL_HOST_USER, emails)




        return Response(data=data, status=200)

    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer









class RegisterAPIView(generics.GenericAPIView):
    serializer_class=UserRegisterSerializer
    authentication_classes=()
    permission_classes=()

    def post(self,request):
        serializer = UserRegisterSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.pop('password')
        user = User(**serializer.validated_data)
        user.set_password(password)
        user.save()

        user.send_verification_code_to_email()

        data = UserSerializer(user).data
        return Response(data=data,status=201)























        # try:
        #     chat_ids = User.objects.filter(is_staff=True).values_list('chat_id', flat=True)
        #     current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #     for chat_id in chat_ids:
        #         message_text = f'Пользователь {str(user.username)} авторизовался в {current_time}'
        #         bot.send_message(chat_id, message_text)
        # except:
        #     pass


        