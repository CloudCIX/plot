# stdlib
from datetime import datetime, timedelta
from typing import List
# lib
from django.core.management.base import BaseCommand
# local
from plot.models import Reading, Source


def get_sources() -> List[Source]:
    objs = Source.objects.all()
    return objs


class Command(BaseCommand):
    """
    For Sources, delete Readings whicj are older than the retention policy of the Source
    """
    help = 'For Sources, delete Readings older than the retention policy of its Source'

    def handle(self, *args, **kwargs):
        """
        Run the command by:
            - Fetching all Sources
            - Iterating through these Sources, delete Readings older than the retention
        """
        self.today = datetime.now().date()

        sources = get_sources()
        for source in sources:
            self.delete_readings(source)

        self.stdout.write(f'{self.today}: Completed deleting Readings older than its Source Retention Policy')

    def delete_readings(self, source: Source):
        policy = self.today - timedelta(days=source.retention)
        Reading.objects.filter(datetime_taken__lt=policy).update(deleted=datetime.now())
        return None
