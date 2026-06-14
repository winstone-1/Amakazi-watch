from reports.utils.sms import send_case_reference_sms


def send_panic_alert(user, location=None):
    """
    Send SMS to all emergency contacts registered by the user.
    """
    from .models import EmergencyContact
    contacts = EmergencyContact.objects.filter(user=user, is_active=True)

    if not contacts.exists():
        return {"success": False, "error": "No emergency contacts registered"}

    location_text = f" Location: {location}" if location else ""
    message = (
        f"URGENT — AmakaziWatch Panic Alert. "
        f"{user.username} may be in danger and needs immediate help.{location_text} "
        f"Please check on them immediately or call Police: 999 / GBV Hotline: 1195"
    )

    results = []
    for contact in contacts:
        result = send_case_reference_sms(contact.phone, message)
        results.append({
            "contact": contact.name,
            "phone": contact.phone,
            "sent": result["success"]
        })

    return {"success": True, "alerts_sent": results}
