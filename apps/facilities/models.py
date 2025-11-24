from django.db import models


class Facility(models.Model):
    """
    Physical location where equipment is located
    """
    name = models.CharField(max_length=200)
    address = models.TextField()
    is_active = models.BooleanField(
        default=True,
        help_text="Facility is active and has valid subscription"
    )
    stripe_customer_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Stripe customer ID for billing"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Facilities"
        ordering = ['name']

    def __str__(self):
        return self.name
