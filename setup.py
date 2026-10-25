#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="django-ical",
    description="iCal feeds for Django based on Django's syndication feed framework.",
    long_description="\n".join(
        [
            open("README.rst", encoding="utf-8").read(),
            open("CHANGES.rst", encoding="utf-8").read(),
        ]
    ),
    keywords="ical calendar django syndication feed",
    author="Ian Lewis",
    author_email="security@jazzband.com",
    maintainer="Jazzband",
    maintainer_email="security@jazzband.com",
    license="MIT License",
    url="https://github.com/jazzband/django-ical",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Environment :: Plugins",
        "Framework :: Django",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.11",
    install_requires=["django>=4.1.3", "icalendar>=4.0.3", "django-recurrence>=1.11.1"],
    packages=find_packages(),
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
)
