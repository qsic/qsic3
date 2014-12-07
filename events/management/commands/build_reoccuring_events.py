from django.core.management.base import BaseCommand, CommandError
from events.utils import build_reoccuring_events


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        start_dt = CalendarWeek().start_dt
        build_reoccuring_events(start_dt, memoize=False)