from rest_framework.permissions import BasePermission

class IsCounselor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'counselor'

class IsAdminOrCounselor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'counselor']

class IsAdminOrOrgStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'org_staff']
