from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

path = "/usr/bin/chromedriver"

#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Browser:
    def __init__(self, **kwargs):
        self.options = webdriver.ChromeOptions()
        # self.options.headless = True
        self.options.add_argument("--headless")
        self.browser = webdriver.Chrome(
            options=self.options, service=Service(path))

    def __enter__(self):
        return self

    def get_page(self, url, wait_secs, label=None):
        self.browser.get(url)
        WebDriverWait(self.browser, wait_secs).until(lambda driver: driver.execute_script(
            'return document.readyState') == 'complete')  # or when says go
        yield "wait done"
        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        html = soup.prettify("utf-8")
        yield html

        if label is not None:
            with open(label + ".html", "wb") as file:
                file.write(html)

    def set_value_element(self, element_id, value):
        try:
            element = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.ID, element_id))
            )   #wait for page to load, so element with ID 'username' is visible
        except :
            print ("Could find element for some reason")
            return False
        
        if element:
            print ("setting valu = ", value)
            element.send_keys(value)
            return True
        
        return False

    def submit_element(self, element_id):
        try:
            element = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.ID, element_id))
            )   #wait for page to load, so element with ID 'username' is visible
        except :
            print ("Could find element for some reason")
            return False
        element.click()
        return True
        
    def __exit__(self, type, value, traceback):
        self.browser.quit()

        
