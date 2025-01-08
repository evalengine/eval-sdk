from setuptools import setup, find_packages
import os

PWD = os.path.abspath(os.path.dirname(__file__))

setup(
    name="eva-sdk",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "aiohttp>=3.11.11",
        "cryptography>=3.4.7",
        "pyasn1>=0.4.8",
        "requests>=2.28.0",
        "secp256k1>=0.13.2",

        f"postchain_client_py @ file://{PWD}/postchain_client_py",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
        ],
    },
    python_requires=">=3.7",
    author="Your Name",
    author_email="your.email@example.com",
    description="A brief description of your project",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/username/project",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 