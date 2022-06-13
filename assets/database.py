import imp
from peewee import *

__all__ = ['Database']

db = SqliteDatabase('data.db')