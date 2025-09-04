from tests.api.test_mock_services.test_without_mocks_0 import DateTimeRequest, WhatIsTodayResponse, \
    get_worldclockap_time, WorldClockResponse
import requests

class TestTodayIsHolidayServiceAPI:
    def run_wiremock_worldclockap_time(self):
        # Запуск WireMock сервера (если используется standalone, этот шаг можно пропустить)
        wiremock_url = "http://localhost:8080/__admin/mappings"
        mapping = {
            "request": {
                "method": "GET",
                "url": "/wire/mock/api/json/utc/now"  # Эмулируем запрос к worldclockapi
            },
            "response": {
                "status": 200,
                "body": '''{
                            "$id": "1",
                            "currentDateTime": "2025-03-08T00:00Z",
                            "utcOffset": "00:00",
                            "isDayLightSavingsTime": false,
                            "dayOfTheWeek": "Wednesday",
                            "timeZoneName": "UTC",
                            "currentFileTime": 1324567890123,
                            "ordinalDate": "2025-1",
                            "serviceResponse": null
                        }'''
            }
        }
        response = requests.post(wiremock_url, json=mapping)
        assert response.status_code == 201

    def test_what_is_today_BY_WIREMOCK(self): #Данный тест максимально похож на базовый
        # запускаем наш мок сервер
        self.run_wiremock_worldclockap_time()

        # Выполняем запрос к WireMock (имитация worldclockapi)
        world_clock_response = requests.get("http://localhost:8080/wire/mock/api/json/utc/now")
        assert world_clock_response.status_code == 200

        current_time_data = WorldClockResponse(**world_clock_response.json()).currentDateTime
        time_data_for_req = DateTimeRequest(currentDateTime=current_time_data).model_dump_json()

        # Выполняем запрос к тестируемому сервису what_is_today
        what_is_today_response = requests.post(
            url="http://0.0.0.0:16002/what_is_today",
            data=time_data_for_req
        )
        assert what_is_today_response.status_code == 200
        what_is_today_data = WhatIsTodayResponse(**what_is_today_response.json())

        # Проверяем, что ответ соответствует ожидаемому
        assert what_is_today_data.message == "Международный женский день", "8 марта же?"
