from subway_kl.geocoding import get_coordinates
from subway_kl.models import SubwayOutlet
from subway_kl.typings import OutletData


class SubwayOutletHandler:
    @staticmethod
    def bulk_update_or_create(datas: list[OutletData]):
        model_datas = [
            SubwayOutlet(
                name=i["name"],
                address=i["address"],
                operating_time=i["operation_time"],
                long=i["long"],
                lat=i["lat"],
            )
            for i in datas
        ]

        SubwayOutlet.objects.bulk_update_or_create(
            model_datas,
            ["address", "operating_time", "long", "lat"],
            match_field="name",
        )

    @staticmethod
    def retrieve_geographical_data():
        subway_outlets = SubwayOutlet.objects.all()
        for subway_outlet in subway_outlets:
            coordinates = get_coordinates(subway_outlet.address)
            if coordinates is not None:
                subway_outlet.retrieve_lat = coordinates[0]
                subway_outlet.retrieve_long = coordinates[1]

        SubwayOutlet.objects.bulk_update(
            subway_outlets, ["retrieve_lat", "retrieve_long"]
        )
