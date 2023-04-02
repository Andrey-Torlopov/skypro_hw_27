import pytest


@pytest.mark.django_db
def test_create_ad(client, access_token, user, category) -> None:
    expected_response = {
        "id": 1,
        "is_published": False,
        "name": "test ads name",
        "price": 100,
        "author": user.pk,
        "category": category.pk,
        "description": None,
        "image": None
    }

    data = {
        "name": "test ads name",
        "author": user.pk,
        "category": category.pk,
        "price": 100
    }

    response = client.post(
        "/ad/",
        data,
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + access_token
    )

    assert response.status_code == 201
    assert response.data == expected_response
