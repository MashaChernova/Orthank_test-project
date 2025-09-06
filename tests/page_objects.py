import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class WebPage():
    TITLE = "Orthanc Explorer"
    PATIENT_ID_FILD = By.ID, "lookup-patient-id"
    PATIENT_NAME_FILD = By.ID, "lookup-patient-name"
    ACCSESSION_NUMBER_FILD = By.ID, "lookup-accession-number"
    FIND_PATIENT_BUTTON = By.CSS_SELECTOR, '[href="#find-patients"]'

    def __init__(self, browser, url):
        self.browser = browser
        self.url = url
        self.browser.get(self.url)
        self.wait = WebDriverWait(self.browser, 5)
        self.wait.until(EC.title_is(self.TITLE))

    def element_in_page(self, element):
        elements_selectors = {
            'patient id': self.PATIENT_ID_FILD,
            'patient all button': self.FIND_PATIENT_BUTTON,
            'patient name': self.PATIENT_NAME_FILD,
            'accsession number': self.ACCSESSION_NUMBER_FILD
        }
        try:
            element_on_page=self.wait.until(EC.presence_of_element_located(elements_selectors.get(element)))
        except:
            raise AssertionError(f'The element {element} did not appear on the page')
        return element_on_page