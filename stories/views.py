from rest_framework import viewsets, permissions
from .models import Story
from .serializers import StorySerializer

class StoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = StorySerializer
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Story.objects.all()
        return Story.objects.filter(is_approved=True)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
