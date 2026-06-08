import pytest


@pytest.mark.parametrize("email, password, status_code", [
    ("drova@team.ru", "123465", 200),
    ("drova@team.ru", "1234", 400),
    ("dreamte@team.ru", "12345", 200),
    ("dreamte@team.ru", "12345", 400),
    ("abc", "12345", 422),
    ("abc@dfs", "12345", 422),
])
async def test_users_register_post(email: str, password: str, status_code: int, ac):
    # /register
    response_register = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        }
    )
    assert response_register.status_code == status_code
    if status_code != 200:
        return

    # /login
    response_login = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )
    assert response_login.status_code == 200
    assert ac.cookies["access_token"]
    assert "access_token" in response_login.json()

    # /me
    response_me = await ac.get("/auth/me")
    assert response_me.status_code == 200
    user = response_me.json()
    assert user["email"] == email
    assert "id" in user
    assert "password" not in user
    assert "hashed_password" not in user

    # /logout
    response_log = await ac.post("/auth/logout")
    assert response_log.status_code == 200
    assert "access_token" not in ac.cookies


