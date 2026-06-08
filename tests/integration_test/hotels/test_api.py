async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params={
            "date_from": "2026-05-04",
            "date_to": "2026-05-07"
        }
    )
    print(f"{response.json()=}")

    assert response.status_code == 200

