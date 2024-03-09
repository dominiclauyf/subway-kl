import json
import pprint
import tempfile
import urllib
from shutil import rmtree

from django.test import override_settings
from factory import fuzzy
from rest_framework import status
from rest_framework.fields import DateTimeField
from rest_framework.test import APIClient
from rest_framework.test import APITestCase as _APITestCase
from rest_framework.utils.encoders import JSONEncoder

from api.enums import HTTPMethod

temp_dir = tempfile.TemporaryDirectory(prefix="mediatest").name
pp = pprint.PrettyPrinter(indent=4)

FuzzyShortText = fuzzy.FuzzyText(length=8)
FuzzyText = fuzzy.FuzzyText()
FuzzyEmail = fuzzy.FuzzyText(suffix="@example.com")


class MockResponse:
    def __init__(self, data=b"", json_data={}, status_code=status.HTTP_200_OK):
        self.data = data
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    @property
    def text(self):
        return self.data.decode("utf-8")

    @property
    def content(self):
        return self.data


class SerializerTestCaseMixin:
    """
    Use it with APITestCase so that serializer class will receive request.
    """

    drf_str_datetime = DateTimeField().to_representation
    debug = False
    list_field_name = None
    many = True
    serializer_class = None

    def get_queryset(self):
        raise NotImplementedError()

    def create_data(self):
        raise NotImplementedError()

    def convert_instance_rule(self, name, instance):
        return getattr(instance, name)

    def convert_queryset_to_data(self, data, field_name, many=True):
        if many:
            result = []
            for instance in data:
                result_content = {}

                for name in field_name:
                    result_content[name] = self.convert_instance_rule(name, instance)

                result.append(result_content)

        else:
            result = {}
            for name in field_name:
                result[name] = self.convert_instance_rule(name, data)

        return result

    def test_serializer_data(self):
        many = getattr(self, "many", True)
        self.create_data()
        data = self.get_queryset()
        # Debug use
        if self.debug:
            print("serializer data")
            pp.pprint(
                self.get_serializer_data(
                    self.serializer_class,
                    data,
                    many=many,
                )
            )
            print("query data")
            pp.pprint(
                self.convert_queryset_to_data(data, self.list_field_name, many=many)
            )
        self.assertEqual(
            self.get_serializer_data(
                self.serializer_class,
                data,
                many=many,
            ),
            self.convert_queryset_to_data(data, self.list_field_name, many=many),
        )


class CustomAPIClient(APIClient):
    # To make convert file url work
    def credentials(self, user, **kwargs):
        """
        Sets headers that will be used on every outgoing request.
        Set user in request.
        """
        self._credentials = kwargs
        self.user = user

    def build_absolute_uri(self, url):
        return f"http://testserver{url}"


@override_settings(MEDIA_ROOT=temp_dir)
class NotLoggedInAPITestCase(_APITestCase):
    client_class = CustomAPIClient

    VALIDATION_REQUIRED = "This field is required."
    VALIDATION_NOT_BLANK = "This field may not be blank."
    VALIDATION_NOT_NULL = "This field may not be null."
    VALIDATION_NOT_FOUND = 'Invalid pk "{}" - object does not exist.'

    @classmethod
    def tearDownClass(cls):
        super(NotLoggedInAPITestCase, cls).tearDownClass()
        rmtree(temp_dir, ignore_errors=True)

    def assertResponseStatusCode(
        self,
        url,
        method=HTTPMethod.GET,
        status_code=status.HTTP_200_OK,
        debug=False,
        **kwargs,
    ):
        # Not using generic because there is some setup around it when data passing in.
        if method == HTTPMethod.GET:
            response = self.client.get(url, **kwargs)
        elif method == HTTPMethod.POST:
            response = self.client.post(url, **kwargs)
        elif method == HTTPMethod.PUT:
            response = self.client.put(url, **kwargs)
        elif method == HTTPMethod.PATCH:
            response = self.client.patch(url, **kwargs)
        elif method == HTTPMethod.DELETE:
            response = self.client.delete(url, **kwargs)
        elif method == HTTPMethod.HEAD:
            response = self.client.head(url, **kwargs)
        elif method == HTTPMethod.OPTIONS:
            response = self.client.options(url, **kwargs)
        else:
            response = self.client.trace(url, **kwargs)

        if debug:
            print(response.content)

        self.assertEqual(response.status_code, status_code)
        return response

    def assertResponseEqual(
        self, response, serializer_class, data, many=False, debug=False
    ):
        if debug:
            print("response data", json.loads(response.content))
            print(
                "serializer data",
                json.loads(
                    json.dumps(
                        serializer_class(
                            data, many=many, context={"request": self.client}
                        ).data,
                        cls=JSONEncoder,
                    )
                ),
            )

        self.assertEqual(
            json.loads(response.content),
            json.loads(
                json.dumps(
                    self.get_serializer_data(
                        serializer_class,
                        data,
                        many=many,
                    ),
                    cls=JSONEncoder,
                )
            ),
        )

    def get_serializer_data(self, serializer_class, data, many=False):
        """
        Prefix context into serializer class.
        """
        return serializer_class(data, many=many, context={"request": self.client}).data

    def assertBadRequestResponse(
        self, url, method, data, error_field=None, error_msg=None, debug=False
    ):
        """
        For POST, PUT, PATCH to test Validation Error
        """
        assert method in [HTTPMethod.POST, HTTPMethod.PUT, HTTPMethod.PATCH]

        response = self.assertResponseStatusCode(
            url, method, status_code=status.HTTP_400_BAD_REQUEST, data=data
        )

        if error_field is not None:
            data = response.json()
            # Debug error message
            if debug:
                print(data)
            error = data.get(error_field)
            self.assertIsNotNone(error)
            if error_msg is not None:
                if isinstance(error_msg, list):
                    for each_error_msg in error_msg:
                        self.assertIn(each_error_msg, error)
                else:
                    self.assertIn(error_msg, error)

    def run_validation(self, test_conditions, funcs, debug=False):
        """
        Params:
            field (str): Field Name
            test_conditions (list):
                {
                    field:(input, error_msg),
                    ...
                }
            func (list(function)):
                [
                    run_post_bad_response, run_patch_bad_response,
                    run_put_bad_response
                ]
        """

        for func in funcs:
            for field, test_condition in test_conditions.items():
                test_condition = [
                    item if len(item) == 3 else (item[0], field, item[1])
                    for item in test_condition
                ]

                for input_data, error_field, error_msg in test_condition:
                    if (
                        hasattr(self, "run_patch_bad_response")
                        and func == self.run_patch_bad_response
                    ):
                        if input_data is None:
                            # Patch no need to test required field
                            continue
                        # Patch is partial update so no need all the data
                        data = {field: input_data}
                    else:
                        assert self.data is not None

                        data = {**self.data}
                        if input_data is None:
                            try:
                                data.pop(field)
                            except KeyError:
                                pass
                        else:
                            data[field] = input_data

                    # Debug use
                    # print(func.__name__, field, input_data, error_msg)
                    func(
                        data=data,
                        error_field=error_field,
                        error_msg=error_msg,
                        debug=debug,
                    )

    def run_request_instance_not_found(self, urls, method):
        for url in urls:
            self.assertResponseStatusCode(
                url, method=method, status_code=status.HTTP_404_NOT_FOUND
            )


class NotLoggedInListAPITestCaseMixin:
    list_url = None
    list_url_string = None
    list_serializer_class = None

    def test_list_url(self):
        assert self.list_url is not None
        assert self.list_url_string is not None

        self.assertEqual(self.list_url_string, self.list_url)

    def make_get_request(
        self, url, filters, status_code=status.HTTP_200_OK, debug=False
    ):
        if filters is not None:
            params = urllib.parse.urlencode(filters)
            url = f"{url}?{params}"

        return self.assertResponseStatusCode(url, debug=debug, status_code=status_code)

    def assertListResponseEqual(
        self,
        queryset,
        serializer_class=None,
        filters=None,
        pagination=True,
        debug=False,
    ):
        assert self.list_url is not None

        if serializer_class is None:
            assert self.list_serializer_class is not None

            serializer_class = self.list_serializer_class

        response = self.make_get_request(self.list_url, filters)

        if pagination:
            data = json.loads(response.content)
            if debug:
                print("response_data", data["results"])
                print(
                    "query_data",
                    self.get_serializer_data(
                        serializer_class,
                        queryset,
                        many=True,
                    ),
                )
            self.assertEqual(
                data["results"],
                self.get_serializer_data(
                    serializer_class,
                    queryset,
                    many=True,
                ),
            )
        else:
            self.assertResponseEqual(
                response, serializer_class, queryset, many=True, debug=debug
            )

    def assertListBadRequestResponse(self, filters, debug=False):
        assert self.list_url is not None

        self.make_get_request(
            self.list_url, filters, status_code=status.HTTP_400_BAD_REQUEST, debug=debug
        )


class ListAPITestCaseMixin(NotLoggedInListAPITestCaseMixin):
    """
    For:
        APIViewSet list method

    Do note that when using this mixin need to work with NotLoggedInAPITestCase
    """

    list_url = None
    list_url_string = None
    list_serializer_class = None

    def test_get_list_when_not_authenticated(self):
        assert self.list_url is not None

        self.assertResponseNotAuthenticated(self.list_url, HTTPMethod.GET)


class NotLoggedInGetAPITestCaseMixin:
    get_url = None
    get_url_string = None
    get_serializer_class = None
    get_instance = None
    get_not_found_url = None

    def test_get_url(self):
        assert self.get_url is not None
        assert self.get_url_string is not None

        self.assertEqual(self.get_url_string, self.get_url)

    def test_get(self):
        assert self.get_url is not None
        assert self.get_serializer_class is not None
        assert self.get_instance is not None

        response = self.assertResponseStatusCode(
            self.get_url, status_code=status.HTTP_200_OK
        )
        self.assertResponseEqual(response, self.get_serializer_class, self.get_instance)

    def test_get_not_found(self):
        assert self.get_not_found_url is not None

        self.run_request_instance_not_found(self.get_not_found_url, HTTPMethod.GET)


class GetAPITestCaseMixin(NotLoggedInGetAPITestCaseMixin):
    """
    For:
        APIView get method

    Do note that when using this mixin need to work with APITestCase
    """

    get_url = None
    get_url_string = None
    get_serializer_class = None
    get_instance = None
    get_not_found_url = None

    def test_get_when_not_authenticated(self):
        assert self.get_url is not None

        self.assertResponseNotAuthenticated(self.get_url, HTTPMethod.GET)
