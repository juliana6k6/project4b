from rest_framework import permissions

class IsModer(permissions.BasePermission):
    """Класс для проверки роли модератора"""
    message = 'Доступно модераторам.'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators').exists()

class IsOwner(permissions.BasePermission):
    """Класс для проверки принадлежности продукта владельцу"""
    message = "Доступно владельцу"
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False

