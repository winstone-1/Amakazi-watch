from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .auth import APIKeyAuthentication


class IntelligenceBaseView(APIView):
    authentication_classes = [APIKeyAuthentication]
    permission_classes     = [permissions.IsAuthenticated]


class CountyRiskScoreView(IntelligenceBaseView):
    def get(self, request):
        from reports.models import IncidentReport
        from django.db.models import Count, Avg

        data = (
            IncidentReport.objects
            .values("county")
            .annotate(
                total=Count("id"),
                avg_urgency=Avg("urgency_score"),
                flagged=Count("id", filter=__import__("django.db.models", fromlist=["Q"]).Q(flagged_for_review=True))
            )
            .order_by("-total")
        )

        results = []
        for row in data:
            total      = row["total"] or 0
            avg_urgency = float(row["avg_urgency"] or 0)
            flagged    = row["flagged"] or 0
            risk_score = round((avg_urgency * 0.5) + (flagged / max(total, 1) * 10 * 0.5), 2)
            results.append({
                "county":      row["county"],
                "total_reports": total,
                "avg_urgency": round(avg_urgency, 2),
                "flagged":     flagged,
                "risk_score":  risk_score,
            })

        results.sort(key=lambda x: x["risk_score"], reverse=True)
        return Response({"data": results, "note": "Risk score: 0-10 scale based on urgency and flagged rate"})


class AbuseTypeDistributionView(IntelligenceBaseView):
    def get(self, request):
        from reports.models import IncidentReport
        from django.db.models import Count

        county = request.query_params.get("county")
        qs = IncidentReport.objects
        if county:
            qs = qs.filter(county__icontains=county)

        total = qs.count()
        data  = qs.values("abuse_type").annotate(count=Count("id")).order_by("-count")

        return Response({
            "county": county or "All counties",
            "total":  total,
            "distribution": [
                {
                    "abuse_type":  row["abuse_type"],
                    "count":       row["count"],
                    "percentage":  round(row["count"] / total * 100, 1) if total else 0
                }
                for row in data
            ]
        })


class TrendForecastView(IntelligenceBaseView):
    def get(self, request):
        import pandas as pd
        from reports.models import IncidentReport
        from django.utils import timezone
        from datetime import timedelta

        days = int(request.query_params.get("days", 60))
        since = timezone.now() - timedelta(days=days)

        reports = IncidentReport.objects.filter(
            created_at__gte=since
        ).values("created_at", "county")

        if not reports:
            return Response({"error": "Not enough data"}, status=404)

        df = pd.DataFrame(list(reports))
        df["date"] = pd.to_datetime(df["created_at"]).dt.date
        daily = df.groupby("date").size().reset_index(name="count")
        daily["7_day_avg"] = daily["count"].rolling(7, min_periods=1).mean().round(2)
        daily["trend"] = daily["7_day_avg"].diff().apply(lambda x: "up" if x > 0 else ("down" if x < 0 else "stable"))

        return Response({
            "days_analysed": days,
            "forecast":      daily.tail(14).to_dict(orient="records"),
            "summary": {
                "total":      int(daily["count"].sum()),
                "daily_avg":  round(float(daily["count"].mean()), 2),
                "peak_day":   str(daily.loc[daily["count"].idxmax(), "date"]),
                "current_trend": daily.iloc[-1]["trend"] if len(daily) > 1 else "stable"
            }
        })


class APIKeyCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        from .models import APIKey

        name = request.data.get("name")
        tier = request.data.get("tier", APIKey.Tier.FREE)

        if not name:
            return Response({"error": "name is required"}, status=400)

        valid_tiers = [t[0] for t in APIKey.Tier.choices]
        if tier not in valid_tiers:
            return Response({"error": f"Invalid tier. Choose from: {valid_tiers}"}, status=400)

        limits = {"free": 100, "researcher": 1000, "enterprise": 999999}

        api_key = APIKey.objects.create(
            user=request.user,
            name=name,
            tier=tier,
            call_limit=limits.get(tier, 100),
        )

        return Response({
            "message":    "API key created",
            "key":        api_key.key,
            "tier":       api_key.tier,
            "call_limit": api_key.call_limit,
            "warning":    "Save this key — it will not be shown again"
        }, status=201)


class APIKeyListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from .models import APIKey
        keys = APIKey.objects.filter(user=request.user)
        return Response([{
            "id":         k.id,
            "name":       k.name,
            "tier":       k.tier,
            "is_active":  k.is_active,
            "calls_made": k.calls_made,
            "call_limit": k.call_limit,
            "created_at": k.created_at,
        } for k in keys])
