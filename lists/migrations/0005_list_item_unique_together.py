# Generated by Django 2.1 on 2018-08-15 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("lists", "0004_item_list")]

    operations = [
        migrations.AlterUniqueTogether(name="item", unique_together={("list", "text")})
    ]
