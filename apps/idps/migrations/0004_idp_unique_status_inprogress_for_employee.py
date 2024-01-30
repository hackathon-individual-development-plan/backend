# Generated by Django 5.0.1 on 2024-01-30 05:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("idps", "0003_alter_goal_options_alter_idp_options"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="idp",
            constraint=models.UniqueConstraint(
                fields=("employee", "status.IN_PROGRESS"),
                name="unique_status_inprogress_for_employee",
            ),
        ),
    ]
