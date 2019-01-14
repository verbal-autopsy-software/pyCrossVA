"""
Structure for Configuration class
"""

# !/usr/bin/env python3
#  -*- coding: utf-8 -*-

from mappings import MapCondition
from utils import report_list
from validation import Validation, Err, Warn
import pandas as pd
import numpy as np

# MAP_PATH = "resources/mapping_configuration_files/"
# EX_MAP_1 = pd.read_csv(MAP_PATH+"example_config_1.csv")
# EX_MAP_2 = pd.read_csv(MAP_PATH+"example_config_2.csv")
# EX_DATA_1 = pd.read_csv("resources/sample_data/who151_va_output.csv")
# create problematic data
# EX_DATA_2


class Configuration():
    """ Configuration class details the relationship between a set of input
    data and output data. It is composed of MapConditions that
    transform an input data source (2012 WHO, 2016 WHO 141, 2016 WHO 151,
    PHRMC SHORT) into a different data form (PHRMC SHORT, InsillicoVA,
    InterVA4, InterVA5, or Tarrif2) for verbal autopsy.

    Attributes:
        given_columns (Pandas Series): columns of mapping dataframe.
        required_columns (Pandas Series): required columns in mapping data.
        main_columns (list): the four main columns required in config_data.
        valid_relationships (Pandas Series): contains list of valid
            relationships to use in comparisons. Relationships should be an
            attr of Pandas Series object, or be defined as a subclass of
            MapCondition.
        config_data (Pandas DataFrame): dataframe containing mapping
            relationships written out.
        given_prereq (Pandas Series): lists pre-requisites referenced in config
            data.
        new_columns (Pandas Series): lists the new columns to be created with
            config data.
        source_columns (Pandas Series): lists the source columns required in
            the raw input data.
        verbose (int): controls default verbosity of printing to console.
        process_strings (boolean): whether or not to remove whitespace and
            non-alphanumeric characters from strings in condition field and in
            raw_data during mapping.
        validation (Validation): a validation object containing the validation
            checks made

    """
    required_columns = pd.Series(['New Column Name',
                                  'New Column Documentation',
                                  'Source Column ID',
                                  'Source Column Documentation',
                                  'Relationship',
                                  'Condition', 'Prerequisite',
                                  ],
                                 name="expected columns")

    main_columns = ["New Column Name", "Source Column ID",
                    "Relationship", "Condition"]

    valid_relationships = pd.Series(["gt", "ge", "lt", "le", "between", "eq",
                                     "ne", "contains"],
                                    name="valid relationships")

    def __init__(self, config_data, verbose=1, process_strings=True):
        """Inits configuration class from a Pandas DataFrame containing
            mapping data.

        Args:
            config_data (Pandas DataFrame): dataframe representing the mapping
                data relationships, in specified format.
            verbose (int): should be in range 1-5,
                controls print output, where 0=silent. Defaults to 1.
            process_strings (boolean): Whether or not to normalize string
                conditions and data. Defaults to True.

        Returns:
            Nothing

        Examples:
            >>> Configuration(EX_MAP_1)
            Unvalidated Configuration instance with 16 mapping conditions

        """
        # TODO check for df & # of rows & these 3 columns
        # throw cant instantiate error?

        self.config_data = config_data
        self.given_columns = pd.Series(config_data.columns,
                                       name="the given columns")
        self.process_strings = process_strings

        def plain_info(aseries, new_name):
            """ returns Pandas Series without NAs or duplicates renamed to
            `new_name` """
            return aseries.drop_duplicates().dropna().rename(new_name)

        self.given_relationships = plain_info(config_data["Relationship"],
                                              "Relationship column")
        self.given_prereq = plain_info(config_data["Prerequisite"],
                                       "Prerequisite column")
        self.new_columns = plain_info(config_data["New Column Name"],
                                      "New Column Name column")
        self.source_columns = plain_info(config_data["Source Column ID"],
                                         "Source Column in Config")
        self.verbose = verbose
        self.validation = Validation()

    def __str__(self):
        """string representation of class"""
        return self.__repr__()

    def __repr__(self):
        """string representation of class"""
        val_status = ("Validated" if self.validation.is_valid() else
                      "Unvalidated")
        return " ".join([val_status, self.__class__.__name__, "instance with",
                         str(len(self.config_data)), "mapping conditions"])

    def list_conditions(self):
        """Lists the final mapping conditions contained in Configuration object

        Returns:
            list: list of MapConditions, where each MapConditions is
            created from a row of processed mapping data.

        Examples:
            >>> c = Configuration(EX_MAP_1)
            >>> c.list_conditions()[:5]
            [<StrMapCondition:     AB_POSIT = [column Id10403].eq(yes)>,
             <StrMapCondition:     AB_SIZE = [column Id10362].eq(yes)>,
             <NumMapCondition:     AC_BRL = [column Id10169].lt(14.0)>,
             <NumMapCondition:     AC_CONV = [column Id10221].lt(10.0)>,
             <NumMapCondition:     AC_COUGH = [column Id10154].lt(21.0)>]

        """
        # TODO config_data["Standalone"] = config_data["Prerequisite"].isnull()
        # self.config_data.sort_values("Standalone", ascending=False)
        return [MapCondition.factory(row["Relationship"])(row)
                for i, row in self.config_data.iterrows()]

    def validate(self, verbose=None):
        """Prepares and validates the Configuration object's mapping conditions.
        Validation fails if there are any inoperable errors. Problems that can
        be fixed in place are processed and flagged as warnings.

        Args:
            verbose (int): controls print output, should be in range 0-5,
                each higher level includes the messages of each level below it.  
                Where verbose = 0, nothing will be printed to console.  
                Where verbose = 1, print only errors to console,  
                where verbose = 2, also print warnings,
                where verbose = 3, also print suggestions and status checks,  
                where verbose = 4, also print passing validation checks,  
                where verbose = 5, also print description of configuration
                conditions.  
                Defaults to None; if none, replace with self.verbose attribute  
        Returns:
            Boolean: boolean representing whether there are any errors that
                prevent validation

        Examples:
            >>> Configuration(EX_MAP_1).validate()
            True
            >>> Configuration(EX_MAP_2).validate(verbose=4)
                Validating configuration file . . .
            <BLANKLINE>
             CHECKS PASSED
            [X]          All expected columns ('New Column Name', 'New Column Documentation', 'Source Column ID', 'Source Column Documentation', 'Relationship', 'Condition', and 'Prerequisite') accounted for in configuration file.
            [X]          No NA's in column New Column Name detected.
            [X]          No NA's in column Source Column ID detected.
            [X]          No leading/trailing spaces column New Column Name detected.
            [X]          No leading/trailing spaces column Relationship detected.
            [X]          No leading/trailing spaces column Prerequisite detected.
            [X]          No leading/trailing spaces column Condition detected.
            [X]          No whitespace in column Condition detected.
            [X]          No upper case value(s) in column Relationship detected.
            [X]          No upper case value(s) in column Condition detected.
            [X]          No non-alphanumeric value(s) in column Source Column ID detected.
            [X]          No non-alphanumeric value(s) in column Relationship detected.
            [X]          No non-alphanumeric value(s) in column Condition detected.
            <BLANKLINE>
             ERRORS
            [!]          1 extraneous column(s) found in the given columns ('unused column') Extraneous column(s) will be ommitted.
            [!]          3 values in Relationship column were invalid ('eqqqq', 'another fake', and 'gee'). These must be a valid method of pd.Series, e.g. ('gt', 'ge', 'lt', 'le', 'between', 'eq', 'ne', and 'contains') to be valid.
            [!]          2 row(s) containing a numericalrelationship with non-number condition detected in row(s) #8, and #9.
            [!]          2 values in Prerequisite column were invalid ('ABDOMM', and 'Placeholder here'). These must be defined in the 'new column name' column of the config file to be valid.
            [!]          1 NA's in column Relationship detected in row(s) #3.
            [!]          1 NA's in column Condition detected in row(s) #6.
            <BLANKLINE>
             WARNINGS
            [?]          2 duplicate row(s) detected in row(s) #1, and #14. Duplicates will be dropped.
            [?]          1 blank row(s) detected in row(s) #10. Blank rows will be dropped.
            [?]          2 whitespace in column New Column Name detected in row(s) #6, and #8. Whitespace will be converted to '_'
            [?]          1 whitespace in column Relationship detected in row(s) #4. Whitespace will be converted to '_'
            [?]          1 whitespace in column Prerequisite detected in row(s) #9. Whitespace will be converted to '_'
            [?]          2 non-alphanumeric value(s) in column New Column Name detected in row(s) #5, and #6. This text should be alphanumeric. Non-alphanumeric characters will be removed.
            False
        """
        if verbose is None:
            verbose = self.verbose

        if verbose >= 3:
            print("Validating configuration file . . .")

        # Check that all expected columns accounted for
        col_passing_msg = " ".join(["All expected columns",
                                    report_list(self.required_columns),
                                    "accounted for in configuration file."])
        self.validation.must_contain(self.given_columns,
                                     self.required_columns,
                                     passing_msg=col_passing_msg)

        # Check for extra columns
        self.validation.no_extraneous(self.given_columns,
                                      self.required_columns,
                                      "column")
        self.config_data = self.config_data.reindex(
            columns=self.required_columns)

        # TODO: check for circular pre-reqs?

        # Check for duplicate rows
        self.validation.flag_rows(self.config_data.duplicated(),
                                  flag_criteria="duplicate row(s)",
                                  flag_action="Duplicates will be dropped.")
        self.config_data = self.config_data.drop_duplicates()

        # Check for blank rows
        self.validation.flag_rows(
            pd.Series(np.all(self.config_data.isnull(), axis=1)),
            flag_tier=Warn,
            flag_criteria="blank row(s)",
            flag_action="Blank rows will be dropped.")
        self.config_data = self.config_data.dropna(how="all")

        # check all relationships in relationship column are valid
        self.validation.all_valid(self.given_relationships,
                                  self.valid_relationships,
                                  "a valid method of pd.Series, e.g. " +
                                  report_list(self.valid_relationships))

        # check for non-number conditions with numerical relationships
        invalid_num = (self.config_data["Relationship"].isin(
                                        ["gt", "ge", "le", "lt"]) &
                       (pd.to_numeric(self.config_data["Condition"],
                                      errors="coerce").isnull()))
        self.validation.flag_rows(invalid_num,
                                  flag_criteria="row(s) containing a numerical"
                                  + "relationship with non-number condition",
                                  flag_tier=Err)

        # check all prerequisite columns are also defined in configuration
        self.validation.all_valid(self.given_prereq, self.new_columns,
                                  "defined in the 'new column name' column " +
                                  "of the config file")

        # Check for missing values
        self.validation.check_na(self.config_data[self.main_columns])

        # Processing strings
        ws_col = ["New Column Name", "Relationship", "Prerequisite"]
        lowercase_col = ["Relationship"]
        if self.process_strings:
            ws_col.append("Condition")
            lowercase_col.append("Condition")

        # Remove whitespace
        self.config_data.loc[:, ws_col] = self.validation.fix_whitespace(
            self.config_data.loc[:, ws_col].fillna(""))

        # Check for uppercase characters
        self.config_data.loc[:, lowercase_col] = self.validation.fix_upcase(
            self.config_data.loc[:, lowercase_col].fillna(""))

        # Check that main columns contain only alphanumeric values
        self.config_data.loc[:, self.main_columns] = self.validation.fix_alnum(
            self.config_data.loc[:, self.main_columns])

        self.validation.report(verbose)  # report
        if verbose == 5:
            self.describe()

        # return true only if there are zero errors
        return self.validation.is_valid()

    def describe(self):
        """Prints the mapping relationships in the Configuration object to
        console.

        Args:
            None

        Returns:
            None

        Examples:
            >>> Configuration(EX_MAP_1).describe()
            MAPPING STATS
            <BLANKLINE>
             -       16 new columns produced ('AB_POSIT', 'AB_SIZE', 'AC_BRL',
             'AC_CONV', 'AC_COUGH', etc.)
             -       12 source columns required ('Id10403', 'Id10362',
             'Id10169', 'Id10221', 'Id10154', etc.)
             -       7 relationships invoked ('eq', 'lt', 'between', 'ge',
             'contains', etc.)
             -       13 conditions listed ('yes', '14', '10', '21', '15 to 49',
             etc.)
             -       1 prerequisites checked ('FEMALE')

        """
        print("MAPPING STATS\n")
        spacer = " - \t"

        unique_checks = [("New Column Name", "new columns produced"),
                         ("Source Column ID", "source columns required"),
                         ("Relationship", "relationships invoked"),
                         ("Condition", "conditions listed"),
                         ("Prerequisite", "prerequisites checked")]

        for col_name, context in unique_checks:
            print(spacer, self.config_data[col_name].nunique(), context,
                  report_list(self.config_data[col_name].dropna().unique(),
                              limit=5))


class CrossVA():
    """Class representing raw VA data, and how to map it to an algorithm

    Attributes:
        mapping (type): a validated Configuration object that details how to
            transform the type of data in `raw_data` to the desired output.
        data (Pandas DataFrame): a Pandas DataFrame containing the raw VA data
        prepared_data (Pandas DataFrame): a Pandas DataFrame containing a
            prepared form of the VA data to use with the Configuration object.
        validation (Validation): Validation object containing the validation
            checks that have been made on the raw data and between the raw data
            and mapping Configuration.
        verbose (int): Controls verbosity of printing to console, 0-5 where 0
            is silent.
    """

    def __init__(self, raw_data, mapping_config, na_values=["dk", "ref", ""],
                 verbose=2):
        """Inits CrossVA class

        Args:
            raw_data (Pandas DataFrame): a Pandas DataFrame containing the
                raw data
            mapping_config (Configuration): a validated Configuration object
                that details how to transform the type of data in `raw_data`
                to the desired output.
            na_values (list): List of values to consider NA.
            verbose (int): Controls verbosity of printing to console. Defaults
                to 2.
        Returns:
            type: Description of returned object.

        Examples
            >>> CrossVA(EX_DATA_1, Configuration(EX_MAP_1))
            <CrossVA with (4, 12) raw data and Validated Configuration instance
            with 16 mapping conditions>

        """
        # if mapping_config isn't valid, attempt to validate before aborting
        if not mapping_config.validation.is_valid():
            if not mapping_config.validate():
                pass
                # raise error - mapping_config should be a valid

        # Crop input data to only the columns which have a matching ID
        # at the end of their name using regex, and any additional columns
        # passed as an argument, and then rename dataframe to just the column
        # IDs
        self.mapping = mapping_config
        new_columns = raw_data.columns.str.extract(
            "("+"$|".join(self.mapping.source_columns.tolist())+"$)",
            expand=False)
        cropped_data = raw_data.loc[:, new_columns.notnull()].copy()
        cropped_data = cropped_data.replace(na_values, np.nan)
        self.data = cropped_data.rename(columns=pd.Series(new_columns,
                                                          raw_data.columns))
        self.prepared_data = pd.DataFrame()
        self.verbose = verbose
        self.validation = Validation()

    def __str__(self):
        """ str representation method """
        return ""

    def __repr__(self):
        return ("<" + self.__class__.__name__ + " with " + str(self.data.shape)
                + " raw data and " + str(self.mapping) + ">")

    def process(self):
        """Applies the given configuration object's mappings to the given raw
        data.

        Args:   None

        Returns:
            Pandas DataFrame: a dataframe where the transformations specified
            have been applied to the raw data.

        """
        if not self.validation.is_valid():
            if not self.validate():
                raise ValueError(("Can't process without valid"
                                 " CrossVA instance"))
        transformed_data = pd.DataFrame(index=np.arange(len(self.data)),
                                        columns=self.mapping.new_columns)
        transformed_data.columns.name = ""
        for condition in self.mapping.list_conditions():
            # create column_values (boolean pd.series) representing if
            # condition and preq is met in raw data for each row, preserving NA

            cond_result = condition.check(self.prepared_data)
            column_val = np.where(cond_result.fillna(False),
                                  condition.check_prereq(transformed_data),
                                  cond_result
                                  )
            # update new column to be met_conditions where new column is
            # currently NA or false, but do not overwrite TRUE values (creates
            # implicit ANY relationship between conditions)
            update_where = ~(transformed_data[condition.name].fillna(False))
            transformed_data.loc[:, condition.name] = np.where(update_where,
                                column_val, transformed_data[condition.name])

        return transformed_data

    def validate(self, verbose=None):
        """Validates that RawVAData's raw input data and its mapping
        configuration object are compatible.

        Args:
            verbose (int): int from 0 to 5, representing verbosity of printing
                to console. Defaults to None; if None, replaced with
                self.verbose attribute.

        Returns:
            boolean: True if valid, False if not.

        Examples:
            >>> CrossVA(EX_DATA_1, Configuration(EX_MAP_1)).validate()
            True

        """
        if verbose is None:
            verbose = self.verbose

        if self.mapping.process_strings:
            # strip whitespace and replace non-trailing/leading with underscore
            self.data.fillna("", inplace=True)
            self.data = self.validation.fix_whitespace(self.data)
            # make all characters lowercase
            self.data = self.validation.fix_upcase(self.data)
            # strip for alphanumeric characters
            self.data = self.validation.fix_alnum(self.data)
            self.data = self.data.replace("", np.nan)
        # check all expected columns from config Source Column ID are present
        self.validation.must_contain(pd.Series(self.data.columns,
                                               name="input data columns"),
                                     self.mapping.source_columns)

        # TODO Check to see if relationship and conditions correspond to
        # logical values in each column
        if self.validation.is_valid():
            for mapping_condition in self.mapping.list_conditions():
                self.prepared_data[mapping_condition.source_dtype] = \
                    mapping_condition.prepare_data(self.data)

        self.validation.report(verbose)
        return self.validation.is_valid()


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
