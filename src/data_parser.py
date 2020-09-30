#!/usr/bin/env python
"""
Data parser module.
"""
import re
import types
import collections

_MESSAGE_REGEX = re.compile(r"((?P<part>.{3}.*?)(\|\||$))")
_FIELD_REGEX = re.compile(r"((?P<name>.{3})(?P<value>.*?)(\||$))")

Field = collections.namedtuple('Field', 'name value')


# Add data parser interface.
class DataParserInterface:
    """
    Data parser interface.
    """
    def segments_iter(self) -> types.GeneratorType:
        """
        Segments iterator.
        """

    def segments_fields_iter(self) -> types.GeneratorType:
        """
        Segments fields iterator.
        """

    def search_segments_iter(self,
                             segment_name: str,
                             field_names: list = None) -> types.GeneratorType:
        """
        Search segments iterator.
        """

    def digest(self, raw_text: str) -> object:
        """
        Digest.
        """


class DataParser(DataParserInterface):
    """
    Data parser.
    """
    def __init__(self):
        self._segments = (segment for segment in [])

    def segments_iter(self):
        """Segments iterator.

        Returns:
            A generator of segments.

        """
        return self._segments

    def segments_fields_iter(self):
        """Segments fields iterator.

        Returns:
            A generator of segments fields.

        """
        for segment in self._segments:
            for field in segment.fields:
                yield field

    def search_segments_iter(self,
                             segment_name: str,
                             field_names: list = None):
        """Search segments iterator.

        Args:
            segment_name: Segment name to search.
            field_names: (Optional) Field names required in segment fields.

        Returns:
            A generator of segments matching segment name if only segment name
            is used. If segment name and field names are used then a generator
            of segments matching segment name and containing any
            field name are returned.

        """
        if field_names:
            for segment in self._segments:
                if segment.name == segment_name:
                    for field in segment.compose().fields:
                        if field.name in field_names:
                            yield segment
        else:
            for segment in self._segments:
                if segment.name == segment_name:
                    yield segment

    def digest(self, raw_text: str):
        """Digest raw text into segments iterator.
        Digestion of raw text is required prior to any segments iterator call.
        After the call of any segments iterator a new digest is required.

        Args:
            raw_text: Raw text to digest.

        Returns:
            Data parser instance for ease of chaining calls.

        """
        self._segments = _segments_iter(raw_text)
        return self


class Segment:
    """
    Segment.
    """
    def __init__(self, raw_text):
        self.raw_text = raw_text
        self.name = None
        self.fields = []

    def compose(self):
        """Compose.

        Returns:
            Segment instance for ease of chaining calls.

        """
        # Factory method to compose message outside of constructor.
        # This reduces likelyhood of exceptions in constructor and
        # allows lazy loading of fields.
        if self.raw_text:
            self.name, raw_fields = self.raw_text.split('|', 1)
            self.fields = list(_segments_fields_iter(raw_fields))

        return self

    def search_fields(self, field_name):
        """Search fields.

        Args:
            field_name: Field name used to search fields.

        Returns:
            A generator of field names matching the field name.

        """
        # Field names can repeat.
        for field in self.fields:
            if field.name == field_name:
                yield field


def _segments_iter(raw_text):
    """Segments iterator.

    Args:
        raw_text: Raw text containing segments.

    Returns:
        A generator of segments.

    Raises:
        TypeError: If `raw_text` is equal to `None`.

    """
    # Data can be very large do not load the entire string into memory.
    # Operation returns generator to lazy load.
    if raw_text is None:
        raise TypeError('Argument \'raw_text\' cannot be \'None\'.')

    return (Segment(m.group("part"))
            for m in re.finditer(_MESSAGE_REGEX, raw_text))


def _segments_fields_iter(raw_text):
    """Segments fields iterator.

    Args:
        raw_text: Raw text containing fields.

    Returns:
        A generator of fields.

    Raises:
        TypeError: If `raw_text` is equal to `None`.

    """
    if raw_text is None:
        raise TypeError('Argument \'raw_text\' cannot be \'None\'.')

    return (Field(m.group("name"), m.group("value"))
            for m in re.finditer(_FIELD_REGEX, raw_text))
