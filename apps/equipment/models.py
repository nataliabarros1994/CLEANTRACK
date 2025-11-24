from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
import qrcode
from io import BytesIO
from django.core.files import File
from apps.facilities.models import Facility
import secrets


class Equipment(models.Model):
    CLEANING_FREQUENCIES = [
        (1, "1 hora"),
        (4, "4 horas"),
        (8, "8 horas"),
        (24, "24 horas"),
        (168, "Semanal (168h)"),
    ]

    EQUIPMENT_CATEGORIES = [
        ('diagnostic', 'Diagnóstico'),
        ('monitoring', 'Monitoramento'),
        ('life_support', 'Suporte à Vida'),
        ('surgical', 'Cirúrgico'),
        ('laboratory', 'Laboratório'),
        ('other', 'Outro'),
    ]

    # Basic Information
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="equipment_set")
    name = models.CharField("Nome do equipamento", max_length=200)
    serial_number = models.CharField("Número de série", max_length=100, unique=True)

    # Additional Information
    description = models.TextField(
        "Descrição",
        blank=True,
        help_text="Descrição detalhada do equipamento"
    )
    category = models.CharField(
        "Categoria",
        max_length=20,
        choices=EQUIPMENT_CATEGORIES,
        default='other',
        help_text="Categoria do equipamento"
    )
    location = models.CharField(
        "Localização específica",
        max_length=200,
        blank=True,
        help_text="Ex: Sala 101, Ala B, 2º andar"
    )

    # Cleaning Configuration
    cleaning_frequency_hours = models.PositiveSmallIntegerField(
        "Frequência de limpeza (horas)",
        choices=CLEANING_FREQUENCIES,
        default=24
    )

    # Status
    is_active = models.BooleanField(default=True)

    # QR Code & Token
    public_token = models.CharField(
        max_length=64,
        unique=True,
        blank=True,
        help_text="Public token for QR code-based cleaning registration (expires in 5 minutes)"
    )
    token_created_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the current token was generated"
    )
    qr_code = models.ImageField(
        upload_to='equipment_qrcodes/',
        blank=True,
        null=True,
        help_text="QR code for quick cleaning registration"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Equipment"

    @property
    def last_cleaning(self):
        """Get the most recent cleaning log"""
        return self.cleaning_logs.order_by('-cleaned_at').first()

    @property
    def is_overdue(self):
        """Check if equipment is overdue for cleaning"""
        from django.utils import timezone
        from datetime import timedelta

        last_log = self.last_cleaning
        if not last_log:
            return True  # Never cleaned

        due_time = last_log.cleaned_at + timedelta(hours=self.cleaning_frequency_hours)
        return timezone.now() > due_time

    @property
    def public_url(self):
        """Get the public URL for QR code registration"""
        from django.contrib.sites.models import Site

        try:
            site = Site.objects.get_current()
            domain = site.domain
            # Use HTTPS in production
            protocol = 'https' if not settings.DEBUG else 'http'
        except:
            domain = 'localhost:8000'
            protocol = 'http'

        return f"{protocol}://{domain}/log/{self.public_token}/"

    @property
    def category_display(self):
        """Get human-readable category name"""
        return dict(self.EQUIPMENT_CATEGORIES).get(self.category, 'Outro')

    @property
    def full_location(self):
        """Get full location string (facility + specific location)"""
        if self.location:
            return f"{self.facility.name} - {self.location}"
        return self.facility.name

    def generate_qr_code(self, size=10, border=4, error_correction='H'):
        """
        Generate QR code for cleaning registration URL using permanent token

        Args:
            size: Box size for QR code (default: 10, recommended: 8-12)
            border: Border size in boxes (default: 4, minimum: 4)
            error_correction: Error correction level ('L', 'M', 'Q', 'H')
                L = 7% correction, M = 15%, Q = 25%, H = 30%
        """
        # Use the public_url property for consistency
        url = self.public_url

        # Map error correction levels
        error_levels = {
            'L': qrcode.constants.ERROR_CORRECT_L,
            'M': qrcode.constants.ERROR_CORRECT_M,
            'Q': qrcode.constants.ERROR_CORRECT_Q,
            'H': qrcode.constants.ERROR_CORRECT_H,
        }
        error_level = error_levels.get(error_correction, qrcode.constants.ERROR_CORRECT_H)

        # Generate QR code with improved settings
        qr = qrcode.QRCode(
            version=1,  # Auto-size
            error_correction=error_level,
            box_size=size,
            border=border,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Create image with high contrast colors
        img = qr.make_image(
            fill_color="black",
            back_color="white"
        )

        # Save to BytesIO
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        # Save to model field with unique filename
        filename = f'qr_equipment_{self.id}_{self.public_token[:8]}.png'
        self.qr_code.save(filename, File(buffer), save=False)
        buffer.close()

    def get_qr_code_cached(self, size=10, border=4, error_correction='H'):
        """
        Get QR code with caching support for production environments

        Returns PIL Image object that can be cached or converted to BytesIO
        Uses Django's cache framework if configured (recommended for production)

        Args:
            size: Box size for QR code (default: 10)
            border: Border size in boxes (default: 4)
            error_correction: Error correction level ('L', 'M', 'Q', 'H')

        Returns:
            PIL Image object
        """
        from django.core.cache import cache

        # Create cache key based on token and parameters
        cache_key = f'qr_code_{self.public_token}_{size}_{border}_{error_correction}'

        # Try to get from cache
        cached_qr = cache.get(cache_key)
        if cached_qr:
            return cached_qr

        # Generate QR code
        url = self.public_url

        error_levels = {
            'L': qrcode.constants.ERROR_CORRECT_L,
            'M': qrcode.constants.ERROR_CORRECT_M,
            'Q': qrcode.constants.ERROR_CORRECT_Q,
            'H': qrcode.constants.ERROR_CORRECT_H,
        }
        error_level = error_levels.get(error_correction, qrcode.constants.ERROR_CORRECT_H)

        qr = qrcode.QRCode(
            version=1,
            error_correction=error_level,
            box_size=size,
            border=border,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Cache for 1 hour (3600 seconds)
        # For temporary tokens (5 min), this doesn't matter as token changes
        # For permanent tokens, this significantly improves performance
        cache.set(cache_key, img, 3600)

        return img

    def regenerate_token(self, regenerate_qr=True):
        """
        Regenerate the public token (for security/revocation)

        Args:
            regenerate_qr: If True, also regenerate the QR code (default: True)

        Returns:
            The new token string
        """
        old_token = self.public_token
        self.public_token = secrets.token_urlsafe(16)
        self.save(update_fields=['public_token', 'updated_at'])

        if regenerate_qr:
            self.generate_qr_code()
            self.save(update_fields=['qr_code'])

        # Log the token regeneration
        import logging
        logger = logging.getLogger(__name__)
        logger.info(
            f"Token regenerated for equipment {self.id} ({self.name}). "
            f"Old token: {old_token[:8]}..., New token: {self.public_token[:8]}..."
        )

        return self.public_token

    @classmethod
    def validate_token(cls, token):
        """
        Validate a token and return the equipment if valid

        Args:
            token: The public token to validate

        Returns:
            Equipment instance if valid and active, None otherwise
        """
        try:
            equipment = cls.objects.get(
                public_token=token,
                is_active=True
            )
            return equipment
        except cls.DoesNotExist:
            return None

    def revoke_access(self):
        """
        Revoke access to this equipment by deactivating it
        Use regenerate_token() if you want to change the token instead
        """
        self.is_active = False
        self.save(update_fields=['is_active', 'updated_at'])

        # Log the revocation
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(
            f"Access revoked for equipment {self.id} ({self.name}). "
            f"Token: {self.public_token[:8]}..."
        )

    def _generate_new_token(self):
        """Generate new token with timestamp (expires in 5 minutes)"""
        from django.utils import timezone
        self.public_token = secrets.token_urlsafe(32)
        self.token_created_at = timezone.now()

    def is_token_valid(self):
        """Check if token is still valid (within 5 minutes of creation)"""
        from django.utils import timezone
        from datetime import timedelta

        if not self.token_created_at:
            return False

        expiration = self.token_created_at + timedelta(minutes=5)
        return timezone.now() <= expiration

    def save(self, *args, **kwargs):
        """Override save to generate public_token and QR code if needed"""
        # Generate public_token if not exists
        if not self.public_token:
            self._generate_new_token()

        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Generate QR code after first save (when we have an ID)
        if is_new or not self.qr_code:
            self.generate_qr_code()
            super().save(update_fields=['qr_code'])
