import africastalking
from django.conf import settings


def initialize_at():
    africastalking.initialize(
        username=settings.AT_USERNAME,
        api_key=settings.AT_API_KEY,
    )


def make_voice_call(phone, message):
    """Initiate an outbound call to a phone number."""
    initialize_at()
    voice = africastalking.Voice
    try:
        response = voice.call(
            callFrom=settings.AT_CALLER_ID,
            callTo=[phone],
        )
        return {"success": True, "response": response}
    except Exception as e:
        return {"success": False, "error": str(e)}
