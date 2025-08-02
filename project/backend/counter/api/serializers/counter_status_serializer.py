from rest_framework import serializers
from counter.models import Counter, CounterEntry, CounterSplitType


class CounterStatusCreateSerializer(serializers.ModelSerializer):
    # count = serializers.SerializerMethodField(required=False)
    count = serializers.IntegerField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    split_type = serializers.ChoiceField(
        choices=CounterSplitType.choices,
        default=CounterSplitType.DAILY
    )

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

