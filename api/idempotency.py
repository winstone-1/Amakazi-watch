from django.db import models
from django.utils import timezone
from functools import wraps
from rest_framework.response import Response

class IdempotencyRecord(models.Model):
    idempotency_key = models.CharField(max_length=255, unique=True)
    response_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

def idempotent(timeout_hours=24):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(view_instance, request, *args, **kwargs):
            key = request.headers.get('Idempotency-Key')
            
            if not key:
                return view_func(view_instance, request, *args, **kwargs)
            
            # Check if already processed
            try:
                existing = IdempotencyRecord.objects.get(idempotency_key=key)
                if existing.expires_at > timezone.now():
                    return Response(existing.response_data, status=200)
                existing.delete()
            except IdempotencyRecord.DoesNotExist:
                pass
            
            # Process and store response
            response = view_func(view_instance, request, *args, **kwargs)
            
            if response.status_code in [200, 201]:
                IdempotencyRecord.objects.create(
                    idempotency_key=key,
                    response_data=response.data,
                    expires_at=timezone.now() + timedelta(hours=timeout_hours)
                )
            
            return response
        return wrapper
    return decorator
