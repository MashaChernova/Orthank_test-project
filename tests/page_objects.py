import logging

import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
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
    LIST_HEADER = By.CLASS_NAME, "ui-li-heading"
    DATA_TYPE_BUTTON = By.ID, "lookup-study-date"
    DATA_FILD = By.ID, "lookup-study-date-specific"


    elements_selectors = {
            'patient id': PATIENT_ID_FILD,
            'patient name': PATIENT_NAME_FILD,
            'patient all button': FIND_PATIENT_BUTTON,
            'accsession number': ACCSESSION_NUMBER_FILD,
            'list plugins': (By.CSS_SELECTOR, '[href="#plugins"]'),
            'ok button': OK_BUTTON,
            'study header': LIST_HEADER
        }


    def __init__(self, browser, url):
        self.browser = browser
        self.url = url
        self.browser.get('http://orthanc:orthanc@' + self.url)
        self.wait = WebDriverWait(self.browser, 5)
        self.wait.until(EC.title_is(self.TITLE))
        self.open_main_page()
        self.wait.until(EC.title_is(self.TITLE))

    def open_main_page(self):
        self.browser.get('http://' + self.url)
        try:
            alert = self.browser.switch_to.alert()
            alert.authenticate("orthanc", "orthanc")
        except:
            logging.info("dont need authorization")
        try:
            self.wait.until(EC.title_is(self.TITLE))
        except:
            raise AssertionError('The main page did not open')


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


    def element_input(self, fild_for_inpute_name, text_for_input):
        try:
            field_for_input = self.element_in_page(fild_for_inpute_name)
            field_for_input.clear()
            field_for_input.send_keys(text_for_input)
        except:
            raise AssertionError('Failed to enter data')


    def get_title(self):
        return self.browser.title


    def get_element_text(self, element):
        try:
            return self.element_in_page(element).text
        except:
            raise AssertionError(f'Failed to get text on element {element}')


    def data_input(self, data):
        try:
            button = self.wait.until(EC.presence_of_element_located(self.DATA_TYPE_BUTTON))
        except:
            raise AssertionError('Element not found')
        try:
            select = Select(button)
            select.select_by_value('specific')
        except:
            raise AssertionError('Failed to select Specific data')
        try:
            data_fild = self.wait.until(EC.presence_of_element_located(self.DATA_FILD))
            data_fild.clear()
            data_fild.send_keys(data)
        except:
            raise AssertionError(f"Failed to enter date {data}")


