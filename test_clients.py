from datetime import date
import os
import unittest
import json
from werkzeug.test import TestResponse
from api import create_app
from config import DevConfig
from test_utilities import generate_auth_token, GOOD_CLIENT_DATA

CLIENT_ID_VAR = "AUTH0_CLIENT_ADMIN"
CLIENT_SECRET_VAR = "AUTH0_SECRET_ADMIN"


class ClientTestSuite(unittest.TestCase):
    """This class performs the full suite of test cases for the CAR app"""

    @classmethod
    def setUpClass(cls) -> None:
        token_response = generate_auth_token(CLIENT_ID_VAR, CLIENT_SECRET_VAR)
        cls._auth_token = token_response.get('access_token', '')

    def setUp(self):
        self.app = create_app(DevConfig)
        self.client = self.app.test_client
        self.headers: dict = {
            "Authorization": f"Bearer {self._auth_token}"}

    def tearDown(self):
        """Executed after reach test"""
        pass

    def add_client(self, client_data) -> TestResponse:
        return self.client().post(
            '/api/clients',
            headers=self.headers,
            json=client_data)

    # =========================================================================
    # Client Tests
    # =========================================================================
    def test_add_client_success(self):

        response = self.add_client(GOOD_CLIENT_DATA)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg="The Reponse Code was not 200")
        self.assertIn(
            'success', data,
            msg="The response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg="The response did not report as successful")
        self.assertIn(
            'data', data,
            msg="The reponse did not contain the contact data")

    def test_add_client_fail(self):
        # fail - bad request data
        client_data = {
            "name": "Will Power",
            "mobile_phone": "0412987654",
            "position_title": "Test Contact",
            "client_type": "other",
            "status": "A"
        }

        response = self.add_client(client_data)

        # get the response body
        data = json.loads(response.data)

        self.assertEqual(
            response.status_code, 400,
            msg="The Reponse Code was not 400")
        self.assertIn(
            'success', data,
            msg="The response does not indicate call success")
        self.assertEqual(
            data['success'], False,
            msg="The response did not report as failed")

    def test_get_client_list_success(self):
        response = self.client().get('/api/clients', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg="Status Code was not 200")
        self.assertIn(
            'data', data,
            msg="The response does not contain a questions array")
        self.assertIn(
            'success', data,
            msg="The response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg="The success indicator is not equal to true")

    def test_get_client_list_fail(self):
        response = self.client().get('/api/clients?page=1000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 404,
            msg="Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg="The response did not report as failed")

    def test_get_client_success(self):
        # Create client to be retreived
        response = self.add_client(GOOD_CLIENT_DATA)
        client: dict = json.loads(response.data)
        client_data: dict = client.get('data')
        client_id = client_data.get('id')

        response = self.client().get(
            f"/api/clients/{client_id}",
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

    def test_get_client_fail(self):
        response = self.client().get('/api/clients/10000', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 404,
            msg="Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg="The response did not report as failed")

    def test_update_client_success(self):
        # Create client to be updated
        response = self.add_client(GOOD_CLIENT_DATA)
        client: dict = json.loads(response.data)
        client_data: dict = client.get('data')
        client_id = client_data.get('id')
        client_data['abbreviation'] = "PHS"

        response = self.client().patch(
            f"/api/clients/{client_id}",
            headers=self.headers,
            json=client_data)

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

    def test_update_client_failed(self):
        # Create client to be updated
        response = self.add_client(GOOD_CLIENT_DATA)
        client: dict = json.loads(response.data)
        client_data: dict = client.get('data')
        client_id = client_data.get('id')

        # Invalid Client Data
        client_data = {
            "name": "William Power",
            "mobile_phone": "9876543210",
            "position_title": "Test Contact",
            "client_type": "invaild_type",
            "status": "I"
        }

        response = self.client().patch(
            f'/api/clients/{client_id}', headers=self.headers, json=client_data)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 400,
            msg="Status Code was not 400")
        self.assertEqual(
            data['success'], False,
            msg="The response did not report as failed")

    def test_delete_client_success(self):
        # Create client to be deleted
        response = self.add_client(GOOD_CLIENT_DATA)
        client: dict = json.loads(response.data)
        client_data: dict = client.get('data')
        client_id = client_data.get('id')

        response = self.client().delete(
            f'/api/clients/{client_id}',
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
            msg="The reponse did not contain the deleted Id")
        self.assertEqual(
            data['id'], client_id,
            msg="The deleted contact did not match the id sent")

    def test_delete_client_fail(self):
        response = self.client().delete('/api/clients/99999', headers=self.headers)
        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 404,
            msg="Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg="The response did not report as failed")

    # =========================================================================
    # Client Contact Tests
    # =========================================================================
    def add_client_contact(self, contact_data) -> TestResponse:
        # return the response
        return self.client().post(
            f"/api/clients/{contact_data['client_id']}/contacts",
            headers=self.headers,
            json=contact_data)


    def update_client_contact(self, contact_data) -> TestResponse:
        # return the response
        return self.client().patch(
            f"/api/clients/{contact_data['client_id']}/contacts/{contact_data['id']}",
            headers=self.headers,
            json=contact_data)

    def get_first_client(self):
        # Get the list of clients
        response = self.client().get('/api/clients', headers=self.headers)
        data:dict = json.loads(response.data)
        client_list:list = data.get('data')

        # Get the first client
        client_list.reverse()
        return client_list.pop()

    def get_first_client_contact(self, client_id: int):
        # query the database for the contacts of the first client
        response = self.client().get(
            f"/api/clients/{client_id}/contacts",
            headers=self.headers)
        data:dict = json.loads(response.data)
        contact_list:list = data.get('data')

        # Get the first contact
        contact_list.reverse()
        return contact_list.pop()

    def test_add_client_contact_success(self):
        # Get the first client
        first_client = self.get_first_client()

        contact_data = {
            "name": "Will Power",
            "client_id": first_client['id'],
            "email_address": "wpower@company.com.au",
            "phone": "0412987654",
            "position_title": "Test Contact"
        }

        response = self.add_client_contact(contact_data)
        data: dict = json.loads(response.data)

        self.assertEqual(
            response.status_code, 200,
            msg="The Reponse Code was not 200.")
        self.assertIn(
            'success', data,
            msg="The response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg="The response did not report as successful")
        self.assertIn(
            'data', data,
            msg="The reponse did not contain the contact data")

    def test_add_client_contact_fail(self):
        # fails - invalid client id
        contact_data = {
            "name": "Will Power",
            "client_id": 0,
            "phone": "0412987654",
            "position_title": "Test Contact"
        }

        response = self.add_client_contact(contact_data)
        data: dict = json.loads(response.data)

        self.assertEqual(
            response.status_code, 400,
            msg="The Reponse Code was not 400")
        self.assertIn(
            'success', data,
            msg="The response does not indicate call success")
        self.assertEqual(
            data['success'], False,
            msg="The response did not report as failed")

    def test_get_client_contact_list_success(self):
        # Get first client
        first_client = self.get_first_client()

        response = self.client().get(
            f"/api/clients/{first_client['id']}/contacts",
            headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 200,
            msg="Status Code was not 200")
        self.assertIn(
            'data', data,
            msg="The response does not contain a questions array")
        self.assertIn(
            'success', data,
            msg="The response does not indicate call success")
        self.assertEqual(
            data['success'], True,
            msg="The success indicator is not equal to true")

    def test_get_client_contact_list_fail(self):
        response = self.client().get('/api/clients/99999/contacts', headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 404,
            msg="Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg="The response did not report as failed")

    def test_get_client_contact_success(self):
        # Get the first client
        first_client = self.get_first_client()
        # Get the first client contact
        first_contact = self.get_first_client_contact(first_client['id'])

        response = self.client().get(
            f"/api/clients/{first_client['id']}/contacts/{first_contact['id']}",
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

    def test_get_client_contact_fail(self):
        # Get the first client
        first_client = self.get_first_client()

        response = self.client().get(
            f"/api/clients/{first_client['id']}/contacts/9999",
            headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 404,
            msg="Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg="The response did not report as failed")


    def test_update_client_contact_success(self):
        # Get the first client
        first_client = self.get_first_client()
        first_contact = self.get_first_client_contact(first_client['id'])

        contact_data = {
            "id": first_contact['id'],
            "client_id": first_contact['client_id'],
            "name": "William Power",
            "phone": "9876543210",
            "position_title": "Test Contact",
            "email_address": "will@power.com"
        }

        # Run the update attempt
        response = self.update_client_contact(
            contact_data)
        # get the response body
        data = json.loads(response.data)
        # run the tests
        self.assertEqual(
            response.status_code, 200,
            msg="Status Code was not 200")
        self.assertEqual(
            data['success'], True,
            msg="the response did not report as successfult")
        self.assertIn(
            'data', data,
            msg="The reponse did not contain the contact data")

    def test_update_client_contact_fail(self):
        first_client = self.get_first_client()
        contact_data = {
            "id": 9999,
            "client_id": first_client['id'],
            "name": "William Power",
            "phone": "9876543210",
            "position_title": "Test Contact",
            "email_address": "will@power.com"
        }
        
        # Run the update attempt
        response = self.update_client_contact(contact_data)
        # get the response body
        data = json.loads(response.data)
        # run the tests
        self.assertEqual(
            response.status_code, 404,
            msg="Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg="The response did not report as failed")

    def test_delete_client_contact_success(self):
                # Get the first client
        first_client = self.get_first_client()
        first_contact = self.get_first_client_contact(first_client['id'])

        response = self.client().delete(
            f"/api/clients/{first_client['id']}/contacts/{first_contact['id']}",
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
            msg="The reponse did not contain the deleted Id")
        self.assertEqual(
            data['id'], first_contact['id'],
            msg="The deleted contact did not match the id sent")

    def test_delete_client_contact_fail(self):
        first_client = self.get_first_client()
        response = self.client().delete(
            f"/api/clients/{first_client['id']}/contacts/9999",
            headers=self.headers)

        # get the response body
        data = json.loads(response.data)
        self.assertEqual(
            response.status_code, 404,
            msg="Status Code was not 404")
        self.assertEqual(
            data['success'], False,
            msg="The response did not report as failed")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
