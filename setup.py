from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="evaengine",
    version="0.1.1",
    author="Chromia",
    author_email="prem.kumar@chromaway.com",
    description="A powerful tweet evaluation engine using advanced LLM models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chromindscan/eva-ui",
    project_urls={
        "Documentation": "https://api.evaengine.ai/docs",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        "pydantic>=2.0.0",
        "aiohttp>=3.8.0",
        "python-dotenv>=0.19.0"
    ],
)