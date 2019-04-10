import click

from datetime import datetime as dt
import os

from pycrossva.transform import transform


def get_default_name(output_type, src):
    """ """
    original_name = src.split(os.path.sep)[-1].split(".")[0]
    return "_".join([output_type, "from", original_name,
                     dt.today().strftime("%m%d%y")]) + ".csv"


@click.command()
@click.argument("input_type",
                nargs=1,
                #prompt="Select the correct type of input data",
                type=click.Choice(["2016WHOv151", "2016WHOv141",
                                   "2012WHO", "PHRMCShort"]),
                required=True)
@click.argument('output_type',
                nargs=1,
                #prompt="Enter path of input data",
                type=click.Choice(["InterVA5", "InterVA4", "InsillicoVA"]),
                required=True)
@click.argument('src',
                nargs=-1,
                type=click.Path(),
                #prompt="Enter path(s) of input data",
                required=True)
@click.option('-d', '--dst', 'dst',
              #prompt="Specify filepath to save transformed data as csv",
              type=click.Path(),
              default=None,
              show_default="current directory",
              required=False)
@click.option('--silent', '-s', is_flag=True, default=False)
# @click.option('--preserve-na/--fill-na', default=False)
def main(input_type, output_type, src, dst, silent):
    """This is a wrapper for the `transform` python function in the pycrossva
    package so that it can be run from the command line.

    If no destination (dst) is specified, the default behavior will be to write
    the resulting data to a csv in the current directory with a name in the pattern
    of "output_type_from_src_mmddyy".

    \b
    Args:
        `input_type` source of the input data
        `output_type` format of output data (which algorithm the data should be prepared for)
        `src` filepath to the input data - can take multiple arguments

    \b
    Example:
        $ python pycrossva-transform.py 2012WHO InterVA4 pycrossva/resources/sample_data/2012WHO_mock_data_1.csv
        2012WHO 'pycrossva/resources/sample_data/2012WHO_mock_data_1.csv' data prepared for InterVA4 written to csv at '/Users/ekarpinski/pyCrossVA/InterVA4_from_2012WHO_mock_data_1_040519.csv')

    """
    verbosity = 2
    if silent:
        verbosity = 0
    for input_data in src:
        result = transform((input_type, output_type), input_data,
                           verbose=verbosity)
        if dst is None:
            dst = os.path.join(
                os.getcwd(), get_default_name(output_type, input_data))

        if result is not None:
            result.to_csv(dst)
            click.echo(
                f"{input_type} '{input_data}' data prepared for {output_type} written to csv at '{dst}')")


if __name__ == '__main__':
    main()
