from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import status
from counter.models import Counter, CounterEntry, CounterSplitType
from datetime import timedelta, date
from tests.base_test import BaseAPITestCase  # base_test.py dosyasından import edin

User = get_user_model()

class CounterAPITests(BaseAPITestCase):
    def setUp(self):
        super().setUp() # Base sınıfın setUp metodunu çağırın

        # Kullanıcıyı oluşturun ve token'ını alın
        self.user, self.token = self._create_user_and_get_token(email="testuser@gmail.com", password="pass1234")
        # Client'ı oluşturulan token ile yetkilendirin
        self._authenticate_client(self.token)

        self.counter = Counter.objects.create(
            user=self.user,
            name="Steps",
            unit="steps",
            split_type=CounterSplitType.DAILY
        )

        # Birkaç entry oluşturalım
        self.entry1 = CounterEntry.objects.create(
            counter=self.counter,
            value=5,
            timestamp=timezone.now() - timedelta(days=1)
        )
        self.entry2 = CounterEntry.objects.create(
            counter=self.counter,
            value=10,
            timestamp=timezone.now()
        )

    def test_counter_list(self):
        url = reverse("api:counter:counter-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data[0])
        # self.assertIn("today_count", response.data[0])
        self.assertIn("count", response.data[0])

    def test_counter_create(self):
        url = reverse("api:counter:counter-list-create")
        data = {
            "name": "Water",
            "unit": "liters",
            "split_type": CounterSplitType.WEEKLY
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Counter.objects.filter(name="Water").exists())

    def test_daily_counter_list(self):
        url = reverse("api:counter:counter-all-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_tick_create(self):
        url = reverse("api:counter:counter-tick-create")
        data = {
            "counter": self.counter.id,
            "value": 7
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CounterEntry.objects.filter(value=7).exists())

    def test_counter_retrieve_update_destroy(self):
        url = reverse("api:counter:counter-crud", args=[self.counter.id])

        # Retrieve
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Update
        resp = self.client.patch(url, {"name": "Updated Name"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.counter.refresh_from_db()
        self.assertEqual(self.counter.name, "Updated Name")

        # Destroy
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Counter.objects.filter(id=self.counter.id).exists())

    def test_grouped_entry_list(self):
        url = reverse("api:counter:counter-grouped-entry-crud", args=[self.counter.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(all("date" in entry and "count" in entry for entry in resp.data))

    def test_grouped_entry_delete_by_index(self):
        url = reverse("api:counter:counter-remove-entry-range-from-index", args=[self.counter.id, 0])
        resp = self.client.delete(url)
        self.assertIn(resp.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_404_NOT_FOUND])

    def test_delete_all_entries(self):
        url = reverse("api:counter:counter-remove-all-entries", args=[self.counter.id])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CounterEntry.objects.filter(counter=self.counter).count(), 0)

    def test_get_trunc_function_variants(self):
        # DAILY
        self.assertEqual(CounterSplitType.get_trunc_function(CounterSplitType.DAILY).__name__, "TruncDay")
        # WEEKLY
        self.assertEqual(CounterSplitType.get_trunc_function(CounterSplitType.WEEKLY).__name__, "TruncWeek")
        # MONTHLY
        self.assertEqual(CounterSplitType.get_trunc_function(CounterSplitType.MONTHLY).__name__, "TruncMonth")
        # NOSPLIT varsayılan TruncDay
        self.assertEqual(CounterSplitType.get_trunc_function(CounterSplitType.NOSPLIT).__name__, "TruncDay")