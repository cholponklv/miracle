from django.shortcuts import render 
from .models import Map, Team, Hero , HeroTeam
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework import generics,mixins, viewsets, filters
from .serializer import MapSerializer , HeroTeamSerializer, TeamSerializer ,HeroSerializer , AddHeroSerializer, DeleteHeroSerializer , TeamSerializer2

from .permissions import IsAdminOrReadOnly , IsOwner
from user.models import User
from rest_framework.response import Response
import datetime
import telebot
from rest_framework.decorators import action
from django_filters import rest_framework as dj_filters
from .filters import TeamFilter


bot_token = "6067726634:AAHTmPG2RnXttGKu75pC502kAYs2L56AP5Y"  
bot = telebot.TeleBot(bot_token)

class MapViewSet(viewsets.ModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer
    permission_classes = [IsAdminOrReadOnly]
class HeroViewSet(viewsets.ModelViewSet):
    queryset = Hero.objects.all()
    serializer_class = HeroSerializer
    
class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsOwner]
    filter_backends = (dj_filters.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    # filterset_fields = ('user', 'heroes')
    filterset_class = TeamFilter
    ordering_fields = ('name', 'total_power', 'amount')
    search_fields = ('name', ' heroes__name')
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Team.objects.all()
        return Team.objects.filter(user=self.request.user)
    
    def perform_destroy(self, instance):
        chat_ids = User.objects.filter(is_staff=True).values_list('chat_id', flat=True)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for chat_id in chat_ids:
            message_text = f'Пользователь {str(instance.user.username)} удалил команду {instance.name} в {current_time}'
            bot.send_message(chat_id, message_text)

        instance.delete()


    @action(detail=True, methods=['POST'], serializer_class=AddHeroSerializer)
    def add_hero(self, request, pk = None):
        team = self.get_object()
        serializer = AddHeroSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        hero = serializer.validated_data['hero']
        is_captain = serializer.validated_data['is_captain']
        if is_captain:
            team.hero_team.filter(is_captain=True).update(is_captain=False)

        hero_team = HeroTeam.objects.create(team = team , hero = hero, is_captain = is_captain)
        return Response({'status':'ok'})

    @action(detail=True, methods=['DELETE'], serializer_class = DeleteHeroSerializer)
    def delete_hero(self, request, pk = None):
        team = self.get_object()
        serializer = DeleteHeroSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        hero = serializer.validated_data['hero']
        hero = HeroTeam.objects.get(hero=hero)
        hero.delete()
        return Response({'status':'ok'})
    
    @action(detail=True, methods=['GET'], serializer_class = HeroSerializer)
    def heroes(self, request, pk):
        team = self.get_object()
        heroteam = HeroTeam.objects.filter(team = team)
        serializer = HeroTeamSerializer(heroteam, many = True)
        heroes = [item['hero'] for item in serializer.data]
        ls = []
        for i in heroes:
            ls.append(Hero.objects.get(id=i))
        serializer = HeroSerializer(ls, many=True)
        print(serializer.data)
        return Response(serializer.data)
    
  
    