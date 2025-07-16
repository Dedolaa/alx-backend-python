#!/usr/bin/env python3

from parameterized import parameterized, parameterized_class
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos
import requests

"""
Unit test for GithubOrgClient class
"""
import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""
        expected = {"login": org_name}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected)

from unittest.mock import PropertyMock


class TestGithubOrgClient(unittest.TestCase):
    ...
    
    def test_public_repos_url(self):
        """Test that _public_repos_url returns expected value from org"""
        test_payload = {"repos_url": "https://api.github.com/orgs/test/repos"}

        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient("test")
            result = client._public_repos_url
            self.assertEqual(result, test_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns list of repo names"""
        test_url = "https://api.github.com/orgs/test/repos"
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_payload

        with patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock) as mock_url:
            mock_url.return_value = test_url
            client = GithubOrgClient("test")
            result = client.public_repos()

            # Assertions
            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(test_url)

from parameterized import parameterized

@parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns the correct boolean"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)

@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up mock for requests.get"""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        # Setup .json() return values depending on the URL
        mock_get.side_effect = [
            Mock(**{"json.return_value": cls.org_payload}),
            Mock(**{"json.return_value": cls.repos_payload}),
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get"""
        cls.get_patcher.stop()
