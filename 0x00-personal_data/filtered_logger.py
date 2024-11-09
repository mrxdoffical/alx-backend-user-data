#!/usr/bin/env python3
"""
Module for filtering log messages.
"""

import re
import logging
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Replaces the values of specified fields
    in a message with a redaction string.

    Args:
        fields (List[str]): Fields to obfuscate.
        redaction (str): Redaction string.
        message (str): Log message.
        separator (str): Character separating fields in the log message.

    Returns:
        str: Obfuscated log message.
    """
    pattern = '|'.join(
        f'{field}=[^{separator}]+' for field in fields
    )
    return re.sub(
        pattern, lambda m: f'{m.group().split("=")[0]}={redaction}', message
    )


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        original_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            original_message, self.SEPARATOR)
