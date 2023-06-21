from django.shortcuts import render 
from .models import Map, Team
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework import generics,mixins, viewsets
from .serializer import MapSerializer , HeroTeamSerializer, TeamSerializer
from .permissions import IsAdminOrReadOnly , IsOwnerOrReadOnly
from user.models import User
from rest_framework.response import Response
import datetime
import telebot


bot_token = "6067726634:AAHTmPG2RnXttGKu75pC502kAYs2L56AP5Y"  
bot = telebot.TeleBot(bot_token)

class MapViewSet(viewsets.ModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer
    permission_classes = [IsAdminOrReadOnly]


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_destroy(self, instance):
        chat_ids = User.objects.filter(is_staff=True).values_list('chat_id', flat=True)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for chat_id in chat_ids:
            message_text = f'Пользователь {str(instance.user.username)} удалил команду {instance.name} в {current_time}'
            bot.send_message(chat_id, message_text)

        instance.delete()

