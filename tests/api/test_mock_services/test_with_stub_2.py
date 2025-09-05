from tests.api.test_mock_services.test_without_mocks_0 import DateTimeRequest, WhatIsTodayResponse, get_worldclockap_time
import requests

class TestTodayIsHolidayServiceAPI:
    def stub_get_worldclockap_time(self):
        class StubWorldClockResponse:
            def __init__(self):
                self.currentDateTime = "2025-05-09T00:00Z"  # Фиксированная дата для Stub

        return StubWorldClockResponse()

    def test_what_is_today_BY_STUB(self, monkeypatch):
        # Подменяем реальную функцию get_worldclockap_time на Stub
        # Нужно передавать ссылку на функцию, а не результат её вызова
        monkeypatch.setattr("test_with_stub_2.get_worldclockap_time", self.stub_get_worldclockap_time)
        #или же можем просто напрямую взять значение из Stub world_clock_response = stub_get_worldclockap_time()

        # Выполним тело предыдущего теста еще раз
        world_clock_response = get_worldclockap_time() # вызов Stub

        # Выполняем запрос к тестируемому сервису
        time_data_json = DateTimeRequest(currentDateTime=world_clock_response.currentDateTime).model_dump_json()
        resp_what_is_today = requests.post(
            "http://127.0.0.1:16002/what_is_today",
            data=time_data_json
        )

        assert resp_what_is_today.status_code == 200
        what_is_today_data = WhatIsTodayResponse(**resp_what_is_today.json())
        assert what_is_today_data.message == "День Победы", "ДОЛЖЕН БЫТЬ ДЕНЬ ПОБЕДЫ!"
