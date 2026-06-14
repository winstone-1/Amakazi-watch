import africastalking
from django.conf import settings


def initialize_at():
    africastalking.initialize(
        username=settings.AT_USERNAME,
        api_key=settings.AT_API_KEY,
    )


def send_whatsapp(phone, message):
    """Send a WhatsApp message via Africa's Talking."""
    initialize_at()
    try:
        response = africastalking.SMS.send(
            message=message,
            recipients=[phone],
            sender_id=settings.AT_SENDER_ID,
            enqueue=False,
        )
        return {"success": True, "response": response}
    except Exception as e:
        return {"success": False, "error": str(e)}
