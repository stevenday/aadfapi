import os
from io import BytesIO
from zipfile import ZipFile

import requests

from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping
from django.conf import settings

from ...models import Ward


class Command(BaseCommand):
    help = """ Imports UK ward boundaries from included shapefile """

    DEFAULT_URL = "https://geoportal.statistics.gov.uk/datasets/afcc88affe5f450e9c03970b237a7999_0.zip"
    DATA_DIR = os.path.join(settings.BASE_DIR, 'data')
    SHAPEFILE = 'Wards_December_2016_Full_Clipped_Boundaries_in_Great_Britain.shp'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete-existing',
            action='store_true',
            dest='delete_existing',
            default=True,
            help="Delete all existing data before loading new file"
        )

        parser.add_argument(
            '--download-data',
            action='store_true',
            dest='download_data',
            default=True,
            help="Download data from {}".format(self.DEFAULT_URL)
        )

    def handle(self, *args, **options):
        if options['delete_existing']:
            self.stdout.write("Deleting all existing data")
            Ward.objects.all().delete()

        if options['download_data']:
            self.stdout.write("Downloading boundaries shapefile")
            self.download_and_extract_boundaries()

        self.stdout.write("Processing boundaries shapefile")
        self.process_shapefile()

        ward_count = Ward.objects.all().count()
        self.stdout.write("=====================================")
        self.stdout.write("Finished")
        self.stdout.write("{} Wards added".format(ward_count))

    def process_shapefile(self):
        shapefile = os.path.abspath(os.path.join(self.DATA_DIR, self.SHAPEFILE))
        layer_mapping = LayerMapping(
            Ward,
            shapefile,
            Ward.LAYER_MAPPING,
            transform=False,
            encoding='utf-8'
        )
        layer_mapping.save(strict=True, verbose=False)

    def download_and_extract_boundaries(self):
        # geoportal.statistics.gov.uk seems to present an SSL cert for
        # opendata.argis.com, so I'm skipping certificate verification as a
        # quick way to get this working. Presumably it's an SNI issue.
        response = requests.get(self.DEFAULT_URL, verify=False)
        zip_file = ZipFile(BytesIO(response.content))
        zip_file.extractall(self.DATA_DIR)
