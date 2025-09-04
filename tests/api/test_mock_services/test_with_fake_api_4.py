from datetime import datetime
import pytz
from tests.api.test_mock_services.test_without_mocks_0 import DateTimeRequest, WhatIsTodayResponse, \
    WorldClockResponse
import requests


def get_fake_worldclockap_time() -> WorldClockResponse:
    resp = requests.get("http://0.0.0.0:16001/fake/worldclockapi/api/json/utc/now")
    assert resp.status_code == 200
    return WorldClockResponse(**resp.json())

class TestTodayIsHolidayServiceAPI:
    # Функция выполняющая запрос в Fake сервис worldclockapi для получения текущей даты
    def test_fake_worldclockap(self):# проверка работоспособности сервиса worldclockap
        world_clock_response = get_fake_worldclockap_time()
        current_date_time = world_clock_response.currentDateTime
        assert current_date_time == datetime.now(pytz.utc).strftime("%Y-%m-%dT%H:%MZ"), "Дата не совпадает"

    def test_fake_what_is_today(self):# проверка работоспособности Fake сервиса what_is_today
        world_clock_response = get_fake_worldclockap_time()
        current_date_time = world_clock_response.currentDateTime
        time_json = DateTimeRequest(currentDateTime=current_date_time).model_dump_json()
        request_what_is_today = requests.post(
            url="http://0.0.0.0:16002/what_is_today",
            data=time_json
        )
        print(time_json)
        assert request_what_is_today.status_code == 200
        what_is_today_resp = WhatIsTodayResponse(**request_what_is_today.json())
        assert what_is_today_resp.message == "Сегодня нет праздников в России.", "Сегодня нет праздника!"
