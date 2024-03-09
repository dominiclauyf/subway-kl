from rest_framework import serializers

from subway_kl.models import SubwayOutlet


class SubwayOutletSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubwayOutlet
        fields = "__all__"
