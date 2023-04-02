import pytest


@pytest.mark.django_db
def test_retrieve_vacancy(client, ad, access_token) -> None:
    expected_response = {
        "id": ad.pk,
        "name": ad.name,
        "price": ad.price,
        "description": ad.description,
        "is_published": ad.is_published,
        "image": ad.image,
        "author": ad.author.pk,
        "category": ad.category.pk
    }

    response = client.get(
        f"/ad/{ad.pk}/",
        HTTP_AUTHORIZATION="Bearer " + access_token
    )

    assert response.status_code == 200
    assert response.data == expected_response
