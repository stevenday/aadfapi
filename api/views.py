# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import serializers
from django.http import JsonResponse
from django.views.generic import ListView

from .models import Count


class CountListView(ListView):
    model = Count
    context_object_name = 'counts'

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = serializers.serialize("json", queryset)
        return JsonResponse(data, status=200, safe=False)
