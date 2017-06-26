from io import StringIO

from django.test import TestCase
from django.core.management import call_command
from django.contrib.gis.geos import Point, Polygon, MultiPolygon
from django.db.models import Sum

from ..models import Count, Ward


class LoadAADFDataTests(TestCase):

    def _call_command(self):
        opts = {}
        call_command('load_aadf_data', stdout=StringIO(), **opts)

    def test_loading_data(self):
        self._call_command()
        self.assertEqual(Count.objects.count(), 3682)

        first_row = Count.objects.get(year=2000, count_point_id=6023)
        self.assertEqual(first_row.estimation_method, "Counted")
        self.assertEqual(first_row.estimation_method_detail, "Manual count")
        self.assertEqual(first_row.road, "M5")
        self.assertEqual(first_row.road_category, "TM")
        # Storing this in the db converts it to WGS84, so we need to convert
        # our expectations too. There's some precision loss here, I think
        # because of the varying numbers of decimal places used in postgres vs
        # python for floating points, hence limiting the comparison to 5 d.p.
        expected_point = Point(303700, 112172, srid=27700)
        expected_point.transform(4326)
        self.assertTrue(first_row.location.equals_exact(expected_point, 5))
        self.assertEqual(first_row.start_junction, "28")
        self.assertEqual(first_row.end_junction, "27")
        self.assertEqual(first_row.link_length_km, 6.7)
        self.assertEqual(first_row.link_length_miles, 4.16)
        self.assertEqual(first_row.pedal_cycles, 0)
        self.assertEqual(first_row.motorcycles, 137)
        self.assertEqual(first_row.cars_taxis, 41341)
        self.assertEqual(first_row.buses_coaches, 384)
        self.assertEqual(first_row.light_goods_vehicles, 4851)
        self.assertEqual(first_row.two_axle_rigid_hgv, 1854)
        self.assertEqual(first_row.three_axle_rigid_hgv, 398)
        self.assertEqual(first_row.four_or_five_axle_rigid_hgv, 173)
        self.assertEqual(first_row.three_or_four_axle_articulated_hgv, 1014)
        self.assertEqual(first_row.five_axle_articulated_hgv, 1935)
        self.assertEqual(first_row.six_or_more_axle_articulated_hgv, 1630)
        self.assertEqual(first_row.all_hgvs, 7004)
        self.assertEqual(first_row.all_motor_vehicles, 53717)

        # I calculated this checksum using Excel, summing the AllMotorVehicles
        # column
        expected_total_vehicles = 55662462
        actual_total_vehicles = Count.objects.aggregate(
            Sum('all_motor_vehicles')
        )['all_motor_vehicles__sum']
        self.assertEqual(actual_total_vehicles, expected_total_vehicles)

    def test_assigning_wards(self):
        # Create a geometry that spans the whole of Devon so that every count
        # ends up in it
        Ward.objects.create(
            wd16nm='DEVON',
            objectid='12345',
            bng_e=12345,
            bng_n=12345,
            long=51,
            lat=-4.6,
            st_areasha=12345,
            st_lengths=12345,
            geom=MultiPolygon(Polygon.from_bbox((-2.8866, 50.2015, -4.6807, 51.2468)))
        )
        self._call_command()
        first_row = Count.objects.get(year=2000, count_point_id=6023)
        self.assertEqual(first_row.ward.wd16nm, 'DEVON')


class LoadWardDataTests(TestCase):

    def _call_command(self):
        opts = {}
        call_command('load_wards', stdout=StringIO(), **opts)

    def test_loading_data(self):
        self._call_command()
        self.assertEqual(Ward.objects.count(), 8668)
