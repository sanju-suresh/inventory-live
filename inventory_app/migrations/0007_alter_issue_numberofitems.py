# Generated by Django 4.0.4 on 2022-06-01 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_app', '0006_alter_issue_numberofitems'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='numberofitems',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
