import time

from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from .models import Student


class StudentListViewTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user("teacher", password="secret")
        self.client.force_login(user)

    def test_lists_all_students(self):
        Student.objects.create(registration_number="1", surname="Doe", firstname="John")
        Student.objects.create(registration_number="2", surname="Roe", firstname="Richard")
        Student.objects.create(registration_number="3", surname="Smith", firstname="James")

        response = self.client.get(reverse("student-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["students"]), 3)
        self.assertContains(response, "Doe John")
        self.assertContains(response, "Roe Richard")
        self.assertContains(response, "Smith James")


class StudentsUITest(StaticLiveServerTestCase):
    serialized_rollback = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = webdriver.ChromeOptions()
        opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1400,1000")
        cls.d = webdriver.Chrome(options=opts)
        cls.d.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.d.quit()
        super().tearDownClass()

    def test_1(self):
        d = self.d
        d.get(self.live_server_url + "/accounts/login/")
        d.find_element(By.ID, "id_username").send_keys("admin")
        d.find_element(By.ID, "id_password").send_keys("admin123")
        d.find_element(By.CSS_SELECTOR, "button.login100-form-btn").click()
        time.sleep(1)
        d.find_element(
            By.XPATH, "/html/body/div/aside[1]/div/div[4]/div/div/nav/ul/li[1]/a"
        ).click()
        time.sleep(1)
        d.find_element(By.XPATH, "//ol[contains(@class,'breadcrumb')]/li/a[1]").click()
        time.sleep(1)
        Select(d.find_element(By.ID, "id_current_status")).select_by_index(0)
        d.find_element(By.ID, "id_registration_number").send_keys("REG/0042")
        d.find_element(By.ID, "id_surname").send_keys("Adeyemi")
        d.find_element(By.ID, "id_firstname").send_keys("Tolu")
        d.find_element(By.ID, "id_other_name").send_keys("Grace")
        Select(d.find_element(By.ID, "id_gender")).select_by_index(1)
        d.execute_script(
            "document.getElementById('id_date_of_birth').value='2012-03-04'"
        )
        Select(d.find_element(By.ID, "id_current_class")).select_by_visible_text(
            "JSS 2"
        )
        d.find_element(By.ID, "id_date_of_admission").clear()
        d.find_element(By.ID, "id_date_of_admission").send_keys("2024-09-09")
        d.find_element(By.ID, "id_parent_mobile_number").send_keys("08031234567")
        d.find_element(By.ID, "id_address").send_keys("12 Allen Avenue, Ikeja")
        d.find_element(By.ID, "id_others").send_keys("asthmatic")
        d.find_element(
            By.CSS_SELECTOR, "form input[type='submit'].btn.btn-primary"
        ).click()
        time.sleep(1)
        self.assertEqual(
            d.find_element(By.CSS_SELECTOR, "#toast-container .toast-message").text,
            "New student successfully added.",
        )
        h4s = d.find_elements(
            By.CSS_SELECTOR, "div.card-body div.col-sm-4 div.float-right h4"
        )
        self.assertEqual(h4s[0].text, "Adeyemi")
        self.assertEqual(h4s[1].text, "Tolu")
        self.assertEqual(h4s[2].text, "Grace")
        self.assertEqual(h4s[3].text, "REG/0042")
        h5s = d.find_elements(By.CSS_SELECTOR, "div.card-body div.col-sm-4 > h5")
        self.assertEqual(h5s[0].text, "JSS 2")
        self.assertEqual(h5s[1].text, "Female | Active")
        rows = d.find_elements(
            By.CSS_SELECTOR, "div.col-sm-8 div.form-group.border-bottom.row"
        )
        self.assertEqual(
            rows[0].find_elements(By.CSS_SELECTOR, "div.col")[0].text,
            "March 4, 2012",
        )
        self.assertEqual(
            rows[1].find_elements(By.CSS_SELECTOR, "div.col")[0].text,
            "08031234567",
        )
        self.assertEqual(
            rows[2].find_elements(By.CSS_SELECTOR, "div.col")[0].text,
            "12 Allen Avenue, Ikeja",
        )
        self.assertEqual(
            rows[3].find_elements(By.CSS_SELECTOR, "div.col")[0].text,
            "asthmatic",
        )
        self.assertIn(
            "There are no payment history for",
            d.find_element(
                By.XPATH, "//h4[text()='Invoice/Payment History']/following-sibling::p"
            ).text,
        )
        d.find_element(
            By.XPATH,
            "//div[@class='card-tools']/a[2]/i[contains(@class,'fa-edit')]/..",
        ).click()
        time.sleep(1)
        d.find_element(By.ID, "id_firstname").clear()
        d.find_element(By.ID, "id_firstname").send_keys("Tolulope")
        Select(d.find_element(By.ID, "id_current_status")).select_by_index(1)
        d.find_element(
            By.CSS_SELECTOR, "form input[type='submit'][value='Update Record']"
        ).click()
        time.sleep(1)
        self.assertEqual(
            d.find_element(By.CSS_SELECTOR, "#toast-container .toast-message").text,
            "Record successfully updated.",
        )
        self.assertEqual(
            d.find_elements(
                By.CSS_SELECTOR, "div.card-body div.col-sm-4 div.float-right h4"
            )[1].text,
            "Tolulope",
        )
        self.assertEqual(
            d.find_elements(By.CSS_SELECTOR, "div.card-body div.col-sm-4 > h5")[1].text,
            "Female | Inactive",
        )
