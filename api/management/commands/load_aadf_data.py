import csv
from contextlib import closing
import codecs

import requests

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from ...models import Count


class Command(BaseCommand):
    help = """ Imports the Devon AADF csv from
               http://api.dft.gov.uk/v2/trafficcounts/export/la/Devon.csv """

    DEFAULT_CSV = 'http://api.dft.gov.uk/v2/trafficcounts/export/la/Devon.csv'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete-existing',
            action='store_true',
            dest='delete_existing',
            default=True,
            help="Delete all existing data before loading new file"
        )

    def handle(self, *args, **options):
        if options['delete_existing']:
            self.stdout.write("Deleting all existing data")
            Count.objects.all().delete()
        log_message = "Processing CSV file from: {}"
        self.stdout.write(log_message.format(self.DEFAULT_CSV))
        with closing(requests.get(self.DEFAULT_CSV, stream=True)) as csv_file:
            self.process_csv(csv_file)

    def process_csv(self, csv_file):
        csv_iterator = codecs.iterdecode(csv_file.iter_lines(), 'utf-8')
        reader = csv.DictReader(csv_iterator)
        counts_added = 0
        for row in reader:
            Count.objects.create(
                count_point_id=int(row['CP']),
                location=Point(
                    int(row['Easting']),
                    int(row['Northing']),
                    srid=27700
                ),
                year=int(row['AADFYear']),
                estimation_method=row['Estimation_method'],
                estimation_method_detail=row['Estimation_method_detailed'],
                road=row['Road'],
                road_category=row['RoadCategory'],
                start_junction=row.get('StartJunction'),
                end_junction=row.get('EndJunction'),
                link_length_km=float(row['LinkLength_km']),
                link_length_miles=float(row['LinkLength_miles']),
                pedal_cycles=int(row['PedalCycles']),
                motorcycles=int(row['Motorcycles']),
                cars_taxis=int(row['CarsTaxis']),
                buses_coaches=int(row['BusesCoaches']),
                light_goods_vehicles=int(row['LightGoodsVehicles']),
                two_axle_rigid_hgv=int(row['V2AxleRigidHGV']),
                three_axle_rigid_hgv=int(row['V3AxleRigidHGV']),
                four_or_five_axle_rigid_hgv=int(row['V4or5AxleRigidHGV']),
                three_or_four_axle_articulated_hgv=int(row['V3or4AxleArticHGV']),
                five_axle_articulated_hgv=int(row['V5AxleArticHGV']),
                six_or_more_axle_articulated_hgv=int(row['V6orMoreAxleArticHGV']),
                all_hgvs=int(row['AllHGVs']),
                all_motor_vehicles=int(row['AllMotorVehicles'])
            )

            log_message = "Added count for CountPoint: {}, year: {}"
            self.stdout.write(log_message.format(row['CP'], row['AADFYear']))
            counts_added += 1

        self.stdout.write("=====================================")
        self.stdout.write("Finished")
        self.stdout.write("{} Counts added".format(counts_added))
