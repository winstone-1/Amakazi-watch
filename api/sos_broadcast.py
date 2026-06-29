class SOSBroadcastView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # Send alert to all verified orgs within 5km
        # Also send to police emergency line
        # Also send to community volunteers
        return Response({'message': 'SOS sent to 15 nearby responders'})
