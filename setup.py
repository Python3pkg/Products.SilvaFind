# -*- coding: utf-8 -*-
# Copyright (c) 2006-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from setuptools import setup, find_packages
import os

version = '1.2.2dev'

setup(name='Products.SilvaFind',
      version=version,
      description="Search support for Silva.",
      long_description=open(os.path.join("Products", "SilvaFind", "README.txt")).read() + "\n" +
                       open(os.path.join("Products", "SilvaFind","HISTORY.txt")).read(),
      classifiers=[
              "Framework :: Zope2",
              "Programming Language :: Python",
              "Topic :: Software Development :: Libraries :: Python Modules",
              ],
      keywords='silva search zope2',
      author='Infrae',
      author_email='info@infrae.com',
      url='http://infrae.com/products/silva/extensions/silva_find',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
              'Products.Silva',
              'five.grok',
              'setuptools',
              'silva.core.conf',
              'silva.core.interfaces',
              'silva.core.services',
              'silva.core.views',
              'zope.component',
              'zope.interface',
              'zope.traversing',
              ],
      )
