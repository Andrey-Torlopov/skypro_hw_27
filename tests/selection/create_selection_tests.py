import pytest


@pytest.mark.django_db
def test_create_selection(client, access_token, user, ad) -> None:
    expected_response = {
        "id": 1,
        "owner": user.username,
        "name": "Test name",
        "items": [ad.pk]
    }

    data = {
        "name": "Test name",
        "owner": user.username,
        "items": [ad.pk]
    }

    response = client.post(
        "/selection/",
        data,
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + access_token
    )

    assert response.status_code == 201
    assert response.data == expected_response
