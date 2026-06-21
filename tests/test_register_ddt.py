# tests/test_register_ddt.py
"""
Data-Driven Testing — Registrasi Pengguna
Target  : https://demoqa.com/automation-practice-form
Data    : data/register_data.csv  (15 skenario)

Form ini TIDAK memiliki reCAPTCHA, sehingga proses submit dapat
diverifikasi penuh: hasil PASS dicek dari munculnya modal konfirmasi,
hasil FAIL dicek dari modal yang TIDAK muncul (field wajib gagal validasi).
"""
import allure
import pytest
import os
import sys

sys.path.insert(0, os.path.abspath('.'))

from tests.conftest import load_csv
from pages.register_page import RegisterPage

_CSV_PATH = os.path.join('data', 'register_data.csv')
REGISTER_DATA = load_csv('register_data.csv') if os.path.exists(_CSV_PATH) else []


@allure.feature('User Registration')
@allure.story('Data-Driven Testing — Form Submission')
class TestRegisterDDT:
    """DDT: setiap baris register_data.csv dijalankan sebagai 1 test case."""

    @pytest.mark.parametrize(
        'row',
        REGISTER_DATA,
        ids=[r.get('description', f'row-{i}') for i, r in enumerate(REGISTER_DATA)]
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register(self, driver, row):
        allure.dynamic.title(f"Register: {row.get('description')}")

        with allure.step('Buka halaman automation practice form'):
            page = RegisterPage(driver)
            page.navigate()

        with allure.step(f"Isi form — skenario: {row.get('description')}"):
            page.fill_form(row)

        with allure.step('Klik tombol Submit'):
            page.submit()

        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"result_{row.get('description', 'unknown')}",
            attachment_type=allure.attachment_type.PNG
        )

        with allure.step(f"Verifikasi hasil — expected: {row.get('expected')}"):
            if row.get('expected') == 'PASS':
                assert page.is_register_successful(), (
                    f"[{row.get('description')}] "
                    f"Registrasi seharusnya BERHASIL (modal konfirmasi muncul), "
                    f"tapi modal tidak muncul."
                )
            else:
                assert page.is_register_failed(), (
                    f"[{row.get('description')}] "
                    f"Registrasi seharusnya GAGAL (modal tidak muncul), "
                    f"tapi modal konfirmasi malah muncul."
                )

        page.close_modal_if_open()
