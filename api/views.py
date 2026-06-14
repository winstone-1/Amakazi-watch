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

        # Audit log
        from notifications.utils import audit, check_report_spike
        audit(
            user=None,
            action="anonymous_report_submitted",
            model_name="IncidentReport",
            object_id=ref,
            details={"county": report.county, "abuse_type": report.abuse_type},
            request=self.request,
        )
        check_report_spike(report.county)

        # Deduplication check
        if report.description:
            from api.utils.Groq import check_duplicate
            dup = check_duplicate(report.description, report.county, report.abuse_type)
            if dup.get("is_duplicate") and dup.get("confidence", 0) > 80:
                report.ai_classification = f"possible_duplicate:{dup.get('confidence')}%"
                report.save()

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
        from io import BytesIO
        import base64

        # Delete any unconfirmed device first
        TOTPDevice.objects.filter(user=request.user, confirmed=False).delete()

        device, created = TOTPDevice.objects.get_or_create(
            user=request.user,
            name="AmakaziWatch 2FA",
            defaults={"confirmed": False}
        )

        if device.confirmed:
            return Response({
                "message": "2FA is already enabled.",
                "enabled": True
            })

        # Generate TOTP URI for authenticator apps
        totp_uri = device.config_url

        # Generate QR code
        qr = qrcode.make(totp_uri)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()

        # Generate manual entry code (base32 secret)
        import base64 as b64
        secret_bytes = bytes.fromhex(device.key)
        totp_secret = b64.b32encode(secret_bytes).decode().rstrip("=")

        return Response({
            "enabled":    False,
            "totp_uri":   totp_uri,
            "totp_secret": totp_secret,
            "qr_code":    f"data:image/png;base64,{qr_base64}",
            "instructions": [
                "1. Open Google Authenticator or Authy on your phone",
                "2. Tap + and choose Scan QR code",
                "3. Scan the QR code above",
                "4. Enter the 6-digit code shown in the app to verify",
                "Alternatively enter the secret key manually in your authenticator app"
            ]
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

# -- Panic Button -------------------------------------------------------------
class EmergencyContactListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from users.models import EmergencyContact
        from .serializers import EmergencyContactSerializer
        contacts = EmergencyContact.objects.filter(user=request.user)
        return Response(EmergencyContactSerializer(contacts, many=True).data)

    def post(self, request):
        from users.models import EmergencyContact
        from .serializers import EmergencyContactSerializer
        serializer = EmergencyContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PanicButtonView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        from users.panic import send_panic_alert
        location = request.data.get("location", None)
        result = send_panic_alert(request.user, location)
        if result["success"]:
            return Response({
                "message": "Panic alert sent to all emergency contacts.",
                "alerts":  result["alerts_sent"]
            })
        return Response({"error": result["error"]}, status=400)


class EmergencyContactDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        from users.models import EmergencyContact
        try:
            contact = EmergencyContact.objects.get(pk=pk, user=request.user)
            contact.delete()
            return Response({"message": "Contact removed"})
        except EmergencyContact.DoesNotExist:
            return Response({"error": "Contact not found"}, status=404)


# -- Case Tracking ------------------------------------------------------------
class CaseTrackingView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, ref_code):
        from reports.models import IncidentReport, CaseUpdate
        try:
            report = IncidentReport.objects.get(sms_ref_code=ref_code)
        except IncidentReport.DoesNotExist:
            return Response({"error": "Case reference not found"}, status=404)

        updates = CaseUpdate.objects.filter(ref_code=ref_code)
        return Response({
            "ref_code":    ref_code,
            "abuse_type":  report.abuse_type,
            "county":      report.county,
            "submitted_at": report.created_at,
            "urgency_score": report.urgency_score,
            "updates": [
                {
                    "type": u.update_type,
                    "notes": u.notes,
                    "date": u.created_at
                } for u in updates
            ]
        })

    def post(self, request, ref_code):
        from reports.models import IncidentReport, CaseUpdate
        try:
            IncidentReport.objects.get(sms_ref_code=ref_code)
        except IncidentReport.DoesNotExist:
            return Response({"error": "Case reference not found"}, status=404)

        update_type = request.data.get("update_type")
        notes = request.data.get("notes", "")

        if not update_type:
            return Response({"error": "update_type is required"}, status=400)

        valid_types = [c[0] for c in CaseUpdate.UpdateType.choices]
        if update_type not in valid_types:
            return Response({"error": f"Invalid update_type. Choose from: {valid_types}"}, status=400)

        update = CaseUpdate.objects.create(
            ref_code=ref_code,
            update_type=update_type,
            notes=notes,
        )
        return Response({
            "message":     "Case update recorded",
            "ref_code":    ref_code,
            "update_type": update.update_type,
            "created_at":  update.created_at,
        }, status=201)


# -- Referral Network ---------------------------------------------------------
class ReferralCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        from organisations.models import Referral
        from organisations.models import Organisation

        from_org_id = request.data.get("from_org")
        to_org_id   = request.data.get("to_org")
        ref_code    = request.data.get("ref_code")
        reason      = request.data.get("reason")

        if not all([from_org_id, to_org_id, ref_code, reason]):
            return Response({"error": "from_org, to_org, ref_code and reason are required"}, status=400)

        if from_org_id == to_org_id:
            return Response({"error": "Cannot refer to the same organisation"}, status=400)

        try:
            from_org = Organisation.objects.get(pk=from_org_id, verified=True)
            to_org   = Organisation.objects.get(pk=to_org_id, verified=True)
        except Organisation.DoesNotExist:
            return Response({"error": "Organisation not found"}, status=404)

        referral = Referral.objects.create(
            from_org=from_org,
            to_org=to_org,
            ref_code=ref_code,
            reason=reason,
        )
        return Response({
            "message":    f"Case {ref_code} referred to {to_org.name}",
            "referral_id": referral.id,
            "status":     referral.status,
        }, status=201)


class ReferralUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        from organisations.models import Referral

        try:
            referral = Referral.objects.get(pk=pk)
        except Referral.DoesNotExist:
            return Response({"error": "Referral not found"}, status=404)

        status = request.data.get("status")
        notes  = request.data.get("notes", "")

        valid = [c[0] for c in Referral.Status.choices]
        if status not in valid:
            return Response({"error": f"Invalid status. Choose from: {valid}"}, status=400)

        referral.status = status
        referral.notes  = notes
        referral.save()

        return Response({
            "message": f"Referral {pk} updated to {status}",
            "referral_id": referral.id,
            "status":  referral.status,
            "notes":   referral.notes,
        })


class ReferralListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from organisations.models import Referral

        org_id = request.query_params.get("org_id")
        direction = request.query_params.get("direction", "both")

        if not org_id:
            return Response({"error": "org_id is required"}, status=400)

        if direction == "sent":
            referrals = Referral.objects.filter(from_org_id=org_id)
        elif direction == "received":
            referrals = Referral.objects.filter(to_org_id=org_id)
        else:
            from django.db.models import Q
            referrals = Referral.objects.filter(
                Q(from_org_id=org_id) | Q(to_org_id=org_id)
            )

        return Response([{
            "id":        r.id,
            "from_org":  r.from_org.name,
            "to_org":    r.to_org.name,
            "ref_code":  r.ref_code,
            "reason":    r.reason,
            "status":    r.status,
            "notes":     r.notes,
            "created_at": r.created_at,
        } for r in referrals])


# -- Content Rating -----------------------------------------------------------
class ContentRatingView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        from content.models import EducationContent, ContentRating
        from django.db.models import Avg

        rating = request.data.get("rating")
        if not rating or int(rating) not in range(1, 6):
            return Response({"error": "rating must be 1-5"}, status=400)

        try:
            content = EducationContent.objects.get(pk=pk, approved=True)
        except EducationContent.DoesNotExist:
            return Response({"error": "Content not found"}, status=404)

        ContentRating.objects.create(content=content, rating=int(rating))
        avg = ContentRating.objects.filter(content=content).aggregate(avg=Avg("rating"))["avg"]

        return Response({
            "message":    "Rating submitted",
            "avg_rating": round(avg, 2),
            "total_ratings": ContentRating.objects.filter(content=content).count()
        })


# -- Organisation Reviews -----------------------------------------------------
class OrganisationReviewView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        from organisations.models import Organisation, OrganisationReview
        from django.db.models import Avg

        try:
            org = Organisation.objects.get(pk=pk, verified=True)
        except Organisation.DoesNotExist:
            return Response({"error": "Organisation not found"}, status=404)

        reviews = OrganisationReview.objects.filter(organisation=org)
        avg = reviews.aggregate(avg=Avg("rating"))["avg"]

        return Response({
            "organisation": org.name,
            "avg_rating":   round(avg, 2) if avg else None,
            "total_reviews": reviews.count(),
            "reviews": [{
                "rating":     r.rating,
                "review":     r.review,
                "helpful":    r.helpful,
                "created_at": r.created_at,
            } for r in reviews[:10]]
        })

    def post(self, request, pk):
        from organisations.models import Organisation, OrganisationReview

        rating = request.data.get("rating")
        review = request.data.get("review", "")

        if not rating or int(rating) not in range(1, 6):
            return Response({"error": "rating must be 1-5"}, status=400)

        try:
            org = Organisation.objects.get(pk=pk, verified=True)
        except Organisation.DoesNotExist:
            return Response({"error": "Organisation not found"}, status=404)

        OrganisationReview.objects.create(
            organisation=org,
            rating=int(rating),
            review=review,
        )
        return Response({"message": "Review submitted anonymously"}, status=201)


# -- Voice Reporting ----------------------------------------------------------
class VoiceReportCallbackView(APIView):
    """
    Africa's Talking Voice callback endpoint.
    AT hits this when a call comes in or recording is ready.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        import hashlib
        from reports.models import VoiceReport

        session_id    = request.data.get("sessionId", "")
        recording_url = request.data.get("recordingUrl", "")
        caller        = request.data.get("callerNumber", "")
        is_active     = request.data.get("isActive", "0")

        if not session_id:
            return Response({"error": "sessionId required"}, status=400)

        phone_hash = hashlib.sha256(caller.encode()).hexdigest() if caller else ""

        report, created = VoiceReport.objects.get_or_create(
            session_id=session_id,
            defaults={"phone_hash": phone_hash}
        )

        if recording_url:
            report.recording_url = recording_url
            report.status = "transcribed"

            # Transcribe with Groq
            try:
                from api.utils.Groq import classify_report
                prompt = f"A caller reported a GBV incident. Recording URL: {recording_url}. Based on context, classify this as a GBV report."
                result = classify_report(prompt, "unknown")
                if result["success"]:
                    data = result["data"]
                    report.abuse_type    = data.get("confirmed_abuse_type", "")
                    report.urgency_score = data.get("urgency_score")
                    report.status        = "classified"
            except Exception:
                pass

            report.save()

        # Return TwiML-style response for AT
        if is_active == "1":
            xml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Welcome to AmakaziWatch. You have reached the GBV anonymous reporting line. Please speak after the tone to describe what happened. Your call is completely anonymous.</Say>
    <Record finishOnKey="#" maxLength="120" trimSilence="true" playBeep="true"/>
</Response>"""
            from django.http import HttpResponse
            return HttpResponse(xml, content_type="application/xml")

        return Response({"message": "Voice report received", "session_id": session_id})


class VoiceReportListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from reports.models import VoiceReport
        if not request.user.is_platform_admin():
            return Response({"error": "Admin only"}, status=403)
        reports = VoiceReport.objects.all()[:20]
        return Response([{
            "session_id":   r.session_id,
            "status":       r.status,
            "abuse_type":   r.abuse_type,
            "county":       r.county,
            "urgency_score": r.urgency_score,
            "transcript":   r.transcript,
            "created_at":   r.created_at,
        } for r in reports])


# -- WhatsApp Bot -------------------------------------------------------------
class WhatsAppWebhookView(APIView):
    """
    Africa's Talking WhatsApp incoming message webhook.
    Handles commands: REPORT, HELP, FIND, STATUS <ref_code>
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        from reports.utils.whatsapp import send_whatsapp
        from reports.utils.sms import send_case_reference_sms
        import random
        import string

        phone   = request.data.get("from", "")
        message = request.data.get("text", "").strip().upper()

        if not phone or not message:
            return Response({"error": "from and text required"}, status=400)

        # HELP command
        if message in ["HELP", "HI", "HELLO", "START"]:
            reply = (
                "Welcome to AmakaziWatch.\n\n"
                "Commands:\n"
                "REPORT — File an anonymous report\n"
                "FIND <county> — Find help near you\n"
                "STATUS <ref_code> — Track your case\n"
                "HOTLINE — Emergency numbers\n\n"
                "All conversations are anonymous."
            )
            send_whatsapp(phone, reply)
            return Response({"message": "Help sent"})

        # HOTLINE command
        if message == "HOTLINE":
            reply = (
                "Kenya GBV Emergency Numbers:\n"
                "GBV Hotline: 1195\n"
                "Childline: 116\n"
                "Police: 999\n"
                "FIDA Kenya: 0202721784\n"
                "GVRC Nairobi: 0800720500"
            )
            send_whatsapp(phone, reply)
            return Response({"message": "Hotline sent"})

        # REPORT command
        if message.startswith("REPORT"):
            ref = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
            from reports.models import IncidentReport
            import hashlib
            IncidentReport.objects.create(
                abuse_type="physical",
                relationship="self",
                county="Unknown",
                description=f"WhatsApp report from {hashlib.sha256(phone.encode()).hexdigest()[:8]}",
                sms_ref_code=ref,
            )
            reply = (
                f"Report received. Your case reference: {ref}\n"
                "Reply with more details:\n"
                "COUNTY <your county>\n"
                "TYPE physical/emotional/financial/sexual/digital\n"
                "DETAIL <what happened>\n\n"
                "You are not alone. GBV Hotline: 1195"
            )
            send_whatsapp(phone, reply)
            return Response({"message": "Report created", "ref": ref})

        # FIND command
        if message.startswith("FIND"):
            parts = message.split(" ", 1)
            county = parts[1] if len(parts) > 1 else ""
            from organisations.models import Organisation
            orgs = Organisation.objects.filter(
                verified=True,
                county__icontains=county
            )[:3]
            if orgs:
                lines = [f"Help near {county}:"]
                for org in orgs:
                    lines.append(f"\n{org.name}\n{org.phone or org.email}")
                reply = "\n".join(lines)
            else:
                reply = f"No verified organisations found in {county}. Try a nearby county or call 1195."
            send_whatsapp(phone, reply)
            return Response({"message": "Orgs sent"})

        # STATUS command
        if message.startswith("STATUS"):
            parts = message.split(" ", 1)
            ref = parts[1].strip() if len(parts) > 1 else ""
            from reports.models import IncidentReport, CaseUpdate
            try:
                report = IncidentReport.objects.get(sms_ref_code=ref)
                updates = CaseUpdate.objects.filter(ref_code=ref)
                lines = [f"Case {ref}:", f"Type: {report.abuse_type}", f"County: {report.county}"]
                if updates.exists():
                    lines.append(f"Updates: {updates.count()}")
                    lines.append(f"Latest: {updates.first().update_type}")
                reply = "\n".join(lines)
            except IncidentReport.DoesNotExist:
                reply = f"Case {ref} not found. Check your reference code."
            send_whatsapp(phone, reply)
            return Response({"message": "Status sent"})

        # Default
        send_whatsapp(phone, "Command not recognised. Reply HELP for available commands.")
        return Response({"message": "Default reply sent"})


# -- USSD ---------------------------------------------------------------------
class USSDView(APIView):
    """
    Africa's Talking USSD callback.
    Dial *384*SHORTCODE# to access AmakaziWatch via USSD.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        session_id   = request.data.get("sessionId", "")
        phone        = request.data.get("phoneNumber", "")
        network_code = request.data.get("networkCode", "")
        text         = request.data.get("text", "")

        response = ""
        parts = text.split("*")
        level = len(parts) if text else 0

        # Level 0 — Main menu
        if text == "":
            response = (
                "CON Welcome to AmakaziWatch
"
                "1. Report incident
"
                "2. Find help near me
"
                "3. Track my case
"
                "4. Emergency numbers"
            )

        # Level 1
        elif text == "1":
            response = (
                "CON Select abuse type:
"
                "1. Physical
"
                "2. Emotional
"
                "3. Financial
"
                "4. Sexual
"
                "5. Digital"
            )

        elif text == "2":
            response = (
                "CON Select your county:
"
                "1. Nairobi
"
                "2. Mombasa
"
                "3. Kisumu
"
                "4. Nakuru
"
                "5. Other"
            )

        elif text == "3":
            response = "CON Enter your case reference code:"

        elif text == "4":
            response = (
                "END Emergency Numbers:
"
                "GBV Hotline: 1195
"
                "Childline: 116
"
                "Police: 999
"
                "FIDA Kenya: 0202721784"
            )

        # Level 2 — Report abuse type selected
        elif parts[0] == "1" and len(parts) == 2:
            abuse_map = {"1": "physical", "2": "emotional", "3": "financial", "4": "sexual", "5": "digital"}
            abuse = abuse_map.get(parts[1], "other")
            response = (
                "CON Select your county:
"
                "1. Nairobi
"
                "2. Mombasa
"
                "3. Kisumu
"
                "4. Nakuru
"
                "5. Other"
            )

        # Level 3 — County selected, create report
        elif parts[0] == "1" and len(parts) == 3:
            import random, string, hashlib
            from reports.models import IncidentReport

            abuse_map  = {"1": "physical", "2": "emotional", "3": "financial", "4": "sexual", "5": "digital"}
            county_map = {"1": "Nairobi", "2": "Mombasa", "3": "Kisumu", "4": "Nakuru", "5": "Other"}

            abuse_type = abuse_map.get(parts[1], "other")
            county     = county_map.get(parts[2], "Other")
            ref        = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

            IncidentReport.objects.create(
                abuse_type=abuse_type,
                relationship="self",
                county=county,
                description=f"USSD report via {hashlib.sha256(phone.encode()).hexdigest()[:8]}",
                sms_ref_code=ref,
            )

            response = (
                f"END Report received.\n"
                f"Reference: {ref}\n"
                f"Save this code to track your case.\n"
                f"GBV Hotline: 1195"
            )

        # Level 2 — Find help county selected
        elif parts[0] == "2" and len(parts) == 2:
            from organisations.models import Organisation
            county_map = {"1": "Nairobi", "2": "Mombasa", "3": "Kisumu", "4": "Nakuru", "5": ""}
            county = county_map.get(parts[1], "")
            orgs   = Organisation.objects.filter(verified=True, county__icontains=county)[:2]

            if orgs:
                lines = ["END Help near you:"]
                for org in orgs:
                    lines.append(f"{org.name}: {org.phone or 'N/A'}")
                response = "\n".join(lines)
            else:
                response = "END No organisations found. Call 1195 for help."

        # Level 2 — Case tracking ref entered
        elif parts[0] == "3" and len(parts) == 2:
            from reports.models import IncidentReport, CaseUpdate
            ref = parts[1].strip()
            try:
                report  = IncidentReport.objects.get(sms_ref_code=ref)
                updates = CaseUpdate.objects.filter(ref_code=ref).count()
                response = (
                    f"END Case {ref}:\n"
                    f"Type: {report.abuse_type}\n"
                    f"County: {report.county}\n"
                    f"Updates: {updates}"
                )
            except IncidentReport.DoesNotExist:
                response = f"END Case {ref} not found. Check your reference."

        else:
            response = "END Invalid option. Dial again."

        from django.http import HttpResponse
        return HttpResponse(response, content_type="text/plain")


# -- Bulk SMS Blast -----------------------------------------------------------
class BulkSMSView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if not request.user.is_platform_admin():
            return Response({"error": "Admin only"}, status=403)

        message = request.data.get("message")
        county  = request.data.get("county")
        phones  = request.data.get("phones", [])

        if not message:
            return Response({"error": "message is required"}, status=400)

        if not phones:
            return Response({"error": "phones list is required"}, status=400)

        if len(message) > 160:
            return Response({"error": "Message must be under 160 characters"}, status=400)

        from reports.utils.sms import initialize_at
        sms = initialize_at()

        try:
            response = sms.send(
                message=f"AmakaziWatch: {message}",
                recipients=phones,
            )
            from notifications.utils import audit
            audit(
                user=request.user,
                action="bulk_sms_sent",
                details={
                    "message":    message,
                    "county":     county,
                    "recipients": len(phones)
                },
                request=request,
            )
            return Response({
                "message":    f"SMS sent to {len(phones)} recipients",
                "county":     county,
                "response":   str(response)
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)
