# Generated by Django 4.2.4 on 2023-09-08 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0046_alter_news_full_description_alter_news_short_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='short_details',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='news',
            name='subject',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='trending_news',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='trending_news',
            name='short_banner',
            field=models.TextField(),
        ),
    ]
