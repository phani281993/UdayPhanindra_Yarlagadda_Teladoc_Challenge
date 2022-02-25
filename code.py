from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import time

class FirefoxAutomation():
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        self.webdriver = webdriver.Firefox(
            options=options,
            service_log_path='/dev/null'
        )
        self.webdriver.get('https://www.way2automation.com/angularjs-protractor/webtables')
        self.webdriver.save_screenshot("way2automation.png")
        time.sleep(5)
            
    def __del__(self):
        self.webdriver.quit()
    
    def add_user(self, first_name, last_name, user_name, cell_phone, password, role):
        no_of_users_initially = self.webdriver.find_elements_by_xpath("//tbody/tr")
        print(f"we have {len(no_of_users_initially)} users initially")
        self._click_element('//*[text() = " Add User"]')
        first_name_field = self.webdriver.find_element_by_xpath('(//*[@type="text"])[2]')
        self._send_keys_to_element(first_name_field, first_name)            
        last_name_field = self.webdriver.find_element_by_xpath('(//*[@type="text"])[3]')
        self._send_keys_to_element(last_name_field, last_name)   
        user_name_field = self.webdriver.find_element_by_xpath('(//*[@type="text"])[4]')
        self._send_keys_to_element(user_name_field, user_name)   
        cell_phone_field = self.webdriver.find_element_by_xpath('(//*[@type="text"])[5]')
        self._send_keys_to_element(cell_phone_field, cell_phone)   
        password_field = self.webdriver.find_element_by_xpath('//*[@type="password"]')
        self._send_keys_to_element(password_field, password)
        try:
            self._click_element(f'//*[@name="RoleId"]/option[text()="{role}"]')
        except Exception as e:
            raise NoSuchElementException("Role Id should only be Sales Team, Customer or Admin.")
        self._click_element(f'//*[text()="Save"]')
        self.webdriver.save_screenshot("add_user.png")
        no_of_users_finally = self.webdriver.find_elements_by_xpath("//tbody/tr")
        print(f"we have {len(no_of_users_finally)} users finally")
        
        assert len(no_of_users_finally) == len(no_of_users_initially) + 1, "Unable to add user"
        
    
    def delete_user(self, first_name):
        no_of_users_initially = self.webdriver.find_elements_by_xpath("//tbody/tr")
        print(f"we have {len(no_of_users_initially)} users initially")
        try:
            self._click_element(f'(//tbody/tr//*[text()="{first_name}"]/..//*[@class="btn btn-link"])[2]')
        except Exception:
            raise NoSuchElementException(f"User with first name {first_name} does not exist.")
        self._click_element(f'//*[text()="OK"]')
        self.webdriver.save_screenshot("delete_user.png")
        no_of_users_finally = self.webdriver.find_elements_by_xpath("//tbody/tr")
        print(f"we have {len(no_of_users_finally)} users finally")
        assert len(no_of_users_finally) == len(no_of_users_initially) - 1, "Unable to delete user"
    
    
    def _click_element(self,
                       search_string,
                       find_by=By.XPATH,
                       timeout=10):
        for i in range(3):
            try:
                print(f"Waiting {timeout-i}s for element {search_string} to be clickable...")
                self._wait_for_element_to_be_clickable(search_string, find_by, timeout=10).click()
                return True
            except Exception as e:
                print(e)
                print("Click failed, trying again by refreshing the page")
                self.webdriver.refresh()
                time.sleep(timeout)

        raise NoSuchElementException(f'Unable to click element: {search_string}')
    
    def _send_keys_to_element(self,
                              element,
                              text_string):
        try:    
            element.send_keys(text_string)
        except Exception as e:
            print(e)
            raise NoSuchElementException(f'Unable to send keys: {text_string} to element: {element}')
    
    def _wait_for_element_to_be_clickable(self,
                                          search_string,
                                          find_by=By.XPATH,
                                          timeout = 20):
        print(f"Waiting {timeout}s for element to be clickable.")
        return WebDriverWait(self.webdriver, timeout).until(EC.element_to_be_clickable(
            (find_by, search_string)))
        
way2automate = FirefoxAutomation()
way2automate.add_user("Test", "User", "test12", "9726512404", "secret", "Sales1 Team")
way2automate.delete_user("Novak")
