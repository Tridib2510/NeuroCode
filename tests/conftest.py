import os
import pytest
from unittest.mock import Mock, MagicMock, patch
from google.genai import types
from pathlib import Path


@pytest.fixture
def temp_working_dir(tmp_path):
    """Create a temporary working directory for file operations."""
    return tmp_path


@pytest.fixture
def mock_subprocess_run():
    """Mock subprocess.run for subprocess-related tests."""
    with patch("subprocess.run") as mock_run:
        yield mock_run


@pytest.fixture
def mock_subprocess_popen():
    """Mock subprocess.Popen for subprocess-related tests."""
    with patch("subprocess.Popen") as mock_popen:
        yield mock_popen


@pytest.fixture
def mock_gemini_client():
    """Mock Google GenAI client for image analysis tests."""
    mock_client = Mock()
    mock_response = Mock()
    mock_candidate = Mock()
    mock_content = Mock()
    mock_part = Mock()

    mock_part.text = "AI analysis response"
    mock_content.parts = [mock_part]
    mock_candidate.content = mock_content
    mock_response.candidates = [mock_candidate]

    mock_client.models.generate_content.return_value = mock_response

    return mock_client


@pytest.fixture
def mock_requests_get():
    """Mock requests.get for web analysis tests."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.encoding = "utf-8"
    mock_response.content = (
        b"<html><head><title>Test Page</title></head><body><h1>Test</h1></body></html>"
    )
    mock_response.text = (
        "<html><head><title>Test Page</title></head><body><h1>Test</h1></body></html>"
    )
    mock_response.headers = {"content-type": "text/html"}

    with patch("requests.get", return_value=mock_response) as mock_get:
        yield mock_get


@pytest.fixture
def sample_python_file(temp_working_dir):
    """Create a sample Python file for testing."""
    file_path = temp_working_dir / "test_script.py"
    file_path.write_text('print("Hello, World!")\nx = 1 + 1\nprint(f"Result: {x}")')
    return str(file_path)


@pytest.fixture
def sample_text_file(temp_working_dir):
    """Create a sample text file for testing."""
    file_path = temp_working_dir / "sample.txt"
    file_path.write_text("This is a sample text file for testing file operations.")
    return str(file_path)


@pytest.fixture
def sample_long_file(temp_working_dir):
    """Create a file longer than 1000 characters for testing truncation."""
    file_path = temp_working_dir / "long_file.txt"
    long_content = "A" * 1500
    file_path.write_text(long_content)
    return str(file_path)


@pytest.fixture
def sample_image_path(temp_working_dir):
    """Create a sample image file path for testing."""
    # Create a minimal valid JPEG header for testing
    file_path = temp_working_dir / "test_image.jpg"
    file_path.write_bytes(b"\xff\xd8\xff\xe0\x00\x10JFIF")  # Minimal JPEG header
    return str(file_path)


@pytest.fixture
def sample_directory(temp_working_dir):
    """Create a sample directory with files for testing."""
    dir_path = temp_working_dir / "test_dir"
    dir_path.mkdir()

    (dir_path / "file1.txt").write_text("File 1 content")
    (dir_path / "file2.py").write_text("print('File 2')")
    (dir_path / "subdir").mkdir()
    (dir_path / "subdir" / "file3.txt").write_text("File 3 content")

    return str(dir_path)


@pytest.fixture
def sample_react_project(temp_working_dir):
    """Create a sample React project structure for testing."""
    project_path = temp_working_dir / "my-react-app"
    project_path.mkdir()

    (project_path / "package.json").write_text(
        '{"name": "my-react-app", "version": "1.0.0"}'
    )
    (project_path / "vite.config.js").write_text("export default {}")
    (project_path / "index.html").write_text("<html></html>")
    src_dir = project_path / "src"
    src_dir.mkdir()
    (src_dir / "main.jsx").write_text('console.log("Hello")')

    return str(project_path)


@pytest.fixture
def sample_python_project(temp_working_dir):
    """Create a sample Python project structure for testing."""
    project_path = temp_working_dir / "python-project"
    project_path.mkdir()

    (project_path / "requirements.txt").write_text(
        "requests==2.31.0\nbeautifulsoup4==4.12.0"
    )
    (project_path / "main.py").write_text('print("Hello")')

    return str(project_path)
