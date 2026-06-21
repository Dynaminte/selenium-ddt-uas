# pages/register_page.py
"""
Page Object untuk DemoQA Automation Practice Form
URL: https://demoqa.com/automation-practice-form

CATATAN:
  Form ini TIDAK memiliki reCAPTCHA, sehingga submit penuh berfungsi normal.
  Setelah submit berhasil, muncul modal konfirmasi dengan judul
  "Thanks for submitting the form".
  Jika ada field wajib yang kosong/invalid, browser akan menampilkan
  border merah (CSS :invalid) pada field tersebut dan modal TIDAK muncul.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time


class RegisterPage(BasePage):
    URL = 'https://demoqa.com/automation-practice-form'

    # ── Locators — Form Fields ───────────────────────────────────────────────
    FIRST_NAME   = (By.ID, 'firstName')
    LAST_NAME    = (By.ID, 'lastName')
    EMAIL        = (By.ID, 'userEmail')
    GENDER_MALE  = (By.CSS_SELECTOR, 'label[for="gender-radio-1"]')
    GENDER_FEM   = (By.CSS_SELECTOR, 'label[for="gender-radio-2"]')
    GENDER_OTHER = (By.CSS_SELECTOR, 'label[for="gender-radio-3"]')
    MOBILE       = (By.ID, 'userNumber')
    SUBMIT_BTN   = (By.ID, 'submit')

    # ── Locators — Hasil ──────────────────────────────────────────────────────
    MODAL_TITLE  = (By.ID, 'example-modal-sizes-title-lg')
    MODAL_TABLE  = (By.CLASS_NAME, 'table-responsive')
    CLOSE_MODAL  = (By.ID, 'closeLargeModal')

    # Field yang menjadi merah (CSS :invalid / class field-error) saat gagal validasi
    FIRST_NAME_INVALID  = (By.CSS_SELECTOR, '#firstName.is-invalid, #firstName.field-error')
    LAST_NAME_INVALID   = (By.CSS_SELECTOR, '#lastName.is-invalid, #lastName.field-error')
    EMAIL_INVALID       = (By.CSS_SELECTOR, '#userEmail.is-invalid, #userEmail.field-error')
    MOBILE_INVALID      = (By.CSS_SELECTOR, '#userNumber.is-invalid, #userNumber.field-error')

    # ── Actions ───────────────────────────────────────────────────────────────
    def navigate(self):
        self.open(self.URL)
        time.sleep(1)
        # Hilangkan iklan/banner yang kadang menutupi form (umum terjadi di DemoQA)
        try:
            self.driver.execute_script(
                "document.querySelectorAll('#fixedban, .ad, iframe[id^=\"google_ads\"]')"
                ".forEach(function(e){ e.remove(); })"
            )
        except Exception:
            pass

    def fill_form(self, row: dict):
        """Isi form dari satu baris dict CSV. Hanya isi field yang bernilai."""
        if row.get('first_name'):
            self.type(self.FIRST_NAME, row['first_name'])
        if row.get('last_name'):
            self.type(self.LAST_NAME, row['last_name'])
        if row.get('email'):
            self.type(self.EMAIL, row['email'])

        gender = (row.get('gender') or '').strip().lower()
        if gender == 'male':
            self.click(self.GENDER_MALE)
        elif gender == 'female':
            self.click(self.GENDER_FEM)
        elif gender == 'other':
            self.click(self.GENDER_OTHER)

        if row.get('mobile'):
            self.type(self.MOBILE, row['mobile'])

    def submit(self):
        """Klik Submit. Scroll dulu agar tombol tidak tertutup elemen lain."""
        btn = self.find_clickable(self.SUBMIT_BTN)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        time.sleep(0.3)
        try:
            btn.click()
        except Exception:
            # Fallback: klik via JS jika ada overlay yang menghalangi
            self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(0.6)

    # ── Assertion helpers ─────────────────────────────────────────────────────
    def is_register_successful(self):
        """True jika modal konfirmasi 'Thanks for submitting the form' muncul"""
        return self.is_visible(self.MODAL_TITLE)

    def is_register_failed(self):
        """
        True jika register GAGAL: modal tidak muncul ATAU ada field
        yang ditandai invalid oleh browser.
        """
        modal_shown = self.is_visible(self.MODAL_TITLE)
        if modal_shown:
            return False
        return True

    def has_invalid_field(self):
        """True jika ada field dengan border merah (invalid)"""
        selectors = [self.FIRST_NAME_INVALID, self.LAST_NAME_INVALID,
                     self.EMAIL_INVALID, self.MOBILE_INVALID]
        for sel in selectors:
            if len(self.driver.find_elements(*sel)) > 0:
                return True
        return False

    def close_modal_if_open(self):
        """Tutup modal konfirmasi jika sedang terbuka (untuk lanjut test berikutnya)"""
        try:
            if self.is_visible(self.MODAL_TITLE):
                self.click(self.CLOSE_MODAL)
                time.sleep(0.3)
        except Exception:
            pass
