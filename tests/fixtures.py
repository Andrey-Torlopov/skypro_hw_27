import pytest


@pytest.fixture
@pytest.mark.django_db
def access_token(client, django_user_model):
    username = "test_user"
    password = "test_pass"

    django_user_model.objects.create_user(
        username=username,
        password=password,
        role="moderator"
    )

    response = client.post(
        "/user/token/",
        {"username": username,
         "password": password
         },
        format="json"
    )
    response = client.post(
        '/user/token/',
        {
            "username": username,
            "password": password
        }
    )
    return response.data["access"]
