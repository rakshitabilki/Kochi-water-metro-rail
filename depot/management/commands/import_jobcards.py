# depot/management/commands/import_jobcards.py
from django.core.management.base import BaseCommand
import csv
from depot.models import Trainset, JobCard

class Command(BaseCommand):
    help = "Import jobcards CSV exported from Maximo. Expected columns: trainset,id,status,desc"

    def add_arguments(self, parser):
        parser.add_argument('csvfile', type=str, help="Path to CSV file")

    def handle(self, *args, **options):
        path = options['csvfile']
        created = 0
        updated = 0
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ts_number = row.get('trainset') or row.get('Trainset') or row.get('train')
                if not ts_number:
                    self.stdout.write(self.style.WARNING(f"Skipping row without trainset: {row}"))
                    continue
                ts, _ = Trainset.objects.get_or_create(number=ts_number)
                obj, was_created = JobCard.objects.update_or_create(
                    maximo_id=row.get('id') or '',
                    defaults={
                        'trainset': ts,
                        'status': row.get('status', 'open').lower(),
                        'description': row.get('desc', row.get('description', '')),
                    }
                )
                if was_created:
                    created += 1
                else:
                    updated += 1
        self.stdout.write(self.style.SUCCESS(f"Import complete. Created: {created}, Updated: {updated}"))
