from setuptools import setup, find_packages

setup(
    name="expense-classifier",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "sqlalchemy",
        "openpyxl",
        "pyyaml",
    ],
    entry_points={
        'console_scripts': [
            'expense-classifier=expense_classifier.main:main',
        ],
    },
    author="Author",
    author_email="author@example.com",
    description="A tool for classifying expenses from bank statements",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/username/expense-classifier",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
