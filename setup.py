import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

setup(name='pycrossva',
      version='0.8',
      description='prepare data from WHO and PHRMC instruments for verbal autopsy algorithms',
      url='https://github.com/verbal-autopsy-software/pyCrossVA',
      license='GNU General Public License v3.0',
      packages=find_packages(),
      entry_points='''
                    [console_scripts]
                    pycrossva-transform=pycrossva.scripts.pycrossva_transform:main
                    ''',
      include_package_data=True,
      package_data={
          'pycrossva': ['resources/mapping/*', 'resources/sample_data/*'],
      },
      keywords="verbal autopsy data preparation",
      install_requires=['numpy', 'pandas', 'Click'],
      zip_safe=False)
