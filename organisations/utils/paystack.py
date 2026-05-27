import requests
from django.conf import settings


PAYSTACK_BASE_URL = 'https://api.paystack.co'


def initialize_donation(email, amount_kes, organisation_id, callback_url):
    """
    Initialize a Paystack payment.
    Amount must be in kobo/cents — Paystack uses smallest currency unit.
    For KES: multiply by 100.
    """
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json',
    }
    payload = {
        'email': email,
        'amount': int(amount_kes * 100),
        'currency': 'KES',
        'callback_url': callback_url,
        'metadata': {
            'organisation_id': organisation_id,
        }
    }
    try:
        response = requests.post(
            f'{PAYSTACK_BASE_URL}/transaction/initialize',
            json=payload,
            headers=headers,
        )
        data = response.json()
        if data['status']:
            return {
                'success': True,
                'payment_url': data['data']['authorization_url'],
                'reference': data['data']['reference'],
            }
        return {'success': False, 'error': data['message']}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def verify_payment(reference):
    """
    Verify a Paystack payment by reference.
    Call this from the callback/webhook endpoint.
    """
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
    }
    try:
        response = requests.get(
            f'{PAYSTACK_BASE_URL}/transaction/verify/{reference}',
            headers=headers,
        )
        data = response.json()
        if data['status'] and data['data']['status'] == 'success':
            return {
                'success': True,
                'amount': data['data']['amount'] / 100,
                'reference': reference,
            }
        return {'success': False, 'error': 'Payment not successful'}
    except Exception as e:
        return {'success': False, 'error': str(e)}
