from rest_framework import serializers
from counter.models import CounterEntry, Counter


class CounterRetrieveUpdateDestroySerializer(serializers.Serializer):
    ...
    count = serializers.IntegerField(read_only=True)
    id = serializers.IntegerField(read_only=True)


