from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import LegalQuery, KenyanLawReference
from .serializers import *

class LegalQueryViewSet(viewsets.ModelViewSet):
    serializer_class = LegalQuerySerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return LegalQuery.objects.all()
    
    @action(detail=False, methods=['post'])
    def ask(self, request):
        question = request.data.get('question')
        # Integrate with GPT or legal KB here
        answer = f"Based on Kenyan law regarding: {question}"
        query = LegalQuery.objects.create(
            session_id=request.data.get('session_id', 'anonymous'),
            question=question,
            answer=answer
        )
        return Response({'answer': answer, 'query_id': query.id})

class KenyanLawReferenceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = KenyanLawReferenceSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = KenyanLawReference.objects.all()
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(keywords__icontains=q)
        return queryset
