# Generated by Django 3.2.11 on 2022-02-21 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('houmer', '0004_auto_20220221_0503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledvisitevent',
            name='scheduled_visit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scheduled_visit_events', to='houmer.scheduledvisit'),
        ),
    ]
