from rest_framework.permissions import BasePermission

from users.models import UserRole


class IsSelectionOwnerPermission(BasePermission):
    message = "Только владелец может вносить правки"

    def has_object_permission(self, request, view, selection) -> bool:
        if request.user == selection.owner:
            return True

        return False


class IsAdSelectionOwner(BasePermission):
    message = "У вас нет прав на изменение объявления"

    def has_object_permission(self, request, view, ad) -> bool:
        print(ad)
        if request.user == ad.author or request.user.role != UserRole.MEMBER:
            return True
        return False
