# Generated by Django 4.2.3 on 2023-08-08 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0004_alter_user_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='plan',
            field=models.CharField(choices=[('Free', 'Free'), ('10', '10'), ('15', '15'), ('20', '20'), ('30', '30')], max_length=50),
        ),
    ]