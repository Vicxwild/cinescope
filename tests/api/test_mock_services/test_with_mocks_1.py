import requests
from unittest.mock import Mock
from tests.api.test_mock_services.test_without_mocks_0 import DateTimeRequest, WhatIsTodayResponse, get_worldclockap_time

class TestTodayIsHolidayServiceAPI:
    # 1 реализация заглушек с Mock в тестах pytest-mock
    def test_what_is_today_BY_MOCK(self, mocker):
        # Создаем мок для функции get_worldclockap_time
        mocker.patch(
            # указываем путь, откуда вызывается функция
            "test_with_mocks_1.get_worldclockap_time",
            return_value=Mock(
                # Фиксированная дата для возврата из мок функции "1 января"
                currentDateTime="2025-01-01T00:00Z"
            )
        )

        # Повторяем предыдущий тест
        world_clock_response = get_worldclockap_time()
        time_data_json = DateTimeRequest(currentDateTime = world_clock_response.currentDateTime).model_dump_json()
        what_is_today_response = requests.post(
            "http://127.0.0.1:16002/what_is_today",
                data=time_data_json
        )

        assert what_is_today_response.status_code == 200
        what_is_today_data = WhatIsTodayResponse(**what_is_today_response.json())

        assert what_is_today_data.message == "Новый год", "ДОЛЖЕН БЫТЬ НОВЫЙ ГОД!"
