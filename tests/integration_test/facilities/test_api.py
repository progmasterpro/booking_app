async def test_facilities_get(ac):
    response = await ac.get("/facilities")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_facilities_add(ac):
    facility_title = "Parking"
    response = await ac.post(
        "/facilities",
        json={"title": facility_title}
    )
    res = response.json()
    print(f"{res=}") #  res={'status': 'ok', 'data': {'title': 'Parking', 'id': 1}}
    print(f"{res["data"]}") # {'title': 'Parking', 'id': 1}
    assert response.status_code == 200
    assert isinstance(res, dict)
    assert res["data"]["title"] == facility_title
    assert res["data"]["id"] == 1
    assert "data" in res
