# -*- coding: utf-8 -*-


import requests
import re
import json
from django.core.management.base import BaseCommand, CommandError
from autonotes.vehicles.models import Maker, Model
from .data import makers
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Fetch makers and their models data from auto.ru.'
    makers = []

    def __load_makers(self):
        for maker in makers.split('\n'):
            self.makers.append(maker)

    def handle(self, *args, **options):
        self.__load_makers()
        sess = requests.session()

        for maker in self.makers:
            resp = sess.get(f'https://auto.ru/moskva/cars/{maker}/all/')
            if resp.status_code == 200:
                m = re.search(
                    ' type="application/json" id="initial-state">(.+?)</script>',
                    resp.text,
                    re.IGNORECASE + re.DOTALL
                )

                if m:
                    j = json.loads(m.group(1))

                    try:
                        data = j['breadcrumbsPublicApi']['data'][0]

                        mark_name = data['mark']['name']
                        models = data['entities']

                        self.stdout.write(f'{mark_name}: found {len(models)} models.')

                        mkr, _ = Maker.objects.get_or_create(title__iexact=mark_name)

                        for model in models:
                            mdl = Model(
                                maker=mkr,
                                slug=model['id'],
                                title=model['name'],
                            )

                            mdl.save()

                    except IntegrityError:
                        self.stdout.write(f'IntegrityError for {mark_name} {model["id"]}')

                    except IndexError:
                        self.stdout.write(f'{maker} got IndexError exception.')

                    except Maker.DoesNotExist:
                        self.stdout.write(f'Cant find {maker} ({mark_name}) in database.')

            else:
                self.stdout.write(f'Maker {maker} is not found on auto.ru.')
