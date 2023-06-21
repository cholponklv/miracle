from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_superuser:  
            return True
        
        if request.method in SAFE_METHODS:  
            return request.user and request.user.is_authenticated
        
        return False  


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.user == request.user