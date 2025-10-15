from setuptools import setup, find_packages

setup(
    name="hello-world-service",
    version="1.0.0",
    description="Simple Hello World Flask Service",
    author="Test Team",
    packages=find_packages(),
    install_requires=[
        "Flask==2.3.3"
    ],
    extras_require={
        "test": [
            "pytest==7.4.2",
            "pytest-html==4.1.1",
            "allure-pytest==2.13.2",
            "requests==2.31.0",
            "weasyprint==52.5"
        ]
    },
    python_requires=">=3.8",
)