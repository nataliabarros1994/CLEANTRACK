"""
Billing app admin configuration
This app uses dj-stripe models, which already have admin registered
"""
from django.contrib import admin

# dj-stripe automatically registers its models in the admin
# No custom models to register here
