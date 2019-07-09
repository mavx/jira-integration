import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="jira-integration",
    version="0.1.16",
    author="mauyong",
    author_email="author@example.com",
    description="JIRA utility commands",
    long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/mavx/jira-integration",
    python_requires="~=3.6",
    install_requires=[
        "jira",
        "click",
        "crayons",
        "python-dateutil"
    ],
    packages=["jiraintegration"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
