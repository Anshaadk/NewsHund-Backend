# Generated by Django 4.2.3 on 2023-08-11 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0019_remove_chatmessage_sender_name_chatmessage_chat_room_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='sender_name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
