from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from counter.api.serializers import CounterEntrySerializer


class CounterTickCreateView(CreateAPIView):
    serializer_class = CounterEntrySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        counter = serializer.validated_data['counter']
        if counter.user != self.request.user:
            raise NotFound("Counter not found.")
        serializer.save()
