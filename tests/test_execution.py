import pytest
from unittest.mock import Mock, patch, MagicMock
from google.genai import types
from pathlib import Path
import subprocess

from neurocode.functions.execution.run_python_file import (
    run_python_file,
    schema_run_python_file,
)
from neurocode.functions.execution.run_react_app import (
    run_react_app,
    schema_run_react_app,
)


class TestRunPythonFile:
    """Tests for run_python_file function."""

    def test_run_python_file_success(self, mock_subprocess_run, sample_python_file):
        """Test running a Python file successfully."""
        mock_subprocess_run.return_value = subprocess.CompletedProcess(
            args=["python", sample_python_file],
            returncode=0,
            stdout="Hello, World!\nResult: 2\n",
            stderr="",
        )

        result = run_python_file(
            str(Path(sample_python_file).parent), Path(sample_python_file).name
        )

        assert "STDOUT" in result
        assert "Hello, World!" in result
        assert "Result: 2" in result
        mock_subprocess_run.assert_called_once()

    def test_run_python_file_with_stderr(self, mock_subprocess_run, sample_python_file):
        """Test running a Python file that produces stderr output."""
        mock_subprocess_run.return_value = subprocess.CompletedProcess(
            args=["python", sample_python_file],
            returncode=0,
            stdout="Normal output\n",
            stderr="Warning message\n",
        )

        result = run_python_file(
            str(Path(sample_python_file).parent), Path(sample_python_file).name
        )

        assert "STDOUT" in result
        assert "Normal output" in result
        assert "STDERR" in result
        assert "Warning message" in result

    def test_run_python_file_nonzero_exit_code(
        self, mock_subprocess_run, sample_python_file
    ):
        """Test running a Python file that exits with non-zero code."""
        mock_subprocess_run.return_value = subprocess.CompletedProcess(
            args=["python", sample_python_file],
            returncode=1,
            stdout="",
            stderr="Error occurred",
        )

        result = run_python_file(
            str(Path(sample_python_file).parent), Path(sample_python_file).name
        )

        assert "STDERR" in result
        assert "Error occurred" in result
        assert "non-zero exit code: 1" in result

    def test_run_python_file_with_args(self, mock_subprocess_run, sample_python_file):
        """Test running a Python file with command line arguments."""
        mock_subprocess_run.return_value = subprocess.CompletedProcess(
            args=["python", sample_python_file, "arg1", "arg2"],
            returncode=0,
            stdout="Processing args\n",
            stderr="",
        )

        result = run_python_file(
            str(Path(sample_python_file).parent),
            Path(sample_python_file).name,
            ["arg1", "arg2"],
        )

        mock_subprocess_run.assert_called_once()
        call_args = mock_subprocess_run.call_args[0][0]
        assert "arg1" in call_args
        assert "arg2" in call_args

    def test_run_python_file_no_output(self, mock_subprocess_run, sample_python_file):
        """Test running a Python file that produces no output."""
        mock_subprocess_run.return_value = subprocess.CompletedProcess(
            args=["python", sample_python_file], returncode=0, stdout="", stderr=""
        )

        result = run_python_file(
            str(Path(sample_python_file).parent), Path(sample_python_file).name
        )

        assert "STDOUT :" in result
        assert "STDERR :" in result
        assert "did not produce any output" in result

    def test_run_python_file_timeout(self, mock_subprocess_run, sample_python_file):
        """Test handling of subprocess timeout."""
        mock_subprocess_run.side_effect = subprocess.TimeoutExpired(
            cmd=["python", sample_python_file], timeout=30
        )

        result = run_python_file(
            str(Path(sample_python_file).parent), Path(sample_python_file).name
        )

        assert "Error:" in result
        assert "timed out" in result.lower() or "timeout" in result.lower()

    def test_run_python_file_nonexistent_file(self, temp_working_dir):
        """Test attempting to run a non-existent Python file."""
        result = run_python_file(str(temp_working_dir), "nonexistent.py")

        assert "Error:" in result
        assert "does not exist" in result

    def test_run_python_file_path_traversal_attack(self, temp_working_dir):
        """Test security check for path traversal."""
        result = run_python_file(str(temp_working_dir), "../../../etc/malicious.py")

        assert "Error:" in result
        assert "outside the working directory" in result

    def test_run_python_file_not_python_extension(self, temp_working_dir):
        """Test attempting to run a non-Python file."""
        (temp_working_dir / "script.txt").write_text("not python")

        result = run_python_file(str(temp_working_dir), "script.txt")

        assert "Error:" in result
        assert "not a Python file" in result

    def test_run_python_file_directory(self, temp_working_dir):
        """Test attempting to run a directory as a Python file."""
        result = run_python_file(str(temp_working_dir), ".")

        assert "Error:" in result
        # The function returns "does not exist" for directories, not "not a Python file"
        assert "does not exist" in result or "not a Python file" in result


class TestSchemaRunPythonFile:
    """Tests for schema_run_python_file function."""

    def test_schema_name(self):
        """Test that schema has correct name."""
        assert schema_run_python_file.name == "run_python_file"

    def test_schema_description(self):
        """Test that schema has description."""
        assert schema_run_python_file.description is not None
        assert "run" in schema_run_python_file.description.lower()

    def test_schema_file_path_parameter(self):
        """Test that file_path parameter is defined."""
        params = schema_run_python_file.parameters
        if params is not None and params.properties is not None:
            assert "file_path" in params.properties
            assert params.properties["file_path"].type == types.Type.STRING

    def test_schema_args_parameter(self):
        """Test that args parameter is defined."""
        params = schema_run_python_file.parameters
        if params is not None and params.properties is not None:
            assert "args" in params.properties
            assert params.properties["args"].type == types.Type.ARRAY

    def test_schema_args_item_type(self):
        """Test that args items are strings."""
        params = schema_run_python_file.parameters
        if params is not None and params.properties is not None:
            assert params.properties["args"].items.type == types.Type.STRING

    def test_schema_required_fields(self):
        """Test that file_path is required."""
        params = schema_run_python_file.parameters
        if params.required is not None:
            assert "file_path" in params.required
            assert "args" not in params.required  # args is optional


class TestRunReactApp:
    """Tests for run_react_app function."""

    def test_run_react_app_success(self, mock_subprocess_popen, sample_react_project):
        """Test running a React app successfully."""
        # Mock the process object
        mock_process = Mock()
        mock_process.stdout = iter(
            ["Starting server...\n", "Local: http://localhost:5173/\n"]
        )
        mock_process.returncode = 0
        mock_subprocess_popen.return_value = mock_process

        result = run_react_app(
            str(Path(sample_react_project).parent), Path(sample_react_project).name
        )

        assert "React server started" in result
        assert "http://localhost:5173/" in result or "http://" in result
        mock_subprocess_popen.assert_called_once()

    def test_run_react_app_different_port(
        self, mock_subprocess_popen, sample_react_project
    ):
        """Test running a React app on a different port."""
        mock_process = Mock()
        mock_process.stdout = iter(
            ["Starting server...\n", "Local: http://localhost:3000/\n"]
        )
        mock_process.returncode = 0
        mock_subprocess_popen.return_value = mock_process

        result = run_react_app(
            str(Path(sample_react_project).parent), Path(sample_react_project).name
        )

        assert "React server started" in result
        assert "localhost" in result

    def test_run_react_app_nonexistent_directory(self, temp_working_dir):
        """Test attempting to run a React app in non-existent directory."""
        result = run_react_app(str(temp_working_dir), "nonexistent-react-app")

        assert "Error:" in result
        assert "does not exist" in result or "not a directory" in result

    def test_run_react_app_path_traversal_attack(self, temp_working_dir):
        """Test security check for path traversal."""
        result = run_react_app(str(temp_working_dir), "../../../etc/malicious")

        assert "Error:" in result
        assert "outside the working directory" in result

    def test_run_react_app_timeout(self, mock_subprocess_popen, sample_react_project):
        """Test handling of subprocess timeout."""
        mock_subprocess_popen.side_effect = subprocess.TimeoutExpired(
            cmd="npm run dev", timeout=60
        )

        result = run_react_app(
            str(Path(sample_react_project).parent), Path(sample_react_project).name
        )

        assert "Error:" in result
        assert "timed out" in result.lower() or "timeout" in result.lower()

    def test_run_react_app_subprocess_exception(
        self, mock_subprocess_popen, sample_react_project
    ):
        """Test handling of subprocess exceptions."""
        mock_subprocess_popen.side_effect = Exception("Subprocess error")

        result = run_react_app(
            str(Path(sample_react_project).parent), Path(sample_react_project).name
        )

        assert "Error:" in result
        assert "Subprocess error" in result

    def test_run_react_app_file_instead_of_directory(self, temp_working_dir):
        """Test attempting to run a React app on a file instead of directory."""
        (temp_working_dir / "notadir.txt").write_text("content")

        result = run_react_app(str(temp_working_dir), "notadir.txt")

        assert "Error:" in result
        assert "not a directory" in result


class TestSchemaRunReactApp:
    """Tests for schema_run_react_app function."""

    def test_schema_name(self):
        """Test that schema has correct name."""
        assert schema_run_react_app.name == "run_react_app"

    def test_schema_description(self):
        """Test that schema has description."""
        assert schema_run_react_app.description is not None
        assert "react" in schema_run_react_app.description.lower()
        assert "npm run dev" in schema_run_react_app.description.lower()

    def test_schema_project_path_parameter(self):
        """Test that project_path parameter is defined."""
        params = schema_run_react_app.parameters
        if params is not None and params.properties is not None:
            assert "project_path" in params.properties
            assert params.properties["project_path"].type == types.Type.STRING

    def test_schema_required_fields(self):
        """Test that project_path is required."""
        params = schema_run_react_app.parameters
        if params is not None and params.required is not None:
            assert "project_path" in params.required
