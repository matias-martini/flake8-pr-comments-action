import json
import unittest
from unittest.mock import patch
from src.github_client import GithubClient


class TestGithubClient(unittest.TestCase):
    @patch('requests.post')
    def test_send_pr_review_comment_with_ok_response(self, mock_post_request):  # noqa: CFQ001
        github_client = GithubClient(
            "gh_token",
            "gh_commit",
            "gh_repo_owner",
            "gh_repo_name",
            "gh_pull_request_id"
        )

        expected_endpoint = "https://api.github.com/repos/gh_repo_owner/gh_repo_name/pulls/gh_pull_request_id/comments"  # noqa: E501

        expected_header = {
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer gh_token",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        expected_data = json.dumps(
                {
                    "body": "message",
                    "commit_id": "gh_commit",
                    "path": "file_path",
                    "line": "line_to_comment",
                    "side": "RIGHT"
                 })

        mock_post_request.return_value.status_code = 200

        github_client.send_pr_review_comment("file_path", "line_to_comment", "message")

        mock_post_request.assert_called_once_with(
            expected_endpoint,
            headers=expected_header,
            data=expected_data
        )

    @patch('requests.post')
    def test_send_pr_review_comment_with_bad_response(self, mock_post_request):
        github_client = GithubClient(
            "gh_token",
            "gh_commit",
            "gh_repo_owner",
            "gh_repo_name",
            "gh_pull_request_id"
        )

        mock_post_request.return_value.status_code = 400

        self.assertRaises(
            Exception,
            lambda: github_client.send_pr_review_comment("file_path", "line_to_comment", "message")
        )

    @patch('requests.get')
    def test_list_changed_python_files_in_pr_with_ok_response(self, mock_get_request):  # noqa: CFQ001
        github_client = GithubClient(
            "gh_token",
            "gh_commit",
            "gh_repo_owner",
            "gh_repo_name",
            "gh_pull_request_id"
        )

        expected_endpoint = "https://api.github.com/repos/gh_repo_owner/gh_repo_name/pulls/gh_pull_request_id/files"  # noqa: E501

        expected_header = {
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer gh_token",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        mock_get_request.return_value.status_code = 200
        mock_get_request.return_value.content = '[{"filename": "file_1.py"}, {"filename": "file_2.pyc"}]'

        changed_files_in_pr = github_client.list_changed_python_files_in_pr()
        expected_changed_files = ["file_1.py"]

        self.assertEqual(changed_files_in_pr, expected_changed_files)

        mock_get_request.assert_called_once_with(
            expected_endpoint,
            headers=expected_header
        )

    @patch('requests.get')
    def test_list_changed_python_files_in_pr_with_bad_response(self, mock_get_request):  # noqa: CFQ001
        github_client = GithubClient(
            "gh_token",
            "gh_commit",
            "gh_repo_owner",
            "gh_repo_name",
            "gh_pull_request_id"
        )

        mock_get_request.return_value.status_code = 401

        self.assertRaises(Exception, github_client.list_changed_python_files_in_pr)


if __name__ == '__main__':
    unittest.main()
