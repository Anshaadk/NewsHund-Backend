# Generated by Django 4.2.3 on 2023-08-16 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0029_rename_following_user_user_following_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_side.follow')),
            ],
        ),
    ]