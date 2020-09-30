#!/usr/bin/env python
import mmap
from src.data_parser import DataParser
import os
from prettytable import PrettyTable
import argparse

PARSER = argparse.ArgumentParser(
    description='Parse of large data sets in the following string format. ' + \
                '<seg>|<field>|<field>...||<seg>|<field>...||<seg>...')
PARSER.add_argument("file_path", help="File path of data set to parse.")
PARSER.add_argument('--segment_name',
                    help='Case sensitive segment name.')
PARSER.add_argument('--field_name',
                    help='Case sensitive field name.')
ARGS = PARSER.parse_args()

DATA_PARSER = DataParser()
SEGMENT_TABLE = PrettyTable()
SEGMENT_TABLE.field_names = ["Field Name", "Field Value"]

def display_segment(segment_name, segment_fields):
    SEGMENT_TABLE.clear_rows()
    SEGMENT_TABLE.title = f'Segment {segment_name}'
    for field in segment_fields:
        SEGMENT_TABLE.add_row([field.name, field.value])

    print(SEGMENT_TABLE)
    SEGMENT_TABLE.clear_rows()

def read_in_chunks(file_object, chunk_size=1024):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def process_data(piece):
    for segment in DATA_PARSER.digest(piece).segments_iter():
        composed_segment = segment.compose()

        # Generators cannot be iterated multiple times
        # Store segment fields into memory.
        segment_fields = list(composed_segment.fields)

        if ARGS.segment_name and ARGS.field_name:
            # Display segments containing
            # matching segment name and containing
            # at least one field with field name.
            if composed_segment.name == ARGS.segment_name:
                for segment_field in segment_fields:
                    if ARGS.field_name == segment_field.name:
                        display_segment(composed_segment.name, segment_fields)
                        break
        elif ARGS.segment_name:
            # Display segments which match 
            if composed_segment.name == ARGS.segment_name:
                display_segment(composed_segment.name, segment_fields)
        elif ARGS.field_name:
            # Display segments containing
            # at least one field with field name.
            for field in composed_segment.fields:
                if ARGS.field_name == field.name:
                    display_segment(composed_segment.name, segment_fields)
                    break
        else:
            # Display all segments.
            display_segment(composed_segment.name, segment_fields)

def start_parse_data():
    with open(ARGS.file_path) as f:
        for piece in read_in_chunks(f):
            process_data(piece)

start_parse_data()
