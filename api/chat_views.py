from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone

class ChatView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        message = request.data.get('message', '')
        
        # Simple response logic
        responses = {
            'help': 'I can help you with: reporting, safety tips, legal rights, finding support.',
            'report': 'To file a report, go to the Reports section and click "Report Now".',
            'safety': 'Your safety is important. Use the Safety Timer and Emergency SOS button.',
            'legal': 'Kenyan law protects you. Visit the Legal Bot for more information.',
            'default': 'I\'m here to help. Try asking about: help, report, safety, or legal.'
        }
        
        # Check for keywords
        response_text = responses.get('default')
        for key, value in responses.items():
            if key in message.lower():
                response_text = value
                break
        
        return Response({
            'response': response_text,
            'timestamp': timezone.now().isoformat()
        })
