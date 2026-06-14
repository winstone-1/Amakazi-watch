from rest_framework.views import APIView
from rest_framework.response import Response
from user_agents import parse

class ResponsiveAPIView(APIView):
    def get_response_format(self, request):
        user_agent = parse(request.META.get('HTTP_USER_AGENT', ''))
        if user_agent.is_mobile:
            return 'mobile'
        elif user_agent.is_tablet:
            return 'tablet'
        return 'desktop'
    
    def finalize_response(self, request, response, *args, **kwargs):
        # Add device info to response headers
        response['X-Device-Type'] = self.get_response_format(request)
        return super().finalize_response(request, response, *args, **kwargs)
