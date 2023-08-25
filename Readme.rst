pyCrossVA
=========

.. image:: https://img.shields.io/pypi/pyversions/pycrossva
    :target: https://pypi.org/project/pycrossva
.. image:: http://readthedocs.org/projects/pycrossva/badge/
    :target: http://pycrossva.readthedocs.io/
.. image:: https://ci.appveyor.com/api/projects/status/d1b842ik4c95x47h?svg=true
    :target: https://ci.appveyor.com/project/jarathomas/pycrossva


Simple Usage - Python
---------------------

The simplest way to get started with CrossVA is to invoke the ``transform`` function
with a default mapping, and the path to a csv containing your raw verbal autopsy
data.

.. code-block:: python

  from pycrossva.transform import transform

  transform(("2016WHOv151", "InterVA5"), "path/to/data.csv")

You can also call the transform function on a Pandas DataFrame, if you wanted to
read in and process the data before calling the function.

.. code-block:: python

  from pycrossva.transform import transform

  input_data = pd.read_csv("path/to/data.csv")
  input_data = some_special_function(input_data)
  final_data = transform(("2016WHOv151", "InterVA5"), input_data)

The transform function returns a Pandas DataFrame object. To write the Pandas DataFrame
to a csv, you can do:

.. code-block:: python

  final_data.to_csv("filename.csv")

pyCrossVA is a python package for transforming verbal autopsy data collected using
the 2016 WHO VA instrument (v1.5.1, or v1.4.1), 2012 WHO VA instrument, and
the PHRMC short questionnaire into a format suitable for openVA.

The flagship function of this package is the transform() function, which
prepares raw data for use in a verbal autopsy algorithm. The user can either
choose to use a default mapping, or create a custom one of their own design. The
default mappings are listed in `Currently Supported`_ and can be invoked by
passing in a tuple as the mapping argument in ``("input", "output")`` format.


Command Line
------------

`pycrossva` also contains a command line tool, `pycrossva-transform` that acts as
a wrapper for the `transform` python function in the pycrossva
package. Once you have installed pycrossva, you can run this from the command
line in order to process verbal autopsy data without having to touch python code.
If you have multiple input files to process from the same input type (or source format) to the same
output type (or algorithm), you can run them all in a single command.

If no destination (--dst) is specified, the default behavior will be to write
the resulting data to a csv in the current working directory with a name in
the pattern of "output_type_from_src_mmddyy", where mmddyy is the current
date. If `dst` is a directory, then the result file will still have the
default name. If `dst` ends in '.csv' but multiple input files are given,
then the output files will be written to dst_1.csv, dst_2.csv, etc.

`pycrossva-transform` takes 3 positional arguments:
  *  `input_type`: source type of the input data (the special input type of 'AUTODETECT' specifies that the type should be detected automatically if possible)
  *  `output_type`: format of output data (which algorithm the data should be prepared for)
  *  `src`: filepath to the input data - can take multiple arguments, separated by a space

Examples:

.. code-block:: bash

    $ pycrossva-transform 2012WHO InterVA4 path/to/mydata.csv
    2012WHO 'path/to/my/data.csv' data prepared for InterVA4 and written to csv at 'my/current/directory/InterVA4_from_mydata_042319.csv'

    $ pycrossva-transform 2012WHO InterVA4 path/to/mydata1.csv path/to/another/data2.csv --dst outputfolder
    2012WHO 'path/to/mydata1.csv' data prepared for InterVA4 and written to csv at 'outputfolder/InterVA4_from_mydata1_042319.csv'
    2012WHO 'path/to/another/data2.csv' data prepared for InterVA4 and written to csv at 'outputfolder/InterVA4_from_data2_042319.csv'

    $ pycrossva-transform 2012WHO InterVA4 path/to/mydata1.csv path/to/another/data2.csv --dst outputfolder/results.csv
    2012WHO 'path/to/mydata1.csv' data prepared for InterVA4 and written to csv at 'outputfolder/results_1.csv'
    2012WHO 'path/to/another/data2.csv' data prepared for InterVA4 and written to csv at 'outputfolder/results_2.csv'

    $ pycrossva-transform AUTODETECT InterVA4 path/to/mydata.csv
    Detected input type: 2012WHO
    2012WHO 'path/to/my/data.csv' data prepared for InterVA4 and written to csv at 'my/current/directory/InterVA4_from_mydata_042319.csv'


Running Tests
-------------

To run unit tests, first make sure all requirements are installed

    pip install -r requirements.txt

Also make sure that pytest is installed

    pip install pytest

Finally, run the tests

    pip install . && cd pycrossva && python -m pytest --doctest-modules

Currently Supported
--------------------

Inputs
^^^^^^^

* 2016 WHO Questionnaire from ODK export, v1.5.1
* 2016 WHO Questionnaire from ODK export, v1.4.1
* 2012 WHO Questionnaire from ODK export
* PHRMC Shortened Questionnaire

Outputs
^^^^^^^^

* InSilicoVA
* InSilicoVA_2012
* InterVA4
* InterVA5

Roadmap
-------

This is an alpha version of package functionality, with only limited support.

Expanding outputs
^^^^^^^^^^^^^^^^^^

One component of moving to a production version will be to offer additional
mapping files to support more output formats. The package currently supports
mapping to the InterVA4 and InSilicoVA format.

The following is a list of
additional outputs for other algorithms to be supported in future versions:

* Tariff
* Tariff 2.0

Style
-----

This package was written using google style guide for Python and PEP8 standards.
Tests have been written using doctest.

Background
----------

About Verbal Autopsy
^^^^^^^^^^^^^^^^^^^^

From `Wikipedia <https://en.wikipedia.org/wiki/Verbal_autopsy>`_:

  A verbal autopsy (VA) is a method of gathering health information about a deceased
  individual to determine his or her cause of death. Health information and a
  description of events prior to death are acquired from conversations or
  interviews with a person or persons familiar with the deceased and analyzed by
  health professional or computer algorithms to assign a probable cause of death.

  Verbal autopsy is used in settings where most deaths are undocumented. Estimates
  suggest a majority of the 60 million annual global deaths occur without medical
  attention or official medical certification of the cause of death. The VA method
  attempts to establish causes of death for previously undocumented subjects,
  allowing scientists to analyze disease patterns and direct public health policy
  decisions.

  Noteworthy uses of the verbal autopsy method include the Million Death Study in
  India, China's national program to document causes of death in rural areas, and
  the Global Burden of Disease Study 2010.


License
--------

This package is licensed under the GNU GENERAL PUBLIC LICENSE (v3, 2007).
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
