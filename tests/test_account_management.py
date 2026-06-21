# tests/test_account_management.py
"""
Test Management Akun — SauceDemo
Mencakup: login sukses, login dikunci, logout, verifikasi sesi setelah logout.
"""
import allure
import pytest
import time
from selenium.webdriver.common.by import By
from pages.login_page import SauceDemoLoginPage



@allure.feature('Account Management')
class TestAccountManagement:

    # ── TC-ACC-001 ────────────────────────────────────────────────────────────
    @allure.title('TC-ACC-001: Login valid → berhasil masuk ke halaman inventory')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_valid_reaches_inventory(self, driver):
        with allure.step('Login sebagai standard_user'):
            page = SauceDemoLoginPage(driver)
            page.login('standard_user', 'secret_sauce')

        with allure.step('Verifikasi URL mengandung /inventory'):
            assert page.is_login_successful(), \
                'standard_user harus berhasil masuk ke /inventory'

        allure.attach(driver.get_screenshot_as_png(),
                      name='tc_acc_001_inventory',
                      attachment_type=allure.attachment_type.PNG)

    # ── TC-ACC-002 ────────────────────────────────────────────────────────────
    @allure.title('TC-ACC-002: Login → Logout → kembali ke halaman login')
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_then_logout(self, driver):
        with allure.step('Login sebagai standard_user'):
            login = SauceDemoLoginPage(driver)
            login.login('standard_user', 'secret_sauce')
            assert login.is_login_successful(), 'Harus berhasil login dulu'

        with allure.step('Buka burger menu dan klik Logout'):
            driver.find_element(By.ID, 'react-burger-menu-btn').click()
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            wait = WebDriverWait(driver, 10)
            logout_btn = wait.until(EC.presence_of_element_located((By.ID, 'logout_sidebar_link')))
            driver.execute_script("arguments[0].click();", logout_btn)

        with allure.step('Verifikasi kembali ke halaman login (URL = saucedemo.com/)'):
            wait.until(EC.url_to_be('https://www.saucedemo.com/'))
            assert driver.current_url == 'https://www.saucedemo.com/', \
                f'Harus kembali ke login, tapi URL: {driver.current_url}'

        allure.attach(driver.get_screenshot_as_png(),
                      name='tc_acc_002_after_logout',
                      attachment_type=allure.attachment_type.PNG)

    # ── TC-ACC-003 ────────────────────────────────────────────────────────────
    @allure.title('TC-ACC-003: User yang dikunci (locked_out_user) tidak bisa login')
    @allure.severity(allure.severity_level.NORMAL)
    def test_locked_user_cannot_login(self, driver):
        with allure.step('Login sebagai locked_out_user'):
            page = SauceDemoLoginPage(driver)
            page.login('locked_out_user', 'secret_sauce')

        with allure.step('Verifikasi muncul pesan error "locked out"'):
            assert page.is_login_failed(), \
                'locked_out_user harus gagal login'
            error_msg = page.get_error_message()
            assert 'locked out' in error_msg.lower(), \
                f'Pesan error harus mengandung "locked out", tapi: {error_msg}'

        allure.attach(driver.get_screenshot_as_png(),
                      name='tc_acc_003_locked_user',
                      attachment_type=allure.attachment_type.PNG)

    # ── TC-ACC-004 ────────────────────────────────────────────────────────────
    @allure.title('TC-ACC-004: Sesi tidak valid setelah logout — akses inventory redirect ke login')
    @allure.severity(allure.severity_level.NORMAL)
    def test_session_invalid_after_logout(self, driver):
        with allure.step('Login lalu Logout'):
            login = SauceDemoLoginPage(driver)
            login.login('standard_user', 'secret_sauce')
            driver.find_element(By.ID, 'react-burger-menu-btn').click()
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            wait = WebDriverWait(driver, 10)
            logout_btn = wait.until(EC.presence_of_element_located((By.ID, 'logout_sidebar_link')))
            driver.execute_script("arguments[0].click();", logout_btn)
            wait.until(EC.url_to_be('https://www.saucedemo.com/'))

        with allure.step('Coba akses /inventory.html langsung tanpa login'):
            driver.get('https://www.saucedemo.com/inventory.html')
            time.sleep(1)

        with allure.step('Verifikasi diarahkan kembali ke halaman login'):
            current = driver.current_url
            assert 'inventory' not in current, \
                f'Setelah logout, inventory tidak boleh bisa diakses. URL: {current}'

        allure.attach(driver.get_screenshot_as_png(),
                      name='tc_acc_004_session_invalid',
                      attachment_type=allure.attachment_type.PNG)

    # ── TC-ACC-005 ────────────────────────────────────────────────────────────
    @allure.title('TC-ACC-005: Login dengan username salah → muncul pesan error')
    @allure.severity(allure.severity_level.NORMAL)
    def test_wrong_username_shows_error(self, driver):
        with allure.step('Login dengan username yang tidak terdaftar'):
            page = SauceDemoLoginPage(driver)
            page.login('user_tidak_ada', 'secret_sauce')

        with allure.step('Verifikasi muncul pesan error'):
            assert page.is_login_failed()
            assert 'Username and password do not match' in page.get_error_message()

        allure.attach(driver.get_screenshot_as_png(),
                      name='tc_acc_005_wrong_user',
                      attachment_type=allure.attachment_type.PNG)
