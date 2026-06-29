from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import FAQ
from .serializers import FAQSerializer

class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = FAQ.objects.filter(is_active=True)
    serializer_class = FAQSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset
