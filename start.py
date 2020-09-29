#!/usr/bin/env python

import mmap
from src.data_parser import DataParser
import os

DATA_PARSER = DataParser()

def print_segment(segment):
    print(f'Segment:\r\n    Name: {segment.name}')

    print('\r\nField(s):')
    for field in segment.fields:
        print(f'    {field.name}, {field.value}')
    print('-----------------------------------------------')

def read_in_chunks(file_object, chunk_size=1024):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def process_data(piece):
    for segment in DATA_PARSER.digest(piece).segments_iter():
        print_segment(segment.compose())

def start():
    with open('test/mock_data/raw_data.txt') as f:
        for piece in read_in_chunks(f):
            process_data(piece)

start()