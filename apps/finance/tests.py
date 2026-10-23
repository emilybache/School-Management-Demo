import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class FinanceUITest(StaticLiveServerTestCase):
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

    def test_invoice(self):
        d = self.d
        d.get(self.live_server_url + "/accounts/login/")
        d.find_element(By.ID, "id_username").send_keys("admin")
        d.find_element(By.ID, "id_password").send_keys("admin123")
        d.find_element(By.CSS_SELECTOR, "button.login100-form-btn").click()
        time.sleep(1)
        d.get(self.live_server_url + "/student/create/")
        d.find_element(By.ID, "id_registration_number").send_keys("REG/0099")
        d.find_element(By.ID, "id_surname").send_keys("Okafor")
        d.find_element(By.ID, "id_firstname").send_keys("Chidi")
        Select(d.find_element(By.ID, "id_current_class")).select_by_index(1)
        d.find_element(By.ID, "id_date_of_admission").clear()
        d.find_element(By.ID, "id_date_of_admission").send_keys("2024-09-09")
        d.execute_script(
            "arguments[0].value='2011-01-02'", d.find_element(By.ID, "id_date_of_birth")
        )
        d.find_element(By.CSS_SELECTOR, "input[value='Add new student']").click()
        time.sleep(2)
        d.find_element(
            By.XPATH,
            "/html/body/div/aside[1]/div/div[4]/div/div/nav/ul/li[4]/a",
        ).click()
        time.sleep(1)
        d.find_element(By.XPATH, "//ol[contains(@class,'breadcrumb')]/li/a[1]").click()
        time.sleep(1)
        Select(d.find_element(By.ID, "id_student")).select_by_index(1)
        Select(d.find_element(By.ID, "id_session")).select_by_index(1)
        Select(d.find_element(By.ID, "id_term")).select_by_index(3)
        Select(d.find_element(By.ID, "id_class_for")).select_by_index(1)
        d.find_element(By.ID, "id_balance_from_previous_term").clear()
        d.find_element(By.ID, "id_balance_from_previous_term").send_keys("2000")
        Select(d.find_element(By.ID, "id_status")).select_by_index(0)
        d.find_element(By.ID, "id_invoiceitem_set-0-description").send_keys("Tuition")
        d.find_element(By.ID, "id_invoiceitem_set-0-amount").send_keys("25000")
        d.find_element(
            By.XPATH,
            "//div[contains(@class,'callout-info')]//a[@class='add-row']"
            "/div[contains(@class,'btn-success')]",
        ).click()
        time.sleep(0.5)
        d.find_elements(By.CSS_SELECTOR, ".items-group input[type='text']")[
            1
        ].send_keys("Uniform")
        d.find_elements(By.CSS_SELECTOR, ".items-group input[type='number']")[
            1
        ].send_keys("7500")
        d.find_element(By.CSS_SELECTOR, "input.btn-primary[type='submit']").click()
        time.sleep(2)
        tds = d.find_elements(By.XPATH, "//table[@id='invoicetable']/tbody/tr[1]/td")
        self.assertEqual(tds[0].text, "1")
        self.assertEqual(tds[1].text, "Okafor Chidi (REG/0099)")
        self.assertEqual(tds[2].text, "2019/2020-3rd Term")
        self.assertEqual(tds[3].text, "34,500")
        self.assertEqual(tds[4].text, "0")
        self.assertEqual(tds[5].text, "34,500")
        d.get(
            tds[6]
            .find_element(By.CSS_SELECTOR, "a.btn.btn-success.btn-sm")
            .get_attribute("href")
        )
        time.sleep(1)
        lis = d.find_elements(By.CSS_SELECTOR, "div.col-4 div.alert.alert-info ul li")
        self.assertEqual(lis[3].text, "Total Amount Payable: 34,500")
        self.assertEqual(lis[5].text, "Balance: 34,500")
        d.find_element(By.ID, "id_amount_paid").send_keys("10000")
        d.find_element(By.ID, "id_date_paid").clear()
        d.find_element(By.ID, "id_date_paid").send_keys("2026-10-01")
        d.find_element(By.ID, "id_comment").send_keys("first instalment")
        d.find_element(By.XPATH, "//input[@value='Add payment']").click()
        time.sleep(2)
        tds = d.find_elements(By.XPATH, "//table[@id='invoicetable']/tbody/tr[1]/td")
        self.assertEqual(tds[3].text, "34,500")
        self.assertEqual(tds[4].text, "10,000")
        self.assertEqual(tds[5].text, "24,500")
        tds[1].click()
        time.sleep(1)
        self.assertEqual(
            d.find_element(By.XPATH, "//div[@class='col-sm-4']/div/h4").text,
            "Expected Balance: 24,500",
        )
        h5s = d.find_elements(By.XPATH, "//div[@class='col-sm-4']/h5")
        self.assertEqual(h5s[1].text, "3rd Term")
        self.assertEqual(h5s[2].text, "JSS 1")
        trs = d.find_elements(By.XPATH, "(//table)[1]/tbody/tr")
        self.assertEqual(len(trs), 2)
        self.assertEqual(trs[0].find_elements(By.TAG_NAME, "td")[1].text, "Tuition")
        self.assertEqual(trs[1].find_elements(By.TAG_NAME, "td")[2].text, "7500")
        self.assertEqual(
            d.find_element(By.XPATH, "(//table)[1]/tfoot/tr[1]/td[3]").text, "32,500"
        )
        self.assertEqual(
            d.find_element(By.XPATH, "(//table)[1]/tfoot/tr[2]/td[3]").text, "2,000"
        )
        self.assertEqual(
            d.find_element(By.XPATH, "(//table)[1]/tfoot/tr[3]/td[3]").text, "34,500"
        )
        self.assertEqual(
            d.find_element(By.XPATH, "(//table)[1]/tfoot/tr[4]/td[3]").text, "10,000"
        )
        tds = d.find_elements(By.XPATH, "(//table)[2]/tbody/tr[1]/td")
        self.assertEqual(tds[1].text, "10000")
        self.assertEqual(tds[2].text, "Oct. 1, 2026")
        self.assertEqual(tds[3].text, "first instalment")
        d.get(self.live_server_url + "/student/1/")
        tds = d.find_elements(
            By.XPATH,
            "//h4[text()='Invoice/Payment History']/following-sibling::table/tbody/tr/td",
        )
        self.assertEqual(tds[0].text, "2019/2020 - 3rd Term - JSS 1")
        self.assertEqual(tds[1].text, "34500")
        self.assertEqual(tds[2].text, "10000")
        self.assertEqual(tds[3].text, "24500")
