import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AppTest(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30)  # Increased timeout to 30 seconds
        self.url = "http://192.168.1.9"  # Make sure this matches your Flask app's host and port
        self.valid_password = "ValidPassword123"
        self.invalid_password = "123456"
        logger.info(f"Setting up test with URL: {self.url}")

    def tearDown(self):
        self.driver.quit()

    def test_login_with_valid_password(self):
        driver = self.driver
        logger.info(f"Navigating to {self.url}")
        driver.get(self.url)
        logger.info("Waiting for page to load...")
        self.wait.until(EC.title_contains("Password Checker - Home"))
        logger.info(f"Page loaded. Title: {driver.title}")

        # Enter valid password
        password_field = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password_field.send_keys(self.valid_password)
        driver.find_element(By.XPATH, "//input[@value='Login']").click()

        # Check the result
        logger.info("Waiting for welcome page...")
        self.wait.until(EC.title_contains("Welcome"))
        logger.info(f"Welcome page loaded. Title: {driver.title}")
        welcome_text = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1"))).text
        self.assertEqual(welcome_text, "Welcome!")

    def test_login_with_invalid_password(self):
        driver = self.driver
        logger.info(f"Navigating to {self.url}")
        driver.get(self.url)
        logger.info("Waiting for page to load...")
        self.wait.until(EC.title_contains("Password Checker - Home"))
        logger.info(f"Page loaded. Title: {driver.title}")

        # Enter invalid password
        password_field = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password_field.send_keys(self.invalid_password)
        driver.find_element(By.XPATH, "//input[@value='Login']").click()

        # Check the result
        logger.info("Waiting for error message...")
        error_msg = self.wait.until(EC.presence_of_element_located((By.XPATH, "//p[@style='color:red;']")))
        self.assertTrue(error_msg.is_displayed())
        self.assertEqual(error_msg.text, "Password does not meet the requirements")

if __name__ == "__main__":
    unittest.main()