import unittest
import subprocess
from unittest.mock import patch
from src.flake8_linter import Flake8Linter


class TestFlake8Linter(unittest.TestCase):
    @patch("subprocess.run")
    def test_flake8_run_with_config_path(self, mock_subprocess_run):
        flake8_linter = Flake8Linter(config_location_path="../.flake8")
        flake8_linter.run_flake8()

        expected_run_arguments = ["flake8", "--format=json", "--config=../.flake8"]

        mock_subprocess_run.assert_called_once_with(expected_run_arguments, stdout=subprocess.PIPE)

    @patch("subprocess.run")
    def test_flake8_run_with_file_path(self, mock_subprocess_run):
        flake8_linter = Flake8Linter(config_location_path="../.flake8")
        flake8_linter.run_flake8(file_path="test.py")

        expected_run_arguments = ["flake8", "--format=json", "--config=../.flake8", "test.py"]

        mock_subprocess_run.assert_called_once_with(expected_run_arguments, stdout=subprocess.PIPE)

    @patch("subprocess.run")
    def test_flake8_set_expected_completed_process(self, mock_subprocess_run):
        flake8_linter = Flake8Linter(config_location_path="../.flake8")
        flake8_linter.run_flake8(file_path = "src/file.py")

        expected_run_arguments = ["flake8", "--format=json", "--config=../.flake8", "src/file.py"]

        mock_subprocess_run.assert_called_once_with(expected_run_arguments, stdout=subprocess.PIPE)
        self.assertEqual(flake8_linter.completed_process, mock_subprocess_run.return_value)

    @patch("subprocess.run")
    def test_flake8_get_expected_list_of_errors_from_source_file(self, mock_subprocess_run):  # noqa: CFQ001
        flake8_output = b"""{
            "./src/__init__.py": [],
            "./src/flake8_linter.py": [
                {
                    "code": "E501",
                    "filename": "./src/flake8_linter.py",
                    "line_number": 17,
                    "column_number": 80,
                    "text": "line too long (95 > 79 characters)",
                    "physical_line": "        list_of_errors = [item for sublist in errors_by_file_dict.values() for item in sublist]"
                },
                {
                    "code": "E501",
                    "filename": "./src/flake8_linter.py",
                    "line_number": 22,
                    "column_number": 80,
                    "text": "line too long (90 > 79 characters)",
                    "physical_line": "        self.completed_process = subprocess.run(self.command_list, stdout=subprocess.PIPE)"
                }
            ]
        }"""  # noqa: E501

        expected_error_list = [
                {
                    "code": "E501",
                    "filename": "./src/flake8_linter.py",
                    "line_number": 17,
                    "column_number": 80,
                    "text": "line too long (95 > 79 characters)",
                    "physical_line": "        list_of_errors = [item for sublist in errors_by_file_dict.values() for item in sublist]"  # noqa: E501
                },
                {
                    "code": "E501",
                    "filename": "./src/flake8_linter.py",
                    "line_number": 22,
                    "column_number": 80,
                    "text": "line too long (90 > 79 characters)",
                    "physical_line": "        self.completed_process = subprocess.run(self.command_list, stdout=subprocess.PIPE)"  # noqa: E501
                }
        ]

        mock_subprocess_run.return_value.stdout = flake8_output

        self.assertEqual(Flake8Linter().get_list_of_errors(file_path="test.py"), expected_error_list)


    @patch("subprocess.run")
    def test_flake8_get_expected_list_of_errors_when_flake8_fails(self, mock_subprocess_run):  # noqa: CFQ001
        flake8_output = b"$&%/"
        expected_error_list = []

        mock_subprocess_run.return_value.stdout = flake8_output

        self.assertEqual(Flake8Linter().get_list_of_errors(file_path="test.py"), expected_error_list)


if __name__ == '__main__':
    unittest.main()
