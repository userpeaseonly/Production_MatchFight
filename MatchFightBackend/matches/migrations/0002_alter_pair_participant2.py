# Generated by Django 5.0.6 on 2024-07-05 09:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0001_initial'),
        ('participants', '0002_alter_participant_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pair',
            name='participant2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='participant2_pairs', to='participants.participant'),
        ),
    ]
