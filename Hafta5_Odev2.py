from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import date
from pathlib import Path
import pytest

class Test_SauceDemo:

    def setup_method(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get("https://www.saucedemo.com/")
        self.folderPath = str(date.today())
        Path(self.folderPath).mkdir(exist_ok=True)
    
    def teardown_method(self): 
        self.driver.quit()

    def waitForElementVisible(self, locator, timeout=5):
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
    
    def inputs(self):
        self.usernameInput = self.driver.find_element(By.ID, "user-name")
        self.passwordInput = self.driver.find_element(By.ID, "password")

    def LoginDeneme(self):
        loginBtn = self.driver.find_element(By.ID, "login-button")
        loginBtn.click()

    @pytest.mark.timeout()
    def test_valid_login(self):
        self.waitForElementVisible((By.ID, "user-name")) 
        self.waitForElementVisible((By.ID, "password"))
        self.inputs()
        self.usernameInput.send_keys("standard_user")   
        self.passwordInput.send_keys("secret_sauce")
        self.LoginDeneme()
        self.driver.save_screenshot(f"{self.folderPath}/test-valid-login.png")

    @pytest.mark.parametrize("username,password", [("mehmet","451290"), ("maslan","turkeY80"), ("kapı", "4512")])
    def test_invalid_login(self, username, password):
        self.waitForElementVisible((By.ID, "user-name"))
        self.waitForElementVisible((By.ID, "password"))
        self.inputs()
        self.usernameInput.send_keys(username)
        self.passwordInput.send_keys(password)
        self.LoginDeneme()
        self.driver.save_screenshot(f"{self.folderPath}/test-invalid-login-{username}-{password}.png")
        errorMessage = self.driver.find_element(By.XPATH, "//*[@id='login_button_container']/div/form/div[3]/h3")
        assert errorMessage.text == "Epic sadface: Username and password do not match any user in this service"
        
    @pytest.mark.skip()
    def test_locked_login(self):
        self.waitForElementVisible((By.ID, "user-name"))
        self.waitForElementVisible((By.ID, "password"))
        self.inputs()
        self.usernameInput.send_keys("locked_out_user")  
        self.passwordInput.send_keys("secret_sauce")
        self.LoginDeneme()
        self.driver.save_screenshot(f"{self.folderPath}/test-locked-login.png")   

    @pytest.mark.slow()
    def test_glitch_login(self):
        self.waitForElementVisible((By.ID, "user-name"))
        self.waitForElementVisible((By.ID, "password"))
        self.inputs()
        self.usernameInput.send_keys("performance_glitch_user")
        self.passwordInput.send_keys("secret_sauce")
        self.LoginDeneme()
        self.driver.save_screenshot(f"{self.folderPath}/test-glitch-login.png")
