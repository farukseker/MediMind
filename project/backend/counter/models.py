from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.utils import timezone


User = get_user_model()


class CounterSplitType(models.TextChoices):
    DAILY = 'daily', 'Daily'
    WEEKLY = 'weekly', 'Weekly'
    MONTHLY = 'monthly', 'Monthly'
    NOSPLIT = 'nosplit', 'NoSplit'

    @classmethod
    def get_trunc_function(cls, split_type):
        return {
            cls.DAILY: TruncDay,
            cls.WEEKLY: TruncWeek,
            cls.MONTHLY: TruncMonth
        }.get(split_type, TruncDay)


class Counter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=50, blank=True, null=True)
    split_type = models.CharField(
        max_length=10,
        choices=CounterSplitType.choices,
        default=CounterSplitType.DAILY
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"


class CounterEntry(models.Model):
    counter = models.ForeignKey(Counter, on_delete=models.CASCADE, related_name="entries")
    timestamp = models.DateTimeField(default=timezone.now)
    value = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.counter.name} - {self.timestamp.date()} - {self.value}"
