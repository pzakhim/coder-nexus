# tests/unit/api/test_<feature>.py - HTTP mapping through the ASGI app with the fixtures of conftest.py.tpl.
# Shape only. Real service over fake ports; authentication overridden, authorization real; no database.
# Error codes and response shapes come from api-contract-design and the agreed contract.


async def test_create_<entity>_with_default_data_returns_201(client, as_user) -> None:
    as_user(USER_A)

    response = await client.post("/<entities>", json=<pass_default_body>)

    assert response.status_code == 201
    assert response.json()["<field>"] == <literal_from_design>


async def test_create_<entity>_with_invalid_body_returns_<422_or_400>(client, as_user) -> None:
    as_user(USER_A)

    response = await client.post("/<entities>", json=<fail_body>)

    assert response.status_code == <422_or_400>
    assert response.json()["<error_field>"] == "<contract_code>"


async def test_get_<entity>_without_token_returns_401(client) -> None:          # no auth override
    response = await client.get("/<entities>/<id>")

    assert response.status_code == 401


async def test_get_<entity>_of_other_owner_returns_<403_or_404>(client, as_user, <entity>_repo) -> None:
    <entity>_repo.rows[<ID_1>] = make_<entity>(id=<ID_1>, owner_id=USER_A.id)
    as_user(USER_B)

    response = await client.get(f"/<entities>/{<ID_1>}")

    assert response.status_code == <403_or_404>                                 # exactly as the contract says


async def test_list_<entities>_when_none_returns_empty_items(client, as_user) -> None:
    as_user(USER_A)

    response = await client.get("/<entities>")

    assert response.status_code == 200
    assert response.json()["items"] == []
