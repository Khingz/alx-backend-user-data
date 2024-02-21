#!/usr/bin/env python3
""" Testing auth end points
"""
import requests

url = 'http://172.17.0.10:5000'
EMAIL = 'test@gmail.com'
PASSWD = 'mypwd'
NEW_PASSWD = 'newpwd'


def register_user(email: str, password: str) -> None:
    """Comment
    """
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(f'{url}/users', data=data)

    msg = {"email": email, "message": "user created"}

    assert response.status_code == 200
    assert response.json() == msg


def log_in_wrong_password(email: str, password: str) -> None:
    """comment
    """
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(f'{url}/sessions', data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """ Comment
    """
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(f'{url}/sessions', data=data)
    msg = {"email": email, "message": "logged in"}
    assert response.status_code == 200
    assert response.json() == msg
    session_id = response.cookies.get("session_id")
    return session_id


def profile_unlogged() -> None:
    """ Comment
    """
    cookies = {
        "session_id": ""
    }
    response = requests.get(f'{url}/profile', cookies=cookies)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """ Comment
    """
    cookies = {
        "session_id": session_id
    }
    response = requests.get(f'{url}/profile', cookies=cookies)
    msg = {"email": EMAIL}
    assert response.status_code == 200
    assert response.json() == msg


def log_out(session_id: str) -> None:
    """ Comment
    """
    cookies = {
        "session_id": session_id
    }
    response = requests.delete(f'{url}/sessions', cookies=cookies)
    msg = {"message": "Bienvenue"}
    assert response.status_code == 200
    assert response.json() == msg


def reset_password_token(email: str) -> str:
    """ Comment
    """
    data = {
        "email": email
    }
    response = requests.post(f'{url}/reset_password', data=data)
    assert response.status_code == 200
    reset_token = response.json().get("reset_token")
    msg = {"email": email, "reset_token": reset_token}
    assert response.json() == msg
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Comment
    """
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(f'{url}/reset_password', data=data)
    msg = {"email": email, "message": "Password updated"}
    assert response.status_code == 200
    assert response.json() == msg


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
