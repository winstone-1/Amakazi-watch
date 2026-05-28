import pandas as pd
from io import StringIO
from reports.models import IncidentReport
from django.utils import timezone
from datetime import timedelta


def generate_county_summary(days=30):
    since = timezone.now() - timedelta(days=days)
    reports = IncidentReport.objects.filter(created_at__gte=since).values(
        "county", "abuse_type", "urgency_score", "flagged_for_review", "created_at"
    )
    if not reports.exists():
        return None, "No reports found for this period"

    df = pd.DataFrame(list(reports))
    df["created_at"] = pd.to_datetime(df["created_at"]).dt.strftime("%Y-%m-%d")
    summary = (
        df.groupby(["county", "abuse_type"])
        .agg(
            total_reports=("county", "count"),
            flagged=("flagged_for_review", "sum"),
            avg_urgency=("urgency_score", "mean"),
        )
        .reset_index()
    )
    summary["avg_urgency"] = summary["avg_urgency"].round(2)
    summary = summary.sort_values("total_reports", ascending=False)
    csv_buffer = StringIO()
    summary.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue(), None


def generate_trend_report(days=30):
    since = timezone.now() - timedelta(days=days)
    reports = IncidentReport.objects.filter(created_at__gte=since).values(
        "county", "abuse_type", "urgency_score", "created_at"
    )
    if not reports.exists():
        return None, "No reports found for this period"

    df = pd.DataFrame(list(reports))
    df["date"] = pd.to_datetime(df["created_at"]).dt.date
    daily = (
        df.groupby("date")
        .agg(total_reports=("date", "count"))
        .reset_index()
    )
    daily["7_day_avg"] = daily["total_reports"].rolling(7, min_periods=1).mean().round(2)
    csv_buffer = StringIO()
    daily.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue(), None
