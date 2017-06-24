"""api URL Configuration"""
from django.conf.urls import url, include

from rest_framework import routers, viewsets
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Count


# Serializers define the API representation.
class CountSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Count
        fields = '__all__'
        geo_field = 'location'


# ViewSets define the view behavior.
class CountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Count.objects.all()
    serializer_class = CountSerializer
    filter_fields = ('year', 'count_point_id', 'road')


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'counts', CountViewSet)


urlpatterns = [
    url(r'^', include(router.urls))
]
