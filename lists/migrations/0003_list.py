# Generated by Django 2.1rc1 on 2018-08-01 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("lists", "0002_item_text")]

    operations = [
        migrations.CreateModel(
            name="List",
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
