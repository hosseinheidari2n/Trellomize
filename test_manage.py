import unittest
from unittest.mock import patch, mock_open
import hashlib
import os

from manage import User, Client, Manager, HashPassword, CalculateHash, CreateManager, LoginManager, CreateClient, LoginClient

class TestUserManagerClient(unittest.TestCase):
    
    def test_user_creation(self):
        user = User('testuser', 'testpass')
        self.assertEqual(user.UserName, 'testuser')
        self.assertEqual(user.Password, 'testpass')

    def test_client_creation(self):
        client = Client('testclient', 'testpass')
        self.assertEqual(client.UserName, 'testclient')
        self.assertEqual(client.Password, 'testpass')

    def test_manager_creation(self):
        manager = Manager('testmanager', 'testpass')
        self.assertEqual(manager.UserName, 'testmanager')
        self.assertEqual(manager.Password, 'testpass')

    def test_hash_password(self):
        password = 'mypassword'
        hashed = HashPassword(password)
        expected_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        self.assertEqual(hashed, expected_hash)

    def test_calculate_hash(self):
        password = 'mypassword'
        calculated_hash = CalculateHash(password)
        expected_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        self.assertEqual(calculated_hash, expected_hash)


    @patch('builtins.input', side_effect=['newmanager', 'newpassword'])
    @patch('builtins.open', new_callable=mock_open, read_data='')
    @patch('os.path.exists', return_value=False)
    def test_create_manager(self, mock_exists, mock_open, mock_input):
        CreateManager()
        mock_open.assert_called_once_with('manager.txt', 'a')
        handle = mock_open()
        handle.write.assert_called_once_with('newmanager : ' + HashPassword('newpassword') + '\n')


    @patch('builtins.input', side_effect=['newmanager', 'wrongpassword'])
    @patch('builtins.open', new_callable=mock_open, read_data='newmanager : ' + HashPassword('newpassword') + '\n')
    @patch('os.path.exists', return_value=True)
    def test_login_manager_success(self, mock_exists, mock_open, mock_input):
        with patch('manage.SecondCommandList') as mock_second_command:
            LoginManager()
            mock_second_command.assert_called_once()

    @patch('builtins.input', side_effect=['newmanager', 'wrongpassword'])
    @patch('builtins.open', new_callable=mock_open, read_data='newmanager : ' + HashPassword('newpassword') + '\n')
    @patch('os.path.exists', return_value=True)
    def test_login_manager_failure(self, mock_exists, mock_open, mock_input):
        with patch('manage.LoginManager') as mock_login_manager:
            LoginManager()
            mock_login_manager.assert_called()

    @patch('builtins.input', side_effect=['newclient', 'newpassword'])
    @patch('builtins.open', new_callable=mock_open, read_data='')
    @patch('os.path.exists', return_value=False)
    def test_create_client(self, mock_exists, mock_open, mock_input):
        CreateClient()
        mock_open.assert_called_once_with('client.txt', 'a')
        handle = mock_open()
        handle.write.assert_called_once_with('newclient : ' + HashPassword('newpassword') + '\n')

    @patch('builtins.input', side_effect=['newclient', 'newpassword'])
    @patch('builtins.open', new_callable=mock_open, read_data='newclient : ' + HashPassword('newpassword') + '\n')
    @patch('os.path.exists', return_value=True)
    def test_login_client_success(self, mock_exists, mock_open, mock_input):
        with patch('manage.SecondCommandList') as mock_second_command:
            LoginClient()
            mock_second_command.assert_called_once()

    @patch('builtins.input', side_effect=['newclient', 'wrongpassword'])
    @patch('builtins.open', new_callable=mock_open, read_data='newclient : ' + HashPassword('newpassword') + '\n')
    @patch('os.path.exists', return_value=True)
    def test_login_client_failure(self, mock_exists, mock_open, mock_input):
        with patch('manage.LoginClient') as mock_login_client:
            LoginClient()
            mock_login_client.assert_called()

if __name__ == '__main__':
    unittest.main()
