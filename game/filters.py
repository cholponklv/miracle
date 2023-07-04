from django_filters.rest_framework import filterset
from .models import Team



class TeamFilter(filterset.FilterSet):
    class Meta:
        model = Team
        fields = ('user', 'heroes')
        