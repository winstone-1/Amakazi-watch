from drf_spectacular.utils import (
    extend_schema, extend_schema_view,
    OpenApiParameter, OpenApiResponse,
    OpenApiExample, OpenApiTypes
)
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
    QuizSerializer, UserRegisterSerializer,
    DonationInitiateSerializer, ChatSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    PasswordChangeSerializer,
    TwoFactorVerifySerializer,
    TwoFactorDisableSerializer,
    GoogleAuthCallbackSerializer,
)


# ── Reports ───────────────────────────────────────────────────────────────────
@extend_schema(
    tags=['Reports'],
    request=IncidentReportSerializer,
    responses={
        201: OpenApiResponse(
            response=IncidentReportSerializer,
            description='Report submitted successfully.',
            examples=[
                OpenApiExample(
                    'ReportExample',
                    summary='Example incident report',
                    value={
                        'abuse_type': 'Physical',
                        'relationship': 'Stranger',
                        'county': 'Nairobi',
                        'sub_county': 'Westlands',
                        'description': 'I witnessed a violent incident near the market.',
                        'phone': '+254700000000',
                    },
                    request_only=True,
                )
            ]
        )
    }
)
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

        # AI classification
        if report.description:
            from api.utils.Groq import classify_report
            result = classify_report(report.description, report.abuse_type)
            if result["success"]:
                data = result["data"]
                report.urgency_score      = data.get("urgency_score")
                report.ai_classification  = data.get("confirmed_abuse_type", "")
                report.flagged_for_review = data.get("flag_for_review", False)
                report.save()

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


@extend_schema(
    tags=['Reports'],
    responses=OpenApiResponse(
        response=list,
        description='County heatmap report counts'
    )
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
@extend_schema(
    tags=['Organisations'],
    parameters=[
        OpenApiParameter(
            name='county',
            location=OpenApiParameter.QUERY,
            description='Filter organisations by county',
            required=False,
            type=str,
        ),
    ],
    responses=OpenApiResponse(response=OrganisationSerializer(many=True))
)
class OrganisationListView(generics.ListAPIView):
    serializer_class   = OrganisationSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs     = Organisation.objects.filter(verified=True)
        county = self.request.query_params.get('county')
        if county:
            qs = qs.filter(county__icontains=county)
        return qs


@extend_schema(
    tags=['Organisations'],
    request=OrganisationSerializer,
    responses=OpenApiResponse(response=OrganisationSerializer)
)
class OrganisationRegisterView(generics.CreateAPIView):
    serializer_class   = OrganisationSerializer
    permission_classes = [permissions.AllowAny]


# ── Content ───────────────────────────────────────────────────────────────────
@extend_schema(
    tags=['Content'],
    parameters=[
        OpenApiParameter(
            name='topic',
            location=OpenApiParameter.QUERY,
            description='Filter content by topic',
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name='format',
            location=OpenApiParameter.QUERY,
            description='Filter content by format',
            required=False,
            type=str,
        ),
    ],
    responses=OpenApiResponse(response=EducationContentSerializer(many=True))
)
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


@extend_schema(
    tags=['Content'],
    request=EducationContentSerializer,
    responses=OpenApiResponse(response=EducationContentSerializer)
)
class ContentCreateView(generics.CreateAPIView):
    serializer_class   = EducationContentSerializer
    permission_classes = [permissions.IsAuthenticated]


# ── Quizzes ───────────────────────────────────────────────────────────────────
@extend_schema(
    tags=['Content'],
    responses=OpenApiResponse(response=QuizSerializer(many=True))
)
class QuizListView(generics.ListAPIView):
    serializer_class   = QuizSerializer
    permission_classes = [permissions.AllowAny]
    queryset           = Quiz.objects.filter(approved=True)


@extend_schema(
    tags=['Content'],
    responses=OpenApiResponse(
        response=OpenApiTypes.OBJECT,
        description='Quiz completion acknowledgement'
    )
)
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
@extend_schema(
    tags=['Auth'],
    request=UserRegisterSerializer,
    responses=OpenApiResponse(response=UserRegisterSerializer)
)
class RegisterView(generics.CreateAPIView):
    serializer_class   = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


# ── Donations (Paystack) ───────────────────────────────────────────────────────
@extend_schema(
    tags=['Donations'],
    request=DonationInitiateSerializer,
    responses=OpenApiResponse(
        response=DonationSerializer,
        description='Donation initialization response',
        examples=[
            OpenApiExample(
                'DonationInitExample',
                summary='Initialize Paystack donation',
                value={
                    'organisation_id': 1,
                    'amount': '500.00',
                    'email': 'donor@example.com',
                    'callback_url': 'https://example.com/callback/',
                },
                request_only=True,
            )
        ]
    )
)
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


@extend_schema(
    tags=['Donations'],
    parameters=[
        OpenApiParameter(
            name='reference',
            location=OpenApiParameter.QUERY,
            description='Paystack payment reference to verify',
            required=True,
            type=str,
        ),
    ],
    responses=OpenApiResponse(response=OpenApiTypes.OBJECT)
)
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


# -- Claude AI Chat ------------------------------------------------------------
@extend_schema(
    tags=['Chat'],
    request=ChatSerializer,
    responses=OpenApiResponse(response=OpenApiTypes.OBJECT)
)
class ChatView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        from api.utils.Groq import chat_with_groq
        message = request.data.get("message")
        history = request.data.get("history", [])

        if not message:
            return Response({"error": "message is required"}, status=400)

        result = chat_with_groq(message, history)

        if result["success"]:
            return Response({"message": result["message"]})

        return Response({"error": result["error"]}, status=500)


# -- Analytics / CSV Export ---------------------------------------------------
@extend_schema(
    tags=['Analytics'],
    parameters=[
        OpenApiParameter(
            name='days',
            location=OpenApiParameter.QUERY,
            description='Number of days to include in the summary',
            required=False,
            type=int,
        ),
    ],
    responses=OpenApiResponse(response=OpenApiTypes.OBJECT)
)
class CountySummaryExportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from reports.utils.analytics import generate_county_summary
        from django.http import HttpResponse

        days = int(request.query_params.get("days", 30))
        csv_data, error = generate_county_summary(days=days)

        if error:
            return Response({"error": error}, status=404)

        response = HttpResponse(csv_data, content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename=amakaziwatch_county_summary_{days}days.csv"
        return response


@extend_schema(
    tags=['Analytics'],
    parameters=[
        OpenApiParameter(
            name='days',
            location=OpenApiParameter.QUERY,
            description='Number of days to include in the trend report',
            required=False,
            type=int,
        ),
    ],
    responses=OpenApiResponse(response=OpenApiTypes.OBJECT)
)
class TrendReportExportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from reports.utils.analytics import generate_trend_report
        from django.http import HttpResponse

        days = int(request.query_params.get("days", 30))
        csv_data, error = generate_trend_report(days=days)

        if error:
            return Response({"error": error}, status=404)

        response = HttpResponse(csv_data, content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename=amakaziwatch_trend_{days}days.csv"
        return response


# -- Report Statistics --------------------------------------------------------
@extend_schema(
    tags=['Reports'],
    responses=OpenApiResponse(response=OpenApiTypes.OBJECT)
)
class ReportStatsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        from django.db.models import Count
        from reports.models import IncidentReport

        total = IncidentReport.objects.count()

        by_type = list(
            IncidentReport.objects
            .values("abuse_type")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        by_county = list(
            IncidentReport.objects
            .values("county")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )

        recent = IncidentReport.objects.order_by("-created_at")[:5]
        from .serializers import IncidentReportSerializer
        recent_data = IncidentReportSerializer(recent, many=True).data

        # Percentages per abuse type
        for item in by_type:
            item["percentage"] = round((item["count"] / total * 100), 1) if total else 0

        return Response({
            "total_reports": total,
            "by_abuse_type": by_type,
            "by_county":     by_county,
            "recent":        recent_data,
        })


# -- NGO / County Impact Dashboard --------------------------------------------
@extend_schema(
    tags=['Organisations'],
    responses=OpenApiResponse(response=OpenApiTypes.OBJECT)
)
class OrganisationImpactView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        from organisations.models import Organisation, Donation
        from reports.models import IncidentReport
        from content.models import EducationContent, Quiz
        from django.db.models import Sum

        try:
            org = Organisation.objects.get(pk=pk, verified=True)
        except Organisation.DoesNotExist:
            return Response({"error": "Organisation not found"}, status=404)

        total_donations = Donation.objects.filter(
            organisation=org, status="completed"
        ).aggregate(total=Sum("amount"))["total"] or 0

        reports_in_county = IncidentReport.objects.filter(
            county__icontains=org.county
        ).count()

        content_count = EducationContent.objects.filter(
            organisation=org, approved=True
        ).count()

        quiz_completions = Quiz.objects.filter(
            organisation=org, approved=True
        ).aggregate(total=Sum("completion_count"))["total"] or 0

        return Response({
            "organisation":      org.name,
            "county":            org.county,
            "org_type":          org.org_type,
            "reports_in_county": reports_in_county,
            "total_donations":   total_donations,
            "content_published": content_count,
            "quiz_completions":  quiz_completions,
        })


# -- Search -------------------------------------------------------------------
@extend_schema(
    tags=['Search'],
    parameters=[
        OpenApiParameter(
            name='q',
            location=OpenApiParameter.QUERY,
            description='Search text for organisations, content and quizzes',
            required=True,
            type=str,
        ),
    ],
    responses=OpenApiResponse(response=OpenApiTypes.OBJECT)
)
class SearchView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        from organisations.models import Organisation
        from content.models import EducationContent, Quiz
        from .serializers import OrganisationSerializer, EducationContentSerializer, QuizSerializer

        q = request.query_params.get("q", "").strip()
        if not q:
            return Response({"error": "q parameter is required"}, status=400)

        orgs = Organisation.objects.filter(
            verified=True,
            name__icontains=q
        ) | Organisation.objects.filter(
            verified=True,
            county__icontains=q
        ) | Organisation.objects.filter(
            verified=True,
            services__icontains=q
        )

        content = EducationContent.objects.filter(
            approved=True,
            title__icontains=q
        ) | EducationContent.objects.filter(
            approved=True,
            body__icontains=q
        )

        quizzes = Quiz.objects.filter(approved=True, title__icontains=q)

        return Response({
            "organisations": OrganisationSerializer(orgs.distinct(), many=True).data,
            "content":       EducationContentSerializer(content.distinct(), many=True).data,
            "quizzes":       QuizSerializer(quizzes.distinct(), many=True).data,
        })


# -- Featured Content ---------------------------------------------------------
@extend_schema(
    tags=['Content'],
    responses=OpenApiResponse(response=OpenApiTypes.OBJECT)
)
class FeaturedContentView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        from content.models import EducationContent, Quiz
        from .serializers import EducationContentSerializer, QuizSerializer

        articles = EducationContent.objects.filter(
            approved=True
        ).order_by("-created_at")[:3]

        quiz = Quiz.objects.filter(approved=True).order_by("-created_at").first()

        return Response({
            "featured_articles": EducationContentSerializer(articles, many=True).data,
            "featured_quiz":     QuizSerializer(quiz).data if quiz else None,
        })


# -- User Profile -------------------------------------------------------------
@extend_schema(
    tags=['Profile'],
    responses={
        200: OpenApiResponse(response=OpenApiTypes.OBJECT),
    }
)
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from users.profile import UserProfile
        from .serializers import UserProfileSerializer

        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        return Response(UserProfileSerializer(profile).data)

    def patch(self, request):
        from users.profile import UserProfile
        from .serializers import UserProfileSerializer

        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


# -- Bookmark Organisation ----------------------------------------------------
@extend_schema(
    tags=['Organisations'],
    responses=OpenApiResponse(response=OpenApiTypes.OBJECT)
)
class BookmarkOrgView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        from users.profile import UserProfile
        from organisations.models import Organisation

        try:
            org = Organisation.objects.get(pk=pk, verified=True)
        except Organisation.DoesNotExist:
            return Response({"error": "Organisation not found"}, status=404)

        profile, _ = UserProfile.objects.get_or_create(user=request.user)

        if org in profile.bookmarked_orgs.all():
            profile.bookmarked_orgs.remove(org)
            return Response({"message": f"Removed {org.name} from bookmarks"})
        else:
            profile.bookmarked_orgs.add(org)
            return Response({"message": f"Bookmarked {org.name}"})


# -- County Official Heatmap --------------------------------------------------
@extend_schema(
    tags=['Reports'],
    responses=OpenApiResponse(response=OpenApiTypes.OBJECT)
)
class CountyOfficialHeatmapView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from django.db.models import Count
        from reports.models import IncidentReport

        if not (request.user.is_county_official() or request.user.is_platform_admin()):
            return Response({"error": "County officials only"}, status=403)

        county = request.user.county
        if not county:
            return Response({"error": "No county assigned to your account"}, status=400)

        data = (
            IncidentReport.objects
            .filter(county__icontains=county)
            .values("sub_county", "abuse_type")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        return Response({
            "county": county,
            "breakdown": list(data),
            "total": IncidentReport.objects.filter(county__icontains=county).count(),
        })


# -- Maps ---------------------------------------------------------------------
@extend_schema(
    tags=['Organisations'],
    responses=OpenApiResponse(response=OpenApiTypes.OBJECT)
)
class OrganisationsGeoJSONView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        from organisations.utils.maps import get_organisations_geojson
        return Response(get_organisations_geojson())


@extend_schema(
    tags=['Organisations'],
    responses=OpenApiResponse(response=OpenApiTypes.OBJECT)
)
class HeatmapGeoJSONView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from organisations.utils.maps import get_heatmap_geojson
        return Response(get_heatmap_geojson())


# -- YouTube ------------------------------------------------------------------
@extend_schema(
    tags=['Content'],
    parameters=[
        OpenApiParameter(
            name='q',
            location=OpenApiParameter.QUERY,
            description='Search term for YouTube videos',
            required=False,
            type=str,
        ),
    ],
    responses=OpenApiResponse(response=OpenApiTypes.OBJECT)
)
class YoutubeVideosView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        from content.utils.youtube import search_youtube_videos
        query = request.query_params.get("q", "GBV awareness Kenya")
        videos = search_youtube_videos(query)
        return Response(videos)


# -- Password Reset -----------------------------------------------------------
@extend_schema(
    tags=['Auth'],
    request=PasswordResetRequestSerializer,
    responses=OpenApiResponse(response=OpenApiTypes.OBJECT)
)
class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        from django.core.mail import send_mail
        from django.conf import settings
        from users.models import User

        email = request.data.get("email")
        if not email:
            return Response({"error": "email is required"}, status=400)

        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid   = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"{request.scheme}://{request.get_host()}/api/auth/password-reset/confirm/?uid={uid}&token={token}"

            send_mail(
                subject="AmakaziWatch Password Reset",
                message=f"Click the link to reset your password: {reset_url}",
                from_email="noreply@amakaziwatch.org",
                recipient_list=[email],
                fail_silently=True,
            )
        except User.DoesNotExist:
            pass

        return Response({"message": "If that email exists, a reset link has been sent."})


@extend_schema(
    tags=['Auth'],
    request=PasswordResetConfirmSerializer,
    responses=OpenApiResponse(response=OpenApiTypes.OBJECT)
)
class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.http import urlsafe_base64_decode
        from django.utils.encoding import force_str
        from users.models import User

        uid      = request.data.get("uid")
        token    = request.data.get("token")
        password = request.data.get("password")

        if not all([uid, token, password]):
            return Response({"error": "uid, token and password are required"}, status=400)

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user    = User.objects.get(pk=user_id)
        except Exception:
            return Response({"error": "Invalid reset link"}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Reset link expired or invalid"}, status=400)

        if len(password) < 8:
            return Response({"error": "Password must be at least 8 characters"}, status=400)

        user.set_password(password)
        user.save()
        return Response({"message": "Password reset successfully. You can now log in."})


@extend_schema(
    tags=['Auth'],
    request=PasswordChangeSerializer,
    responses=OpenApiResponse(response=OpenApiTypes.OBJECT)
)
class PasswordChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not all([old_password, new_password]):
            return Response({"error": "old_password and new_password are required"}, status=400)

        if not request.user.check_password(old_password):
            return Response({"error": "Current password is incorrect"}, status=400)

        if len(new_password) < 8:
            return Response({"error": "New password must be at least 8 characters"}, status=400)

        request.user.set_password(new_password)
        request.user.save()
        return Response({"message": "Password changed successfully."})


# -- Two Factor Auth ----------------------------------------------------------
@extend_schema(
    tags=['Auth'],
    responses=OpenApiResponse(response=OpenApiTypes.OBJECT)
)
class TwoFactorSetupView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from django_otp.plugins.otp_totp.models import TOTPDevice
        import qrcode
        import qrcode.image.svg
        from io import BytesIO
        import base64

        device, created = TOTPDevice.objects.get_or_create(
            user=request.user,
            name="AmakaziWatch 2FA",
            defaults={"confirmed": False}
        )

        if device.confirmed:
            return Response({"message": "2FA is already enabled for this account."})

        config_url = device.config_url

        qr = qrcode.make(config_url)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()

        return Response({
            "config_url": config_url,
            "qr_code":    f"data:image/png;base64,{qr_base64}",
            "secret":     device.key,
            "message":    "Scan the QR code with Google Authenticator or Authy, then verify with a code."
        })

    def post(self, request):
        from django_otp.plugins.otp_totp.models import TOTPDevice

        code = request.data.get("code")
        if not code:
            return Response({"error": "code is required"}, status=400)

        try:
            device = TOTPDevice.objects.get(user=request.user, name="AmakaziWatch 2FA")
        except TOTPDevice.DoesNotExist:
            return Response({"error": "2FA not set up. Call GET first."}, status=400)

        if device.verify_token(code):
            device.confirmed = True
            device.save()
            return Response({"message": "2FA enabled successfully."})

        return Response({"error": "Invalid code. Try again."}, status=400)


@extend_schema(
    tags=['Auth'],
    request=TwoFactorVerifySerializer,
    responses=OpenApiResponse(response=OpenApiTypes.OBJECT)
)
class TwoFactorVerifyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        from django_otp.plugins.otp_totp.models import TOTPDevice

        code = request.data.get("code")
        if not code:
            return Response({"error": "code is required"}, status=400)

        try:
            device = TOTPDevice.objects.get(
                user=request.user,
                name="AmakaziWatch 2FA",
                confirmed=True
            )
        except TOTPDevice.DoesNotExist:
            return Response({"error": "2FA not enabled on this account"}, status=400)

        if device.verify_token(code):
            return Response({"message": "2FA verified successfully."})

        return Response({"error": "Invalid or expired code"}, status=400)


@extend_schema(
    tags=['Auth'],
    request=TwoFactorDisableSerializer,
    responses=OpenApiResponse(response=OpenApiTypes.OBJECT)
)
class TwoFactorDisableView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        from django_otp.plugins.otp_totp.models import TOTPDevice

        password = request.data.get("password")
        if not password:
            return Response({"error": "password is required to disable 2FA"}, status=400)

        if not request.user.check_password(password):
            return Response({"error": "Incorrect password"}, status=400)

        TOTPDevice.objects.filter(user=request.user).delete()
        return Response({"message": "2FA disabled successfully."})


# -- Google OAuth Token Exchange ----------------------------------------------
@extend_schema(
    tags=['Auth'],
    request=GoogleAuthCallbackSerializer,
    responses=OpenApiResponse(response=OpenApiTypes.OBJECT)
)
class GoogleAuthCallbackView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        from rest_framework_simplejwt.tokens import RefreshToken
        from allauth.socialaccount.models import SocialAccount

        uid = request.data.get("uid")
        if not uid:
            return Response({"error": "uid is required"}, status=400)

        try:
            social_account = SocialAccount.objects.get(uid=uid, provider="google")
            user = social_account.user
            refresh = RefreshToken.for_user(user)
            return Response({
                "access":   str(refresh.access_token),
                "refresh":  str(refresh),
                "username": user.username,
                "email":    user.email,
                "role":     user.role,
            })
        except SocialAccount.DoesNotExist:
            return Response({"error": "Google account not found"}, status=404)