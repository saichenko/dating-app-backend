import json
import typing

from django.core.management import BaseCommand

from celery import group

from apps.precedency.models import Precedence
from apps.precedency.tasks import save_sample_data_line_task


def create_precedency(lines: typing.Iterable):
    """Collect all precedency then save them to DB."""
    precedency = {key for line in lines for key in line["precedents"]}
    Precedence.objects.bulk_create(
        [Precedence(title=title) for title in precedency],
        ignore_conflicts=True  # Used to avoid duplication errors.
    )


class Command(BaseCommand):
    """Fill sample data to DB.
    Make sure your Celery server is up before run.

    Props:
    FILE_DIR (str): Path to the .jsonl file with sample data.
    """

    help: str = "Load users and their precedency to DB"
    FILE_PATH: str = "apps/precedency/data/participants.jsonl"

    def handle(self, *args, **options):
        """Create precedency and run celery tasks for each record."""
        with open(self.FILE_PATH, "r") as file:
            lines = list(map(json.loads, file.read().splitlines()))
        create_precedency(lines)
        tasks = [save_sample_data_line_task.s(line) for line in lines]
        run_group = group(tasks)
        run_group()

        self.stdout.write(self.style.SUCCESS("Make sure Celery is up"))
