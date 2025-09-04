# docker run -it --rm -p 8080:8080 --name wiremock wiremock/wiremock:3.12.0

import requests
import pytest

# Настройка WireMock для мока
def setup_wirewock_mock():
    url = "http://localhost:8080/__admin/mappings"
    payload = {
        "request": {
            "method": "GET",
            # мы указываем что если кто-то сделает запрос на ручку http://localhost:8080/gismeteo/get/weather
            "url": "/gismeteo/get/weather",
        },
        "response": {
            "status": 200,
            "body": {"temperature": 25},
            "headers": {"Content-Type": "application/json"}
        }
    }

    # Отправляем запрос на наш WireMock
    requests.post(url, json=payload)

@pytest.mark.skip(reason="not implemented")
def test_wirewock_mock():
    setup_wirewock_mock()
    response = requests.get("http://localhost:8080/gismeteo/get/weather")
    assert response.status_code == 200
    assert response.json() == {"temperature": 25}
