# Generated by Django 4.2.4 on 2023-09-08 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0045_remove_user_blocked_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='full_description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='news',
            name='short_details',
            field=models.CharField(max_length=500),
        ),
    ]
