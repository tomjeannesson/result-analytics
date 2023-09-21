from distutils.core import setup

from setuptools import find_packages

setup(
    name="result-analytics",
    packages=find_packages(exclude=["test", "test.*"]),
    version="{{VERSION}}",
    license="MIT",
    description="A simple project to extract data from PDFs and analyse them.",
    long_description="A simple project to extract data from PDFs and analyse them.",
    author="Mateo & Tom Jeannesson",
    author_email="tomjeannesson@gmail.com",
    url="https://github.com/tomjeannesson/result-analytics",
    download_url="https://github.com/tomjeannesson/result-analytics/archive/refs/tags/v{{VERSION}}.tar.gz",
    keywords=["Sport", "Ski", "Result", "Analytics", "Moguls"],
    install_requires=["PyPDF2>=3.0.0", "pandas"],
    classifiers=[
        "Development Status :: 4 - Beta",  # "3 - Alpha", "4 - Beta" or "5 - Production/Stable "
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
    ],
)
