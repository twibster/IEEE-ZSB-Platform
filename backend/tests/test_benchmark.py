"""
this benchmark test was to find out if using event listeners affects
the performance heavily or not.
through repteated test, Here are the mean time required to add 10k users to the db):
with a listener: 7.6 seconds
without a listneer (adding the permissions excplicitly in the logic): 8.4 seconds
"""

import datetime
from backend.constants import default_permissions
from backend.database.models import User, Permission
from backend.tests.utils import generate_random_string
from backend.database.init_db import SessionLocal


def generate_user(email: str, username: str) -> dict:
    user_model: dict = {
        "first_name": "John",
        "last_name": "Jacky",
        "birthdate": datetime.datetime.utcnow(),
        "email": email,
        "username": username,
        "password": "stringst",
        "chapter": "ras",
        "department": "embedded systems",
        "position": "leader"
    }
    return user_model


def generate_users_list(count: int) -> list:
    return [generate_user(generate_random_string(7, True), generate_random_string(7)) for i in range(count)]


def add_users() -> None:
    session = SessionLocal()
    for user in generate_users_list(10000):
        user = User(**user)
        # permissions = Permission(**default_permissions[user.position])
        # permissions.user = user
        # session.add(permissions)
        session.add(user)
    session.commit()
    

def add_users_sessions() -> None:
    session = SessionLocal()
    for user in generate_users_list(10000):
        user = User(**user)
        # permissions = Permission(**default_permissions[user.position])
        # permissions.user = user
        # session.add(permissions)
        session.add(user)
        session.commit()


# def test_one_session(benchmark) -> None:
#     result = benchmark(add_users)


# def test_sessions(benchmark) -> None:
#     result = benchmark(add_users_sessions)


