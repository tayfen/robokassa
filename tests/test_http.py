import pytest

from robokassa import HashAlgorithm
from robokassa.asyncio.connection import AsyncHttpConnection
from robokassa.connection import HttpConnection, Requests
from robokassa.exceptions import RobokassaInterfaceError
from robokassa.hash import Hash
from robokassa.payment import PaymentRequests
from robokassa.types import RobokassaParams, Signature

pytest_plugins = ("pytest_asyncio",)


class TestHttpRequests:
    def test_http_request(self):
        conn = HttpConnection()

        with conn as connection:
            request = connection.get(
                "https://httpbin.org/anything",
            )
            assert request.status_code == 200

        with conn as connection:
            request = connection.get("https://example.com")
            assert request.status_code == 200

    @pytest.mark.asyncio
    async def test_async_http_request(self):
        conn = AsyncHttpConnection()

        async with conn as connection:
            request = await connection.get(
                "https://httpbin.org/anything",
            )
            assert request.status_code == 200

        async with conn as connection:
            request = await connection.get("https://google.com/hello_world1234")

            assert request.status_code == 404


def test_sync_http_link_generation():
    _requests = Requests().connection

    requests = PaymentRequests(_requests)
    robo_data = {
        "merchant_login": "test_login",
        "out_sum": 1,
        "inv_id": 0,
        "description": "Hello WORLD",
        "is_test": True,
        "culture": "ru",
    }
    signature = Signature(
        **{
            "merchant_login": "test_login",
            "out_sum": 1,
            "inv_id": 0,
        },
        password="<PASSWORD>",
        hash_=Hash(HashAlgorithm.md5),
    )
    try:
        link = requests.create_url_to_payment_page(
            RobokassaParams(**robo_data, signature_value=signature.value)
        )
        assert link
    except RobokassaInterfaceError as ex:
        assert "26" in str(ex)
