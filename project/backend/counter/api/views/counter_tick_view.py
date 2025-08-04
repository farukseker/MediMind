from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from counter.api.serializers import CounterEntrySerializer
from counter.models import CounterEntry


class CounterTickCreateView(CreateAPIView):
    serializer_class = CounterEntrySerializer
    permission_classes = [
        IsAuthenticated
    ]
    queryset = CounterEntry.objects.all()
