from rest_framework import serializers


class CounterEntryGroupedSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    count = serializers.IntegerField()
