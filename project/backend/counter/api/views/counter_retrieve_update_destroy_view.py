from rest_framework.generics import RetrieveUpdateDestroyAPIView
from counter.models import Counter
from counter.api.serializers import CounterRetrieveUpdateDestroySerializer


class CounterRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = CounterRetrieveUpdateDestroySerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Counter.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, **serializer.validated_data)
