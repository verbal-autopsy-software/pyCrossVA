#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Defines main CrossVA function, `transform` which maps raw VA data into data
for use with a VA algorithm in OpenVA.
"""

import pandas as pd
from configuration import Configuration, CrossVA
from utils import flexible_read


def transform(mapping, raw_data, verbose=2, preserve_na=True):
    """transforms raw VA data (`raw_data`) into data suitable for use with a VA
    algorithm, according to the specified transformations given in `mapping`.

    Args:
        mapping (string, tuple or Pandas DataFrame): Should be either a tuple
            in form (input, output), a path to csv containing a configuration
            data file, or a Pandas DataFrame containing configuration data
        raw_data (string or Pandas DataFrame): raw verbal autopsy data to
            process
        verbose (int): integer from 0 to 5, controlling how much status detail
            is printed to console. Silent if 0. Defaults to 2.
        preserve_na (bool): whether to preserve NAs in data, or to count them
            as FALSE. Overridden with True for InsillicoVA, False for InterVA4
            when mapping is given as a tuple.

    Returns:
        Pandas DataFrame: the raw data transformed according to specifications
        given in mapping data.

    Examples:
        You can specify the mapping as (input, output) and the path to csv:
            
        >>> transform(("2016WHOv151", "InterVA4"), "resources/sample_data/mock_data_1.csv").iloc[:5,:5]
           AB_POSIT  AB_SIZE  ABD_MASS  ABD_PAIN  ABDOM
        0     False     True     False      True  False
        1     False    False      True     False   True
        2     False    False      True     False  False
        3      True    False     False     False  False
        4     False    False     False      True  False
    
        >>> transform(("2016WHOv151", "InsillicoVA"), "resources/sample_data/mock_data_1.csv").iloc[:5,:5]
          AB_POSIT AB_SIZE ABD_MASS ABD_PAIN  ABDOM
        0    False    True    False     True  False
        1      NaN     NaN     True      NaN   True
        2      NaN   False     True    False    NaN
        3     True   False      NaN    False    NaN
        4      NaN     NaN      NaN     True  False
        
        Or you can give the data and mapping as Pandas DataFrames:
            
        >>> my_special_data = pd.read_csv("resources/sample_data/mock_data_1.csv")
        >>> my_special_mapping = pd.read_csv("resources/mapping_configuration_files/example_config_1.csv")
        >>> transform(my_special_mapping, my_special_data).iloc[:5,:5]
          AB_POSIT AB_SIZE AC_BRL AC_CONV AC_COUGH
        0    False    True   True   False     True
        1      NaN     NaN   True   False    False
        2      NaN   False   True    True    False
        3     True   False   True   False     True
        4      NaN     NaN   True    True     True
    
        However, the mapping-data relationship must be valid.
        
        >>> bad_mapping = pd.read_csv("resources/mapping_configuration_files/example_config_2.csv")
        >>> transform(bad_mapping, my_special_data).iloc[:5,:5]
        Traceback (most recent call last):
        ValueError: Configuration from mapping file must be valid before
        transform.

    """
    mapping_data = pd.DataFrame()
    # TODO - this is clunky in current form, could stand to be more elegant
    # read in mapping data
    if isinstance(mapping, tuple):  # if mapping is in (input, output) format
        internal_path = "resources/mapping_configuration_files/"
        if len(mapping) == 2:
            supported_outputs = ["InterVA4", "InsillicoVA"]
            supported_inputs = ["2016WHOv151"]
            if mapping[0] in supported_inputs:
                if mapping[1] in supported_outputs:
                    preserve_na = mapping[1] == "InsillicoVA" #overides given
                    mapping_data = pd.read_csv((f"{internal_path}"
                                                f"{mapping[0]}_to_"
                                                f"{mapping[1]}.csv"))
                else:
                    raise ValueError(("Output not supported. Expected one of"
                                      f" {supported_outputs}, but received "
                                      f"'{mapping[1]}'"))
            else:
                raise ValueError(("Input not supported. Expected one of"
                                  f" {supported_inputs}, but received "
                                  f"'{mapping[0]}'"))
        else:
            raise ValueError(("If mapping is tuple, input should be of length "
                              "two in the form (input type, output type)"))

    else:
        mapping_data = flexible_read(mapping)

    if mapping_data.empty:  # this shouldn't happen; if it does, raise
        raise ValueError(("No valid mapping data provided to transform. Should be"
                       " either a tuple in form (input, output), a path to csv"
                       " or a Pandas DataFrame."))

    # init configuration obj from given mapping data
    config = Configuration(mapping_data, verbose, process_strings=False)

    # if the configuration isn't valid, or if the data isn't valid for the
    # config file, then raise error
    if not config.validate():
        # Raise Error
        raise ValueError(("Configuration from mapping file must be valid "
                           "before transform."))

    # TODO adds args to init based on data type?
    input_data = flexible_read(raw_data)
    cross_va = CrossVA(input_data, config)
    if not cross_va.validate():
        raise ValueError(("Cannot transform if provided raw data and "
                           "configuration file are not a valid match."))
    final_data = cross_va.process()

    if preserve_na:
        return final_data
    return final_data.fillna(False)

# transform(("2016WHOv151", "InterVA4"), "resources/sample_data/mock_data_1.csv")
    
