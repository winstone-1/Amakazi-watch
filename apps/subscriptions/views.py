from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import Subscription, SubscriptionPayment, Plan
from organisations.models import Organisation


PLAN_PRICES = {
    Plan.FREE:      0,
    Plan.NGO_BASIC: 5000,
    Plan.NGO_PRO:   10000,
    Plan.COUNTY:    15000,
}

PLAN_FEATURES = {
    Plan.FREE:      ["Directory listing", "Basic organisation profile"],
    Plan.NGO_BASIC: ["Everything in Free", "County heatmap access", "Coverage area filter"],
    Plan.NGO_PRO:   ["Everything in NGO Basic", "CSV analytics exports", "Trend reports", "Impact dashboard"],
    Plan.COUNTY:    ["Everything in NGO Pro", "County-official heatmap", "Sub-county breakdown", "Priority support"],
}


class PlansView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        plans = []
        for plan_key, price in PLAN_PRICES.items():
            plans.append({
                "plan":     plan_key,
                "name":     Plan(plan_key).label,
                "price_kes": price,
                "features": PLAN_FEATURES[plan_key],
            })
        return Response(plans)


class SubscriptionStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, org_id):
        org = get_object_or_404(Organisation, pk=org_id, verified=True)
        sub, created = Subscription.objects.get_or_create(
            organisation=org,
            defaults={"plan": Plan.FREE}
        )
        return Response({
            "organisation": org.name,
            "plan":         sub.plan,
            "is_active":    sub.is_valid(),
            "expires_at":   sub.expires_at,
            "auto_renew":   sub.auto_renew,
            "features":     PLAN_FEATURES.get(sub.plan, []),
        })


class SubscriptionUpgradeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, org_id):
        from organisations.utils.paystack import initialize_donation

        org = get_object_or_404(Organisation, pk=org_id, verified=True)
        plan = request.data.get("plan")
        email = request.data.get("email")

        if plan not in PLAN_PRICES:
            return Response({"error": f"Invalid plan. Choose from: {list(PLAN_PRICES.keys())}"}, status=400)

        if not email:
            return Response({"error": "email is required"}, status=400)

        amount = PLAN_PRICES[plan]
        if amount == 0:
            sub, _ = Subscription.objects.get_or_create(organisation=org)
            sub.plan = plan
            sub.is_active = True
            sub.save()
            return Response({"message": "Downgraded to free plan"})

        callback_url = request.data.get(
            "callback_url",
            f"{request.scheme}://{request.get_host()}/api/subscriptions/{org_id}/verify/"
        )

        result = initialize_donation(email, amount, org_id, callback_url)
        if result["success"]:
            sub, _ = Subscription.objects.get_or_create(organisation=org)
            payment = SubscriptionPayment.objects.create(
                subscription=sub,
                amount=amount,
                paystack_ref=result["reference"],
                status="pending",
            )
            return Response({
                "payment_url": result["payment_url"],
                "reference":   result["reference"],
                "plan":        plan,
                "amount_kes":  amount,
            })
        return Response({"error": result["error"]}, status=400)


class SubscriptionVerifyView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, org_id):
        from organisations.utils.paystack import verify_payment
        from django.utils import timezone
        from datetime import timedelta

        reference = request.query_params.get("reference")
        if not reference:
            return Response({"error": "reference is required"}, status=400)

        result = verify_payment(reference)
        if result["success"]:
            try:
                payment = SubscriptionPayment.objects.get(paystack_ref=reference)
                payment.status = "completed"
                payment.paid_at = timezone.now()
                payment.save()

                sub = payment.subscription
                plan = request.query_params.get("plan", sub.plan)
                sub.plan      = plan
                sub.is_active = True
                sub.started_at = timezone.now()
                sub.expires_at = timezone.now() + timedelta(days=30)
                sub.paystack_ref = reference
                sub.save()

                return Response({
                    "message":    "Subscription activated successfully",
                    "plan":       sub.plan,
                    "expires_at": sub.expires_at,
                })
            except SubscriptionPayment.DoesNotExist:
                return Response({"error": "Payment record not found"}, status=404)
        return Response({"error": result["error"]}, status=400)
