# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.gis.db import models as geomodels


class Count(models.Model):
    """ A particular year's AADF count at a particular Count Point """
    ESTIMATION_METHOD_CHOICES = (
        ('Counted', 'Counted'),
        ('Estimated', 'Estimated'),
    )
    ROAD_CATEGORY_CHOICES = (
        ("PM", "M or Class A Principal Motorway"),
        ("PR", "Class A Principal road in Rural area"),
        ("PU", "Class A Principal road in Urban area"),
        ("TM", "M or Class A Trunk Motorway"),
        ("TR", "Class A Trunk road in Rural area"),
        ("TU", "Class A Trunk road in Urban area"),
        ("BR", "Class B road in Rural area"),
        ("BU", "Class B road in Urban area"),
        ("CR", "Class C road in Rural area"),
        ("CU", "Class C road in Urban area"),
        ("UR", "Class U road in Rural area"),
        ("UU", "Class U road in Urban area "),
    )
    count_point_id = models.IntegerField(db_index=True)
    location = geomodels.PointField()
    year = models.PositiveIntegerField(db_index=True)
    estimation_method = models.CharField(
        max_length=9,
        choices=ESTIMATION_METHOD_CHOICES,
        db_index=True
    )
    estimation_method_detail = models.TextField()
    road = models.TextField(db_index=True)
    road_category = models.CharField(
        max_length=2,
        choices=ROAD_CATEGORY_CHOICES
    )
    start_junction = models.TextField(blank=True)
    end_junction = models.TextField(blank=True)
    link_length_km = models.FloatField()
    link_length_miles = models.FloatField()

    pedal_cycles = models.PositiveIntegerField()
    motorcycles = models.PositiveIntegerField()
    cars_taxis = models.PositiveIntegerField()
    buses_coaches = models.PositiveIntegerField()
    light_goods_vehicles = models.PositiveIntegerField()
    two_axle_rigid_hgv = models.PositiveIntegerField()
    three_axle_rigid_hgv = models.PositiveIntegerField()
    four_or_five_axle_rigid_hgv = models.PositiveIntegerField()
    three_or_four_axle_articulated_hgv = models.PositiveIntegerField()
    five_axle_articulated_hgv = models.PositiveIntegerField()
    six_or_more_axle_articulated_hgv = models.PositiveIntegerField()
    all_hgvs = models.PositiveIntegerField()
    all_motor_vehicles = models.PositiveIntegerField()

    # Timestamps
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['year', 'count_point_id']
