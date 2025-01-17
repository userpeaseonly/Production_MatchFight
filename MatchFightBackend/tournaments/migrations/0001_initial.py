# Generated by Django 5.0.6 on 2024-07-04 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('min_age', models.IntegerField()),
                ('max_age', models.IntegerField()),
                ('min_weight', models.FloatField()),
                ('max_weight', models.FloatField()),
            ],
        ),
    ]
