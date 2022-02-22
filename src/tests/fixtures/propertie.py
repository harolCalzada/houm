import pytest
from apps.propertie.models import Propertie
from ..factories.propertie import propertie_factory


@pytest.fixture
def propertie_a(db) -> Propertie:
    return propertie_factory(
        name='propertie_a',
        description='propertie_a',
        location_latitude=-11.942575733453172,
        location_longitude=-77.04949454548695,
        price=1000000,
    )


@pytest.fixture
def propertie_b(db) -> Propertie:
    return propertie_factory(
        name='propertie_b',
        description='propertie_b',
        location_latitude=-12.102932897486912,
        location_longitude=-77.03692073205877,
        price=2000000,
    )
