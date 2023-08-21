import os
from pathlib import Path
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, "pycrossva", "__version__.py"),
          mode="r", encoding="utf-8") as f:
    exec(f.read(), about)

this_directory = Path(__file__).parent
readme = (this_directory / "Readme.rst").read_text()

setup(name=about["__title__"],
      version=about["__version__"],
      description=about["__description__"],
      long_description=readme,
      long_description_content_type="text/x-rst",
      url=about["__url__"],
      author=about["__author__"],
      maintainer=about["__maintainer__"],
      maintainer_email=about["__maintainer_email__"],
      license=about["__license__"],
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
