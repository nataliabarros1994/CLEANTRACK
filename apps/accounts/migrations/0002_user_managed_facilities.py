# Generated migration for adding managed_facilities field to User model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('facilities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='managed_facilities',
            field=models.ManyToManyField(
                blank=True,
                help_text='Facilities that this user manages (for managers/admins)',
                related_name='managers',
                to='facilities.facility'
            ),
        ),
    ]
