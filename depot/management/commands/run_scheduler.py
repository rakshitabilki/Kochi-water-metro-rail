from django.core.management.base import BaseCommand
from depot.scheduler import run_scheduler_all

class Command(BaseCommand):
    help = "Run the depot scheduler and persist results."

    def handle(self, *args, **options):
        ranking = run_scheduler_all()
        self.stdout.write(self.style.SUCCESS(
            f"Scheduler executed. {len(ranking)} trains evaluated."
        ))
