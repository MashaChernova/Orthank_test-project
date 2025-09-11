import pytest
import time

element_list = ['patient id', 'patient all button', 'patient name', 'accsession number', 'list plugins']
@pytest.mark.parametrize('element_for_test',
                          element_list,
                          ids=element_list)
def test_presence_of_elements(page, element_for_test):
    assert page.element_in_page(element_for_test)


@pytest.mark.parametrize('element_for_test, title_sub_string',
                          [
                              ('patient all button', 'patient'),
                              ('list plugins', 'Plugins')
                          ],
                          ids=['patient all button', 'list plugins'])
def test_open_page_by_button(page, element_for_test, title_sub_string):
    page.open_main_page()
    assert page.element_click(element_for_test)
    page.get_title()
    assert title_sub_string in page.get_title()

@pytest.mark.parametrize('patient_number', [0, -1, 'random'])
def test_patients_name_search(api_connecter, page, patient_number):
    i = api_connecter.get_number_for_list('patients', patient_number)
    patient_name = api_connecter.get_patient_name(i)
    page.open_main_page()
    page.element_input('patient name', patient_name)
    page.element_click('ok button')
    assert patient_name in page.get_element_text('study header'), f" {page.get_element_text('study header')} instead {patient_name} The list of studies for another patient is displayed"


@pytest.mark.parametrize('patient_number', [-1, 0, 1, 'random'])
@pytest.mark.only2
def test_date_search(api_connecter, page, patient_number):
    i = api_connecter.get_number_for_list('patients', patient_number)
    study_data = api_connecter.get_study_info(i, 'StudyDate')
    patient_name = api_connecter.get_study_info(i, 'PatientName')
    study_year = study_data[:4]
    study_month = study_data[4:6]
    study_day = study_data[6:]
    page.data_input(study_day + study_month + study_year)
    time.sleep(1)
    page.element_click('ok button')
    study_text = page.get_element_text('study header')
    assert patient_name in study_text, f"{study_text} instead {patient_name} The list of studies for another patient is displayed"
