"""
Compliance models for tracking cleaning logs and alerts
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from equipment.models import Equipment
from accounts.models import User


class CleaningLog(models.Model):
    """
    Record of a cleaning activity for a piece of equipment
    """
    SOURCE_CHOICES = [
        ('manual', 'Manual Entry'),
        ('iot', 'IoT Sensor'),
        ('qr_scan', 'QR Code Scan'),
    ]

    VALIDATION_STATUS = [
        ('pending', 'Pending Validation'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('flagged', 'Flagged for Review'),
    ]

    # Core info
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='cleaning_logs'
    )
    performed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='performed_cleanings'
    )

    # Timing
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField()
    duration = models.IntegerField(
        help_text="Duration in minutes",
        blank=True,
        null=True
    )

    # Protocol compliance
    protocol_version = models.CharField(
        max_length=50,
        blank=True,
        help_text="Version of cleaning protocol used"
    )
    chemicals_used = models.JSONField(
        default=list,
        help_text="List of chemicals/products used"
    )
    steps_completed = models.JSONField(
        default=list,
        help_text="List of protocol steps completed"
    )

    # Validation
    contact_time_met = models.BooleanField(
        default=True,
        help_text="Required contact time was met"
    )
    all_steps_completed = models.BooleanField(
        default=True,
        help_text="All protocol steps were completed"
    )
    validation_status = models.CharField(
        max_length=20,
        choices=VALIDATION_STATUS,
        default='approved'
    )
    validated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='validated_cleanings'
    )
    validated_at = models.DateTimeField(blank=True, null=True)

    # Evidence
    photo_before = models.ImageField(
        upload_to='cleaning_logs/before/',
        blank=True,
        null=True
    )
    photo_after = models.ImageField(
        upload_to='cleaning_logs/after/',
        blank=True,
        null=True
    )

    # Source tracking
    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default='manual'
    )
    iot_sensor_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Raw data from IoT sensor if applicable"
    )

    # Notes
    notes = models.TextField(blank=True)
    issues_found = models.TextField(blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-completed_at']
        verbose_name = _('cleaning log')
        verbose_name_plural = _('cleaning logs')
        indexes = [
            models.Index(fields=['-completed_at']),
            models.Index(fields=['equipment', '-completed_at']),
            models.Index(fields=['validation_status']),
        ]

    def __str__(self):
        return f"{self.equipment} - {self.completed_at.strftime('%Y-%m-%d %H:%M')}"

    @property
    def is_compliant(self):
        """Check if cleaning meets compliance requirements"""
        return (
            self.validation_status == 'approved' and
            self.contact_time_met and
            self.all_steps_completed
        )

    def save(self, *args, **kwargs):
        # Calculate duration if not set
        if not self.duration and self.started_at and self.completed_at:
            delta = self.completed_at - self.started_at
            self.duration = int(delta.total_seconds() / 60)

        # Auto-approve if all conditions met
        if (
            self.validation_status == 'pending' and
            self.contact_time_met and
            self.all_steps_completed and
            not self.issues_found
        ):
            self.validation_status = 'approved'

        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Update equipment's last_cleaned_at
        if is_new and self.validation_status == 'approved':
            self.equipment.last_cleaned_at = self.completed_at
            self.equipment.update_next_cleaning_due()


class ComplianceAlert(models.Model):
    """
    Alerts for compliance issues (overdue cleanings, protocol violations, etc.)
    """
    ALERT_TYPE_CHOICES = [
        ('overdue', 'Cleaning Overdue'),
        ('due_soon', 'Cleaning Due Soon'),
        ('missed', 'Cleaning Missed'),
        ('incomplete', 'Incomplete Cleaning'),
        ('protocol_violation', 'Protocol Violation'),
        ('equipment_issue', 'Equipment Issue'),
    ]

    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('acknowledged', 'Acknowledged'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]

    # Core info
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='alerts'
    )
    alert_type = models.CharField(
        max_length=30,
        choices=ALERT_TYPE_CHOICES
    )
    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES
    )

    # Details
    title = models.CharField(max_length=255)
    message = models.TextField()
    suggested_action = models.TextField(blank=True)

    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    # Assignment
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_alerts'
    )
    acknowledged_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='acknowledged_alerts'
    )
    acknowledged_at = models.DateTimeField(blank=True, null=True)

    resolved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_alerts'
    )
    resolved_at = models.DateTimeField(blank=True, null=True)
    resolution_notes = models.TextField(blank=True)

    # Related cleaning log (if applicable)
    related_cleaning_log = models.ForeignKey(
        CleaningLog,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='alerts'
    )

    # Notifications
    email_sent = models.BooleanField(default=False)
    email_sent_at = models.DateTimeField(blank=True, null=True)

    # Due date
    due_by = models.DateTimeField(blank=True, null=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('compliance alert')
        verbose_name_plural = _('compliance alerts')
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['equipment', 'status']),
            models.Index(fields=['alert_type', 'severity']),
        ]

    def __str__(self):
        return f"{self.get_alert_type_display()} - {self.equipment.name}"

    def acknowledge(self, user):
        """Mark alert as acknowledged"""
        from django.utils import timezone
        self.status = 'acknowledged'
        self.acknowledged_by = user
        self.acknowledged_at = timezone.now()
        self.save()

    def resolve(self, user, notes=''):
        """Mark alert as resolved"""
        from django.utils import timezone
        self.status = 'resolved'
        self.resolved_by = user
        self.resolved_at = timezone.now()
        self.resolution_notes = notes
        self.save()


class AuditReport(models.Model):
    """
    Generated audit reports for compliance tracking
    """
    REPORT_TYPE_CHOICES = [
        ('daily', 'Daily Report'),
        ('weekly', 'Weekly Report'),
        ('monthly', 'Monthly Report'),
        ('custom', 'Custom Report'),
        ('audit', 'Audit Report'),
    ]

    # Basic info
    title = models.CharField(max_length=255)
    report_type = models.CharField(
        max_length=20,
        choices=REPORT_TYPE_CHOICES
    )
    generated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='generated_reports'
    )

    # Scope
    location = models.ForeignKey(
        'accounts.Location',
        on_delete=models.CASCADE,
        related_name='audit_reports',
        null=True,
        blank=True
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    # Content
    summary = models.JSONField(
        default=dict,
        help_text="Summary statistics (total cleanings, compliance rate, etc.)"
    )
    findings = models.JSONField(
        default=list,
        help_text="List of findings and issues"
    )

    # Files
    pdf_file = models.FileField(
        upload_to='audit_reports/pdf/',
        blank=True,
        null=True
    )
    excel_file = models.FileField(
        upload_to='audit_reports/excel/',
        blank=True,
        null=True
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('audit report')
        verbose_name_plural = _('audit reports')

    def __str__(self):
        return f"{self.title} - {self.created_at.strftime('%Y-%m-%d')}"
