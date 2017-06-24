"""api URL Configuration"""
from django.conf.urls import url, include

from rest_framework import routers, serializers, viewsets

from .models import Count


# Serializers define the API representation.
class CountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Count
        fields = '__all__'


# ViewSets define the view behavior.
class CountViewSet(viewsets.ModelViewSet):
    queryset = Count.objects.all()
    serializer_class = CountSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'counts', CountViewSet)


urlpatterns = [
    url(r'^', include(router.urls))
]
