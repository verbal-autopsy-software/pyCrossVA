#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convenience functions for the CrossVA module, which help to provide a more
user-friendly experience with inputs and error messages across different files.
"""
import re
import pandas as pd


def report_list(alist, limit=10, paren=True):
    """Converts alist into a user-friendly string for clearer error messages.
    Each element is reported single quotes and seperated by commas, with the
    last element preceded by " and ".
    When limit is shorter than the list, cuts the list at the limit,
    omits the 'and', and ends with 'etc' to indicate incompleteness.

    Args:
        alist (list): Description of parameter `alist`.
        limit (int): The maximum number of items to report. If more than limit,
            the list is reported without conjunction and ends with "etc."
            Defaults to 10.
        paren (boolean): Encloses string in parentheses if true. Defaults to
            True.

    Returns:
        str: human-friendly sentence describing the items in alist

    Examples
    >>> report_list(["A","B","C"])
    "('A', 'B', and 'C')"

    >>> report_list(["A","B","C"], limit=2)
    "('A', 'B', etc)"

    >>> report_list(["A","B","C"], limit=2, paren=False)
    "'A', 'B', etc"

    >>> report_list([])
    ''
    """
    if len(alist) == 0:
        return ""

    if limit is not None:
        if len(alist) <= limit:
            limit = None
        else:
            alist = alist[:limit]

    str_list = "'" + "', '".join([str(a) for a in alist]) + "'"
    if limit is None:
        report = re.sub(r'(.*), ', r'\1, and ',
                        str_list)  # use "and" if complete
    else:
        report = str_list + ", etc"  # end with etc. if incomplete

    if paren:
        return "(" + report + ")"
    return report


def flexible_read(path_or_df):
    """Takes either a path or a Pandas DataFrame, if path, read in as a pandas
    dataframe. Convenience method to add input flexibility for main transform
    method.

    Args:
        path_or_df (string or Pandas DataFrame): Either a string representing
            a path to the file containing the data, or a dataframe that has
            already been read into Python.

    Returns:
        Pandas DataFrame: either the data at the given path as read by pandas,
            or the DataFrame constructor used on the path_or_df argument

    Examples:
    Can return a dataframe from a string:
    >>> flexible_read("resources/sample_data/2016WHO_mock_data_1.csv").iloc[:5,:5]
       ID -Id10004 -Id10019 -Id10059 -Id10077
    0   0      wet       dk  married       dk
    1   1      wet   female      NaN       dk
    2   2      dry     male       dk      NaN
    3   3       dk       dk       dk       dk
    4   4      dry      NaN  married       dk

    Or apply the pandas dataframe constructor to the input:
    >>> flexible_read(np.arange(9).reshape(3,3))
       0  1  2
    0  0  1  2
    1  3  4  5
    2  6  7  8
    """

    if isinstance(path_or_df, str):  # if mapping is path
        ext = path_or_df.split(".")[:-1]  # file extension
        if ext in ["xlsm", "xlsx", "xls"]:
            return_df = pd.read_excel(ext)
        else:
            return_df = pd.read_csv(path_or_df)
    else:
        return_df = pd.DataFrame(path_or_df)
    return return_df


def english_relationship(rel):
    """Returns abbreviated relationship as full english phrase.

    Args:
        rel (str): a string with the relationship being translated, e.g., "gt"

    Returns:
        str: a string with the relationship as a longer english phrase e.g.,
            "greater than". If relationship not defined in the dict english,
            then this method returns rel without modification.

    Raises:    TODO

    Examples
        >>> english_relationship("gt")
        'is greater than'

        >>> english_relationship("unknown")
        'unknown'

    """
    english = {"gt": "greater than", "ge": "greater than or equal to",
               "lt": "less than", "le": "less than or equal to",
               "ne": "not equal to", "eq": "equal to",
               "between": "between"}
    if rel in english.keys():
        return "is " + english[rel]
    return rel


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
