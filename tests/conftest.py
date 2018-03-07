import pytest


@pytest.fixture(scope="session")
def api_tq():
    from fixturetypes import ApiFixture
    return ApiFixture(host="tq-api")


# @pytest.fixture(scope="session")
# def mongo():
#     from fixturetypes import MongoFixture
#     return MongoFixture()
