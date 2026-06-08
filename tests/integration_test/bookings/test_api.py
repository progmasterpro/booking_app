import pytest

from tests.conftest import get_db_null_pool


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (5, "2026-05-04", "2026-05-07", 200),
    (5, "2026-05-04", "2026-05-07", 200),
    (5, "2026-05-04", "2026-05-07", 200),
    (5, "2026-05-04", "2026-05-07", 200),
    (5, "2026-05-04", "2026-05-07", 200),
    (5, "2026-05-04", "2026-05-07", 500),
])
async def test_add_booking(room_id, date_from, date_to, status_code, db, authenticated_ac):
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to
        }
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        print(res)
        assert isinstance(res, dict)
        assert res["status"] == "ok"
        assert "data" in res
    # return {"status": "ok", "data": booking}


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()


@pytest.mark.parametrize("room_id, date_from, date_to, booked_room", [
    (1, "2026-05-04", "2026-05-07", 1),
    (1, "2026-05-04", "2026-05-07", 2),
    (1, "2026-05-04", "2026-05-07", 3),
])
async def test_add_and_get_my_bookings(
        room_id,
        date_from,
        date_to,
        booked_room,
        delete_all_bookings,
        authenticated_ac,
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to
        }
    )
    assert response.status_code == 200
    response_my_booking = await authenticated_ac.get("/bookings/me")
    assert response_my_booking.status_code == 200
    assert len(response_my_booking.json()) == booked_room

