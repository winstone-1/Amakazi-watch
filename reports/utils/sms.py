import africastalking
from django.conf import settings


def initialize_at():
    africastalking.initialize(
        username=settings.AT_USERNAME,
        api_key=settings.AT_API_KEY,
    )
    return africastalking.SMS


def send_case_reference_sms(phone_number, ref_code):
    """
    Send SMS to reporter with their case reference number.
    Phone number must be in international format: +254XXXXXXXXX
    """
    try:
        sms = initialize_at()
        message = (
            f"AmakaziWatch: Your report has been received. "
            f"Your case reference is {ref_code}. "
            f"You are not alone. GBV Hotline: 1195"
        )
        response = sms.send(
            message=message,
            recipients=[phone_number],
            sender_id=settings.AT_SENDER_ID,
        )
        return {'success': True, 'response': response}
    except Exception as e:
        return {'success': False, 'error': str(e)}
