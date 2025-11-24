from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model for CleanTrack
    """
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(
        max_length=20,
        choices=[
            ('admin', 'Administrator'),
            ('manager', 'Manager'),
            ('technician', 'Technician'),
        ],
        default='technician'
    )
    managed_facilities = models.ManyToManyField(
        'facilities.Facility',
        related_name='managers',
        blank=True,
        help_text="Facilities that this user manages (for managers/admins)"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # username removido - não pode estar aqui quando USERNAME_FIELD é email

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    @property
    def is_manager_or_admin(self):
        """Check if user is a manager or admin"""
        return self.role in ['admin', 'manager']


class Account(models.Model):
    """
    Organization/tenant account
    """
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_accounts'
    )
    stripe_customer_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Stripe customer ID for billing"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
