from rest_framework_jwt.settings import api_settings
from django.conf import settings

def custom_payload_handler(user) -> dict:
    """Appending custom claims to JWT token"""
    # Default payload using the original DRF handler
    payload = api_settings.JWT_PAYLOAD_HANDLER(user)

    # Appending custom claim to the token
    payload["apiVersion"] = settings.API_VERSION

    return payload
