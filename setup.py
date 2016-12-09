"""yml2sif setup module

"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='yml2sif',
      version='0.1.0', 
      long_description=long_description,
      description='YAML to sif translator.',
      url='https://github.com/CSC-IT-Center-for-science/yml2sif',
      author='Juhani Kataja / CSC',
      author_email='juhani.kataja@csc.fi',
      license='MIT',
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',],
      keywords='science yml sif helper',
      install_requires=['pyyaml','argparse'],
      packages=find_packages(),
      entry_points={
          'console_sripts': [
              'yml2sif = ymlsif:main']})


