from celery import shared_task
from django.utils import timezone
from .models import Trending_News

@shared_task
def delete_trending_news(trending_news_id):
    try:
        trending_news = Trending_News.objects.get(pk=trending_news_id)
        trending_news.delete()
    except Trending_News.DoesNotExist:
        pass
    
    
# your_app/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import User

@shared_task
def update_subscription_status():
    expired_users = User.objects.filter(subscription_expiration__lt=timezone.now())
    expired_users.update(is_staffs=False)

