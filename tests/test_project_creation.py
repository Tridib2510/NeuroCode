import pytest
from unittest.mock import Mock, patch
from google.genai import types
from pathlib import Path
import subprocess

from neurocode.functions.project_creation.createReactApp import (
    create_react_vite_app,
    schema_create_react_vite_app,
)


class TestCreateReactViteApp:
    """Tests for create_react_vite_app function."""

    def test_create_react_vite_app_success(self, mock_subprocess_run, temp_working_dir):
        """Test successfully creating a React Vite app."""
        mock_subprocess_run.return_value = subprocess.CompletedProcess(
            args=["npx", "create-vite@latest", "my-app", "--template", "react"],
            returncode=0,
            stdout="Creating project in ./my-app\nDone. Now run:\n  cd my-app\n  npm install\n  npm run dev\n",
            stderr="",
        )

        result = create_react_vite_app(str(temp_working_dir), "my-app")

        assert "React Vite project 'my-app' created successfully" in result
        assert "Creating project" in result
        mock_subprocess_run.assert_called_once()

    def test_create_react_vite_app_with_different_name(
        self, mock_subprocess_run, temp_working_dir
    ):
        """Test creating a React Vite app with a custom name."""
        mock_subprocess_run.return_value = subprocess.CompletedProcess(
            args=["npx", "create-vite@latest", "custom-app", "--template", "react"],
            returncode=0,
            stdout="Creating project in ./custom-app\nDone.\n",
            stderr="",
        )

        result = create_react_vite_app(str(temp_working_dir), "custom-app")

        assert "React Vite project 'custom-app' created successfully" in result
        mock_subprocess_run.assert_called_once()

    def test_create_react_vite_app_nonzero_exit_code(
        self, mock_subprocess_run, temp_working_dir
    ):
        """Test creating a React Vite app that fails."""
        mock_subprocess_run.return_value = subprocess.CompletedProcess(
            args=["npx", "create-vite@latest", "my-app", "--template", "react"],
            returncode=1,
            stdout="",
            stderr="Error: Failed to create project\n",
        )

        result = create_react_vite_app(str(temp_working_dir), "my-app")

        assert "Error creating project" in result
        assert "Failed to create project" in result

    def test_create_react_vite_app_timeout(self, mock_subprocess_run, temp_working_dir):
        """Test handling of subprocess timeout."""
        mock_subprocess_run.side_effect = subprocess.TimeoutExpired(
            cmd="npx create-vite@latest", timeout=120
        )

        result = create_react_vite_app(str(temp_working_dir), "my-app")

        assert "Error:" in result
        assert "timed out" in result.lower() or "timeout" in result.lower()

    def test_create_react_vite_app_with_output(
        self, mock_subprocess_run, temp_working_dir
    ):
        """Test creating React app and capturing all output."""
        mock_subprocess_run.return_value = subprocess.CompletedProcess(
            args=["npx", "create-vite@latest", "test-app", "--template", "react"],
            returncode=0,
            stdout="Scaffolding project in test-app...\nInstalling dependencies...\nDone!\n",
            stderr="",
        )

        result = create_react_vite_app(str(temp_working_dir), "test-app")

        assert "Scaffolding project" in result
        assert "Installing dependencies" in result
        assert "Done!" in result

    def test_create_react_vite_app_with_warnings(
        self, mock_subprocess_run, temp_working_dir
    ):
        """Test creating React app with warnings in output."""
        mock_subprocess_run.return_value = subprocess.CompletedProcess(
            args=["npx", "create-vite@latest", "my-app", "--template", "react"],
            returncode=0,
            stdout="Creating project...\nDone.\n",
            stderr="WARN: Some warning message\n",
        )

        result = create_react_vite_app(str(temp_working_dir), "my-app")

        # Should still be successful despite warnings
        assert "React Vite project 'my-app' created successfully" in result

    def test_create_react_vite_app_exception(
        self, mock_subprocess_run, temp_working_dir
    ):
        """Test handling of unexpected exceptions."""
        mock_subprocess_run.side_effect = Exception("Unexpected error")

        result = create_react_vite_app(str(temp_working_dir), "my-app")

        assert "Error:" in result
        assert "Unexpected error" in result

    def test_create_react_vite_app_command_verification(
        self, mock_subprocess_run, temp_working_dir
    ):
        """Test that correct command is executed."""
        mock_subprocess_run.return_value = subprocess.CompletedProcess(
            args=["npx", "create-vite@latest", "my-app", "--template", "react"],
            returncode=0,
            stdout="Done.\n",
            stderr="",
        )

        create_react_vite_app(str(temp_working_dir), "my-app")

        # Verify the command includes npx create-vite
        call_args = mock_subprocess_run.call_args[0][0]
        assert "npx" in call_args
        assert "create-vite@latest" in call_args
        assert "my-app" in call_args
        assert "--template react" in call_args


class TestSchemaCreateReactViteApp:
    """Tests for schema_create_react_vite_app function."""

    def test_schema_name(self):
        """Test that schema has correct name."""
        assert schema_create_react_vite_app.name == "create_react_vite_app"

    def test_schema_description(self):
        """Test that schema has description."""
        assert schema_create_react_vite_app.description is not None
        assert "react" in schema_create_react_vite_app.description.lower()
        assert "vite" in schema_create_react_vite_app.description.lower()

    def test_schema_project_name_parameter(self):
        """Test that project_name parameter is defined."""
        params = schema_create_react_vite_app.parameters
        assert params is not None
        assert "project_name" in params.properties
        assert params.properties["project_name"].type == types.Type.STRING

    def test_schema_required_fields(self):
        """Test that project_name is required."""
        params = schema_create_react_vite_app.parameters
        assert params is not None
        assert "project_name" in params.required
