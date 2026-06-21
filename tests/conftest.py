# tests/conftest.py
import pytest
import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# ── Driver fixture ────────────────────────────────────────────────────────────
@pytest.fixture(scope='function')
def driver():
    """Fixture: buat driver baru setiap test, tutup otomatis setelah selesai"""
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')

    # Aktifkan headless saat berjalan di CI/CD (GitHub Actions)
    if os.getenv('CI'):
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')

    d = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    yield d          # <-- test berjalan di sini
    d.quit()         # <-- teardown otomatis setelah test selesai


# ── Page fixtures ─────────────────────────────────────────────────────────────
@pytest.fixture(scope='function')
def saucedemo_login_page(driver):
    from pages.login_page import SauceDemoLoginPage
    return SauceDemoLoginPage(driver)


# ── Helper: baca CSV ──────────────────────────────────────────────────────────
def load_csv(filename):
    """Baca file CSV dari folder data/ dan kembalikan sebagai list of dict"""
    filepath = os.path.join('data', filename)
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


# ── Screenshot otomatis saat test FAIL ────────────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            os.makedirs('reports/screenshots', exist_ok=True)
            # Nama file screenshot dari nama test (bersihkan karakter khusus)
            name = item.nodeid.replace('/', '_').replace('::', '_')
            screenshot_path = f'reports/screenshots/{name}.png'
            driver.save_screenshot(screenshot_path)
            print(f'\n[SCREENSHOT] Screenshot disimpan: {screenshot_path}')
