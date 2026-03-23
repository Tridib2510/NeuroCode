import pytest
from unittest.mock import Mock, patch, MagicMock
from google.genai import types
from pathlib import Path
import base64

from neurocode.functions.image_analysis.analyzeImage import (
    analyze_image,
    schema_analyze_image,
)


class TestAnalyzeImage:
    """Tests for analyze_image function."""

    def test_analyze_image_classification_success(
        self, mock_gemini_client, sample_image_path, temp_working_dir
    ):
        """Test successful image classification."""
        mock_response = mock_gemini_client.models.generate_content.return_value
        mock_response.text = "This image shows a cat with confidence 0.95"

        with patch(
            "neurocode.functions.image_analysis.analyzeImage.genai.Client"
        ) as mock_client_class:
            mock_client_class.return_value = mock_gemini_client

            result = analyze_image(
                str(temp_working_dir),
                Path(sample_image_path).name,
                "image-classification",
                "test-api-key",
            )

            assert "Image Analysis Results" in result
            assert "cat" in result
            assert "confidence" in result
            mock_gemini_client.models.generate_content.assert_called_once()

    def test_analyze_image_description_success(
        self, mock_gemini_client, sample_image_path, temp_working_dir
    ):
        """Test successful image description."""
        mock_response = mock_gemini_client.models.generate_content.return_value
        mock_response.text = (
            "A detailed description of the image with colors, objects, and setting."
        )

        with patch(
            "neurocode.functions.image_analysis.analyzeImage.genai.Client"
        ) as mock_client_class:
            mock_client_class.return_value = mock_gemini_client

            result = analyze_image(
                str(temp_working_dir),
                Path(sample_image_path).name,
                "description",
                "test-api-key",
            )

            assert "Image Description" in result
            assert "detailed description" in result

    def test_analyze_image_with_absolute_path(
        self, mock_gemini_client, sample_image_path, temp_working_dir
    ):
        """Test analyzing an image with absolute path."""
        mock_response = mock_gemini_client.models.generate_content.return_value
        mock_response.text = "Image analyzed successfully"

        with patch(
            "neurocode.functions.image_analysis.analyzeImage.genai.Client"
        ) as mock_client_class:
            mock_client_class.return_value = mock_gemini_client

            # Pass absolute path
            result = analyze_image(
                str(temp_working_dir),
                sample_image_path,
                "image-classification",
                "test-api-key",
            )

            assert "Image Analysis Results" in result

    def test_analyze_image_nonexistent_file(self, temp_working_dir):
        """Test analyzing a non-existent image file."""
        result = analyze_image(
            str(temp_working_dir),
            "nonexistent.jpg",
            "image-classification",
            "test-api-key",
        )

        assert "Error:" in result
        assert "does not exist" in result

    def test_analyze_image_path_traversal_attack(self, temp_working_dir):
        """Test security check for path traversal."""
        result = analyze_image(
            str(temp_working_dir),
            "../../../etc/passwd",
            "image-classification",
            "test-api-key",
        )

        assert "Error:" in result
        assert "outside the working directory" in result

    def test_analyze_image_missing_api_key(self, sample_image_path, temp_working_dir):
        """Test analyzing image without API key."""
        with patch.dict("os.environ", {}, clear=True):
            result = analyze_image(
                str(temp_working_dir),
                Path(sample_image_path).name,
                "image-classification",
                None,
            )

            assert "Error:" in result
            assert "GEMINI_API_KEY" in result
            assert "not provided" in result or "not found" in result

    def test_analyze_image_unsupported_task(self, sample_image_path, temp_working_dir):
        """Test analyzing image with unsupported task type."""
        result = analyze_image(
            str(temp_working_dir),
            Path(sample_image_path).name,
            "unsupported-task",
            "test-api-key",
        )

        assert "Error:" in result
        assert "Unsupported task" in result
        assert "image-classification" in result
        assert "description" in result

    def test_analyze_image_no_response_from_model(
        self, mock_gemini_client, sample_image_path, temp_working_dir
    ):
        """Test when model returns no text response."""
        mock_response = mock_gemini_client.models.generate_content.return_value
        mock_response.text = None

        with patch(
            "neurocode.functions.image_analysis.analyzeImage.genai.Client"
        ) as mock_client_class:
            mock_client_class.return_value = mock_gemini_client

            result = analyze_image(
                str(temp_working_dir),
                Path(sample_image_path).name,
                "image-classification",
                "test-api-key",
            )

            assert "Error:" in result
            assert "No response" in result

    def test_analyze_image_api_exception(
        self, mock_gemini_client, sample_image_path, temp_working_dir
    ):
        """Test handling of API exceptions."""
        mock_gemini_client.models.generate_content.side_effect = Exception("API Error")

        with patch(
            "neurocode.functions.image_analysis.analyzeImage.genai.Client"
        ) as mock_client_class:
            mock_client_class.return_value = mock_gemini_client

            result = analyze_image(
                str(temp_working_dir),
                Path(sample_image_path).name,
                "image-classification",
                "test-api-key",
            )

            assert "Error:" in result
            assert "Failed to analyze image" in result

    def test_analyze_image_file_read_error(self, temp_working_dir):
        """Test handling of file read errors."""
        # Create a file that can't be read
        file_path = temp_working_dir / "unreadable.jpg"
        file_path.write_bytes(b"")

        with patch("builtins.open", side_effect=IOError("Cannot read file")):
            result = analyze_image(
                str(temp_working_dir),
                "unreadable.jpg",
                "image-classification",
                "test-api-key",
            )

            assert "Error:" in result
            assert "Could not read image file" in result

    def test_analyze_image_base64_encoding(
        self, mock_gemini_client, sample_image_path, temp_working_dir
    ):
        """Test that image is properly base64 encoded."""
        mock_response = mock_gemini_client.models.generate_content.return_value
        mock_response.text = "Analysis result"

        with patch(
            "neurocode.functions.image_analysis.analyzeImage.genai.Client"
        ) as mock_client_class:
            mock_client_class.return_value = mock_gemini_client

            analyze_image(
                str(temp_working_dir),
                Path(sample_image_path).name,
                "image-classification",
                "test-api-key",
            )

            # Check that generate_content was called with proper content
            call_args = mock_gemini_client.models.generate_content.call_args
            contents = call_args[1]["contents"][0]

            # Verify inline_data blob is present
            assert len(contents.parts) >= 2
            assert hasattr(contents.parts[0], "inline_data")
            assert hasattr(contents.parts[0].inline_data, "mime_type")
            assert "image/jpeg" in contents.parts[0].inline_data.mime_type

    def test_analyze_image_default_task(
        self, mock_gemini_client, sample_image_path, temp_working_dir
    ):
        """Test that default task is image-classification."""
        mock_response = mock_gemini_client.models.generate_content.return_value
        mock_response.text = "Image classified"

        with patch(
            "neurocode.functions.image_analysis.analyzeImage.genai.Client"
        ) as mock_client_class:
            mock_client_class.return_value = mock_gemini_client

            # Don't specify task
            result = analyze_image(
                str(temp_working_dir),
                Path(sample_image_path).name,
                api_key="test-api-key",
            )

            assert "Image Analysis Results" in result


class TestSchemaAnalyzeImage:
    """Tests for schema_analyze_image function."""

    def test_schema_name(self):
        """Test that schema has correct name."""
        assert schema_analyze_image.name == "analyze_image"

    def test_schema_description(self):
        """Test that schema has description."""
        assert schema_analyze_image.description is not None
        assert "image" in schema_analyze_image.description.lower()
        assert "analyze" in schema_analyze_image.description.lower()

    def test_schema_image_path_parameter(self):
        """Test that image_path parameter is defined."""
        params = schema_analyze_image.parameters
        assert params is not None
        assert "image_path" in params.properties
        assert params.properties["image_path"].type == types.Type.STRING

    def test_schema_task_parameter(self):
        """Test that task parameter is defined."""
        params = schema_analyze_image.parameters
        assert params is not None
        assert "task" in params.properties
        assert params.properties["task"].type == types.Type.STRING

    def test_schema_task_enum_values(self):
        """Test that task enum values are correct."""
        params = schema_analyze_image.parameters
        assert params is not None
        task_param = params.properties["task"]
        assert task_param.enum is not None
        assert "image-classification" in task_param.enum
        assert "description" in task_param.enum

    def test_schema_required_fields(self):
        """Test that image_path is required."""
        params = schema_analyze_image.parameters
        assert params is not None
        assert "image_path" in params.required
        assert "task" not in params.required  # task is optional

    def test_schema_description_mentions_absolute_paths(self):
        """Test that schema description mentions absolute paths support."""
        assert schema_analyze_image.description is not None
        assert (
            "absolute path" in schema_analyze_image.description.lower()
            or "absolute" in schema_analyze_image.description.lower()
        )
