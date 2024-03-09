from django.http import HttpResponse

from subway_kl.handlers import SubwayOutletHandler
from subway_kl.typings import OutletData

from .scraping import scrape_subway_kl_data


def index(request):
    return HttpResponse("hello")


def scrape_and_update_subway_kl_data(request):
    subway_kl_data: list[OutletData] = scrape_subway_kl_data()

    SubwayOutletHandler.bulk_update_or_create(subway_kl_data)

    return HttpResponse("Update complete")


def retrieve_subway_kl_geo_coord(request):
    SubwayOutletHandler.retrieve_geographical_data()

    return HttpResponse("Update complete")
