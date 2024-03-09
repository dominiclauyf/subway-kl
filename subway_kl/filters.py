from django_filters import rest_framework as filters

from subway_kl.models import SubwayOutlet


class SubwayOutletListFileter(filters.FilterSet):
    search = filters.CharFilter(method="filter_search")

    class Meta:
        model = SubwayOutlet
        fields = [
            "search",
            "name",
        ]

    def filter_search(self, queryset, name, value):
        return queryset
