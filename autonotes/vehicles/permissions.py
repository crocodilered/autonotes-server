from rest_framework.permissions import BasePermission


class OwnerPerm(BasePermission):
    # User must be vehicle owner to deal with.
    def has_object_permission(self, request, view, vehicle):
        return request.user == vehicle.user
