"""Database: interface, SQLite and PostgreSQL connection pools."""
from airbot.db.interface import Database
from airbot.db.factory import create_database

__all__ = ["Database", "create_database"]
