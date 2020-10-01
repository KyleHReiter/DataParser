#!/usr/bin/env python
"""
Data parser CLI
"""
import argparse
from prettytable import PrettyTable
from src.data_parser import DataParser


PARSER = argparse.ArgumentParser(
    description='Parse of large data sets in the following string format. ' +
    '<seg>|<field>|<field>...||<seg>|<field>...||<seg>...')
PARSER.add_argument("file_path", help="File path of data set to parse.")
PARSER.add_argument('--segment_name',
                    help='Case sensitive segment name which will ' +
                    'display matching segments.')
PARSER.add_argument('--field_name',
                    help='Case sensitive field name. ' +
                    'If used alone will display segments which ' +
                    'contain a field with field name. ' +
                    'If used in conjunction with segment name switch will ' +
                    'display segments matching segment name and ' +
                    'containing a field with field name.')
PARSER.add_argument("--debug",
                    help="Increase output verbosity to include errors.",
                    action="store_true")

ARGS = PARSER.parse_args()

DATA_PARSER = DataParser()
SEGMENT_TABLE = PrettyTable()
SEGMENT_TABLE.field_names = ["Field Name", "Field Value"]


def display_segment(segment):
    """Display segment.

    Args:
        segment_name: Segment to display.

    """
    SEGMENT_TABLE.clear_rows()
    SEGMENT_TABLE.title = f'Segment {segment.name}'
    for field in segment.fields:
        SEGMENT_TABLE.add_row([field.name, field.value])

    print(SEGMENT_TABLE)
    SEGMENT_TABLE.clear_rows()


def read_in_chunks(file_object, chunk_size=1024):
    """Read in chunks.

    Args:
        file_object: File object to read in chunks.
        chunk_size: Size of chunk to read.

    Returns:
        A generator of data from the file object.

    """
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def _segment_field_name_query(segment):
    """Segment field name query.
        Display segments containing matching segment name and
        containing at least one field with field name.

    Args:
        segment: Segment to query.

    """
    if segment.name == ARGS.segment_name:
        for segment_field in segment.fields:
            if segment_field.name == ARGS.field_name:
                display_segment(segment)
                break


def _segment_name_query(segment):
    """Segment name query.
       Display segments which match segment name.

    Args:
        segment: Segment to query.

    """
    if segment.name == ARGS.segment_name:
        display_segment(segment)


def _field_name_query(segment):
    """Field name query.
       Display segments containing at least one
       field with field name.

    Args:
        segment: Segment to query.

    """
    for field in segment.fields:
        if field.name == ARGS.field_name:
            display_segment(segment)
            break


def process_data(piece):
    """Process data.

    Args:
        piece: Piece to process.

    """
    for segment in DATA_PARSER.digest(piece).segments_iter():
        composed_segment = None
        try:
            composed_segment = segment.compose()
        except ValueError as err:
            if ARGS.debug:
                print(err)

            continue

        if ARGS.segment_name and ARGS.field_name:
            _segment_field_name_query(composed_segment)
        elif ARGS.segment_name:
            _segment_name_query(composed_segment)
        elif ARGS.field_name:
            _field_name_query(composed_segment)
        else:
            # Display all segments by default.
            display_segment(composed_segment)


def start_parse_data():
    """
    Start parse data.
    """
    with open(ARGS.file_path) as raw_data_file:
        for piece in read_in_chunks(raw_data_file):
            process_data(piece)


def validate_arguments():
    """Validate arguments.
    """
    if ARGS.segment_name:
        segment_name_count = len(ARGS.segment_name)
        segment_name_count_max = 3
        if not segment_name_count == segment_name_count_max:
            raise ValueError(f"Segment name '{ARGS.segment_name}' " +
                             f"must be exactly {segment_name_count_max} " +
                             "characters long.")

    if ARGS.field_name:
        field_name_count = len(ARGS.field_name)
        field_name_count_max = 3
        if not field_name_count == field_name_count_max:
            raise ValueError(f"Field name '{ARGS.field_name}' " +
                             f"must be exactly {field_name_count_max} " +
                             "characters long.")


if __name__ == "__main__":
    # Garbage in garbage out.
    validate_arguments()
    start_parse_data()
