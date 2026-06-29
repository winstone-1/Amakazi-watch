from django.utils import translation
from django.utils.deprecation import MiddlewareMixin

class LanguageMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Check for language in header or session
        language = request.headers.get('Accept-Language', 'en')
        
        # Also check POST data for language switch
        if request.method == 'POST' and request.path == '/api/language/':
            try:
                import json
                data = json.loads(request.body)
                language = data.get('language', 'en')
                request.session['django_language'] = language
            except:
                pass
        elif request.session.get('django_language'):
            language = request.session['django_language']
        
        # Validate language
        if language not in ['en', 'sw']:
            language = 'en'
        
        translation.activate(language)
        request.LANGUAGE_CODE = language
    
    def process_response(self, request, response):
        if hasattr(request, 'LANGUAGE_CODE'):
            response['Content-Language'] = request.LANGUAGE_CODE
        return response
