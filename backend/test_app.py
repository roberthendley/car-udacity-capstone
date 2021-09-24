from datetime import date
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import Headers
from werkzeug.wrappers import response
import http
from api import create_app
from config import TestConfig

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")

# get a token to test the protected routes


def generate_access_token(client_id, client_secret):
    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
    payload = f'{{"client_id":"{client_id}}}",' \
        f'"client_secret":"{client_secret}",' \
        f'"audience":"{AUTH0_AUDIENCE}",' \
        '"grant_type":"client_credentials"}'

    headers = {'content-type': "application/json"}
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")


class FullSuiteTest(unittest.TestCase):
    """This class performs the full suite of test cases for the CAR app"""

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client

        # Get a token so that the protected end points can be reached
        auth0_client_id = os.getenv('AUTH0_CLIENT_1')
        auth0_secret = os.getenv('AUTH0_SECRET_1')
        token_dict: dict = generate_access_token(auth0_client_id, auth0_secret)
        self.headers: dict = {
            "Authorization": f"Bearer {token_dict.get('access_token')}"}
        self.contact_id = 1
        self.client_id = 1

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_contact_list_success(self):
        response = self.client().get('/api/contacts', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Get Contacts - Status Code was not 200")
        self.assertIn(
            'data', data, msg="Test: Get Contacts - the response does not contain a questions array")
        self.assertIn(
            'success', data, msg="Test: Get Contacts - the response does not indicate call success")
        self.assertEqual(
            data['success'], True, msg="Test: Get Contacts - the success indicator is not equal to true")

    def test_get_contact_list_fail(self):
        response = self.client().get('/api/contacts?page=1000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Get Contacts Fail - Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg="Test: Get Contacts Fail - the response did not report as failed")

    def test_add_contact_success(self):
        contact_data = {
            "name": "Will Power",
            "email_address": "wpower@company.com.au",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "contact_type": "other",
            "status": "A"
        }

        response = self.client().post(
            '/api/contacts', headers=self.headers, json=contact_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200,
                         msg="The Reponse Code was not 200")
        self.assertIn(
            'success', data, msg="Test: Get Contacts - the response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg="Test: Add Contact Success - the response did not report as successful")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

        self.contact_id = data.get('id', default=1)

    def test_add_contact_fail(self):
        contact_data = {
            "name": "Will Power",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "contact_type": "other",
            "status": "A"
        }

        response = self.client().post(
            '/api/contacts', headers=self.headers, json=contact_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400,
                         msg="The Reponse Code was not 400")
        self.assertIn(
            'success', data, msg="Test: Get Contacts - the response does not indicate call success")
        self.assertEqual(
            data['success'], False,
            msg="Test: Get Contacts Fail - the response did not report as failed")

    def test_get_contact_success(self):
        response = self.client().get(
            f'/api/contacts/{self.contact_id}', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Get Contact Success - Status Code was not 200")
        self.assertEqual(data['success'], True,
                         msg="Test: Get Contacts Success - the response did not report as successful")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

    def test_get_contact_fail(self):
        response = self.client().get('/api/contacts/10000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Get Contacts Fail 404 - Status Code was not 404")
        self.assertEqual(data['success'], False,
                         msg="Test: Get Contacts Fail 404 - the response did not report as failed")

    def test_update_contact_success(self):
        contact_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "contact_type": "other",
            "status": "I"
        }

        response = self.client().patch(
            f'/api/contacts/{self.contact_id}', headers=self.headers, json=contact_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Update Contact Success - Status Code was not 200")
        self.assertEqual(data['success'], True,
                         msg="Test: Update Contacts Success - the response did not report as successfult")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

    def test_update_contact_failed(self):
        contact_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "contact_type": "invaild_type",
            "status": "I"
        }

        response = self.client().patch(
            f'/api/contacts/{self.contact_id}', headers=self.headers, json=contact_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400,
                         msg="Test: Update Contact Success - Status Code was not 400")
        self.assertEqual(data['success'], False,
                         msg="Test: Update Contacts Success - the response did not report as failed")

    def test_delete_contact_success(self):
        response = self.client().delete(
            f'/api/contacts/{self.contact_id}', headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Delete Contact - Status Code was not 200")
        self.assertEqual(
            data['success'], True, msg="Test: Delete Contact - the response did not report as successful")
        self.assertIn(
            'id', data, msg="The reponse did not contain the deeleted Id")
        self.assertEqual(
            data['id'], self.contact_id, msg="Test: Delete Contact - the deleted contact did not match the id sent")

    def test_delete_contact_fail(self):
        response = self.client().delete('/api/contacts/99', headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Delete Contact - Status Code was not 404")
        self.assertEqual(
            data['success'], False, msg="Test: Delete Contact - the response did not report as failed")

    # -------------------------------------------------------------------------
    # Client Tests
    # -------------------------------------------------------------------------
    def test_get_client_list_success(self):
        response = self.client().get('/api/clients', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Get clients - Status Code was not 200")
        self.assertIn(
            'data', data, msg="Test: Get clients - the response does not contain a questions array")
        self.assertIn(
            'success', data, msg="Test: Get clients - the response does not indicate call success")
        self.assertEqual(
            data['success'], True, msg="Test: Get clients - the success indicator is not equal to true")

    def test_get_client_list_fail(self):
        response = self.client().get('/api/clients?page=1000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Get clients Fail - Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg="Test: Get clients Fail - the response did not report as failed")

    def test_add_client_success(self):
        client_data = {
            "name": "Will Power",
            "email_address": "wpower@company.com.au",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "client_type": "other",
            "status": "A"
        }

        response = self.client().post(
            '/api/clients', headers=self.headers, json=client_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200,
                         msg="The Reponse Code was not 200")
        self.assertIn(
            'success', data, msg="Test: Get clients - the response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg="Test: Add Contact Success - the response did not report as successful")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

        self.client_id = data.get('id', default=1)

    def test_add_client_fail(self):
        client_data = {
            "name": "Will Power",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "client_type": "other",
            "status": "A"
        }

        response = self.client().post(
            '/api/clients', headers=self.headers, json=client_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400,
                         msg="The Reponse Code was not 400")
        self.assertIn(
            'success', data, msg="Test: Get clients - the response does not indicate call success")
        self.assertEqual(
            data['success'], False,
            msg="Test: Get clients Fail - the response did not report as failed")

    def test_get_client_success(self):
        response = self.client().get(
            f'/api/clients/{self.client_id}', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Get Contact Success - Status Code was not 200")
        self.assertEqual(data['success'], True,
                         msg="Test: Get clients Success - the response did not report as successful")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

    def test_get_client_fail(self):
        response = self.client().get('/api/clients/10000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Get clients Fail 404 - Status Code was not 404")
        self.assertEqual(data['success'], False,
                         msg="Test: Get clients Fail 404 - the response did not report as failed")

    def test_update_client_success(self):
        client_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "client_type": "other",
            "status": "I"
        }

        response = self.client().patch(
            f'/api/clients/{self.client_id}', headers=self.headers, json=client_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Update Contact Success - Status Code was not 200")
        self.assertEqual(data['success'], True,
                         msg="Test: Update clients Success - the response did not report as successfult")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

    def test_update_client_failed(self):
        client_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "client_type": "invaild_type",
            "status": "I"
        }

        response = self.client().patch(
            f'/api/clients/{self.client_id}', headers=self.headers, json=client_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400,
                         msg="Test: Update Contact Success - Status Code was not 400")
        self.assertEqual(data['success'], False,
                         msg="Test: Update clients Success - the response did not report as failed")

    def test_delete_client_success(self):
        response = self.client().delete(
            f'/api/clients/{self.client_id}', headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Delete Contact - Status Code was not 200")
        self.assertEqual(
            data['success'], True, msg="Test: Delete Contact - the response did not report as successful")
        self.assertIn(
            'id', data, msg="The reponse did not contain the deeleted Id")
        self.assertEqual(
            data['id'], self.client_id, msg="Test: Delete Contact - the deleted contact did not match the id sent")

    def test_delete_client_fail(self):
        response = self.client().delete('/api/clients/99', headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Delete Contact - Status Code was not 404")
        self.assertEqual(
            data['success'], False, msg="Test: Delete Contact - the response did not report as failed")

    # -------------------------------------------------------------------------
    # Client Contact Tests
    # -------------------------------------------------------------------------
    def test_get_client_contact_list_success(self):
        response = self.client().get('/api/clients/1/contacts', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Get clients - Status Code was not 200")
        self.assertIn(
            'data', data, msg="Test: Get clients - the response does not contain a questions array")
        self.assertIn(
            'success', data, msg="Test: Get clients - the response does not indicate call success")
        self.assertEqual(
            data['success'], True, msg="Test: Get clients - the success indicator is not equal to true")

    def test_get_client_contact_list_fail(self):
        response = self.client().get('/api/clients/1/contacts?page=1000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Get clients Fail - Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg="Test: Get clients Fail - the response did not report as failed")

    def test_add_client_contact_success(self):
        client_data = {
            "name": "Will Power",
            "email_address": "wpower@company.com.au",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "client_type": "other",
            "status": "A"
        }

        response = self.client().post(
            '/api/clients', headers=self.headers, json=client_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200,
                         msg="The Reponse Code was not 200")
        self.assertIn(
            'success', data, msg="Test: Get clients - the response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg="Test: Add Contact Success - the response did not report as successful")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

        self.client_id = data.get('id', default=1)

    def test_add_client_fail(self):
        client_data = {
            "name": "Will Power",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "client_type": "other",
            "status": "A"
        }

        response = self.client().post(
            '/api/clients', headers=self.headers, json=client_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400,
                         msg="The Reponse Code was not 400")
        self.assertIn(
            'success', data, msg="Test: Get clients - the response does not indicate call success")
        self.assertEqual(
            data['success'], False,
            msg="Test: Get clients Fail - the response did not report as failed")

    def test_get_client_success(self):
        response = self.client().get(
            f'/api/clients/{self.client_id}', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Get Contact Success - Status Code was not 200")
        self.assertEqual(data['success'], True,
                         msg="Test: Get clients Success - the response did not report as successful")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

    def test_get_client_fail(self):
        response = self.client().get('/api/clients/10000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Get clients Fail 404 - Status Code was not 404")
        self.assertEqual(data['success'], False,
                         msg="Test: Get clients Fail 404 - the response did not report as failed")

    def test_update_client_success(self):
        client_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "client_type": "other",
            "status": "I"
        }

        response = self.client().patch(
            f'/api/clients/{self.client_id}', headers=self.headers, json=client_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Update Contact Success - Status Code was not 200")
        self.assertEqual(data['success'], True,
                         msg="Test: Update clients Success - the response did not report as successfult")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

    def test_update_client_failed(self):
        client_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "client_type": "invaild_type",
            "status": "I"
        }

        response = self.client().patch(
            f'/api/clients/{self.client_id}', headers=self.headers, json=client_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400,
                         msg="Test: Update Contact Success - Status Code was not 400")
        self.assertEqual(data['success'], False,
                         msg="Test: Update clients Success - the response did not report as failed")

    def test_delete_client_success(self):
        response = self.client().delete(
            f'/api/clients/{self.client_id}', headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Delete Contact - Status Code was not 200")
        self.assertEqual(
            data['success'], True, msg="Test: Delete Contact - the response did not report as successful")
        self.assertIn(
            'id', data, msg="The reponse did not contain the deeleted Id")
        self.assertEqual(
            data['id'], self.client_id, msg="Test: Delete Contact - the deleted contact did not match the id sent")

    def test_delete_client_fail(self):
        response = self.client().delete('/api/clients/99', headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Delete Contact - Status Code was not 404")
        self.assertEqual(
            data['success'], False, msg="Test: Delete Contact - the response did not report as failed")


class ClientMgrTest(unittest.TestCase):
    """This class performs the client manager suite of test cases for the CAR app"""

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client

        client_id = os.getenv('AUTH0_CLIENT_2')
        secret = os.getenv('AUTH0_SECRET_2')

        # Get a token so that the protected end points can be reached
        token_dict: dict = generate_access_token(client_id, secret)
        self.headers: dict = {
            "Authorization": f"Bearer {token_dict.get('access_token')}"}
        self.contact_id = 1
        self.client_id = 1

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_contact_list_success(self):
        response = self.client().get('/api/contacts', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Get Contacts - Status Code was not 200")
        self.assertIn(
            'data', data, msg="Test: Get Contacts - the response does not contain a questions array")
        self.assertIn(
            'success', data, msg="Test: Get Contacts - the response does not indicate call success")
        self.assertEqual(
            data['success'], True, msg="Test: Get Contacts - the success indicator is not equal to true")

    def test_get_contact_list_fail(self):
        response = self.client().get('/api/contacts?page=1000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Get Contacts Fail - Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg="Test: Get Contacts Fail - the response did not report as failed")

    def test_add_contact_success(self):
        contact_data = {
            "name": "Will Power",
            "email_address": "wpower@company.com.au",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "contact_type": "other",
            "status": "A"
        }

        response = self.client().post(
            '/api/contacts', headers=self.headers, json=contact_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200,
                         msg="The Reponse Code was not 200")
        self.assertIn(
            'success', data, msg="Test: Get Contacts - the response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg="Test: Add Contact Success - the response did not report as successful")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

        self.contact_id = data.get('id', default=1)

    def test_add_contact_fail(self):
        contact_data = {
            "name": "Will Power",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "contact_type": "other",
            "status": "A"
        }

        response = self.client().post(
            '/api/contacts', headers=self.headers, json=contact_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400,
                         msg="The Reponse Code was not 400")
        self.assertIn(
            'success', data, msg="Test: Get Contacts - the response does not indicate call success")
        self.assertEqual(
            data['success'], False,
            msg="Test: Get Contacts Fail - the response did not report as failed")

    def test_get_contact_success(self):
        response = self.client().get(
            f'/api/contacts/{self.contact_id}', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Get Contact Success - Status Code was not 200")
        self.assertEqual(data['success'], True,
                         msg="Test: Get Contacts Success - the response did not report as successful")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

    def test_get_contact_fail(self):
        response = self.client().get('/api/contacts/10000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Get Contacts Fail 404 - Status Code was not 404")
        self.assertEqual(data['success'], False,
                         msg="Test: Get Contacts Fail 404 - the response did not report as failed")

    def test_update_contact_success(self):
        contact_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "contact_type": "other",
            "status": "I"
        }

        response = self.client().patch(
            f'/api/contacts/{self.contact_id}', headers=self.headers, json=contact_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Update Contact Success - Status Code was not 200")
        self.assertEqual(data['success'], True,
                         msg="Test: Update Contacts Success - the response did not report as successfult")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

    def test_update_contact_failed(self):
        contact_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "contact_type": "invaild_type",
            "status": "I"
        }

        response = self.client().patch(
            f'/api/contacts/{self.contact_id}', headers=self.headers, json=contact_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400,
                         msg="Test: Update Contact Success - Status Code was not 400")
        self.assertEqual(data['success'], False,
                         msg="Test: Update Contacts Success - the response did not report as failed")

    def test_delete_contact_success(self):
        response = self.client().delete(
            f'/api/contacts/{self.contact_id}', headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Delete Contact - Status Code was not 200")
        self.assertEqual(
            data['success'], True, msg="Test: Delete Contact - the response did not report as successful")
        self.assertIn(
            'id', data, msg="The reponse did not contain the deeleted Id")
        self.assertEqual(
            data['id'], self.contact_id, msg="Test: Delete Contact - the deleted contact did not match the id sent")

    def test_delete_contact_fail(self):
        response = self.client().delete('/api/contacts/99', headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Delete Contact - Status Code was not 404")
        self.assertEqual(
            data['success'], False, msg="Test: Delete Contact - the response did not report as failed")

    # -------------------------------------------------------------------------
    # Client Tests
    # -------------------------------------------------------------------------
    def test_get_client_list_success(self):
        response = self.client().get('/api/clients', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Get clients - Status Code was not 200")
        self.assertIn(
            'data', data, msg="Test: Get clients - the response does not contain a questions array")
        self.assertIn(
            'success', data, msg="Test: Get clients - the response does not indicate call success")
        self.assertEqual(
            data['success'], True, msg="Test: Get clients - the success indicator is not equal to true")

    def test_get_client_list_fail(self):
        response = self.client().get('/api/clients?page=1000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Get clients Fail - Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg="Test: Get clients Fail - the response did not report as failed")

    def test_add_client_success(self):
        client_data = {
            "name": "Will Power",
            "email_address": "wpower@company.com.au",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "client_type": "other",
            "status": "A"
        }

        response = self.client().post(
            '/api/clients', headers=self.headers, json=client_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200,
                         msg="The Reponse Code was not 200")
        self.assertIn(
            'success', data, msg="Test: Get clients - the response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg="Test: Add Contact Success - the response did not report as successful")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

        self.client_id = data.get('id', default=1)

    def test_add_client_fail(self):
        client_data = {
            "name": "Will Power",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "client_type": "other",
            "status": "A"
        }

        response = self.client().post(
            '/api/clients', headers=self.headers, json=client_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400,
                         msg="The Reponse Code was not 400")
        self.assertIn(
            'success', data, msg="Test: Get clients - the response does not indicate call success")
        self.assertEqual(
            data['success'], False,
            msg="Test: Get clients Fail - the response did not report as failed")

    def test_get_client_success(self):
        response = self.client().get(
            f'/api/clients/{self.client_id}', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Get Contact Success - Status Code was not 200")
        self.assertEqual(data['success'], True,
                         msg="Test: Get clients Success - the response did not report as successful")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

    def test_get_client_fail(self):
        response = self.client().get('/api/clients/10000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Get clients Fail 404 - Status Code was not 404")
        self.assertEqual(data['success'], False,
                         msg="Test: Get clients Fail 404 - the response did not report as failed")

    def test_update_client_success(self):
        client_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "client_type": "other",
            "status": "I"
        }

        response = self.client().patch(
            f'/api/clients/{self.client_id}', headers=self.headers, json=client_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Update Contact Success - Status Code was not 200")
        self.assertEqual(data['success'], True,
                         msg="Test: Update clients Success - the response did not report as successfult")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

    def test_update_client_failed(self):
        client_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "client_type": "invaild_type",
            "status": "I"
        }

        response = self.client().patch(
            f'/api/clients/{self.client_id}', headers=self.headers, json=client_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400,
                         msg="Test: Update Contact Success - Status Code was not 400")
        self.assertEqual(data['success'], False,
                         msg="Test: Update clients Success - the response did not report as failed")

    def test_delete_client_success(self):
        response = self.client().delete(
            f'/api/clients/{self.client_id}', headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Delete Contact - Status Code was not 200")
        self.assertEqual(
            data['success'], True, msg="Test: Delete Contact - the response did not report as successful")
        self.assertIn(
            'id', data, msg="The reponse did not contain the deeleted Id")
        self.assertEqual(
            data['id'], self.client_id, msg="Test: Delete Contact - the deleted contact did not match the id sent")

    def test_delete_client_fail(self):
        response = self.client().delete('/api/clients/99', headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Delete Contact - Status Code was not 404")
        self.assertEqual(
            data['success'], False, msg="Test: Delete Contact - the response did not report as failed")


class ConsultantTest(unittest.TestCase):
    """This class performs the client manager suite of test cases for the CAR app"""

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client

        client_id = os.getenv('AUTH0_CLIENT_3')
        secret = os.getenv('AUTH0_SECRET_3')

        # Get a token so that the protected end points can be reached
        token_dict: dict = generate_access_token(client_id, secret)
        self.headers: dict = {
            "Authorization": f"Bearer {token_dict.get('access_token')}"}
        self.contact_id = 1
        self.client_id = 1

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_contact_list_success(self):
        response = self.client().get('/api/contacts', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Get Contacts - Status Code was not 200")
        self.assertIn(
            'data', data, msg="Test: Get Contacts - the response does not contain a questions array")
        self.assertIn(
            'success', data, msg="Test: Get Contacts - the response does not indicate call success")
        self.assertEqual(
            data['success'], True, msg="Test: Get Contacts - the success indicator is not equal to true")

    def test_get_contact_list_fail(self):
        response = self.client().get('/api/contacts?page=1000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Get Contacts Fail - Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg="Test: Get Contacts Fail - the response did not report as failed")

    def test_add_contact_success(self):
        contact_data = {
            "name": "Will Power",
            "email_address": "wpower@company.com.au",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "contact_type": "other",
            "status": "A"
        }

        response = self.client().post(
            '/api/contacts', headers=self.headers, json=contact_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200,
                         msg="The Reponse Code was not 200")
        self.assertIn(
            'success', data, msg="Test: Get Contacts - the response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg="Test: Add Contact Success - the response did not report as successful")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

        self.contact_id = data.get('id', default=1)

    def test_add_contact_fail(self):
        contact_data = {
            "name": "Will Power",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "contact_type": "other",
            "status": "A"
        }

        response = self.client().post(
            '/api/contacts', headers=self.headers, json=contact_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400,
                         msg="The Reponse Code was not 400")
        self.assertIn(
            'success', data, msg="Test: Get Contacts - the response does not indicate call success")
        self.assertEqual(
            data['success'], False,
            msg="Test: Get Contacts Fail - the response did not report as failed")

    def test_get_contact_success(self):
        response = self.client().get(
            f'/api/contacts/{self.contact_id}', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Get Contact Success - Status Code was not 200")
        self.assertEqual(data['success'], True,
                         msg="Test: Get Contacts Success - the response did not report as successful")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

    def test_get_contact_fail(self):
        response = self.client().get('/api/contacts/10000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Get Contacts Fail 404 - Status Code was not 404")
        self.assertEqual(data['success'], False,
                         msg="Test: Get Contacts Fail 404 - the response did not report as failed")

    def test_update_contact_success(self):
        contact_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "contact_type": "other",
            "status": "I"
        }

        response = self.client().patch(
            f'/api/contacts/{self.contact_id}', headers=self.headers, json=contact_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Update Contact Success - Status Code was not 200")
        self.assertEqual(data['success'], True,
                         msg="Test: Update Contacts Success - the response did not report as successfult")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

    def test_update_contact_failed(self):
        contact_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "contact_type": "invaild_type",
            "status": "I"
        }

        response = self.client().patch(
            f'/api/contacts/{self.contact_id}', headers=self.headers, json=contact_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400,
                         msg="Test: Update Contact Success - Status Code was not 400")
        self.assertEqual(data['success'], False,
                         msg="Test: Update Contacts Success - the response did not report as failed")

    def test_delete_contact_success(self):
        response = self.client().delete(
            f'/api/contacts/{self.contact_id}', headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Delete Contact - Status Code was not 200")
        self.assertEqual(
            data['success'], True, msg="Test: Delete Contact - the response did not report as successful")
        self.assertIn(
            'id', data, msg="The reponse did not contain the deeleted Id")
        self.assertEqual(
            data['id'], self.contact_id, msg="Test: Delete Contact - the deleted contact did not match the id sent")

    def test_delete_contact_fail(self):
        response = self.client().delete('/api/contacts/99', headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Delete Contact - Status Code was not 404")
        self.assertEqual(
            data['success'], False, msg="Test: Delete Contact - the response did not report as failed")

    # -------------------------------------------------------------------------
    # Client Tests
    # -------------------------------------------------------------------------
    def test_get_client_list_success(self):
        response = self.client().get('/api/clients', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Get clients - Status Code was not 200")
        self.assertIn(
            'data', data, msg="Test: Get clients - the response does not contain a questions array")
        self.assertIn(
            'success', data, msg="Test: Get clients - the response does not indicate call success")
        self.assertEqual(
            data['success'], True, msg="Test: Get clients - the success indicator is not equal to true")

    def test_get_client_list_fail(self):
        response = self.client().get('/api/clients?page=1000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Get clients Fail - Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg="Test: Get clients Fail - the response did not report as failed")

    def test_add_client_success(self):
        client_data = {
            "name": "Will Power",
            "email_address": "wpower@company.com.au",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "client_type": "other",
            "status": "A"
        }

        response = self.client().post(
            '/api/clients', headers=self.headers, json=client_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200,
                         msg="The Reponse Code was not 200")
        self.assertIn(
            'success', data, msg="Test: Get clients - the response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg="Test: Add Contact Success - the response did not report as successful")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

        self.client_id = data.get('id', default=1)

    def test_add_client_fail(self):
        client_data = {
            "name": "Will Power",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "client_type": "other",
            "status": "A"
        }

        response = self.client().post(
            '/api/clients', headers=self.headers, json=client_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400,
                         msg="The Reponse Code was not 400")
        self.assertIn(
            'success', data, msg="Test: Get clients - the response does not indicate call success")
        self.assertEqual(
            data['success'], False,
            msg="Test: Get clients Fail - the response did not report as failed")

    def test_get_client_success(self):
        response = self.client().get(
            f'/api/clients/{self.client_id}', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Get Contact Success - Status Code was not 200")
        self.assertEqual(data['success'], True,
                         msg="Test: Get clients Success - the response did not report as successful")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

    def test_get_client_fail(self):
        response = self.client().get('/api/clients/10000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Get clients Fail 404 - Status Code was not 404")
        self.assertEqual(data['success'], False,
                         msg="Test: Get clients Fail 404 - the response did not report as failed")

    def test_update_client_success(self):
        client_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "client_type": "other",
            "status": "I"
        }

        response = self.client().patch(
            f'/api/clients/{self.client_id}', headers=self.headers, json=client_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200,
                         msg="Test: Update Contact Success - Status Code was not 200")
        self.assertEqual(data['success'], True,
                         msg="Test: Update clients Success - the response did not report as successfult")
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

    def test_update_client_failed(self):
        client_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "client_type": "invaild_type",
            "status": "I"
        }

        response = self.client().patch(
            f'/api/clients/{self.client_id}', headers=self.headers, json=client_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400,
                         msg="Test: Update Contact Success - Status Code was not 400")
        self.assertEqual(data['success'], False,
                         msg="Test: Update clients Success - the response did not report as failed")

    def test_delete_client_fail(self):
        response = self.client().delete('/api/clients/99', headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404,
                         msg="Test: Delete Contact - Status Code was not 404")
        self.assertEqual(
            data['success'], False, msg="Test: Delete Contact - the response did not report as failed")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
