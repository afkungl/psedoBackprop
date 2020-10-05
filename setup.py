#!/usr/bin/env python
"""
  Setup for pip install using setuptools
"""

from setuptools import setup
import pseudo_backprop

version = pseudo_backprop.__version__

setup(name='pseudoBackprop',
      version="0.1",
      description='',
      author='Akos Kungl',
      author_email='afkungl@kip.uni-heidelberg.de',
      url='https://github.com/afkungl/psedoBackprop',
      packages=["pseudo_backprop"],
      package_dir={
          "pseudoBackprop": "pseudoBackprop",
      },
      license="GNUv3",
      install_requires=["matplotlib", "numpy", "torch"],
      )
