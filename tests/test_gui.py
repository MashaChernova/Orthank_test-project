import pytest
#response_list = ['changes', 'exports','tools', 'statistics','instances', 'modalities', 'patients', 'peers', 'plugins', 'series', 'studies'] # ,'instances', 'modalities', 'patients', 'peers', 'plugins', 'series', 'studies'
# @pytest.mark.parametrize('response_for_test',
#                          response_list,
#                          ids=response_list)
@pytest.mark.only
def test_presence_of_elements(page):
    assert page.element_in_page('patient_id')