# Generated by Django 4.2.4 on 2023-09-06 04:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0042_rating_news_average_rating_news_total_ratings_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set(),
        ),
    ]