from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import Notification, AuditLog


class NotificationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        unread = notifications.filter(is_read=False).count()
        return Response({
            "unread_count": unread,
            "notifications": [{
                "id":         n.id,
                "type":       n.type,
                "title":      n.title,
                "message":    n.message,
                "is_read":    n.is_read,
                "created_at": n.created_at,
            } for n in notifications[:20]]
        })


class NotificationMarkReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk=None):
        if pk:
            Notification.objects.filter(pk=pk, user=request.user).update(is_read=True)
            return Response({"message": "Notification marked as read"})
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({"message": "All notifications marked as read"})


class AuditLogListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not request.user.is_platform_admin():
            return Response({"error": "Admin only"}, status=403)

        logs = AuditLog.objects.all()[:50]
        return Response([{
            "id":         l.id,
            "user":       l.user.username if l.user else "system",
            "action":     l.action,
            "model":      l.model_name,
            "object_id":  l.object_id,
            "details":    l.details,
            "ip":         l.ip_address,
            "created_at": l.created_at,
        } for l in logs])
