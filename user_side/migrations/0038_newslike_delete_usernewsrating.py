# Generated by Django 4.2.4 on 2023-09-05 09:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_side', '0037_news_total_dislikes_news_total_likes_usernewsrating'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked', models.CharField(choices=[('Like', 'Like'), ('Dislike', 'Dislike'), ('Not', 'Not')], max_length=50)),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_side.news')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'news')},
            },
        ),
        migrations.DeleteModel(
            name='UserNewsRating',
        ),
    ]
