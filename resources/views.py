from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Resource
from .serializers import ResourceSerializer

class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Resource.objects.filter(is_active=True)
    serializer_class = ResourceSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset
