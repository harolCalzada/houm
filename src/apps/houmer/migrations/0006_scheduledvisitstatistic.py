# Generated by Django 3.2.11 on 2022-02-21 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('houmer', '0005_alter_scheduledvisitevent_scheduled_visit'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledVisitStatistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stay_time_in_minutes', models.IntegerField(null=True)),
                ('velocity_km_x_h', models.IntegerField(null=True)),
                ('schedule_visit', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='scheduled_visit_statistic', to='houmer.scheduledvisit')),
            ],
            options={
                'verbose_name': 'Scheduled Visit Report',
                'verbose_name_plural': 'Scheduled Visit Reports',
            },
        ),
    ]
