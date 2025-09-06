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
    LIST_PLAGINS_BUTTON = By.CSS_SELECTOR, '[href="#plugins"]'
    FIND_STUDIES_BUTTON = By.CSS_SELECTOR, '[href="#find-studies"]'
    OK_BUTTON = By.ID, "lookup-submit"
    elements_selectors = {
            'patient id': PATIENT_ID_FILD,
            'patient name': PATIENT_NAME_FILD,
            'patient all button': FIND_PATIENT_BUTTON,
            'accsession number': ACCSESSION_NUMBER_FILD,
            'list plugins': (By.CSS_SELECTOR, '[href="#plugins"]')

        }

    def __init__(self, browser, url):
        self.browser = browser
        self.url = url
        self.browser.get(self.url)
        self.wait = WebDriverWait(self.browser, 5)
        self.wait.until(EC.title_is(self.TITLE))

    def element_in_page(self, element):
        try:
            element_on_page=self.wait.until(EC.presence_of_element_located(self.elements_selectors.get(element)))
        except:
            self.browser.save_screenshot(f"screenshorts/{time.strftime('%Y%m%d_%H%M%S')}.png")  # {time.strftime('%Y%m%d_%H%M%S')}
            raise AssertionError(f'The element {element} did not appear on the page')
        return element_on_page

    def element_click(self, element):
        try:
            selector = self.elements_selectors.get(element)
        except:
            raise AssertionError(f"Unnown element {element}")
        try:
            self.wait.until(EC.element_to_be_clickable(selector)).click()
        except:
            raise AssertionError('Element is not clickable or epsent')
        return True

    def open_main_page(self):
        self.browser.get(self.url)
        try:
            self.wait.until(EC.title_is(self.TITLE))
        except:
            raise AssertionError('The main page did not open')

