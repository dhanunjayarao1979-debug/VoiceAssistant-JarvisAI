"""Shared path helpers so the project works on Windows, macOS and Linux."""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))


def data_path(*parts):
    return os.path.join(ROOT, "Data", *parts)


def db_path(*parts):
    return os.path.join(ROOT, "DataBase", *parts)
