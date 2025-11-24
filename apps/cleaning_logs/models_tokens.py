"""
Optional: Temporary Token Model for audit/history tracking

This model stores temporary token generation events for auditing purposes.
The actual validation still uses HMAC (no database lookup needed).
"""
from django.db import models
from django.utils import timezone
from datetime import timedelta
from apps.equipment.models import Equipment
from apps.accounts.models import User


class TemporaryTokenLog(models.Model):
    """
    Audit log for temporary token generation

    Note: This is for TRACKING purposes only.
    Token validation is still done via HMAC (apps/cleaning_logs/tokens.py)
    """
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='temporary_tokens'
    )
    token = models.CharField(
        max_length=128,
        help_text="Format: equipment_id:expiry_timestamp:signature"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='generated_tokens'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    expiry_minutes = models.IntegerField(default=5)

    # Usage tracking
    was_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    times_accessed = models.IntegerField(default=0)

    # IP tracking (optional)
    generated_from_ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Temporary Token Log'
        verbose_name_plural = 'Temporary Token Logs'
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['equipment', '-created_at']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self):
        return f"Token for {self.equipment.name} (expires {self.expires_at})"

    def is_expired(self):
        """Check if token is expired"""
        return timezone.now() > self.expires_at

    def time_remaining(self):
        """Get time remaining until expiration"""
        if self.is_expired():
            return timedelta(0)
        return self.expires_at - timezone.now()

    def mark_as_used(self):
        """Mark token as used"""
        if not self.was_used:
            self.was_used = True
            self.used_at = timezone.now()
            self.save(update_fields=['was_used', 'used_at'])

    def increment_access(self):
        """Increment access counter"""
        self.times_accessed += 1
        self.save(update_fields=['times_accessed'])
