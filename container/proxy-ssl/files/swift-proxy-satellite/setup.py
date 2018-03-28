# !/usr/bin/python

from setuptools import setup

setup(name='proxy_satellite',
      version='0.0.1',
      author='SwiftStack',
      packages=['proxy_satellite'],
      entry_points={
          'paste.filter_factory': [
              'proxy_satellite=proxy_satellite:filter_factory',
          ],
      })
