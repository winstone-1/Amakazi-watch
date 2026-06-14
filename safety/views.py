from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import SafetyTimer, SafeWord, RiskAssessment, EscapePlan
from .serializers import (
    SafetyTimerSerializer, SafeWordSerializer, 
    RiskAssessmentSerializer, EscapePlanSerializer
)

class SafetyTimerViewSet(viewsets.ModelViewSet):
    serializer_class = SafetyTimerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SafetyTimer.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def start(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, status='active')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def check_in(self, request):
        timer = SafetyTimer.objects.filter(user=request.user, status='active').first()
        if not timer:
            return Response({'error': 'No active timer'}, status=status.HTTP_404_NOT_FOUND)
        timer.status = 'checked_in'
        timer.check_in_time = timezone.now()
        timer.save()
        return Response({'message': 'Checked in successfully'})

class SafeWordViewSet(viewsets.ModelViewSet):
    serializer_class = SafeWordSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SafeWord.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def trigger(self, request):
        safe_word = SafeWord.objects.filter(user=request.user, is_active=True).first()
        if not safe_word:
            return Response({'error': 'No active safe word'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Alert triggered successfully'})

class RiskAssessmentViewSet(viewsets.ModelViewSet):
    serializer_class = RiskAssessmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return RiskAssessment.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        answers = self.request.data.get('answers', {})
        score = sum(1 for v in answers.values() if v)
        risk_level = 'low' if score < 3 else 'medium' if score < 7 else 'high'
        serializer.save(user=self.request.user, score=score, risk_level=risk_level)

class EscapePlanViewSet(viewsets.ModelViewSet):
    serializer_class = EscapePlanSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return EscapePlan.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
