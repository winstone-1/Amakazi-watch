from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from reports.models import IncidentReport
from organisations.models import Organisation, Donation
from content.models import EducationContent, Quiz
from reports.utils.sms import send_case_reference_sms
from .serializers import (
    IncidentReportSerializer, OrganisationSerializer,
    DonationSerializer, EducationContentSerializer,
    QuizSerializer, UserRegisterSerializer
)


# ── Reports ───────────────────────────────────────────────────────────────────
class ReportCreateView(generics.CreateAPIView):
    serializer_class   = IncidentReportSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        import random, string
        ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

        # Get optional phone from request
        phone = self.request.data.get('phone', None)

        report = serializer.save(sms_ref_code=ref)

        # Send SMS if phone provided
        if phone:
            send_case_reference_sms(phone, ref)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                'message': 'Report submitted successfully.',
                'ref_code': serializer.instance.sms_ref_code,
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class HeatmapView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = (
            IncidentReport.objects
            .values('county')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        return Response(data)


# ── Organisations ─────────────────────────────────────────────────────────────
class OrganisationListView(generics.ListAPIView):
    serializer_class   = OrganisationSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs     = Organisation.objects.filter(verified=True)
        county = self.request.query_params.get('county')
        if county:
            qs = qs.filter(county__icontains=county)
        return qs


class OrganisationRegisterView(generics.CreateAPIView):
    serializer_class   = OrganisationSerializer
    permission_classes = [permissions.AllowAny]


# ── Content ───────────────────────────────────────────────────────────────────
class ContentListView(generics.ListAPIView):
    serializer_class   = EducationContentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs     = EducationContent.objects.filter(approved=True)
        topic  = self.request.query_params.get('topic')
        fmt    = self.request.query_params.get('format')
        if topic:
            qs = qs.filter(topic=topic)
        if fmt:
            qs = qs.filter(format=fmt)
        return qs


class ContentCreateView(generics.CreateAPIView):
    serializer_class   = EducationContentSerializer
    permission_classes = [permissions.IsAuthenticated]


# ── Quizzes ───────────────────────────────────────────────────────────────────
class QuizListView(generics.ListAPIView):
    serializer_class   = QuizSerializer
    permission_classes = [permissions.AllowAny]
    queryset           = Quiz.objects.filter(approved=True)


class QuizCompleteView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        try:
            quiz = Quiz.objects.get(pk=pk, approved=True)
            quiz.completion_count += 1
            quiz.save()
            return Response({'message': 'Completion recorded'})
        except Quiz.DoesNotExist:
            return Response({'error': 'Quiz not found'}, status=404)


# ── Auth ──────────────────────────────────────────────────────────────────────
class RegisterView(generics.CreateAPIView):
    serializer_class   = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


# ── Donations (Paystack) ──────────────────────────────────────────────────────
class DonationInitiateView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        from organisations.utils.paystack import initialize_donation
        from organisations.models import Organisation, Donation

        org_id   = request.data.get('organisation_id')
        amount   = request.data.get('amount')
        email    = request.data.get('email')
        callback = request.data.get('callback_url', 'http://localhost:8000/api/donations/verify/')

        if not all([org_id, amount, email]):
            return Response(
                {'error': 'organisation_id, amount and email are required'},
                status=400
            )

        try:
            org = Organisation.objects.get(id=org_id, verified=True)
        except Organisation.DoesNotExist:
            return Response({'error': 'Organisation not found'}, status=404)

        result = initialize_donation(email, float(amount), org_id, callback)

        if result['success']:
            Donation.objects.create(
                organisation=org,
                amount=amount,
                phone=email,
                mpesa_checkout_id=result['reference'],
                status='pending',
            )
            return Response({
                'payment_url': result['payment_url'],
                'reference': result['reference'],
            })

        return Response({'error': result['error']}, status=400)


class DonationVerifyView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        from organisations.utils.paystack import verify_payment
        from organisations.models import Donation

        reference = request.query_params.get('reference')
        if not reference:
            return Response({'error': 'reference is required'}, status=400)

        result = verify_payment(reference)

        if result['success']:
            try:
                donation = Donation.objects.get(mpesa_checkout_id=reference)
                donation.status = 'completed'
                donation.mpesa_receipt = reference
                donation.save()
            except Donation.DoesNotExist:
                pass
            return Response({'message': 'Payment verified', 'amount': result['amount']})

        return Response({'error': result['error']}, status=400)
