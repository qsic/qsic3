from django.core.management.base import BaseCommand, CommandError
from performers.models import Performer


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        for performer in Performer.objects.all():
            self.stdout.write('Loading {}...'.format(performer), ending='')
            performer.load_from_it()
            self.stdout.write('done.'.format(performer))