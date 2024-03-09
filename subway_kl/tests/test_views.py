from django.urls import reverse

from api.tests.mixins import NotLoggedInAPITestCase, NotLoggedInListAPITestCaseMixin
from subway_kl.models import SubwayOutlet
from subway_kl.serializers import SubwayOutletSerializer
from subway_kl.tests.factories import SubwayOutletFactory


class SubwayOutletViewSetTestCase(
    NotLoggedInListAPITestCaseMixin, NotLoggedInAPITestCase
):
    list_url = reverse("all:subway-list")
    list_url_string = "/api/subway/"
    list_serializer_class = SubwayOutletSerializer

    def get_queryset(self):
        return SubwayOutlet.objects.all()

    def test_get_list(self):
        SubwayOutletFactory.create_batch(3)

        queryset_result = self.get_queryset()

        self.assertEqual(queryset_result.count(), 3)
        self.assertListResponseEqual(queryset_result, pagination=False)
