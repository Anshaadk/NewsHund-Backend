# Generated by Django 4.2.3 on 2023-08-17 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0032_alter_follow_unique_together_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
