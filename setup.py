import codecs

from os import path
from setuptools import find_packages, setup


def read(*parts):
    filename = path.join(path.dirname(__file__), *parts)
    with codecs.open(filename, encoding="utf-8") as fp:
        return fp.read()


setup(
    author="Pinax Developers",
    author_email="developers@pinaxproject.com",
    description="",
    name="pinax-identity",
    long_description=read("README.md"),
    version="0.1.0",
    url="http://github.com/pinax/pinax-identity/",
    license="MIT",
    packages=find_packages(),
    package_data={
        "identity": []
    },
    install_requires=[
        "django-oidc-provider==0.3.6",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=False
)
