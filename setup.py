from setuptools import setup, find_packages
import os

# Read version dynamically from the package
version = None
with open(os.path.join(os.path.dirname(__file__), "expense_classifier", "__init__.py")) as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().replace('"', '')
            break

# Read long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="expense-classifier",
    version=version,
    packages=find_packages(),
    install_requires=[
        "alembic==1.14.0",
        "pandas==2.2.3",
        "psycopg2-binary==2.9.10",
        "SQLAlchemy==2.0.36",
        "openpyxl==3.1.5",
        "transformers~=4.51.3",
        "pyyaml",
        "numpy"
    ],
    entry_points={
        'console_scripts': [
            'expense-classifier=expense_classifier.main:main',
        ],
    },
    author="Author",
    author_email="author@example.com",
    description="A tool for classifying expenses from bank statements",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/expense-classifier",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console"
    ],
    python_requires=">=3.8",
)

# Note: Modern builds should use pyproject.toml for configuration and packaging.
