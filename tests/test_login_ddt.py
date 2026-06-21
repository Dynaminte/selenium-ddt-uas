# tests/test_login_ddt.py
"""
Data-Driven Testing — Login SauceDemo
Target : https://www.saucedemo.com
Data   : data/login_data.csv  (7 skenario)
"""
import allure
import pytest
import os
import sys

sys.path.insert(0, os.path.abspath('.'))

from tests.conftest import load_csv
from pages.login_page import SauceDemoLoginPage

_CSV_PATH = os.path.join('data', 'login_data.csv')
LOGIN_DATA = load_csv('login_data.csv') if os.path.exists(_CSV_PATH) else []


@allure.feature('User Authentication')
@allure.story('Data-Driven Testing — Login SauceDemo')
class TestLoginDDT:
    """DDT: setiap baris login_data.csv = 1 test case login SauceDemo."""

    @pytest.mark.parametrize(
        'row',
        LOGIN_DATA,
        ids=[r.get('description', f'row-{i}') for i, r in enumerate(LOGIN_DATA)]
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login(self, driver, row):
        allure.dynamic.title(f"Login DDT: {row.get('description')}")

        with allure.step('Buka halaman login SauceDemo'):
            page = SauceDemoLoginPage(driver)

        with allure.step(f"Login dengan data: username={row.get('username') or '(kosong)'}, "
                         f"password={row.get('password') or '(kosong)'}"):
            page.login(
                row.get('username', ''),
                row.get('password', '')
            )

        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"result_{row.get('description', 'unknown')}",
            attachment_type=allure.attachment_type.PNG
        )

        with allure.step(f"Verifikasi hasil — expected: {row.get('expected')}"):
            if row.get('expected') == 'PASS':
                assert page.is_login_successful(), (
                    f"[{row.get('description')}] "
                    f"Login seharusnya BERHASIL tapi gagal."
                )
            else:
                assert page.is_login_failed(), (
                    f"[{row.get('description')}] "
                    f"Login seharusnya GAGAL tapi berhasil masuk."
                )
