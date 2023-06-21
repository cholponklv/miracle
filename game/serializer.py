from rest_framework import serializers
from .models import Map, HeroTeam, Hero, Team
from user.models import User
import datetime
import telebot

bot_token = "6067726634:AAHTmPG2RnXttGKu75pC502kAYs2L56AP5Y"  
bot = telebot.TeleBot(bot_token)


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ('name','describe')

class HeroTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroTeam
        fields = ('id','team', 'hero', 'is_captain')

class TeamSerializer(serializers.ModelSerializer):
    hero_team = HeroTeamSerializer(many=True)
    class Meta:
        model = Team
        fields = ('id','name', 'user','hero_team', 'amount', 'total_power', )

    def create(self, validated_data):
        hero_team = validated_data.pop('hero_team')
        team = Team.objects.create(**validated_data)
        total_amount = 0
        total_power = 0
        to_create = []

        for ht in hero_team:
            hero = ht['hero']
            is_captain = ht['is_captain']
            power = hero.power
            amount = 1
            total_power += power
            total_amount += amount
            to_create.append(HeroTeam(team = team, hero= hero,is_captain = is_captain))
        HeroTeam.objects.bulk_create(to_create)
        team.amount = total_amount
        team.total_power= total_power

        team.save()

        chat_ids = User.objects.filter(is_staff=True).values_list('chat_id', flat=True)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for chat_id in chat_ids:
            message_text = f'Пользователь {str(team.user.username)} создал команду {team.name} в {current_time}'
            bot.send_message(chat_id, message_text)
        return(team)
        

    def update(self, instance, validated_data):
        hero_team = validated_data.pop('hero_team')
        hero_team_by_pk = {ht['hero'].id: ht for ht in hero_team}
        team = super().update(instance,validated_data)
        db_hero = set(team.hero_team.all().values_list('hero_id', flat = True))
        new_hero = set([ht['hero'].id for ht in hero_team])

        to_create = new_hero.difference(db_hero)
        to_delete = db_hero.difference(new_hero)
        to_update = new_hero.intersection(db_hero)

        to_create_objects = []
        for hero_id in to_create:
            hero_team = hero_team_by_pk[hero_id]
            hero = hero_team['hero']
            is_captain = hero_team['is_captain']
            
            to_create_objects.append(HeroTeam(team = team, hero= hero,is_captain = is_captain))
    
        HeroTeam.objects.bulk_create(to_create_objects)

        team.hero_team.filter(hero_id__in=to_delete).delete()
        
        to_update_objects = []
        for hero_id in to_update:
            hero_team = hero_team_by_pk[hero_id]
            hero = hero_team['hero']
            is_captain = hero_team['is_captain']
            db_hero_team = team.hero_team.get(hero_id=hero_id)

            to_update_objects.append(db_hero_team)

        HeroTeam.objects.bulk_update(to_update_objects, ['is_captain'])
        chat_ids = User.objects.filter(is_staff=True).values_list('chat_id', flat=True)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for chat_id in chat_ids:
            message_text = f'Пользователь {str(team.user.username)} изменил команду {team.name} в {current_time}'
            bot.send_message(chat_id, message_text)
        team.save()
        return team

