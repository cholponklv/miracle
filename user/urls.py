from django.urls import path, include
from user import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', viewset=views.UserViewSet , basename='users')

urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', views.LoginApiView.as_view(), name='login'),
    path('register/', views.RegisterAPIView.as_view(), name = 'register')

]