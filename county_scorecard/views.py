from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CountyScorecard, ScorecardHistory
from .serializers import CountyScorecardSerializer, ScorecardHistorySerializer

class CountyScorecardViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CountyScorecardSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return CountyScorecard.objects.all().order_by('rank')
    
    @action(detail=False, methods=['get'])
    def rankings(self, request):
        scorecards = self.get_queryset()
        return Response([
            {'county': s.county, 'overall_score': s.overall_score, 'rank': s.rank}
            for s in scorecards
        ])
