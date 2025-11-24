"""
Equipment models for managing medical equipment and cleaning protocols
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import Location, User


class EquipmentType(models.Model):
    """
    Categories of medical equipment with standard cleaning protocols
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    # Regulatory info
    requires_fda_compliance = models.BooleanField(default=False)
    requires_daily_cleaning = models.BooleanField(default=False)

    # Default cleaning frequency (in hours)
    default_cleaning_frequency = models.IntegerField(
        default=24,
        help_text="Default hours between cleanings"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('equipment type')
        verbose_name_plural = _('equipment types')

    def __str__(self):
        return self.name


class CleaningProtocol(models.Model):
    """
    Step-by-step cleaning instructions for equipment types
    """
    name = models.CharField(max_length=255)
    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.CASCADE,
        related_name='protocols'
    )
    version = models.CharField(max_length=50, default='1.0')

    # Protocol details
    description = models.TextField()
    steps = models.JSONField(
        default=list,
        help_text="List of cleaning steps in order"
    )

    # Required supplies
    required_chemicals = models.JSONField(
        default=list,
        help_text="List of required cleaning chemicals"
    )
    required_equipment = models.JSONField(
        default=list,
        help_text="List of required cleaning equipment (cloths, brushes, etc.)"
    )

    # Timing
    estimated_duration = models.IntegerField(
        help_text="Estimated duration in minutes"
    )
    contact_time = models.IntegerField(
        default=0,
        help_text="Required contact time for disinfectant in seconds"
    )

    # Documentation
    manual_document = models.FileField(
        upload_to='protocols/',
        blank=True,
        null=True,
        help_text="PDF or document with full protocol"
    )

    # Status
    is_active = models.BooleanField(default=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('cleaning protocol')
        verbose_name_plural = _('cleaning protocols')
        unique_together = [['equipment_type', 'version']]

    def __str__(self):
        return f"{self.name} v{self.version}"


class Equipment(models.Model):
    """
    Individual piece of medical equipment to be tracked
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired'),
    ]

    # Basic info
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='equipment'
    )
    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.PROTECT,
        related_name='equipment'
    )
    protocol = models.ForeignKey(
        CleaningProtocol,
        on_delete=models.PROTECT,
        related_name='equipment',
        null=True,
        blank=True
    )

    # Identification
    name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255, unique=True)
    asset_tag = models.CharField(max_length=100, blank=True)
    qr_code = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        help_text="QR code for quick scanning"
    )

    # Details
    manufacturer = models.CharField(max_length=255, blank=True)
    model_number = models.CharField(max_length=255, blank=True)
    purchase_date = models.DateField(blank=True, null=True)

    # Cleaning schedule
    cleaning_frequency = models.IntegerField(
        help_text="Hours between required cleanings"
    )
    last_cleaned_at = models.DateTimeField(blank=True, null=True)
    next_cleaning_due = models.DateTimeField(blank=True, null=True)

    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    is_iot_enabled = models.BooleanField(
        default=False,
        help_text="Equipment has IoT sensor for automatic logging"
    )
    iot_device_id = models.CharField(max_length=255, blank=True, null=True)

    # Notes
    notes = models.TextField(blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['location', 'name']
        verbose_name = _('equipment')
        verbose_name_plural = _('equipment')

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

    @property
    def is_overdue(self):
        """Check if cleaning is overdue"""
        if not self.next_cleaning_due:
            return False
        from django.utils import timezone
        return self.next_cleaning_due < timezone.now()

    @property
    def compliance_status(self):
        """Get current compliance status"""
        if self.status != 'active':
            return 'inactive'
        if not self.last_cleaned_at:
            return 'never_cleaned'
        if self.is_overdue:
            return 'overdue'

        from django.utils import timezone
        from datetime import timedelta

        # Calculate time until next cleaning
        time_until_due = self.next_cleaning_due - timezone.now()
        warning_threshold = timedelta(hours=self.cleaning_frequency * 0.2)

        if time_until_due <= warning_threshold:
            return 'due_soon'

        return 'compliant'

    def update_next_cleaning_due(self):
        """Calculate and update next cleaning due date"""
        if self.last_cleaned_at:
            from django.utils import timezone
            from datetime import timedelta
            self.next_cleaning_due = self.last_cleaned_at + timedelta(
                hours=self.cleaning_frequency
            )
            self.save(update_fields=['next_cleaning_due'])

    def save(self, *args, **kwargs):
        # Set cleaning frequency from equipment type if not set
        if not self.cleaning_frequency and self.equipment_type:
            self.cleaning_frequency = self.equipment_type.default_cleaning_frequency

        # Auto-assign protocol from equipment type if not set
        if not self.protocol and self.equipment_type:
            active_protocol = self.equipment_type.protocols.filter(
                is_active=True
            ).first()
            if active_protocol:
                self.protocol = active_protocol

        super().save(*args, **kwargs)
