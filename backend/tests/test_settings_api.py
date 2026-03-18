def test_patch_settings_updates_intervals(client) -> None:
    response = client.patch(
        "/api/settings",
        json={
            "sync_interval_minutes": 30,
            "analysis_interval_minutes": 120,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["sync_interval_minutes"] == 30
    assert payload["analysis_interval_minutes"] == 120
