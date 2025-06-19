#!/usr/bin/env python3
"""
Development environment setup script using uv.
This script helps set up and manage the development environment using uv.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    return subprocess.run(command, check=check, text=True)


def setup_dev_environment():
    """Set up the development environment using uv."""

    # Ensure we're in the project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    try:
        # Install uv if not already installed
        try:
            run_command(["uv", "--version"])
        except (subprocess.CalledProcessError, FileNotFoundError):
            run_command([sys.executable, "-m", "pip", "install", "uv"])

        # Create virtual environment if it doesn't exist
        venv_path = project_root / ".venv"
        if not venv_path.exists():
            run_command(["uv", "venv"])

        # Install dependencies
        run_command(["uv", "pip", "install", "-r", "requirements.txt"])

        # Install development dependencies
        dev_packages = ["pytest", "ruff", "pre-commit", "black", "mypy"]
        run_command(["uv", "pip", "install", *dev_packages])

        # Install pre-commit hooks
        run_command(["pre-commit", "install"])

        if os.name == "nt":  # Windows
            pass
        else:  # Unix-like
            pass

    except subprocess.CalledProcessError:
        sys.exit(1)


if __name__ == "__main__":
    setup_dev_environment()
