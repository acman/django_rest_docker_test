from rest_framework import permissions


class AnonCreateAndRetrieveUpdateDeleteOwnerOrStaffOnly(permissions.BasePermission):
    """
    Custom permission:
        - allow anonymous POST
        - allow authenticated GET, PUT, DELETE on *own* record
        - allow all actions for staff
    """

    def has_permission(self, request, view):
        return view.action == 'create' or request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (view.action in ['retrieve', 'update', 'partial_update', 'delete']
                and obj.client.id == request.user.id
                or request.user.is_staff)
