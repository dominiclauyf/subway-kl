from django.db.models import Q
from django_filters import rest_framework as filters

from subway_kl.models import SubwayOutlet


class SubwayOutletListFileter(filters.FilterSet):
    search = filters.CharFilter(method="filter_search")

    class Meta:
        model = SubwayOutlet
        fields = [
            "search",
        ]

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
            | Q(address__icontains=value)
            | Q(operating_time__icontains=value)
        )
