from slugify import slugify
from django.core.management.base import BaseCommand, CommandError
from autonotes.vehicles.models import Maker, Model
from .data import makers
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Populate models from datafile for maker, shown in arg.'

    def add_arguments(self, parser):
        parser.add_argument('maker_title', type=str)
        parser.add_argument('data_file', type=str)

    def handle(self, *args, **options):
        try:
            maker_title = options['maker_title']
            data_file = open(options['data_file'], 'r', encoding='UTF-8')

            maker = Maker.objects.get(title__iexact=maker_title)

            for title in data_file.readlines():
                model = Model(
                    maker=maker,
                    title=title,
                    slug=slugify(title),
                )

                model.save()

        except Maker.DoesNotExist:
            self.stdout.write(f'Cant find maker with id {maker_title} in database.')

        except IntegrityError:
            self.stdout.write(f'IntegrityError for {maker.title} {title}')

        self.stdout.write('Done.')
