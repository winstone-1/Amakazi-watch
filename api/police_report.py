from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class PoliceReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, ref_code):
        return Response({
            'pdf_url': f'/reports/police/{ref_code}.pdf',
            'message': 'Police report generated successfully'
        })
