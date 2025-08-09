from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from counter.models import Counter, CounterEntry, CounterSplitType

User = get_user_model()


class CounterSecurityTests(APITestCase):
    def setUp(self):
        # Kullanıcı 1
        self.user1 = User.objects.create_user(
            email="user1@example.com",
            password="pass1234"
        )
        # Kullanıcı 2
        self.user2 = User.objects.create_user(
            email="user2@example.com",
            password="pass5678"
        )

        # User1'in counter'ı
        self.counter_user1 = Counter.objects.create(
            user=self.user1,
            name="User1 Counter",
            unit="steps",
            split_type=CounterSplitType.DAILY
        )
        self.entry_user1 = CounterEntry.objects.create(
            counter=self.counter_user1,
            value=10,
            timestamp=timezone.now()
        )

        # Endpoint URL'leri
        self.counter_list_url = reverse("api:counter:counter-list-create")
        self.counter_detail_url = reverse("api:counter:counter-crud", args=[self.counter_user1.id])
        self.grouped_entry_url = reverse("api:counter:counter-grouped-entry-crud", args=[self.counter_user1.id])
        self.delete_all_entries_url = reverse("api:counter:counter-remove-all-entries", args=[self.counter_user1.id])
        self.delete_by_index_url = reverse(
            "api:counter:counter-remove-entry-range-from-index",
            args=[self.counter_user1.id, 0]
        )

    def test_user_cannot_access_other_users_counter_detail(self):
        self.client.login(email="user2@example.com", password="pass5678")
        resp = self.client.get(self.counter_detail_url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_update_other_users_counter(self):
        self.client.login(email="user2@example.com", password="pass5678")
        resp = self.client.patch(self.counter_detail_url, {"name": "Hacked"})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_delete_other_users_counter(self):
        self.client.login(email="user2@example.com", password="pass5678")
        resp = self.client.delete(self.counter_detail_url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Counter.objects.filter(id=self.counter_user1.id).exists())

    def test_user_cannot_access_other_users_grouped_entries(self):
        self.client.login(email="user2@example.com", password="pass5678")
        resp = self.client.get(self.grouped_entry_url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_delete_other_users_entries_by_index(self):
        self.client.login(email="user2@example.com", password="pass5678")
        resp = self.client.delete(self.delete_by_index_url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(CounterEntry.objects.filter(counter=self.counter_user1).count(), 1)

    def test_user_cannot_delete_all_other_users_entries(self):
        self.client.login(email="user2@example.com", password="pass5678")
        resp = self.client.delete(self.delete_all_entries_url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(CounterEntry.objects.filter(counter=self.counter_user1).count(), 1)

    def test_user_cannot_tick_other_users_counter(self):
        self.client.login(email="user2@example.com", password="pass5678")
        tick_url = reverse("api:counter:counter-tick-create")
        resp = self.client.post(tick_url, {"counter": self.counter_user1.id, "value": 5})
        self.assertIn(resp.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND])
        self.assertEqual(CounterEntry.objects.filter(counter=self.counter_user1).count(), 1)
