from django.core.management.base import BaseCommand, CommandError
from qsic.groups.models import Group


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        for group in Group.objects.all():
            self.stdout.write('Loading {}...'.format(group), ending='')
            group.load_from_it()
            self.stdout.write('done.'.format(group))