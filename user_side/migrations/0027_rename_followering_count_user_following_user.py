# Generated by Django 4.2.3 on 2023-08-16 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0026_rename_following_user_user_followering_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='Followering_count',
            new_name='following_user',
        ),
    ]
