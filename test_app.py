import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class AppTest(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30)
        self.url = "http://192.168.1.9:5000"  # Make sure this matches your Flask app's host and port
        self.valid_password = "ValidPassword123"
        self.invalid_password = "123456"

    def tearDown(self):
        self.driver.quit()

    def test_login_with_valid_password(self):
        driver = self.driver
        driver.get(self.url)
        print(f"Current URL: {driver.current_url}")
        print(f"Page title: {driver.title}")
        self.wait.until(EC.title_contains("Password Checker - Home"))

        # Enter valid password
        password_field = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password_field.send_keys(self.valid_password)
        driver.find_element(By.XPATH, "//input[@value='Login']").click()

        # Check the result
        self.wait.until(EC.title_contains("Welcome"))
        welcome_text = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1"))).text
        self.assertEqual(welcome_text, "Welcome!")

    def test_login_with_invalid_password(self):
        driver = self.driver
        driver.get(self.url)
        self.wait.until(EC.title_contains("Password Checker - Home"))

        # Enter invalid password
        password_field = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password_field.send_keys(self.invalid_password)
        driver.find_element(By.XPATH, "//input[@value='Login']").click()

        # Check the result
        error_msg = self.wait.until(EC.presence_of_element_located((By.XPATH, "//p[@style='color:red;']")))
        self.assertTrue(error_msg.is_displayed())
        self.assertEqual(error_msg.text, "Password does not meet the requirements")

if __name__ == "__main__":
    unittest.main()