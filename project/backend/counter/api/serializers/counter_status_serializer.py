import calendar
from datetime import timedelta, date, time, datetime
from rest_framework import serializers
from counter.models import Counter, CounterEntry, CounterSplitType

from rest_framework import serializers
from django.db.models import Sum, Value, Q
from django.db.models.functions import Coalesce


class CounterStatusCreateSerializer(serializers.ModelSerializer):
    # count = serializers.SerializerMethodField(required=False)
    # count = serializers.IntegerField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    split_type = serializers.ChoiceField(
        choices=CounterSplitType.choices,
        default=CounterSplitType.DAILY
    )


    count = serializers.SerializerMethodField(method_name='get_interval_count')

    @staticmethod
    def get_interval_count(obj: Counter) -> int:
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

    # @staticmethod
    # def get_count(i) -> int:
    #     if counts := CounterEntry.objects.filter(counter=i).all():
    #         return sum([count.value for count in counts])
    #     else:
    #         return 0

    class Meta:
        model = Counter
        fields: tuple[str] =  'name', 'unit', 'count', 'id', 'split_type'
        # exclude: tuple[str] = 'user',

