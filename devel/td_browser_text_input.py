from Browser import Browser
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

url = "http://127.0.0.1:8000/"
with Browser() as browser:
    ph = browser.get_page(url, 1, label="test_page")
    load_done = ph.__next__()
    page_source = ph.__next__()
    try:
        ph.__next__()
    except:
        pass

    driver = browser.browser
    #elements = driver.find_elements_by_xpath("//*")
    elements = WebDriverWait(driver, 1).until(
        EC.presence_of_all_elements_located((By.XPATH, "//*"))
    )
    # print the IDs of all elements
    # for element in elements:
    #     print(element.get_attribute("id"))
    # element = WebDriverWait(driver, 1).until(
    #     EC.presence_of_element_located((By.ID, "/password"))
    # )
    #print (element)
    # print the IDs of all elements
    # for element in elements:
    #     print(element.get_attribute("id"))

    #print (page_source)
    element_id = "/password"
    browser.set_value_text_element(element_id, "mypassword")
    
