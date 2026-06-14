from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Workshop, WorkshopAttendance
from .serializers import WorkshopSerializer, WorkshopAttendanceSerializer

class WorkshopViewSet(viewsets.ModelViewSet):
    serializer_class = WorkshopSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return Workshop.objects.filter(scheduled_start__gte=timezone.now())
    
    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        workshop = self.get_object()
        if request.user.is_authenticated:
            attendance, created = WorkshopAttendance.objects.get_or_create(
                user=request.user,
                workshop=workshop
            )
            return Response({'message': 'Registered successfully'})
        return Response({'error': 'Login required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    @action(detail=True, methods=['post'])
    def feedback(self, request, pk=None):
        workshop = self.get_object()
        attendance = WorkshopAttendance.objects.get(workshop=workshop, user=request.user)
        attendance.feedback_rating = request.data.get('rating')
        attendance.feedback_text = request.data.get('feedback')
        attendance.save()
        return Response({'message': 'Feedback submitted'})
