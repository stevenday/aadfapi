import json

from django.test import TransactionTestCase
from django.contrib.gis.geos import Point, Polygon, MultiPolygon

from ..models import Count, Ward


class APITests(TransactionTestCase):
    def setUp(self):
        self.ward_1 = Ward.objects.create(
            wd16cd='DEVON',
            objectid='12345',
            bng_e=12345,
            bng_n=12345,
            long=51,
            lat=-4.6,
            st_areasha=12345,
            st_lengths=12345,
            geom=MultiPolygon(Polygon.from_bbox((-2.8866, 50.2015, -4.6807, 51.2468)))
        )
        self.ward_2 = Ward.objects.create(
            wd16cd='EDINBURGH',
            objectid='12345',
            bng_e=12345,
            bng_n=12345,
            long=51,
            lat=-4.6,
            st_areasha=12345,
            st_lengths=12345,
            geom=MultiPolygon(Polygon.from_bbox((-3.077659, 55.890423, -3.333019, 55.991994)))
        )

        self.count_1 = Count.objects.create(
            count_point_id=6023,
            location=Point(-3, 50.5, srid=4326),
            ward=self.ward_1,
            year=2000,
            estimation_method='Manual',
            estimation_method_detail='Manual count',
            road='M5',
            road_category='TM',
            start_junction='28',
            end_junction='27',
            link_length_km=6.7,
            link_length_miles=4.16,
            pedal_cycles=0,
            motorcycles=137,
            cars_taxis=41341,
            buses_coaches=384,
            light_goods_vehicles=4851,
            two_axle_rigid_hgv=1854,
            three_axle_rigid_hgv=398,
            four_or_five_axle_rigid_hgv=173,
            three_or_four_axle_articulated_hgv=1014,
            five_axle_articulated_hgv=1935,
            six_or_more_axle_articulated_hgv=1630,
            all_hgvs=7004,
            all_motor_vehicles=53717
        )
        self.count_2 = Count.objects.create(
            count_point_id=6023,
            location=Point(-3.1, 55.9, srid=4326),
            ward=self.ward_2,
            year=2001,
            estimation_method='Manual',
            estimation_method_detail='Manual count',
            road='M5',
            road_category='TM',
            start_junction='28',
            end_junction='27',
            link_length_km=6.7,
            link_length_miles=4.16,
            pedal_cycles=0,
            motorcycles=138,
            cars_taxis=41342,
            buses_coaches=385,
            light_goods_vehicles=4852,
            two_axle_rigid_hgv=1855,
            three_axle_rigid_hgv=399,
            four_or_five_axle_rigid_hgv=174,
            three_or_four_axle_articulated_hgv=1015,
            five_axle_articulated_hgv=1936,
            six_or_more_axle_articulated_hgv=1631,
            all_hgvs=7005,
            all_motor_vehicles=53718
        )
        self.count_3 = Count.objects.create(
            count_point_id=6024,
            location=Point(-3, 50.5, srid=4326),
            ward=self.ward_1,
            year=2000,
            estimation_method='Estimated',
            estimation_method_detail='Estimated using previous years AADF',
            road='A30',
            road_category='TM',
            start_junction='M5',
            end_junction='Airport',
            link_length_km=6.7,
            link_length_miles=4.16,
            pedal_cycles=0,
            motorcycles=138,
            cars_taxis=41342,
            buses_coaches=385,
            light_goods_vehicles=4852,
            two_axle_rigid_hgv=1855,
            three_axle_rigid_hgv=399,
            four_or_five_axle_rigid_hgv=174,
            three_or_four_axle_articulated_hgv=1015,
            five_axle_articulated_hgv=1936,
            six_or_more_axle_articulated_hgv=1631,
            all_hgvs=7005,
            all_motor_vehicles=53718
        )

    def test_listing_counts(self):
        response = json.loads(self.client.get('/counts/').content)
        features = response['results']['features']
        self.assertEqual(features[0]['id'], self.count_1.id)
        self.assertEqual(features[1]['id'], self.count_3.id)
        self.assertEqual(features[2]['id'], self.count_2.id)

    def test_filtering_by_ward(self):
        url = "/counts/?ward__wd16cd=DEVON"
        response = json.loads(self.client.get(url).content)
        features = response['results']['features']
        self.assertEqual(len(features), 2)
        self.assertEqual(features[0]['id'], self.count_1.id)
        self.assertEqual(features[1]['id'], self.count_3.id)

    def test_filtering_by_year(self):
        url = "/counts/?year=2001"
        response = json.loads(self.client.get(url).content)
        features = response['results']['features']
        self.assertEqual(len(features), 1)
        self.assertEqual(features[0]['id'], self.count_2.id)

    def test_filtering_by_road(self):
        url = "/counts/?road=A30"
        response = json.loads(self.client.get(url).content)
        features = response['results']['features']
        self.assertEqual(len(features), 1)
        self.assertEqual(features[0]['id'], self.count_3.id)

    def test_getting_single_count(self):
        url = "/counts/{}/".format(self.count_1.id)
        response = json.loads(self.client.get(url).content)
        count = response['properties']
        self.assertEqual(count['count_point_id'], 6023)
        expected_location = {
            "type": "Point",
            "coordinates": [-3.0, 50.5]
        }
        self.assertEqual(response['geometry'], expected_location)
        self.assertEqual(count['ward'], self.ward_1.id)
        self.assertEqual(count['year'], 2000)
        self.assertEqual(count['estimation_method'], 'Manual')
        self.assertEqual(count['estimation_method_detail'], 'Manual count')
        self.assertEqual(count['road'], 'M5')
        self.assertEqual(count['road_category'], 'TM')
        self.assertEqual(count['start_junction'], '28')
        self.assertEqual(count['end_junction'], '27')
        self.assertEqual(count['link_length_km'], 6.7)
        self.assertEqual(count['link_length_miles'], 4.16)
        self.assertEqual(count['pedal_cycles'], 0)
        self.assertEqual(count['motorcycles'], 137)
        self.assertEqual(count['cars_taxis'], 41341)
        self.assertEqual(count['buses_coaches'], 384)
        self.assertEqual(count['light_goods_vehicles'], 4851)
        self.assertEqual(count['two_axle_rigid_hgv'], 1854)
        self.assertEqual(count['three_axle_rigid_hgv'], 398)
        self.assertEqual(count['four_or_five_axle_rigid_hgv'], 173)
        self.assertEqual(count['three_or_four_axle_articulated_hgv'], 1014)
        self.assertEqual(count['five_axle_articulated_hgv'], 1935)
        self.assertEqual(count['six_or_more_axle_articulated_hgv'], 1630)
        self.assertEqual(count['all_hgvs'], 7004)
        self.assertEqual(count['all_motor_vehicles'], 53717)
