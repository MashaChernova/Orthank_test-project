from gc import get_objects

import requests
import json
import pytest
import logging
import random

class RestApiConnecter():

    def __init__(self, url):
        self.url = url

    def response_status_ok(self, response_for_test):
        response = requests.request("GET", self.url + response_for_test)
        try:
            if response.ok:
                return True
            else:
                raise AssertionError(f'The report contains an error, response code: {response.status_code}')
        except:
            raise AssertionError('Failed to get response status')

    def message_response(self, response_for_test):
        logging.info("massage response funktion")
        response = requests.request("GET", self.url + response_for_test)
        assert response.ok
        try:
            return response.json()
        except:
            raise AssertionError("Unable to read response text")

    def instance_for_id(self, get_list_response, function_name):
        try:
            list_responce = requests.request("GET", self.url + get_list_response)
        except:
            raise AssertionError(f'No response from the server to the request {self.url + get_list_response} was received')
        try:
            list_lenth = len(list_responce.json())
            if function_name == "random":
                logging.info('Getting a random value from a list')
                id = random.randint(0, list_lenth-1)
            else:
                logging.info('Getting first value from a list')
                id=0
            logging.info(f"id={id}")
        except:
            raise AssertionError("The answer is not a list")
        try:
            get_instanse_response = get_list_response + f"/{id}"
            logging.info(f'new requests: {get_instanse_response}')
            instance_for_id = requests.request("GET", self.url + get_instanse_response)
        except:
            raise AssertionError(f"Unable to retrieve response for request {self.url + get_instanse_response}")
        try:
            assert instance_for_id.ok
            return instance_for_id.json() #.get('message')
        except:
            raise AssertionError(f'Failed to extract json from response {self.url + get_instanse_response} {id}/{list_lenth} in {list_responce.json()}')




#https://orthanc.uclouvain.be/demo/changes