import pytest
from tests.factories import AdFactory
from ads.serializers import AdListSerializer


@pytest.mark.django_db
def test_vacancy_list(client) -> None:
    items = AdFactory.create_batch(5)
    expected_response = {
        "count": 5,
        "next": None,
        "previous": None,
        "results": AdListSerializer(items, many=True).data
    }

    response = client.get("/ad/")
    assert response.status_code == 200
    assert response.data == expected_response
