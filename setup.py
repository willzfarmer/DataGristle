#!/usr/bin/env python

import os
from setuptools import setup, find_packages

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

version          = "0.56"
DESCRIPTION      = 'A toolbox and library of ETL, data quality, and data analysis tools'

setup(name             = 'datagristle'     ,
      version          = version           ,
      description      = DESCRIPTION       ,
      long_description=(read('README.rst') + '\n\n' +
                        read('CHANGELOG.rst')),
      keywords         = "data analysis quality utility etl",
      author           = 'Ken Farmer'      ,
      author_email     = 'kenfar@gmail.com',
      url              = 'http://github.com/kenfar/DataGristle',
      license          = 'BSD'             ,
      classifiers=[
            'Development Status :: 5 - Production/Stable'            ,
            'Environment :: Console'                                 ,
            'Intended Audience :: Developers'                        ,
            'Intended Audience :: Information Technology'            ,
            'Intended Audience :: Science/Research'                  ,
            'License :: OSI Approved :: BSD License'                 ,
            'Programming Language :: Python'                         ,
            'Operating System :: POSIX'                              ,
            'Topic :: Scientific/Engineering'                        ,
            'Topic :: Database'                                      ,
            'Topic :: Scientific/Engineering :: Information Analysis',
            'Topic :: Text Processing'                               ,
            'Topic :: Utilities'
            ],
      scripts      = ['scripts/gristle_determinator'  ,
                      'scripts/gristle_differ'        ,
                      'scripts/gristle_file_converter',
                      'scripts/gristle_filter'        ,
                      'scripts/gristle_freaker'       ,
                      'scripts/gristle_metadata'      ,
                      'scripts/gristle_md_reporter'   ,
                      'scripts/gristle_scalar'        ,
                      'scripts/gristle_slicer'        ,
                      'scripts/gristle_validator'     ,
                      'scripts/gristle_viewer'         ],
      install_requires     = ['appdirs     >= 1.2.0' ,
                              'sqlalchemy  >= 0.8.4' ,
                              'envoy       >= 0.0.2' ,
                              'pytest      >= 2.5.2' ,
                              'tox         >= 1.7.0' ,
                              'validictory >= 0.9.3' ,
                              'pyyaml      >= 3.10'  ,
                              'unittest2'           ],
      packages     = find_packages(),
     )
