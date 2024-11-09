#!/usr/bin/env python3
"""
Module for filtering log messages and creating a logger.
"""

import os
import re
import logging
import mysql.connector
from typing import List
from mysql.connector import connection

# Define the PII fields to be redacted
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the specified record as text.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: Formatted log message with specified fields redacted.
        """
        original_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            original_message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Creates a logger named 'user_data' that logs up to INFO level
    and has a StreamHandler with RedactingFormatter.

    Returns:
        logging.Logger: Configured logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> connection.MySQLConnection:
    """
    Connects to the database using credentials from environment variables.

    Returns:
        connection.MySQLConnection: Database connector object.
    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME', '')

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )


def main() -> None:
    """
    Main function to retrieve and display user data in a filtered format.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT name, email, phone, ssn, password, ip, last_login, user_agent FROM users;")
    logger = get_logger()
    
    for (name, email, phone, ssn, password, ip, last_login, user_agent) in cursor:
        row = f"name={name}; email={email}; phone={phone}; ssn={ssn}; password={password}; ip={ip}; last_login={last_login}; user_agent={user_agent};"
        logger.info(row)
    
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
