# Generated migration for adding is_active and stripe_customer_id to Facility

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Facility is active and has valid subscription'),
        ),
        migrations.AddField(
            model_name='facility',
            name='stripe_customer_id',
            field=models.CharField(
                blank=True,
                help_text='Stripe customer ID for billing',
                max_length=255,
                null=True
            ),
        ),
    ]
