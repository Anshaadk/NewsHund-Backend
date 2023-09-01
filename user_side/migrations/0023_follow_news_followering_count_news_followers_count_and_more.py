# Generated by Django 4.2.3 on 2023-08-16 05:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0022_room_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_user_set', to=settings.AUTH_USER_MODEL)),
                ('following_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following_user_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('following_user', 'followed_user')},
            },
        ),
        migrations.AddField(
            model_name='news',
            name='Followering_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='news',
            name='Followers_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Followers',
        ),
    ]
