# Generated by Django 5.0.3 on 2024-03-09 06:52

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SubwayOutlet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
                ("address", models.TextField()),
                ("operating_time", models.CharField(max_length=100)),
                ("long", models.DecimalField(decimal_places=4, max_digits=10)),
                ("lat", models.DecimalField(decimal_places=4, max_digits=10)),
            ],
        ),
    ]
