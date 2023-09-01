# Generated by Django 4.2.3 on 2023-08-10 04:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0008_room_message'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={},
        ),
        migrations.RemoveField(
            model_name='message',
            name='body',
        ),
        migrations.RemoveField(
            model_name='message',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='message',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='message',
            name='send_by',
        ),
        migrations.RemoveField(
            model_name='room',
            name='agent',
        ),
        migrations.RemoveField(
            model_name='room',
            name='client',
        ),
        migrations.RemoveField(
            model_name='room',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='room',
            name='status',
        ),
        migrations.RemoveField(
            model_name='room',
            name='url',
        ),
        migrations.RemoveField(
            model_name='room',
            name='uuid',
        ),
        migrations.AddField(
            model_name='message',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_side.room'),
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
