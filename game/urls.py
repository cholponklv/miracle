from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MapViewSet, TeamViewSet , HeroViewSet

router = DefaultRouter()
router.register(r'map', MapViewSet)
router.register(r'team', TeamViewSet)
router.register(r'hero', HeroViewSet)

urlpatterns = [
    path('', include(router.urls))

]