#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-ical',
    version='1.5',
    description="iCal feeds for Django based on Django's syndication feed "
                "framework.",
    long_description=(open('README.rst').read() + '\n' +
                      open('CHANGES.rst').read()),
    author='Ian Lewis',
    author_email='IanMLewis@gmail.com',
    license='MIT License',
    url='https://github.com/jazzband/django-ical',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'Django>=1.11',
        'icalendar>=4.0.3',
        'django-recurrence>=1.10.0',
    ],
    packages=find_packages(),
    test_suite='tests.main',
)
