from django.db.models.functions import Coalesce
from rest_framework.generics import ListAPIView, get_object_or_404, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, Value
from django.contrib.postgres.aggregates import ArrayAgg

from counter.models import Counter, CounterEntry, CounterSplitType
from counter.api.serializers import CounterEntryGroupedSerializer
from typing import override



class CounterEntryGroupedRetrieveDestroyListView(ListAPIView, DestroyAPIView):
    lookup_field = 'counter_pk'
    serializer_class = CounterEntryGroupedSerializer

    def get_counter_obj(self) -> Counter:
        counter_pk = self.kwargs.get('counter_pk', None)
        counter: Counter =  get_object_or_404(
            Counter,
            user=self.request.user,
            pk=counter_pk
        )
        return counter

    def get_grouped_entries_list(self) -> CounterEntry:
        counter = self.get_counter_obj()

        trunc_function = CounterSplitType.get_trunc_function(
            counter.split_type
        )
        return (
            CounterEntry.objects
            .filter(counter=counter)
            .annotate(date=trunc_function('timestamp'))
            .values('date')
            .annotate(count=Coalesce(Sum('value'), Value(0)))
            .order_by('date')
        )

    def get_grouped_entries_id_list(self) -> list:
        counter = self.get_counter_obj()

        trunc_function = CounterSplitType.get_trunc_function(counter.split_type)

        return (
            CounterEntry.objects
            .filter(counter=counter)
            .annotate(group=trunc_function('timestamp'))
            .values('group')
            .annotate(entry_ids=ArrayAgg('id'))
            .order_by('group')
        )

    @staticmethod
    def delete_entries_objects_from_id_list(entries_id_list: list[int]) -> int:
        deleted_count, _ = CounterEntry.objects.filter(id__in=entries_id_list).delete()
        return deleted_count

    @override
    def delete(self, request, *args, **kwargs):
        status_code = status.HTTP_400_BAD_REQUEST
        response_data = {}

        delete_index = self.kwargs.get("delete_index")
        if type(delete_index) is int and delete_index >= 0:
            status_code = status.HTTP_404_NOT_FOUND

            grouped_entries = self.get_grouped_entries_id_list()

            if (
                not (delete_index < 0) and not (delete_index >= len(grouped_entries))
            ) and (
                entry_ids := grouped_entries[delete_index].get('entry_ids')
            ):
                deleted_count = self.delete_entries_objects_from_id_list(entry_ids)

                status_code = status.HTTP_204_NO_CONTENT
                response_data = {
                    "deleted": deleted_count,
                    "entry_ids": entry_ids,
                    "group": grouped_entries[delete_index]['group']
                }

        return Response(
            data=response_data,
            status=status_code
        )

    @override
    def get_queryset(self, *args, **kwargs):
        return self.get_grouped_entries_list()
