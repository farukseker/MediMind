from rest_framework import serializers
from django.db.models import Sum, Value, Q
from django.db.models.functions import Coalesce

from counter.models import CounterEntry, Counter, CounterSplitType

from datetime import timedelta, date, time, datetime
import calendar


class CounterRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    interval_count = serializers.SerializerMethodField()

    def get_interval_count(self, obj: Counter):
        today = date.today()

        match obj.split_type:
            case CounterSplitType.DAILY:
                start = datetime.combine(today, time.min)
                end = datetime.combine(today, time.max)

            case CounterSplitType.WEEKLY:
                start_of_week = today - timedelta(days=today.weekday())
                start = datetime.combine(start_of_week, time.min)
                end = datetime.combine((start_of_week + timedelta(days=6)), time.max)

            case CounterSplitType.MONTHLY:
                month_start = today.replace(day=1)
                last_day = calendar.monthrange(today.year, today.month)[1]
                month_end = today.replace(day=last_day)

                start = datetime.combine(month_start, time.min)
                end = datetime.combine(month_end, time.max)
            case _:
                start = None
                end = None

        if start and end:
            case_query = Q(timestamp__range=(start, end))
        else:
            case_query = Q()

        return obj.entries.aggregate(
            interval_count=Coalesce(
                Sum('value', filter=case_query),
                Value(0)
            )
        )['interval_count']

    class Meta:
        model: Counter = Counter
        fields: str = '__all__'

