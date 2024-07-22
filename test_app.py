import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class AppTest(unittest.TestCase):
    def setUp(self):
        #self.driver = webdriver.Chrome()  # You can use HtmlUnitDriver or FirefoxDriver as well
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "http://192.168.1.9"  # Local port http://127.0.0.1:5000, http://192.168.1.9
        self.valid_password = "ValidPassword123"
        self.invalid_password = "123456"
    
    def tearDown(self):
        self.driver.quit()

    def test_login_with_valid_password(self):
        driver = self.driver
        driver.get(self.url)
        self.wait.until(EC.title_contains("Home"))

        # Enter valid password
        driver.find_element(By.NAME, "password").send_keys(self.valid_password)
        driver.find_element(By.XPATH, "//input[@value='Login']").click()

        # Check the result
        expected_result = "Welcome"
        is_result_correct = self.wait.until(EC.title_contains(expected_result))
        self.assertTrue(is_result_correct)

    def test_login_with_invalid_password(self):
        driver = self.driver
        driver.get(self.url)
        self.wait.until(EC.title_contains("Home"))

        # Enter invalid password
        driver.find_element(By.NAME, "password").send_keys(self.invalid_password)
        driver.find_element(By.XPATH, "//input[@value='Login']").click()

        # Check the result
        error_msg = driver.find_element(By.XPATH, "//p[@style='color:red;']")
        self.assertTrue(error_msg.is_displayed())
        self.assertEqual(error_msg.text, "Password does not meet the requirements")

if __name__ == "__main__":
    unittest.main()
