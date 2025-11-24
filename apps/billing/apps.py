from django.apps import AppConfig


class BillingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.billing'
    verbose_name = 'Billing & Subscriptions'

    def ready(self):
        """
        Import webhook handlers when Django starts.
        This registers all @webhooks.handler decorators with dj-stripe.
        """
        import logging
        logger = logging.getLogger(__name__)

        try:
            # Only import if djstripe is available and enabled
            from django.conf import settings
            if 'djstripe' in settings.INSTALLED_APPS:
                from . import webhook_handlers
                logger.info("Billing webhook handlers registered successfully")
            else:
                logger.warning("djstripe not in INSTALLED_APPS, skipping webhook handlers")
        except ImportError as e:
            logger.warning(f"Could not import webhook_handlers: {e}")
        except Exception as e:
            logger.error(f"Error in billing app ready(): {e}", exc_info=True)
            # Don't re-raise - allow Django to continue starting
