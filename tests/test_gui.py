import pytest

element_list = ['patient id', 'patient all button', 'patient name', 'accsession number']
@pytest.mark.parametrize('element_for_test',
                          element_list,
                          ids=element_list)
@pytest.mark.only
def test_presence_of_elements(page, element_for_test):
    assert page.element_in_page(element_for_test)