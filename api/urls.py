"""api URL Configuration"""
from django.conf.urls import url, include

from rest_framework import routers, viewsets
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Count, Ward


# Serializers define the API representation.
class CountSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Count
        fields = '__all__'
        geo_field = 'location'


class WardSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Ward
        fields = '__all__'
        geo_field = 'geom'


# ViewSets define the view behavior.
class CountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given AADF count.

    list:
    Return a list of all the existing counts.
    """
    queryset = Count.objects.all()
    serializer_class = CountSerializer
    filter_fields = ('year', 'count_point_id', 'road', 'ward__wd16cd')


class WardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given Ward.

    list:
    Return a list of all the existing wards.
    """
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    filter_fields = ('wd16cd', 'lad16cd')


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'counts', CountViewSet)
router.register(r'wards', WardViewSet)


urlpatterns = [
    url(r'^', include(router.urls))
]
