# Generated by Django 2.1.4 on 2018-12-18 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("accounts", "0002_auto_20181218_1201")]

    operations = [
        migrations.CreateModel(
            name="Token",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                )
            ],
        )
    ]
