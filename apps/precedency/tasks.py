from django.db import transaction

from celery.app import shared_task

from apps.precedency.models import Precedence, UsersPrecedency
from apps.users.factories import UserFactory


@shared_task
@transaction.atomic
def save_sample_data_line_task(data: dict):
    """Celery shared task for saving sample data lines
    in transaction atomic way.
    """
    first_name, last_name = data["name"].split()
    user = UserFactory(first_name=first_name, last_name=last_name)

    for precedent in data["precedents"]:
        precedence = Precedence.objects.get(title=precedent)

        precedent_obj = data["precedents"][precedent]
        attitude = 2 if precedent_obj["attitude"] == "positive" else 1

        UsersPrecedency.objects.create(
            user=user,
            precedence=precedence,
            attitude=attitude,
            importance=precedent_obj["importance"]
        )
