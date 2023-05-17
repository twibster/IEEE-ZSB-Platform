import httpx
from fastapi import status
from api.tests.utils import generate_random_string


BASE_URL = "http://localhost:8000/"
USER_EMAIL = "teser@gmail.com"
USER_USERNAME = "lobalizer"
USER_PASSWORD = "tester123"


def test_home():
    response = httpx.get(BASE_URL)
    assert response.is_redirect
    assert response.next_request.url == BASE_URL+"docs"


def test_user_already_exists():
    body = {
        "first_name": "John",
        "last_name": "Jacky",
        "birthdate": "2023-04-24T22:01:32.904Z",
        "email": USER_EMAIL,
        "username": USER_USERNAME,
        "password": USER_PASSWORD,
        "chapter": "ras",
        "department": "embedded systems",
        "position": "leader"
    }
    response = httpx.post(BASE_URL+"register", json=body)
    assert response.status_code == status.HTTP_201_CREATED
    response = httpx.post(BASE_URL+"register", json=body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json().get("detail") == [
        {'loc': ['body', 'email'],
         'msg': 'this email is already in use',
         'type': 'value_error'
         },
        {'loc': ['body', 'username'],
         'msg': 'this username is already in use',
         'type': 'value_error'
         }]


def test_team_data_logic():
    body = {
        "first_name": "John",
        "last_name": "Jacky",
        "birthdate": "2023-04-24T22:01:32.904Z",
        "email": generate_random_string(8, email=True),
        "username": generate_random_string(8),
        "password": "stringst",
        "chapter": "ras",
        "department": "embedded systems",
        "position": "chairman"
    }
    response = httpx.post(BASE_URL+"register", json=body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    body.pop("chapter")
    response = httpx.post(BASE_URL+"register", json=body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    body["position"] = "leader"
    response = httpx.post(BASE_URL+"register", json=body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    body.pop("department")
    response = httpx.post(BASE_URL+"register", json=body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    body["position"] = "member"
    response = httpx.post(BASE_URL+"register", json=body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    body["department"] = "ai"
    response = httpx.post(BASE_URL+"register", json=body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    body["position"] = "rookie"
    response = httpx.post(BASE_URL+"register", json=body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    body["chapter"] = "ras"
    response = httpx.post(BASE_URL+"register", json=body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    body.pop("department")
    response = httpx.post(BASE_URL+"register", json=body)
    assert response.status_code == status.HTTP_201_CREATED


def test_login_not_found():
    body = {
        "username": generate_random_string(8),
        "password": generate_random_string(8)
    }
    response = httpx.post(BASE_URL+"login", data=body, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    assert response.json() == {'detail': 'user not found'}


def test_login_incorrect_password():
    body = {
        "username": USER_EMAIL,
        "password": generate_random_string(8)
    }
    response = httpx.post(BASE_URL+"login", data=body, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    assert response.json() == {'detail': 'Incorrect Password'}


def test_login_get_token():
    body = {
        "username": USER_EMAIL,
        "password": USER_PASSWORD
    }
    response = httpx.post(BASE_URL+"login", data=body, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    assert response.json().get("access_token") != None
    assert response.json().get("token_type") == "bearer"