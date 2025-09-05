# Сначала нужно запустить WireMock
# docker run -it --rm -p 8080:8080 --name wiremock wiremock/wiremock:3.12.0

import subprocess
import time
import os
import signal
import pytest
from pathlib import Path

SERVICE_PATH = Path("/Users/viktorklementyev/src/edu/python_qa/module_4/python test_services").resolve()

@pytest.fixture(scope="session", autouse=True)
def start_fake_services():
    worldclock_process = subprocess.Popen(
        ["python", "service_fake_worldclockapi.py"],
        cwd=str(SERVICE_PATH),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    what_is_today_process = subprocess.Popen(
        ["python", "service_what_is_today.py"],
        cwd=str(SERVICE_PATH),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    time.sleep(2)

    if worldclock_process.poll() is not None:
        out, err = worldclock_process.communicate()
        print("❌ worldclock_process failed to start")
        print("stdout:", out.decode())
        print("stderr:", err.decode())

    if what_is_today_process.poll() is not None:
        out, err = what_is_today_process.communicate()
        print("❌ what_is_today_process failed to start")
        print("stdout:", out.decode())
        print("stderr:", err.decode())

    yield

    if worldclock_process.poll() is None:
        os.killpg(os.getpgid(worldclock_process.pid), signal.SIGTERM)
    if what_is_today_process.poll() is None:
        os.killpg(os.getpgid(what_is_today_process.pid), signal.SIGTERM)

@pytest.fixture(scope="session", autouse=True)
def wiremock_server():
    print("🚀 Запуск WireMock на порту 8080...")
    process = subprocess.Popen(
        ["docker", "run", "--rm", "-p", "8080:8080", "--name", "wiremock", "wiremock/wiremock:3.12.0"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    time.sleep(2)

    yield

    print("🧹 Остановка WireMock...")
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
