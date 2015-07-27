from setuptools import setup
from setuptools import find_packages


setup(
    name='doceboSSO',
    version='0.0.0',
    description='Single Sign On Implementation for the Docebo LMS',
    author='Chris Dee',
    author_email='chris.dee@optimizely.com',
    url='http://github.com/optimizely/docebo-SSO',
    classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: Web Environment',
      'Intended Audience :: Developers',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages(
      exclude=['tests']
    ),
    install_requires=[
      'requests>=2.6.0',
    ],
    test_suite='sso_test',
)
