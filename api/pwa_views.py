from django.views.generic import TemplateView
from django.http import JsonResponse

class ManifestView(TemplateView):
    content_type = 'application/manifest+json'
    template_name = 'manifest.json'
    
    def get_context_data(self, **kwargs):
        return {
            'name': 'AmakaziWatch',
            'short_name': 'Amakazi',
            'description': 'GBV reporting and support platform',
            'theme_color': '#FF6B6B',
            'background_color': '#FFFFFF'
        }

class OfflineView(TemplateView):
    template_name = 'offline.html'
