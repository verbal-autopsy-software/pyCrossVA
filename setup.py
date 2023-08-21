import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

setup(name="pycrossva",
      version="0.95",
      description="prepare data from WHO and PHRMC instruments for verbal autopsy algorithms",
      url="https://github.com/verbal-autopsy-software/pyCrossVA",
      license="GNU General Public License v3.0",
      packages=[
          "pycrossva",
          "pycrossva.resources.mapping_configuration_files",
          "pycrossva.resources.sample_data",
          "pycrossva.scripts",
      ],
      entry_points='''
                    [console_scripts]
                    pycrossva-transform=pycrossva.scripts.pycrossva_transform:main
                    ''',
      keywords="verbal autopsy data preparation",
      install_requires=["numpy", "pandas", "Click"],
      classifiers=[
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3.11",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: POSIX :: Linux",
      ],
      zip_safe=False,
      )
