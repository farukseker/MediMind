from django.core.management.base import BaseCommand, CommandError
from medication_management.models import MedicationAutoCompilationModel
import json


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('source_file', type=str)

    @staticmethod
    def bulk_update_medications(new_medications):
        existing_names = set(MedicationAutoCompilationModel.objects.values_list('name', flat=True))
        new_entries = [med for med in new_medications if med['name'] not in existing_names]

        if new_entries:
            medication_objects = [MedicationAutoCompilationModel(**med) for med in new_entries]
            MedicationAutoCompilationModel.objects.bulk_create(medication_objects)

    def handle(self, *args, **options):
        source_file = options.get('source_file')
        with open(source_file, 'r', encoding='utf-8') as data_file:
            data = json.loads(data_file.read())
        data_set = [
            {
                "name": m.get('medicine_name'),
                "dosage": m.get('medicine_measurement') if m.get('medicine_measurement', None) else 'Unknown'}
            for m in data
        ]
        self.bulk_update_medications(data_set)
