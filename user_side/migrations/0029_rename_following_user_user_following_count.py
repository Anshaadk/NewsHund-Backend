# Generated by Django 4.2.3 on 2023-08-16 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0028_rename_followers_count_user_followers_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='following_user',
            new_name='following_count',
        ),
    ]