def test_create_user_invalid_password(api_client, test_create_user):
    response = api_client.post(
        "/api/v1.0/auth/register",
        data={
            "email": "ellah400@gmail.com",
            "other_names": "Nathan",
            "surname": "Daniel",
            "date_of_birth": "2019-08-30",
            "password": "Simplepass123",
            "password2": "Simplepass123",
        },
    )
    assert response.status_code == 422
    assert response.json() == {"error": {"message": "Password is not valid!"}}


def test_create_user_wrong_email_format(api_client, test_create_user):
    response = api_client.post(
        "/api/v1.0/auth/register",
        data={
            "email": "ellah400@",
            "other_names": "Nathan",
            "surname": "Daniel",
            "date_of_birth": "2019-08-30",
            "password": "Simplepass123!",
            "password2": "Simplepass123!",
        },
    )
    assert response.status_code == 422
    assert (
        response.json()
        .get("error")
        .get("message")
        .get("msg")
        .startswith("value is not a valid email address:")
    )


def test_create_user_with_future_birth_date(api_client, test_create_user):
    response = api_client.post(
        "/api/v1.0/auth/register",
        data={
            "email": "ellah400@gmail.com",
            "other_names": "Nathan",
            "surname": "Daniel",
            "date_of_birth": "2029-08-30",
            "password": "Simplepass123!",
            "password2": "Simplepass123!",
        },
    )
    assert response.status_code == 422
    assert (
        response.json()
        .get("error")
        .get("message")
        .get("msg")
        .startswith("Input should be less than or equal to")
    )


def test_user_change_password(api_client, test_create_user):
    response = api_client.post(
        "/api/v1.0/auth/change-password",
        data={
            "current_password": "Simplepass123!",
            "new_password": "Simplepass1234!",
        },
    )
    assert response.status_code == 200


def test_refresh_tokens_failure(api_client, test_create_user):
    response = api_client.post(
        "/api/v1.0/auth/token-refresh/",
        data={
            "refresh": "eyJhbGciOiJIUzI1..",
        },
    )
    assert response.status_code == 401
