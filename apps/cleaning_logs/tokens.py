"""
Token expirável para registro de limpeza
Tokens válidos por 5 minutos
"""
import time
import hashlib
import hmac
from django.conf import settings


def generate_expirable_token(equipment_id, expiry_minutes=5):
    """
    Generate a token that expires after specified minutes

    Args:
        equipment_id: ID of the equipment
        expiry_minutes: Minutes until token expires (default: 5)

    Returns:
        str: Token string with format "equipment_id:timestamp:signature"
    """
    # Generate expiry timestamp
    expiry_timestamp = int(time.time()) + (expiry_minutes * 60)

    # Create message to sign
    message = f"{equipment_id}:{expiry_timestamp}"

    # Generate HMAC signature
    secret_key = settings.SECRET_KEY.encode('utf-8')
    signature = hmac.new(
        secret_key,
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()[:16]  # Use first 16 chars

    # Return token
    token = f"{equipment_id}:{expiry_timestamp}:{signature}"
    return token


def validate_expirable_token(token):
    """
    Validate a token and check if it's expired

    Args:
        token: Token string

    Returns:
        int or None: Equipment ID if valid, None if invalid/expired
    """
    try:
        # Parse token
        parts = token.split(':')
        if len(parts) != 3:
            return None

        equipment_id_str, expiry_timestamp_str, provided_signature = parts
        equipment_id = int(equipment_id_str)
        expiry_timestamp = int(expiry_timestamp_str)

        # Check if expired
        current_timestamp = int(time.time())
        if current_timestamp > expiry_timestamp:
            return None  # Token expired

        # Verify signature
        message = f"{equipment_id}:{expiry_timestamp}"
        secret_key = settings.SECRET_KEY.encode('utf-8')
        expected_signature = hmac.new(
            secret_key,
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()[:16]

        if provided_signature != expected_signature:
            return None  # Invalid signature

        return equipment_id

    except (ValueError, AttributeError):
        return None


def get_token_expiry_info(token):
    """
    Get information about token expiry

    Args:
        token: Token string

    Returns:
        dict: Information about token expiry or None if invalid
    """
    try:
        parts = token.split(':')
        if len(parts) != 3:
            return None

        equipment_id = int(parts[0])
        expiry_timestamp = int(parts[1])
        current_timestamp = int(time.time())

        seconds_remaining = expiry_timestamp - current_timestamp
        minutes_remaining = seconds_remaining / 60

        return {
            'equipment_id': equipment_id,
            'expiry_timestamp': expiry_timestamp,
            'current_timestamp': current_timestamp,
            'seconds_remaining': seconds_remaining,
            'minutes_remaining': round(minutes_remaining, 2),
            'is_expired': seconds_remaining <= 0,
            'expires_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expiry_timestamp))
        }
    except (ValueError, AttributeError):
        return None
