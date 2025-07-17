#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient class
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value
        and makes the right API call
        """
        # Create test payload
        test_payload = {"name": org_name, "id": 123}

        # Configure the mock to return our test payload
        mock_get_json.return_value = test_payload

        # Create client instance and call the org property
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert that get_json was called once with the correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # Assert that the result matches our test payload
        self.assertEqual(result, test_payload)

#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient class
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""
    
    # ... (previous test_org method remains the same) ...

    def test_public_repos_url(self):
        """
        Test that _public_repos_url returns the correct URL from the org payload
        """
        # Define the test payload
        test_payload = {
            "repos_url": "https://api.github.com/orgs/testorg/repos"
        }

        # Use patch as a context manager to mock the org property
        with patch(
            'client.GithubOrgClient.org',
            new_callable=PropertyMock,
            return_value=test_payload
        ) as mock_org:
            # Create client instance
            client = GithubOrgClient("testorg")
            
            # Get the _public_repos_url property
            result = client._public_repos_url

            # Assert that the org property was accessed
            mock_org.assert_called_once()
            
            # Assert that the result matches the expected URL
            self.assertEqual(result, test_payload["repos_url"])



#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient class
"""
import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""
    
    # ... (previous test methods remain the same) ...

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns the correct list of repos
        """
        # Define test data
        test_repos_url = "https://api.github.com/orgs/testorg/repos"
        test_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]
        expected_repos = ["repo1", "repo2"]

        # Mock _public_repos_url property
        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock,
            return_value=test_repos_url
        ) as mock_public_repos_url:
            # Mock get_json to return our test repos payload
            mock_get_json.return_value = test_repos_payload

            # Create client instance and call public_repos
            client = GithubOrgClient("testorg")
            repos = client.public_repos()

            # Assert that _public_repos_url was accessed once
            mock_public_repos_url.assert_called_once()

            # Assert that get_json was called once with test_repos_url
            mock_get_json.assert_called_once_with(test_repos_url)

            # Assert that the result is the expected list of repo names
            self.assertEqual(repos, expected_repos)


#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient class
"""
import unittest
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""
    
    # ... (previous test methods remain the same) ...

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """
        Test that has_license correctly identifies license matches
        """
        # Create client instance (org name doesn't matter for this test)
        client = GithubOrgClient("testorg")
        
        # Call the method and assert the result
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


#!/usr/bin/env python3
"""
Integration tests for client.GithubOrgClient class
"""
import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient"""
    
    @classmethod
    def setUpClass(cls):
        """Set up class with mock patcher"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            """Side effect function to return different payloads based on URL"""
            if "orgs/testorg" in url:
                return cls.org_payload
            elif "repos" in url:
                return cls.repos_payload
            return None

        cls.mock_get.return_value.json.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method with integration"""
        client = GithubOrgClient("testorg")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with license filter"""
        client = GithubOrgClient("testorg")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)

#!/usr/bin/env python3
"""
Integration tests for client.GithubOrgClient class
"""
import unittest
from parameterized import parameterized_class
from unittest.mock import patch, Mock
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient"""
    
    @classmethod
    def setUpClass(cls):
        """Set up class with mock patcher"""
        cls.get_patcher = patch('requests.get')  # Must be named exactly 'get_patcher'
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            """Side effect function to return different payloads based on URL"""
            mock_response = Mock()
            if "orgs/testorg" in url:
                mock_response.json.return_value = cls.org_payload
            elif "repos" in url:
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher"""
        cls.get_patcher.stop()  # Must call stop() on the patcher

    def test_public_repos(self):
        """Test public_repos method with integration"""
        client = GithubOrgClient("testorg")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with license filter"""
        client = GithubOrgClient("testorg")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)