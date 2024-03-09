from rest_framework import viewsets

from subway_kl.filters import SubwayOutletListFileter
from subway_kl.models import SubwayOutlet
from subway_kl.serializers import SubwayOutletSerializer


class SubwayOutletViewSet(viewsets.ReadOnlyModelViewSet):
    filterset_class = SubwayOutletListFileter
    serializer_class = SubwayOutletSerializer
    queryset = SubwayOutlet.objects.all()
