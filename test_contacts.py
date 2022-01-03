import os
import unittest
import json
from werkzeug.test import TestResponse
from api.api import create_app
from config import DevConfig
from test_utilities import generate_auth_token, GOOD_CONTACT_DATA

CLIENT_ID_VAR = "AUTH0_CLIENT_ADMIN"
CLIENT_SECRET_VAR = "AUTH0_SECRET_ADMIN"

class ContactTestSuite(unittest.TestCase):
    """This class performs the full suite of test cases for the CAR app"""

    @classmethod
    def setUpClass(cls) -> None:
        cls._auth_token = generate_auth_token(CLIENT_ID_VAR, CLIENT_SECRET_VAR).get('access_token')

    def setUp(self):
        self.app = create_app(DevConfig)
        self.client = self.app.test_client
        self.headers: dict = {
            "Authorization": f"Bearer {self._auth_token}"}

    def tearDown(self):
        """Executed after reach test"""
        pass

    # =========================================================================
    # Internal Contact Tests
    # =========================================================================
    def add_contact(self, contact_data) -> TestResponse:
        return self.client().post(
            '/api/contacts',
            headers=self.headers,
            json=contact_data)

    def test_add_contact_success(self):
        
        response = self.add_contact(GOOD_CONTACT_DATA)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(
            response.status_code, 200,
            msg="The Reponse Code was not 200"
        )
        self.assertIn(
            'success', data,
            msg="The response does not indicate call success"
        )
        self.assertEqual(
            data['success'], True,
            msg="The response did not report as successful"
        )
        self.assertIn(
            'data', data, msg="The reponse did not contain the contact data")

    def test_add_contact_fail(self):
        # fails - no contact type
        contact_data = {
            "name": "Will Power",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "status": "A"
        }

        response = self.add_contact(contact_data)
        # get the response body
        data = json.loads(response.data)

        self.assertEqual(
            response.status_code, 400,
            msg=f"The Reponse Code was not 400")
        self.assertIn(
            'success', data,
            msg=f"The response does not indicate call success")
        self.assertEqual(
            data['success'], False,
            msg=f"The response did not report as failed")

    def test_get_contact_list_success(self):
        response = self.client().get('/api/contacts', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg="Status Code was not 200")
        self.assertIn(
            'data', data,
            msg="The response does not contain a questions array")
        self.assertIn(
            'success', data, msg="The response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg="The success indicator is not equal to true")

    def test_get_contact_list_fail(self):
        response = self.client().get('/api/contacts?page=1000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 404,
            msg="Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg="The response did not report as failed")

    def test_get_contact_success(self):

        contact_response = self.add_contact(GOOD_CONTACT_DATA)
        contact = json.loads(contact_response.data)
        contact_id = contact.get('data').get('id')
        response = self.client().get(
            f'/api/contacts/{contact_id}',
            headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg="Status Code was not 200")
        self.assertEqual(
            data['success'], True,
            msg="The response did not report as successful")
        self.assertIn(
            'data', data,
            msg="The reponse did not contain the contact data")

    def test_get_contact_fail(self):
        test_name = "Test: Get Contact fail"
        response = self.client().get('/api/contacts/10000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 404,
            msg=f"{test_name} - Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg=f"{test_name} - The response did not report as failed")

    def test_update_contact_success(self):

        # Create the contact to be updated
        contact_response = self.add_contact(GOOD_CONTACT_DATA)
        contact = json.loads(contact_response.data)
        contact_data:dict = contact.get('data')
        contact_id = contact_data.get('id')
        print(contact_id)

        contact_data = {
            "name": "William Power",
            "email_address": "wpower@company.com.au",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "contact_type": "other",
            "status": "I"
        }

        response = self.client().patch(
            f'/api/contacts/{contact_id}',
            headers=self.headers,
            json=contact_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg="Status Code was not 200")
        self.assertEqual(
            data['success'], True,
            msg="The response did not report as successfult")
        self.assertIn(
            'data', data,
            msg="The reponse did not contain the contact data")

    def test_update_contact_failed(self):

        # Create the contact to be updated
        contact_response = self.add_contact(GOOD_CONTACT_DATA)
        contact = json.loads(contact_response.data)
        contact_data:dict = contact.get('data')
        contact_id = contact_data.get('id')

        contact_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "contact_type": "invaild_type",
            "status": "I"
        }
        test_name = "Test: Update Contact fail"
        response = self.client().patch(
            f'/api/contacts/{contact_id}', headers=self.headers, json=contact_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 400,
            msg=f"{test_name} - Status Code was not 400")
        self.assertEqual(
            data['success'], False,
            msg=f"{test_name} - The response did not report as failed")

    def test_delete_contact_success(self):

        # Create the contact to be deleted
        contact_response = self.add_contact(GOOD_CONTACT_DATA)
        contact = json.loads(contact_response.data)
        contact_data:dict = contact.get('data')
        contact_id = contact_data.get('id')

        response = self.client().delete(
            f'/api/contacts/{contact_id}',
            headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg="Status Code was not 200")
        self.assertEqual(
            data['success'], True,
            msg="The response did not report as successful")
        self.assertIn(
            'id', data,
            msg="The reponse did not contain the deeleted Id")
        self.assertEqual(
            data['id'], contact_id,
            msg="The deleted contact did not match the id sent")

    def test_delete_contact_fail(self):
        response = self.client().delete(
            '/api/contacts/99',
            headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 404,
            msg="Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg="the response did not report as failed")

    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
