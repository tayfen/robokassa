import pytest

from robokassa import Robokassa, HashAlgorithm
from robokassa.exceptions import RobokassaInterfaceError
from robokassa.types import RobokassaParams

from robokassa.asyncio import Robokassa as AsyncRobokassa


pytest_plugins = ("pytest_asyncio",)


class TestRobokassaClient:
    robokassa = Robokassa(
        merchant_login="test_login",
        password1="password",
        password2="password",
        algorithm=HashAlgorithm.sha384,
    )

    result_url = "https://example.com"

    def test_client(self) -> None:
        assert self.robokassa._merchant_login == "test_login"

    def test_link_generator(self) -> None:
        link = self.robokassa.create_link_to_payment_page_by_script(out_sum=1, inv_id=0)
        assert link

    def test_robokassa_params(self) -> None:
        dict_params = RobokassaParams(
            merchant_login="test_login",
            out_sum=1,
            description="Hello, World!",
            additional_params={"shp_id": 1234, "shp_data": "My data"},
        )
        assert isinstance(dict_params.as_dict(), dict)

    def test_robokassa_currency(self) -> None:
        result = self.robokassa.get_currencies(language="en")

        assert result
        assert isinstance(result, dict)


class TestRobokassaAsyncioClient:
    robokassa = AsyncRobokassa(
        is_test=True,
        merchant_login="test_login",
        password1="<PASSWORD>",
        password2="<PASSWORD>",
        algorithm=HashAlgorithm.md5,
    )

    @pytest.mark.asyncio
    async def test_link(self) -> None:
        try:
            link = self.robokassa.create_link_to_payment_page_by_script(
                out_sum=1,
                inv_id=0,
            )
            assert link

            link1 = await self.robokassa.create_link_to_payment_page_by_invoice_id(
                inv_id=0,
                description="Hello world!",
                out_sum=1000,
            )
            assert link1

        except RobokassaInterfaceError as ex:
            assert "26" in str(ex)

    @pytest.mark.asyncio
    async def test_currency(self) -> None:
        data = await self.robokassa.get_currencies(language="en")

        assert data
        assert isinstance(data, dict)
