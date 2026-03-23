import pytest
from unittest.mock import patch
from google.genai import types
from pathlib import Path
import os

from neurocode.functions.file_operations.getFilesInfo import (
    get_files_info,
    schema_get_files_info,
)
from neurocode.functions.file_operations.getFilesContent import (
    get_file_content,
    schema_get_files_content,
)
from neurocode.functions.file_operations.writeIntoFile import (
    write_file,
    schema_write_file,
)
from neurocode.functions.file_operations.createFolderAndFile import (
    create_file,
    schema_create_file,
)


class TestGetFilesInfo:
    """Tests for get_files_info function."""

    def test_list_files_in_directory(self, temp_working_dir):
        """Test listing files in a directory."""
        (temp_working_dir / "file1.txt").write_text("content1")
        (temp_working_dir / "file2.txt").write_text("content2")

        result = get_files_info(str(temp_working_dir))

        assert "file1.txt" in result
        assert "file2.txt" in result
        assert "is_directory=False" in result

    def test_list_files_in_subdirectory(self, temp_working_dir):
        """Test listing files in a subdirectory."""
        sub_dir = temp_working_dir / "subdir"
        sub_dir.mkdir()
        (sub_dir / "nested_file.txt").write_text("nested content")

        result = get_files_info(str(temp_working_dir), "subdir")

        assert "nested_file.txt" in result
        assert "is_directory=False" in result

    def test_list_empty_directory(self, temp_working_dir):
        """Test listing an empty directory."""
        empty_dir = temp_working_dir / "empty"
        empty_dir.mkdir()

        result = get_files_info(str(temp_working_dir), "empty")

        assert result == "" or "Empty" in result or len(result.strip()) == 0

    def test_list_with_directories(self, temp_working_dir):
        """Test listing files with mixed files and directories."""
        (temp_working_dir / "file.txt").write_text("file")
        dir_path = temp_working_dir / "directory"
        dir_path.mkdir()

        result = get_files_info(str(temp_working_dir))

        assert "file.txt" in result
        assert "directory" in result
        assert "is_directory=False" in result
        assert "is_directory=True" in result

    def test_path_traversal_attack(self, temp_working_dir):
        """Test security check for path traversal attacks."""
        result = get_files_info(str(temp_working_dir), "../../../etc")

        assert "Error:" in result
        assert "outside the working directory" in result

    def test_absolute_path_attack(self, temp_working_dir):
        """Test security check for absolute paths."""
        result = get_files_info(str(temp_working_dir), "/etc/passwd")

        assert "Error:" in result
        assert "outside the working directory" in result

    def test_nonexistent_directory(self, temp_working_dir):
        """Test listing a non-existent directory."""
        with pytest.raises(FileNotFoundError):
            get_files_info(str(temp_working_dir), "nonexistent")

    def test_file_size_reported(self, temp_working_dir):
        """Test that file sizes are correctly reported."""
        file_path = temp_working_dir / "test.txt"
        file_path.write_text("Hello World!")

        result = get_files_info(str(temp_working_dir))

        assert "file_size=" in result
        assert "bytes" in result


class TestSchemaGetFilesInfo:
    """Tests for schema_get_files_info function."""

    def test_schema_name(self):
        """Test that schema has correct name."""
        assert schema_get_files_info.name == "get_files_info"

    def test_schema_description(self):
        """Test that schema has description."""
        assert schema_get_files_info.description is not None
        assert len(schema_get_files_info.description) > 0

    def test_schema_parameters(self):
        """Test that schema has correct parameters."""
        assert hasattr(schema_get_files_info, "parameters")
        assert schema_get_files_info.parameters is not None

    def test_schema_directory_parameter(self):
        """Test that directory parameter is defined correctly."""
        params = schema_get_files_info.parameters
        if params is not None and params.properties is not None:
            assert "directory" in params.properties
            assert params.properties["directory"].type == types.Type.STRING

    def test_schema_required_fields(self):
        """Test that required fields are correctly defined."""
        params = schema_get_files_info.parameters
        if params is not None and params.required is not None:
            # directory is optional (defaults to working directory)
            assert len(params.required) == 0


class TestGetFileContent:
    """Tests for get_file_content function."""

    def test_read_existing_file(self, sample_text_file):
        """Test reading an existing file."""
        result = get_file_content(
            str(Path(sample_text_file).parent), Path(sample_text_file).name
        )

        assert "sample text file" in result
        assert "testing file operations" in result

    def test_read_python_file(self, sample_python_file):
        """Test reading a Python file."""
        result = get_file_content(
            str(Path(sample_python_file).parent), Path(sample_python_file).name
        )

        assert "print" in result
        assert "Hello, World!" in result

    def test_read_long_file_truncation(self, sample_long_file):
        """Test that long files are truncated at 1000 characters."""
        result = get_file_content(
            str(Path(sample_long_file).parent), Path(sample_long_file).name
        )

        assert len(result) <= 1100  # 1000 + truncation message
        assert "(truncated)" in result

    def test_nonexistent_file(self, temp_working_dir):
        """Test reading a non-existent file."""
        result = get_file_content(str(temp_working_dir), "nonexistent.txt")

        assert "Error:" in result
        assert "not a valid file" in result

    def test_path_traversal_attack(self, temp_working_dir):
        """Test security check for path traversal."""
        result = get_file_content(str(temp_working_dir), "../../../etc/passwd")

        assert "Error:" in result
        assert "outside the working directory" in result

    def test_read_directory_instead_of_file(self, temp_working_dir):
        """Test attempting to read a directory as a file."""
        result = get_file_content(str(temp_working_dir), ".")

        assert "Error:" in result
        assert "not a valid file" in result

    def test_read_empty_file(self, temp_working_dir):
        """Test reading an empty file."""
        empty_file = temp_working_dir / "empty.txt"
        empty_file.write_text("")

        result = get_file_content(str(temp_working_dir), "empty.txt")

        assert result == "" or len(result.strip()) == 0


class TestSchemaGetFilesContent:
    """Tests for schema_get_files_content function."""

    def test_schema_name(self):
        """Test that schema has correct name."""
        assert schema_get_files_content.name == "get_file_content"

    def test_schema_description(self):
        """Test that schema has description."""
        assert schema_get_files_content.description is not None
        assert "read" in schema_get_files_content.description.lower()

    def test_schema_file_path_parameter(self):
        """Test that file_path parameter is defined."""
        params = schema_get_files_content.parameters
        if params is not None and params.properties is not None:
            assert "file_path" in params.properties
            assert params.properties["file_path"].type == types.Type.STRING

    def test_schema_required_fields(self):
        """Test that file_path is required."""
        params = schema_get_files_content.parameters
        if params is not None and params.required is not None:
            assert "file_path" in params.required


class TestWriteFile:
    """Tests for write_file function."""

    def test_write_to_existing_file(self, temp_working_dir):
        """Test writing to an existing file."""
        file_path = temp_working_dir / "test.txt"
        file_path.write_text("original content")

        result = write_file(str(temp_working_dir), "test.txt", "new content")

        assert "Successfully wrote" in result
        assert file_path.read_text() == "new content"

    def test_write_to_new_file(self, temp_working_dir):
        """Test writing to a new file."""
        result = write_file(str(temp_working_dir), "newfile.txt", "new file content")

        assert "Successfully wrote" in result
        assert (temp_working_dir / "newfile.txt").exists()
        assert (temp_working_dir / "newfile.txt").read_text() == "new file content"

    def test_write_with_nested_path(self, temp_working_dir):
        """Test writing to a file in a nested directory."""
        result = write_file(
            str(temp_working_dir), "subdir/nested/file.txt", "nested content"
        )

        assert "Successfully wrote" in result
        assert (temp_working_dir / "subdir" / "nested" / "file.txt").exists()
        assert (
            temp_working_dir / "subdir" / "nested" / "file.txt"
        ).read_text() == "nested content"

    def test_write_creates_parent_directories(self, temp_working_dir):
        """Test that write_file creates parent directories."""
        result = write_file(
            str(temp_working_dir), "deep/nested/path/file.txt", "content"
        )

        assert "Successfully wrote" in result
        assert (temp_working_dir / "deep" / "nested" / "path").exists()

    def test_path_traversal_attack(self, temp_working_dir):
        """Test security check for path traversal."""
        result = write_file(
            str(temp_working_dir), "../../../etc/malicious.txt", "bad content"
        )

        assert "Error:" in result
        assert "outside the working directory" in result

    def test_write_empty_content(self, temp_working_dir):
        """Test writing empty content to a file."""
        result = write_file(str(temp_working_dir), "empty.txt", "")

        assert "Successfully wrote" in result
        assert (temp_working_dir / "empty.txt").read_text() == ""

    def test_write_special_characters(self, temp_working_dir):
        """Test writing content with special characters."""
        special_content = "Hello\nWorld\t!@#$%^&*()_+-=[]{}|;':\",./<>?"
        result = write_file(str(temp_working_dir), "special.txt", special_content)

        assert "Successfully wrote" in result
        assert (temp_working_dir / "special.txt").read_text() == special_content

    def test_write_large_content(self, temp_working_dir):
        """Test writing large content."""
        large_content = "X" * 10000
        result = write_file(str(temp_working_dir), "large.txt", large_content)

        assert "Successfully wrote" in result
        assert len((temp_working_dir / "large.txt").read_text()) == 10000


class TestSchemaWriteFile:
    """Tests for schema_write_file function."""

    def test_schema_name(self):
        """Test that schema has correct name."""
        assert schema_write_file.name == "write_file"

    def test_schema_description(self):
        """Test that schema has description."""
        assert schema_write_file.description is not None
        assert "write" in schema_write_file.description.lower()

    def test_schema_file_path_parameter(self):
        """Test that file_path parameter is defined."""
        params = schema_write_file.parameters
        if params is not None and params.properties is not None:
            assert "file_path" in params.properties
            assert params.properties["file_path"].type == types.Type.STRING

    def test_schema_content_parameter(self):
        """Test that content parameter is defined."""
        params = schema_write_file.parameters
        if params is not None and params.properties is not None:
            assert "content" in params.properties
            assert params.properties["content"].type == types.Type.STRING

    def test_schema_required_fields(self):
        """Test that required fields are correct."""
        params = schema_write_file.parameters
        if params is not None and params.required is not None:
            # Both file_path and content should be required based on usage
            assert "file_path" in params.required
            assert "content" in params.required


class TestCreateFile:
    """Tests for create_file function."""

    def test_create_new_file(self, temp_working_dir):
        """Test creating a new file."""
        result = create_file(str(temp_working_dir), "newfile.txt", "content")

        assert "Successfully created" in result
        assert (temp_working_dir / "newfile.txt").exists()

    def test_create_file_with_content(self, temp_working_dir):
        """Test creating a file with content."""
        result = create_file(
            str(temp_working_dir), "withcontent.txt", "initial content"
        )

        assert "Successfully created" in result
        assert (temp_working_dir / "withcontent.txt").read_text() == "initial content"

    def test_create_file_in_subdirectory(self, temp_working_dir):
        """Test creating a file in a subdirectory."""
        result = create_file(str(temp_working_dir), "subdir/file.txt", "content")

        assert "Successfully created" in result
        assert (temp_working_dir / "subdir" / "file.txt").exists()

    def test_create_file_creates_directories(self, temp_working_dir):
        """Test that create_file creates nested directories."""
        result = create_file(
            str(temp_working_dir), "deep/nested/path/file.txt", "content"
        )

        assert "Successfully created" in result
        assert (temp_working_dir / "deep" / "nested" / "path").exists()

    def test_create_file_empty_directory_already_exists(self, temp_working_dir):
        """Test creating a file when parent directory already exists."""
        (temp_working_dir / "existing").mkdir()

        result = create_file(str(temp_working_dir), "existing/file.txt", "content")

        assert "Successfully created" in result
        assert (temp_working_dir / "existing" / "file.txt").exists()

    def test_path_traversal_attack(self, temp_working_dir):
        """Test security check for path traversal."""
        result = create_file(
            str(temp_working_dir), "../../../etc/malicious.txt", "bad content"
        )

        assert "Error:" in result
        assert "outside the working directory" in result

    def test_create_file_with_empty_content(self, temp_working_dir):
        """Test creating a file with empty content."""
        result = create_file(str(temp_working_dir), "empty.txt", "")

        assert "Successfully created" in result
        assert (temp_working_dir / "empty.txt").read_text() == ""

    def test_create_file_overwrite_existing(self, temp_working_dir):
        """Test that create_file overwrites existing files."""
        (temp_working_dir / "existing.txt").write_text("old content")

        result = create_file(str(temp_working_dir), "existing.txt", "new content")

        assert "Successfully created" in result
        assert (temp_working_dir / "existing.txt").read_text() == "new content"


class TestSchemaCreateFile:
    """Tests for schema_create_file function."""

    def test_schema_name(self):
        """Test that schema has correct name."""
        assert schema_create_file.name == "create_file"

    def test_schema_description(self):
        """Test that schema has description."""
        assert schema_create_file.description is not None
        assert "create" in schema_create_file.description.lower()

    def test_schema_file_path_parameter(self):
        """Test that file_path parameter is defined."""
        params = schema_create_file.parameters
        if params is not None and params.properties is not None:
            assert "file_path" in params.properties
            assert params.properties["file_path"].type == types.Type.STRING

    def test_schema_content_parameter(self):
        """Test that content parameter is defined."""
        params = schema_create_file.parameters
        if params is not None and params.properties is not None:
            assert "content" in params.properties
            assert params.properties["content"].type == types.Type.STRING

    def test_schema_required_fields(self):
        """Test that file_path is required."""
        params = schema_create_file.parameters
        if params is not None and params.required is not None:
            assert "file_path" in params.required
            # content should not be required (defaults to empty string)
            assert "content" not in params.required
