#!/usr/bin/env python
"""
This module tests the data parser.
"""
import unittest
from unittest.mock import patch
import types
import src.data_parser as dp


def create_segment_helper(name, fields):
    segment = dp.Segment(None)
    segment.name = name
    segment.fields = fields
    return segment

class TestDataParser(unittest.TestCase):
    """
    Test data parser class.
    """
    def test_segments_iter_should_return_generator_when_called(self):
        # Arrange, Act, Assert
        assert type(dp._segments_iter('')) is types.GeneratorType

    def test_segments_iter_should_raise_type_error_when_raw_text_is_none(self):
        # Arrange, Act, Assert
        with self.assertRaises(TypeError):
            dp._segments_iter(None)

    def test_segments_iter_should_return_zero_segments_when_raw_text_is_empty(self):
        # Arrange, Act, Assert
        assert len(list(dp._segments_iter(''))) == 0

    def test_segments_iter_should_return_zero_segments_when_raw_text_is_double_pipe(self):
        # Arrange, Act, Assert
        assert len(list(dp._segments_iter('||'))) == 0

    def test_segments_iter_should_return_single_segment_when_raw_text_does_not_contain_double_pipe(self):
        # Arrange, Act, Assert
        assert len(list(dp._segments_iter('MTY|FOOspam'))) == 1

    def test_segments_iter_should_split_raw_text_when_raw_text_contains_double_pipe_between_segments(self):
        # Arrange, Act, Assert
        assert len(list(dp._segments_iter('MTY|FOOspam||GRL|BRVsir_robin'))) == 2

    def test_segments_iter_should_return_single_segment_when_raw_text_contains_trailing_double_pipe(self):
        # Arrange, Act, Assert
        assert len(list(dp._segments_iter('MTY|FOOspam||'))) == 1

    def test_segments_iter_should_return_segment_when_raw_text_contains_segment(self):
        # Arrange, Act, Assert
        assert type(list(dp._segments_iter('FOOspam'))[0]) == dp.Segment

    def test_segments_fields_iter_should_return_generator_when_called(self):
        # Arrange, Act, Assert
        assert type(dp._segments_fields_iter('')) is types.GeneratorType

    def test_segments_fields_iter_should_raise_type_error_when_raw_text_is_none(self):
        # Arrange, Act, Assert
        with self.assertRaises(TypeError):
            dp._segments_fields_iter(None)

    def test_segments_fields_iter_should_return_zero_segments_when_raw_text_is_empty(self):
        # Arrange, Act, Assert
        assert len(list(dp._segments_fields_iter(''))) == 0

    def test_segments_fields_iter_should_return_zero_segments_when_raw_text_is_single_pipe(self):
        # Arrange, Act, Assert
        assert len(list(dp._segments_fields_iter('|'))) == 0

    def test_segments_fields_iter_should_return_multiple_fields_when_raw_text_contains_single_pipe(self):
        # Arrange, Act, Assert
        assert len(list(dp._segments_fields_iter('FOOspam|BAReggs'))) == 2

    def test_segments_fields_iter_should_return_field_when_raw_text_contains_field(self):
        # Arrange, Act, Assert
        assert type(list(dp._segments_fields_iter('FOOspam'))[0]) == dp.Field

    def test_segments_fields_iter_should_return_field_with_name_when_raw_text_does_not_contain_single_pipe(self):
        # Arrange, Act, Assert
        assert list(dp._segments_fields_iter('FOO'))[0].name == 'FOO'

    def test_segments_fields_iter_should_return_field_with_value_empty_string_when_raw_text_does_not_contain_single_pipe(self):
        # Arrange, Act, Assert
        assert list(dp._segments_fields_iter('FOO'))[0].value == ''

    def test_segments_fields_iter_should_return_field_with_value_field_when_raw_text_does_not_contain_single_pipe(self):
        # Arrange, Act, Assert
        assert list(dp._segments_fields_iter('FOOspam'))[0].value == 'spam'

    def test_segment_should_set_raw_text_as_raw_text_when_initialized(self):
        # Arrange
        raw_text = 'MTY|FOOspam'

        # Act, Assert
        assert dp.Segment(raw_text).raw_text == raw_text

    def test_segment_should_set_name_as_none_when_initialized(self):
        # Arrange, Act, Assert
        assert dp.Segment('MTY|FOOspam').name == None

    def test_segment_should_set_fields_to_list_when_initialized(self):
        # Arrange, Act, Assert
        assert type(dp.Segment('MTY|FOOspam').fields) is list

    def test_segment_should_set_fields_as_empty_when_initialized(self):
        # Arrange, Act, Assert
        assert len(list(dp.Segment('MTY|FOOspam').fields)) == 0

    def test_segment_compose_should_return_self_when_called(self):
        # Arrange
        with patch("src.data_parser._segments_fields_iter", return_value=[]):
            segment = dp.Segment('MTY|FOOspam')

            # Act, Assert
            assert segment.compose() == segment

    def test_segment_compose_should_raise_value_error_when_raw_text_is_invalid(self):
        # Arrange
        with patch("src.data_parser._segments_fields_iter", return_value=[]):

            # Act, Assert
            with self.assertRaises(ValueError):
                dp.Segment('NO|WAYwork').compose()

    def test_segment_compose_should_update_name_when_called(self):
        # Arrange
        with patch("src.data_parser._segments_fields_iter", return_value=[]):
            # Act
            segment = dp.Segment('MTY|FOOspam').compose()

            # Assert
            assert segment.name == 'MTY'

    def test_segment_compose_should_call_segments_fields_iter_with_field_raw_text_when_called(self):
        # Arrange
        with patch("src.data_parser._segments_fields_iter", return_value=[]) as iter_segments_fields_mock:
            # Act
            dp.Segment('MTY|FOOspam').compose()

            # Assert
            iter_segments_fields_mock.assert_called_once_with('FOOspam')

    def test_segment_compose_should_update_fields_when_called(self):
        # Arrange
        fields = []
        with patch("src.data_parser._segments_fields_iter", return_value=fields):
            # Act
            segment = dp.Segment('MTY|FOOspam').compose()

            # Assert
            assert segment.fields == fields

    def test_segment_search_fields_should_return_field_when_called(self):
        # Arrange
        field_name = 'BAR'
        field = dp.Field(field_name, 'eggs')
        fields = [dp.Field('FOO', 'spam'), field]
        with patch("src.data_parser._segments_fields_iter", return_value=fields):
            segment = dp.Segment('MTY|FOOspam|BAReggs').compose()

            # Act, Assert
            assert list(segment.search_fields(field_name))[0] == field

    def test_segment_search_fields_should_return_zero_field_when_field_name_not_in_fields(self):
        # Arrange
        fields = [dp.Field('FOO', 'spam'), dp.Field('BAR', 'eggs')]
        with patch("src.data_parser._segments_fields_iter", return_value=fields):
            segment = dp.Segment('MTY|FOOspam|BAReggs').compose()

            # Act, Assert
            assert len(list(segment.search_fields('BAZ'))) == 0

    def test_segment_search_fields_should_return_multiple_fields_when_called(self):
        # Arrange
        field_name = 'BAR'
        fields = [
            dp.Field('FOO', 'spam'),
            dp.Field(field_name, 'eggs'),
            dp.Field(field_name, 'sir_robin')
        ]
        with patch("src.data_parser._segments_fields_iter", return_value=fields):
            segment = dp.Segment('MTY|FOOspam|BAReggs').compose()

            # Act, Assert
            assert len(list(segment.search_fields(field_name))) == 2

    def test_data_parser_should_set_segments_to_generator_when_initialized(self):
        # Arrange, Act, Assert
        assert type(dp.DataParser()._segments) is types.GeneratorType

    def test_data_parser_should_set_segments_as_empty_when_initialized(self):
        # Arrange, Act, Assert
        assert len(list(dp.DataParser()._segments)) == 0

    def test_data_parser_segments_iter_should_return_segments_fields_generator_when_called(self):
        # Arrange
        segments = (x for x in [
            create_segment_helper('MTY', [dp.Field('FOO', 'spam'), dp.Field('BAR', 'eggs')]),
            create_segment_helper('GRL', [dp.Field('BAZ', 'sir_robin')])])
        data_parser = dp.DataParser()
        data_parser._segments = segments

        # Act, Assert
        assert len(list(data_parser.segments_fields_iter())) == 3

    def test_data_parser_segments_iter_should_return_empty_generator_when_called(self):
        # Arrange
        empty_generator = (x for x in [])
        data_parser = dp.DataParser()
        data_parser._segments = empty_generator

        # Act, Assert
        assert data_parser.segments_iter() == empty_generator

    def test_data_parser_digest_should_digest_raw_text_when_called(self):
        # Arrange
        segments = [create_segment_helper('MTY', [dp.Field('FOO', 'spam')])]
        with patch("src.data_parser._segments_iter", return_value=segments):
            data_parser = dp.DataParser()

            # Act
            data_parser.digest('MTY|FOOspam')

            # Assert
            assert data_parser._segments == segments

    def test_data_parser_search_segments_iter_should_find_segments_when_searched_by_segment_name(self):
        # Arrange
        segment = create_segment_helper('GRL', [dp.Field('BAZ', 'sir_robin')])
        segments = (x for x in [
            create_segment_helper('MTY', [dp.Field('FOO', 'spam'), dp.Field('BAR', 'eggs')]),
            segment])
        data_parser = dp.DataParser()
        data_parser._segments = segments

        # Act, Assert
        assert list(data_parser.search_segments_iter('GRL'))[0] == segment

    def test_data_parser_search_segments_iter_should_find_segments_when_searched_by_segment_name_and_field_name(self):
        # Arrange
        segments = (x for x in [
            create_segment_helper('MTY', [dp.Field('FOO', 'spam'), dp.Field('BAR', 'eggs')]),
            create_segment_helper('GRL', [dp.Field('BAZ', 'sir_robin')]),
            create_segment_helper('GRL', [dp.Field('BAZ', 'king_arthur')]),
            create_segment_helper('GRL', [dp.Field('QUXX', 'sir_lancelot')])])
        data_parser = dp.DataParser()
        data_parser._segments = segments

        # Act, Assert
        assert len(list(data_parser.search_segments_iter('GRL', ['BAZ']))) == 2
