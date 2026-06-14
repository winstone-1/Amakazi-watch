from .models import Notification, AuditLog


def notify(user, type, title, message):
    """Create an in-app notification for a user."""
    return Notification.objects.create(
        user=user,
        type=type,
        title=title,
        message=message,
    )


def notify_org_staff(org, type, title, message):
    """Notify all staff of an organisation."""
    from users.models import User
    staff = User.objects.filter(role="org_staff")
    for user in staff:
        notify(user, type, title, message)


def audit(user, action, model_name="", object_id="", details=None, request=None):
    """Log an admin or system action."""
    ip = None
    if request:
        x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        ip = x_forwarded.split(",")[0] if x_forwarded else request.META.get("REMOTE_ADDR")

    AuditLog.objects.create(
        user=user,
        action=action,
        model_name=model_name,
        object_id=str(object_id),
        details=details or {},
        ip_address=ip,
    )


def check_report_spike(county):
    """
    Check if reports in a county have spiked in the last 24hrs.
    If count > 5 in 24hrs, notify all org staff in that county.
    """
    from reports.models import IncidentReport
    from django.utils import timezone
    from datetime import timedelta
    from users.models import User

    since = timezone.now() - timedelta(hours=24)
    count = IncidentReport.objects.filter(
        county__icontains=county,
        created_at__gte=since
    ).count()

    if count >= 5:
        staff = User.objects.filter(role__in=["org_staff", "county_official"])
        for user in staff:
            notify(
                user=user,
                type="report_spike",
                title=f"Report spike in {county}",
                message=f"{count} reports filed in {county} in the last 24 hours. Immediate attention may be needed."
            )
        return {"spike": True, "count": count, "county": county}

    return {"spike": False, "count": count, "county": county}
