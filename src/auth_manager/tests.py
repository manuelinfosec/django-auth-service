from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse_lazy

# TODO: Collect test passwords from environment

class RegistrationTests(APITestCase):
    def setUp(self):
        # Setting up the URL for user registration
        self.register_user_url = reverse_lazy("register_user")

    def test_create_account(self):
        # Attempt to create an account with incomplete data
        data = {"username": "user1", "password": "password"}
        response = self.client.post(self.register_user_url, data, format="json")
        # Expect a validation error due to missing fields
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_account_missed_fields(self):
        # Attempt to create an account with missing fields
        data = {"password": "password"}
        response = self.client.post(self.register_user_url, data, format="json")
        # Expect a validation error and ensure that 'username' is in the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        # Ensure that 'password' is not in the response
        self.assertNotIn("password", response.data)

        # Attempt to create an account with a missing 'username'
        data = {"username": "username"}
        response = self.client.post(self.register_user_url, data, format="json")
        # Expect a validation error and ensure that 'username' is not in the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("username", response.data)
        # Ensure that 'password' is in the response
        self.assertIn("password", response.data)

        # Attempt to create an account with no data
        data = {}
        response = self.client.post(self.register_user_url, data, format="json")
        # Expect a validation error and ensure that both 'username' and 'password' are in the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertIn("username", response.data)

    def test_create_existing_username(self):
        # Attempt to create an account with an existing username
        # First, create an account with the same username and password
        self.test_create_account()
        data = {"username": "user1", "password": "password"}
        response = self.client.post(self.register_user_url, data, format="json")
        # Expect a validation error related to the existing username
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("A user with that username already exists", str(response.data.get("username")[0]))

    def test_create_password_blank(self):
        # Attempt to create an account with a blank password
        data = {"username": "user1", "password": ""}
        response = self.client.post(self.register_user_url, data, format="json")
        # Expect a validation error related to the blank password
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field may not be blank", str(response.data.get("password")[0]))


class Logintests(APITestCase):
    def setUp(self):
        # Set up a user account for login tests
        register_user_url = reverse_lazy("register_user")
        data = {"username": "user1", "password": "password"}
        _ = self.client.post(register_user_url, data, format="json")
        # Setting up the URL for user login
        self.login_user_url = reverse_lazy("login_user")

    def test_login(self):
        # Attempt to log in with correct credentials
        data = {"username": "user1", "password": "password"}
        response = self.client.post(self.login_user_url, data, format="json")
        # Expect successful login without returning a token
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("token", response.data)

    def test_login_wrong_credentials(self):
        # Attempt to log in with incorrect credentials
        data = {"username": "user1", "password": "wrong_password"}
        response = self.client.post(self.login_user_url, data, format="json")
        # Expect login failure with no token returned
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", response.data)

class VerifyTokenTests(APITestCase):
    """
    This test case checks the functionality of verifying and refreshing tokens.
    """
    def setUp(self):
        # Set up a user account for token verification tests
        register_user_url = reverse_lazy('register_user')
        data = {'username': 'user1', 'password': 'password'}
        # Create a user account and get the response with the token
        self.response_with_token = self.client.post(register_user_url, data, format='json')
        # Setting up the URL for token verification
        self.verify_token_url = reverse_lazy('verify_token')

    def test_verify_token(self):
        # Attempt to verify a valid token
        data = {'token': self.response_with_token.data.get('token', '')}
        response = self.client.post(self.verify_token_url, data, format='json')
        # Expect a successful token verification with a new token returned
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

    def test_verify_token_fail(self):
        # Attempt to verify an invalid token
        data = {'token': 'wrong token'}
        response = self.client.post(self.verify_token_url, data, format='json')
        # Expect token verification failure
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_token(self):
        # Attempt to refresh a valid token
        refresh_token_url = reverse_lazy('refresh_token')
        data = {'token': self.response_with_token.data.get('token', '')}
        response = self.client.post(refresh_token_url, data, format='json')
        # Expect successful token refresh with a new token returned
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)


class AccessSecureResourceTests(APITestCase):
    def setUp(self):
        # Set up a user account for accessing a secure resource
        register_user_url = reverse_lazy('register_user')
        data = {'username': 'user1', 'password': 'password'}
        response = self.client.post(register_user_url, data, format='json')
        self.token = response.data.get('token')
        # Setting up the URL for the secure resource
        self.secure_resource_url = reverse_lazy('secure_endpoint')

    def test_access_secure_resource(self):
        # Attempt to access a secure resource with a valid token
        response = self.client.get(self.secure_resource_url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        # Expect successful access to the secure resource
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('ok', response.data)

    def test_fail_access_secure_resource(self):
        # Attempt to access a secure resource with an invalid token
        response = self.client.get(self.secure_resource_url, HTTP_AUTHORIZATION=f'Bearer invalid_token')
        # Expect access failure to the secure resource
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('ok', response.data)


class UserUpdateTests(APITestCase):
    def setUp(self):
        # Set up a user account for updating user information
        register_user_url = reverse_lazy('register_user')
        data = {'username': 'user1', 'password': 'password'}
        response = self.client.post(register_user_url, data, format='json')
        self.token = response.data.get('token')
        # Setting up the URL for managing user information
        self.user_url = reverse_lazy('manage_user')

    def test_user_get_own_info(self):
        # Attempt to get information about the user using a valid token
        response = self.client.get(self.user_url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        # Expect successful retrieval of user information
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)

    def test_user_update(self):
        # Attempt to update the user's information using a valid token
        new_first_name = 'new_first_name'
        data = {'first_name': new_first_name}
        response = self.client.patch(self.user_url, data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        # Expect successful update of user information
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('new_first_name', response.data.get('first_name'))

    def test_user_update_fail(self):
        # Attempt to update the user's information with an invalid token
        response = self.client.patch(self.user_url, data={}, HTTP_AUTHORIZATION=f'Bearer invalid_token')
        # Expect update failure due to unauthorized access
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_delete(self):
        # Verify that the user exists and can receive own info
        self.test_user_get_own_info()

        # Attempt to delete the user using a valid token
        response = self.client.delete(self.user_url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        # Expect successful user deletion
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify that the user is no longer available
        response = self.client.get(self.user_url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        # Expect unauthorized access due to the deleted user
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
