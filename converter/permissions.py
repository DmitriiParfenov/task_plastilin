from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsActiveAndIsOwner(BasePermission):
    """
    Доступ разрешен только авторизованным пользователям. Детали записей могут смотреть только владельцы записей.
    Пользователь может видеть список всех объектов без возможности их как-то редактировать или удалять, если он не
    является их владельцем.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user == obj.converter_user
        elif request.method in ('PATCH', 'PUT', 'POST'):
            return request.user == obj.converter_user
        elif request.method == 'DELETE':
            if not request.user.is_authenticated:
                return False
            return request.user == obj.converter_user or request.user.is_superuser
        return False
