#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-ical',
    version='1.4',
    description="iCal feeds for Django based on Django's syndication feed "
                "framework.",
    long_description=(open('README.rst').read() + '\n' +
                      open('CHANGES.rst').read()),
    author='Ian Lewis',
    author_email='IanMLewis@gmail.com',
    license='MIT License',
    url='https://github.com/Pinkerton/django-ical',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Django',
        'Framework :: Django :: 1.3',
        'Framework :: Django :: 1.4',
        'Framework :: Django :: 1.5',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'Django>=1.3.4',
        'icalendar>=3.1',
    ],
    packages=find_packages(),
    test_suite='tests.main',
)
