"""
Account models for multi-tenant architecture
"""
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model with email as username"""
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email


class Account(models.Model):
    """
    Organization account - top level of multi-tenant hierarchy
    Account → Locations → Equipment
    """
    PLAN_CHOICES = [
        ('trial', 'Trial - $50/month'),
        ('standard', 'Standard - $100/month'),
        ('custom', 'Custom/Enterprise'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_accounts')
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='trial')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    # Subscription info
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    subscription_end_date = models.DateTimeField(blank=True, null=True)

    # Limits based on plan
    max_locations = models.IntegerField(default=5)  # Trial: 5, Standard: 50
    max_users = models.IntegerField(default=10)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('account')
        verbose_name_plural = _('accounts')

    def __str__(self):
        return self.name

    @property
    def is_subscription_active(self):
        """Check if subscription is active"""
        if self.status != 'active':
            return False
        if self.subscription_end_date:
            from django.utils import timezone
            return self.subscription_end_date > timezone.now()
        return True


class Location(models.Model):
    """
    Physical location within an account (e.g., hospital wing, clinic branch)
    """
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='USA')

    # Contact
    contact_name = models.CharField(max_length=255, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)

    # Status
    is_active = models.BooleanField(default=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('location')
        verbose_name_plural = _('locations')
        unique_together = [['account', 'name']]

    def __str__(self):
        return f"{self.name} ({self.account.name})"


class AccountMembership(models.Model):
    """
    User membership in an account with role-based access
    """
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('technician', 'Technician'),
        ('auditor', 'Auditor (Read-only)'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    locations = models.ManyToManyField(Location, blank=True, related_name='members')

    # Permissions
    can_manage_users = models.BooleanField(default=False)
    can_manage_equipment = models.BooleanField(default=True)
    can_log_cleaning = models.BooleanField(default=True)
    can_view_reports = models.BooleanField(default=True)
    can_export_data = models.BooleanField(default=False)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('account membership')
        verbose_name_plural = _('account memberships')
        unique_together = [['user', 'account']]

    def __str__(self):
        return f"{self.user.email} - {self.account.name} ({self.role})"

    def save(self, *args, **kwargs):
        """Auto-set permissions based on role"""
        if self.role == 'admin':
            self.can_manage_users = True
            self.can_manage_equipment = True
            self.can_log_cleaning = True
            self.can_view_reports = True
            self.can_export_data = True
        elif self.role == 'manager':
            self.can_manage_users = False
            self.can_manage_equipment = True
            self.can_log_cleaning = True
            self.can_view_reports = True
            self.can_export_data = True
        elif self.role == 'technician':
            self.can_manage_users = False
            self.can_manage_equipment = False
            self.can_log_cleaning = True
            self.can_view_reports = False
            self.can_export_data = False
        elif self.role == 'auditor':
            self.can_manage_users = False
            self.can_manage_equipment = False
            self.can_log_cleaning = False
            self.can_view_reports = True
            self.can_export_data = True

        super().save(*args, **kwargs)
