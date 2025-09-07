import pytest

element_list = ['patient id', 'patient all button', 'patient name', 'accsession number', 'list plugins']
@pytest.mark.parametrize('element_for_test',
                          element_list,
                          ids=element_list)
@pytest.mark.only
def test_presence_of_elements(page, element_for_test):
    assert page.element_in_page(element_for_test)

element_list = ['patient id', 'patient all button', 'patient name', 'accsession number', 'list plugins']
@pytest.mark.parametrize('element_for_test',
                          element_list,
                          ids=element_list)
@pytest.mark.only
def test_click_elements(page, element_for_test):
    page.open_main_page()
    assert page.element_click(element_for_test)

@pytest.mark.parametrize('element_for_test, title_sub_string',
                          [
                              ('patient all button', 'patient'),
                              ('list plugins', 'Plugins')
                          ],
                          ids=['patient all button', 'list plugins'])
@pytest.mark.only
def test_open_page_by_button(page, element_for_test, title_sub_string):
    page.open_main_page()
    assert page.element_click(element_for_test)
    page.get_title()
    assert title_sub_string in page.get_title()