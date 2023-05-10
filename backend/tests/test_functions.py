import pytest
from fastapi import HTTPException, status
from backend.functions import decode_token, generate_token, create_payload, create_token_json


class Payload:
    def __init__(self, id: int, username: str, position: str):
        self.id = id
        self.username = username
        self.position = position


PAYLOAD = Payload(2, "tester", "tester_role")

def test_payload_for_jwt(payload: Payload = PAYLOAD):
    assert create_payload(payload) == {  # type: ignore
        "id": payload.id,
        "username": payload.username,
        "role": payload.position
        }
    with pytest.raises(HTTPException) as exc:
        create_payload(None)  # type: ignore
    assert exc.value.status_code == status.HTTP_406_NOT_ACCEPTABLE


def test_generate_token():
    with pytest.raises(HTTPException) as exc:
        generate_token(None)  # type: ignore
    assert exc.value.status_code == status.HTTP_406_NOT_ACCEPTABLE

    with pytest.raises(TypeError) as exc:
        generate_token({"test": "test"}, expiry_duration=30.5)  # type: ignore
    assert exc.type == TypeError

    assert isinstance(generate_token({"test": "test"}), str)


def test_create_token_json():
    assert create_token_json("test") == {"access_token": "test", "token_type": "bearer"}

def test_decode_token():
    assert decode_token("not_a_token") == None
    payload = {"test": "test"}
    assert decode_token(generate_token(payload)) == payload
    