import factory
from factory import fuzzy

from subway_kl.models import SubwayOutlet


class SubwayOutletFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubwayOutlet

    name = factory.Sequence(lambda n: "Test SubwayOutlet {}".format(n))
    address = fuzzy.FuzzyText()
    operating_time = fuzzy.FuzzyText()
    long = fuzzy.FuzzyDecimal(low=0)
    lat = fuzzy.FuzzyDecimal(low=0)
    retrieve_long = fuzzy.FuzzyDecimal(low=0)
    retrieve_lat = fuzzy.FuzzyDecimal(low=0)
