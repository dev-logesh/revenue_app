# Generated by Django 4.2 on 2023-04-13 02:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("staffs", "0003_staff_quali"),
    ]

    operations = [
        migrations.AlterField(
            model_name="staff",
            name="quali",
            field=models.CharField(
                blank=True, max_length=500, verbose_name="Qualification"
            ),
        ),
    ]
