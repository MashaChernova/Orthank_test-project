import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class WebPage():
    TITLE = "Orthanc Explorer"
    PATIENT_ID_FILD = By.ID, "lookup-patient-id"

    def __init__(self, browser, url):
        self.browser = browser
        self.url = url
        self.browser.get(self.url)
        self.wait = WebDriverWait(self.browser, 5)
        self.wait.until(EC.title_is(self.TITLE))

    def element_in_page(self, element):
        try:
            self.wait.until (EC.presence_of_element_located(self.PATIENT_ID_FILD))
        except:
            raise AssertionError(f'The element {element} did not appear on the page')
        return True