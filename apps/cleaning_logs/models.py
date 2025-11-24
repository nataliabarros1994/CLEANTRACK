import os
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from apps.equipment.models import Equipment

User = get_user_model()

def cleaning_photo_path(instance, filename):
    # Organiza uploads por data e equipamento
    ext = filename.split('.')[-1]
    filename = f"cleaning_{instance.equipment.id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    return os.path.join('cleaning_logs', str(instance.equipment.facility.id), filename)

class CleaningLog(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="cleaning_logs")
    cleaned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    cleaned_at = models.DateTimeField("Data/hora da limpeza")
    notes = models.TextField("Observações", blank=True)
    photo = models.ImageField("Foto comprobatória", upload_to=cleaning_photo_path, blank=True, null=True)
    is_compliant = models.BooleanField("Em conformidade", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Validação: não permitir limpeza futura
        if self.cleaned_at and self.cleaned_at > timezone.now():
            raise ValidationError("A data da limpeza não pode ser futura.")

        # Validação: verificar se já existe uma limpeza muito recente (evitar spam)
        if self.pk is None:  # só valida em criação
            recent = CleaningLog.objects.filter(
                equipment=self.equipment,
                cleaned_at__gte=self.cleaned_at - timezone.timedelta(hours=1)
            ).exists()
            if recent:
                raise ValidationError("Já existe um registro de limpeza para este equipamento na última hora.")

    def save(self, *args, **kwargs):
        from datetime import timedelta

        # Auto-set cleaned_at to now if not provided
        if not self.cleaned_at:
            self.cleaned_at = timezone.now()

        # Validate compliance based on cleaning frequency
        if self.equipment:
            last_cleaning = self.equipment.last_cleaning

            if last_cleaning and last_cleaning.pk != self.pk:
                # Calculate expected cleaning time
                expected_time = last_cleaning.cleaned_at + timedelta(
                    hours=self.equipment.cleaning_frequency_hours
                )

                # If cleaning is done after expected time, mark as non-compliant
                if self.cleaned_at > expected_time:
                    self.is_compliant = False
                else:
                    # Cleaning done on time
                    self.is_compliant = True
            else:
                # First cleaning - always compliant
                self.is_compliant = True

        # Run validations
        self.full_clean()
        super().save(*args, **kwargs)

        # Send notification to managers if cleaning was non-compliant
        if not self.is_compliant and self.equipment:
            self._notify_managers_of_non_compliant_cleaning()

    def _notify_managers_of_non_compliant_cleaning(self):
        """Send email notification to managers about non-compliant cleaning"""
        from apps.accounts.models import User
        from apps.notifications.services import send_cleaning_alert

        # Get all managers and admins
        managers = User.objects.filter(
            role__in=['admin', 'manager'],
            is_active=True
        )

        # Send email to each manager
        for manager in managers:
            try:
                send_cleaning_alert(
                    to_email=manager.email,
                    equipment_name=f"{self.equipment.name} ({self.equipment.facility.name}) - LIMPEZA FORA DO PRAZO"
                )
            except Exception as e:
                # Log error but don't fail the save operation
                print(f"Failed to send notification to {manager.email}: {e}")

    def __str__(self):
        return f"Limpeza de {self.equipment.name} em {self.cleaned_at.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        ordering = ["-cleaned_at"]
        verbose_name = "Registro de Limpeza"
        verbose_name_plural = "Registros de Limpeza"


class TemporaryTokenLog(models.Model):
    """
    Audit log for temporary token generation (optional)

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
