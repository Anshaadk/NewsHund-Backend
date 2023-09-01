# your_app_name/cron.py
from datetime import timedelta
from django.utils import timezone
from django_cron import CronJobBase, Schedule
from .models import User

class UpdateExpiredSubscriptions(CronJobBase):
    RUN_EVERY_MINS = 1440  # Run every 24 hours (1 day)

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'user_side.update_expired_subscriptions'

    def do(self):
        expired_users = User.objects.filter(subscription_expiration__lt=timezone.now())
        for user in expired_users:
            user.is_staff = False
            user.save()

from .cron import UpdateExpiredSubscriptions

# your_app/management/commands/update_subscription_status.py
from django.core.management.base import BaseCommand
from .task import update_subscription_status

class Command(BaseCommand):
    help = 'Update is_staffs status for expired subscriptions'

    def handle(self, *args, **options):
        update_subscription_status.delay()
        self.stdout.write(self.style.SUCCESS('Subscription status updated'))
